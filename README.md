<h1 align="center">电子科技大学清水河校区寝室电信网络自动接入工具</h1>
<p>
  <a href="https://mit-license.org/">
    <img alt="License: MIT License" src="https://img.shields.io/badge/License-MIT License-yellow.svg" target="_blank" />
  </a>
</p>

> 电子科技大学寝室网络（电信）自动后台常驻保证在线，支持 windows、linux、mac(x86)。mac(m1) 用户请自行更换 webdriver 目录下的 chromedriver_mac64 驱动。

# 一、使用 python 脚本完成自动化接入

### Requirements
```sh
requests
python >= 3.6
selenium >= 3.141.0
```
**本地安装的 Chrome 需要和 webdriver 目录下使用的 chromedriver 版本吻合！！！**

## Usage
在config.py文件中输入您的账户和密码，然后愉快的开始运行吧。

## WIndows后台运行
```sh
pythonw auto_login.py
```

## Mac and Linux后台运行
```sh
nohup python3 auto_login.py 2>&1 &
```

## 注册windows开机自启
1. 将auto_login.py 改名成auto_login.pyw，并右键创建快捷方式
2. 点击开始--所有程序--启动--右击--打开，将已快捷方式复制到该目录（C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup）下，可能杀毒软件会阻止，选择允许，然后重启电脑即可。

# 二、使用 docker 容器进行部署

## 方法一：下载 docker 镜像
（暂未上传镜像，请等待）

## 方法二：使用 dockerfile 自动部署
```sh
export all_proxy=socks5://代理服务器地址:代理端口
docker build -t docker build -t coolmoon-uestc-srun-telecom:lastest .
```

## 运行镜像
```sh
docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' coolmoon-uestc-srun-telecom:lastest
```

# 使用须知

## What's new
1. 本项目基于 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) 开发
2. 相对之前的 UESTC SRUN 项目，本项目重新在 2022 年测试电子科技大学清水河校区电信网络的接入网页，网址和 id 均有变化（经测试，在清水河校区无法使用旧的项目）
3. 在清水河校区的接入网页下，本项目为 input 修改 value 值，更改代码为 ` driver.execute_script(f'document.getElementById("username").value={self.username}')`
4. web driver 在 [google 官方 api 仓库](http://chromedriver.storage.googleapis.com/index.html) 下载，请下载等于或低于本机 chrome 版本的 driver，下载后替换 webdriver 目录下的对应驱动文件
5. 如何使用请参考 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) ，或直接用 python 工具运行 auto_login.py 脚本
6. 在使用该脚本之前，请确保已经安装 chrome，尤其是 linux 用户需要检查依赖是否都安装完成
7. 该项目对 macOS 的支持存在兼容性问题，arm Mac 用户需要去 [仓库](http://chromedriver.storage.googleapis.com/index.html) 下载 arm macOS 对应的 Chrome 内核，并手动将 self.path 指定到该内核的位置（或者直接替换 chromedriver_mac64）


## Docker Build
1. 在本项目的根目录下使用 `docker build -t docker build -t coolmoon-uestc-srun-telecom:lastest .` 命令可自动生成 docker 镜像，运行容器将直接开启全自动的 SRUN 服务
2. 若使用 docker，推荐直接在容器中设置环境变量 SRUN_USERNAME 和 SRUN_PASSWORD 的值：`docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' coolmoon-uestc-srun-telecom:lastest`
3. 如果希望自行构建 docker，可以在 dockerfile 中修改上述环境变量的值为你的账号和密码
4. 由于使用了官方的 Chrome 镜像，需要在 build 之前设置终端代理，这里以本地 Clash 为例： `export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890`
5. 整个 build 过程需要 1000s 以上，如果网速较快建议直接下载 image 使用



## Author

👤 **coolmoon327**

* Github: [@coolmoon327](https://github.com/coolmoon327)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2022 [@coolmoon327](https://github.com/coolmoon327).<br />
This project is [MIT License](https://mit-license.org/) licensed.