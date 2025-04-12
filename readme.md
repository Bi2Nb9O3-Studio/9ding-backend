# 9ding Backend

## 📦 部署 Deployment

- 从 [Releases](github.com/Bi2Nb9O3-Studio/9ding-backend/releases/) 下载最新版本的`app.zip`文件并解压
- 将解压目录中`src`目录中的内容复制到你的部署文件夹
- 建立虚拟环境并激活(可选)
- 安装`requirements.txt`中的依赖
- 运行`init.py`
- 修改`security.cfg`中的`salt`和`key` **部署后不可修改**
- 在`atp.cfg`文件中修改`fifo`的值为实际fifo路径
- 部署你的uwsgi环境并在配置文件中添加如下信息,并设置端口为5002

```config
master-fifo=your/path/to/fifo/file #请填写实际fifo文件路径
master = true
processes = 1
threads = 2
lazy-apps = true
callable=app
```

- 将你的模型放入models文件夹并重命名为`model.glb`
- 运行服务
- 访问`/admin/login`并登录

> 默认账号：admin
> 默认密码：admin

- 在后台的`配置管理`选项卡中修改`站点URL`为实际值（为解决CORS问题）

### 宝塔部署额外步骤

- 修改`atp.cfg`中的`envmode`的值为`bt`
- 运行时使用`root`运行
**本项目完全开源，root权限仅用于自动更新时安装依赖**
