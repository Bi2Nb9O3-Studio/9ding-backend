import os
import shutil
import zipfile
import requests
from tqdm import tqdm

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
        print("Failed to retrieve the latest release")


def download_file(url: str, fname: str, github:bool=True):
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
            return 1
        elif int(a[i]) < int(b[i]):
            return 0


def checkifnewversion(tag):
    if os.path.exists("./bundle/version"):
        with open("./bundle/version", mode="r") as f:
            return compare_version(f.read(), tag)
    else:
        return 1


def update_bundle():
    url, tag = get_latest_release_download_url_tag()
    os.makedirs("./bundle/", exist_ok=True)
    if checkifnewversion(tag):
        download_file(url, "./bundle/bundle.js")
        with open("./bundle/version", mode="w") as f:
            f.write(tag)
        print("Bundle updated")
    else:
        print("Bundle is up to date")


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