from asyncio import Lock
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time
import zipfile
import requests
from tqdm import tqdm
from app.models import config
from app.version import v

fifofile = ""

updating = False
update_lock = threading.Lock()
eta = 0
_thread = None


def trigger_uwsgi_reload():
    with open(fifofile, 'w') as fifo:
        fifo.write('r')


def get_latest_release_download_url_tag(repo_owner='bi2nb9o3-studio', repo_name='9ding-js', file_name="bundle.js"):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        # print(response.json())
        release_info = response.json()
        for asset in release_info['assets']:
            if asset['name'] == file_name:
                return asset['browser_download_url'], release_info['tag_name']
    else:
        # print(response.text)
        print("Failed to retrieve the latest release", response.text)
        return "Failed to retrieve the latest release"


def download_file(url: str, fname: str, github: bool = True):
    if github:
        url = "https://github.moeyy.xyz/"+url
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def compare_version(a, b):
    if a.startswith("v"):
        a = a[1:]
    if b.startswith("v"):
        b = b[1:]
    a = a.split(".")
    b = b.split(".")
    for i in range(3):
        if int(a[i]) > int(b[i]):
            # print(f"New version: {a} > {b}")
            return 1
    # print(f"Old version: {a} <= {b}")
    return 0


def checkifnewversion(tag, current=None):
    if current is None:
        if os.path.exists("./bundle/version"):
            with open("./bundle/version", mode="r") as f:
                return compare_version(tag, f.read())
        else:
            return 1
    else:
        return compare_version(tag, current)


def update_bundle():
    res = get_latest_release_download_url_tag()
    os.makedirs("./bundle/", exist_ok=True)
    if res == "Failed to retrieve the latest release":
        print("Failed to retrieve the latest release")
        return -1
    url, tag = res
    if checkifnewversion(tag):
        download_file(url, "./bundle/bundle.js")
        with open("./bundle/version", mode="w") as f:
            f.write(tag)
        print("Bundle updated")
    else:
        print("Bundle is up to date")
        return 1


def download_font():
    if os.path.exists("./FiraCode-Regular.ttf"):
        return
    download_file(
        "https://github.moeyy.xyz/https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip", "./Fira_Code_v6.2.zip", github=False)
    zipfile.ZipFile("./Fira_Code_v6.2.zip").extractall("./tmp")
    os.rename("./tmp/ttf/FiraCode-Regular.ttf", "./FiraCode-Regular.ttf")
    os.remove("./Fira_Code_v6.2.zip")
    shutil.rmtree("./tmp", ignore_errors=True)
    print("Font downloaded")


def update_dependencies():
    # 获取虚拟环境二进制路径
    venv_python = sys.executable
    venv_bin_dir = os.path.dirname(venv_python)
    venv_python = os.path.join(os.path.dirname(venv_python),"pip")

    # 设置虚拟环境专属缓存目录
    venv_cache_dir = str(Path(venv_bin_dir).parent / "pip_cache")
    os.makedirs("venv_cache_dir",exist_ok=True, mode=0o755)
    print("venv python:", venv_python)
    try:
        # 生成旧依赖列表（不使用shell重定向）
        with open("old_requirements.txt", "w") as f:
            subprocess.check_call(
                [venv_python, "freeze"],
                stdout=f,
                env={**os.environ, "PIP_CACHE_DIR": venv_cache_dir,
                     "PYTHONHOME": "", }  # 关键环境变量设置
            )

        # 执行安装（使用虚拟环境专属缓存）
        subprocess.check_call([
            'sudo',
            venv_python, "install",
            "--upgrade",
            "--no-cache-dir",  # 可选：完全禁用缓存
            "-r", "./tmp2/requirements.txt"
        ], env={**os.environ, "PIP_CACHE_DIR": venv_cache_dir, "PYTHONHOME": ""})

    except subprocess.CalledProcessError as e:
        print(f"更新失败，错误码 {e.returncode}")

def update_self():
    res = get_latest_release_download_url_tag(
        repo_name="9ding-backend", file_name="app.zip")
    if res == "Failed to retrieve the latest release":
        print("Failed to retrieve the latest release")
        return -1
    url, tag = res
    if checkifnewversion(tag, v):
        os.makedirs("./tmp2", exist_ok=True)
        download_file(url, "./tmp2/app.zip")
        # Strucutre of app.zip:
        # - app.zip
        #   - src
        #     - app
        #       ...
        #   - requirements.txt
        zipfile.ZipFile("./tmp2/app.zip").extractall("./tmp2")
        os.remove("./tmp2/app.zip")
        # 将解压后的文件中的src目录每个都复制到当前目录的对应位置，如 src/app/setup.py 复制到 ./app/setup.py
        for root, dirs, files in os.walk("./tmp2/src"):
            for file in files:
                os.makedirs(os.path.join(".", root[11:]), exist_ok=True)
                shutil.copy(os.path.join(root, file),
                            os.path.join(".", root[11:], file))
        # 安装新的依赖
        update_dependencies()
        print("Self updated")
        shutil.rmtree("./tmp2", ignore_errors=True)
        trigger_uwsgi_reload()
        sys.exit(0)
    else:
        print("Self is up to date")
        return 1


def do():
    global updating
    global eta
    eta = 60
    updating = False
    while True:
        for _ in range(60):
            time.sleep(1)
            eta -= 1
        do_once()
        eta = 60


def do_once():
    global updating, update_lock
    print("Checking for updates")
    if updating:
        return
    with update_lock:
        updating = True
        if config.panelconfig["update"]["bundle"]["action"] == "at_once":
            update_bundle()
        if config.panelconfig["update"]["app"]["action"] == "at_once":
            update_self()
        updating = False


def start_thread():
    global _thread
    if not _thread or not _thread.is_alive():
        _thread = threading.Thread(target=do, daemon=True)
        _thread.start()
