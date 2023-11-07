<h1 align="center">电子科技大学清水河校区寝室电信网络自动接入工具</h1>
<p>
  <a href="https://mit-license.org/">
    <img alt="License: MIT License" src="https://img.shields.io/badge/License-MIT License-yellow.svg" target="_blank" />
  </a>
</p>

> 电子科技大学寝室网络（电信）自动后台常驻保证在线，支持 linux64, mac-arm64, mac-x64, win32, win64。~~如果 chromium 内核自动更新失败，请从 [官网下载](https://chromedriver.chromium.org/downloads) 更换 webdriver 目录下对应的 chromedriver 驱动, **一定要和 Chrome 版本 (chrome://settings/help) 对应上**~~ 

# 更新
- 2023.7.11: 转为使用[独立的无头chrome for testing及chromedriver](https://developer.chrome.com/blog/chrome-for-testing/)，不再需要完整的chrome环境或配置对应版本的webdriver。

- 2023.6.23: [@yao-yun](https://github.com/yao-yun) 提供了 chromium 内核的自动检测与下载的更新，无需用户自行配置驱动。

- 2022.12.12: 修复 issue #2 提到的 dockerfile 的问题。

- 2022.9.30: 电信入网登陆地址发生变动 172.25.249.8 -> 172.25.249.64
> 如何查看入网地址? 当无法正常使用该工具时, 请手动在浏览器进入入网登陆页面, 然后将该页面的 IP 复制进 auto_login.py 相应位置即可（self.login_gateway）。

# 直接部署

### Requirements
```sh
requests
argparse
python >= 3.10
selenium >= 3.141.0
```
~~**本地安装的 Chrome 需要和 webdriver 目录下使用的 chromedriver 版本吻合！！！**~~
~~selenium 的环境调试过程较为复杂，推荐使用本项目提供的 docker 镜像，不需要手动配置环境。~~\

Chrome for testing 及 Chrome driver 可通过 `python .\setup_cft.py`, `auto_login.py` 自动获取。获取到的 `./webdriver/chromedriver-xxx/chromedriver` 与 `./webdriver/chrome-headless-shell-xxx/chrome-headless-shell` 文件需要设置权限（如 chmod 777）。

（不推荐）此外也可手动从 [googlechromelabs](https://googlechromelabs.github.io/chrome-for-testing/) 下载。需将对应平台、相互匹配的 `chrome-headless-shell.zip` 及 `chromedriver.zip` 下载并解压至 ./webdriver/。 

**需要能访问 [googlechromelabs.github.io](googlechromelabs.github.io) 的网络环境**

## Usage
在config.py文件中输入您的账户和密码，然后愉快的开始运行吧。

## Windows 后台运行
```sh
pythonw auto_login.py
```

## Mac & Linux 后台运行
```sh
nohup python3 auto_login.py 2>&1 &
```

## 注册 Windows 开机自启
1. 将 auto_login.py 改名成 auto_login.pyw，并右键创建快捷方式
2. 点击开始--所有程序--启动--右击--打开，将已快捷方式复制到该目录（C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup）下，可能杀毒软件会阻止，选择允许，然后重启电脑即可。

# 使用 docker 容器部署

## 方法一：下载 docker 镜像
*注：由于镜像中需要完整的 Chrome 环境，整个镜像较大*

```sh
docker pull coolmoon327/uestc-srun-telecom
```

## 方法二：使用 dockerfile 自动部署
*注：build 过程受网络影响严重，建议直接下载镜像*
```sh
# 如果发现没法成功 build, 很有可能是 chrome 相关组件需要梯子才能下载
# 需要在执行 docker build 前配置 terminal 的代理, 或者在路由器上配置代理
# 注: terminal 不会自动跟随系统代理设置
export all_proxy=socks5://代理服务器地址:代理端口

# build 命令
docker build -t uestc-srun-telecom:latest .
```

## 运行镜像
```sh
# 通过环境变量运行 docker 镜像
docker run -e SRUN_USERNAME='手机号' -e SRUN_PASSWORD='默认为12345678' uestc-srun-telecom

# 示例 1: 使用 dockerhub 的镜像
docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' coolmoon327/uestc-srun-telecom:latest

# 示例 2: 使用自己 build 的镜像
docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' uestc-srun-telecom
```

## NAS 部署
1. 在 NAS 的 docker 软件中找到本项目上传到 Hub 的 uestc-srun-telecom 镜像：
<div align="center"><img src="https://gitee.com/coolmoon327/picBed/raw/master/pictures/20220110165355.png" style="zoom: 30%;"></div>
2. 只需要修改两条环境变量即可使用：
<div align="center"><img src="https://gitee.com/coolmoon327/picBed/raw/master/pictures/20220110165127.png" style="zoom: 30%;"></div>

# 使用须知

## What's new
1. 本项目基于 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) 开发
2. 相对之前的 UESTC SRUN 项目，本项目重新在 2022 年测试电子科技大学清水河校区电信网络的接入网页，网址和 id 均有变化（经测试，在清水河校区无法使用旧的项目）
3. 在清水河校区的接入网页下，本项目为 input 修改 value 值，更改代码为 ` driver.execute_script(f'document.getElementById("username").value={self.username}')`
4. ~~web driver 在 [google 官方 api 仓库](http://chromedriver.storage.googleapis.com/index.html) 下载，请下载等于或低于本机 chrome 版本的 driver，下载后替换 webdriver 目录下的对应驱动文件~~
5. 如何使用请参考 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) ，或直接用 python 工具运行 auto_login.py 脚本
6. 在使用该脚本之前，请确保已经安装 chrome，尤其是 linux 用户需要检查依赖是否都安装完成
7. ~~该项目对 macOS 的支持存在兼容性问题，arm Mac 用户需要去 [仓库](http://chromedriver.storage.googleapis.com/index.html) 下载 arm macOS 对应的 Chrome 内核，并手动将 self.path 指定到该内核的位置（或者直接替换 chromedriver_mac64）~~


## Docker Build
1. 在本项目的根目录下使用 `docker build -t uestc-srun-telecom:latest .` 命令可自动生成 docker 镜像，运行容器将直接开启全自动的 SRUN 服务
2. 若使用 docker，推荐直接在容器中设置环境变量 SRUN_USERNAME 和 SRUN_PASSWORD 的值：`docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' uestc-srun-telecom:latest`
3. 如果希望自行构建 docker，可以在 dockerfile 中修改上述环境变量的值为你的账号和密码
4. 由于使用了官方的 Chrome 镜像，需要在 build 之前设置终端代理，这里以本地 Clash 为例： `export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890`
5. 整个 build 过程需要 ~~1000s 以上~~ 约46s，如果网速较快建议直接 [下载 image](https://hub.docker.com/repository/docker/coolmoon327/uestc-srun-telecom) 使用



## Author

👤 **coolmoon327**

* Github: [@coolmoon327](https://github.com/coolmoon327)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2022 [@coolmoon327](https://github.com/coolmoon327).<br />
This project is [MIT License](https://mit-license.org/) licensed.
