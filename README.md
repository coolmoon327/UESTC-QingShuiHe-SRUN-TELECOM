

<h1 align="center">电子科技大学清水河校区寝室电信网络自动接入工具</h1>

<p>
  <a href="https://mit-license.org/">
    <img alt="License: MIT License" src="https://img.shields.io/badge/License-MIT License-yellow.svg" target="_blank" />
  </a>
</p>

> 电子科技大学寝室的电信网络自动登录工具，可通过无头浏览器或模拟登录请求自动登录。可用于无人值守情况下主机/ Homelab / NAS 保持在线。
> 
> 支持 linux64, mac-arm64, mac-x64, win32, win64。

## 这是什么？

这是电子科技大学，清水河校区寝室的电信“宽带”/Wifi网络的自动登录工具

<details>

<summary>为什么我需要它？</summary>

校内电信营业厅提供的“宽带”可通过寝室楼公共的 `ChinaTelecom-EDU5.8/2.4G` Wifi 或 寝室内的RJ45以太网接口 接入。两者均通过 Portal 认证 ———— 这一认证页面通常会在系统进行 Captive Portal 检查时“自动”出现，在安卓上为一则 “网络……需要认证” 的通知，而在 Windows 上为通过默认浏览器弹出的 Portal 页面。

但因为

1. 清水河校区本科楼十一月初至四月底夜间断电。
2. 寝室内的以太网接口没有持久化登录：断开后重连即需重新认证；而公共Wifi的持久化登录时间很短。
3. 电信提供的网络早先只支持一个设备同时登录。
4. 认证界面地址 `http://172.25.249.64/eportal/index.jsp?...` 频繁抽风，表现为不能自动跳转认证界面、访问认证界面时报 `502 bad gateway` 。

这会导致如下问题：

1. 以上网络均有AP隔离，这会导致依赖局域网的服务和应用无法正常工作。
2. 你的NAS、打印机或是自制物联网小玩具等没有可直接操作的 Web 界面的设备无法连接到网络。
3. 每次设备离开公共Wifi范围，或是断开以太网连接后，均需要重新认证。频率可高达一天数次
4. 原因 4 中的认证界面抽风的发生频率高到令人沮丧

即使使用路由器来实现多设备共享同一“宽带”账号，由于原因 1，登录频率也只是降为了一天一次，并且网络SLA视起床时间而定，总的来说低于 73%。

因此，使用自动脚本可以节约您宝贵的生命。

</details>

## 如何使用？

### Usage

```
usage: cli.py [-h] [-u] [-i USERID] [-p PASSWORD] [--method METHOD] [-g LOGIN_GATEWAY] [--interval INTERVAL] [--debug] [--silent] [--logfile LOGFILE]

Automated logging in for China Telecom's portal authentication in UESTC student apartments.

options:
  -h, --help            show this help message and exit
  -u, --update-cft      (legacy) download/update newest chrome for test and corresponding driver
  -i USERID, --userid USERID
                        username
  -p PASSWORD, --password PASSWORD
                        password
  --method METHOD       loging method, available: browser, request
  -g LOGIN_GATEWAY, --login-gateway LOGIN_GATEWAY
                        address of the portal page, should have scheme (e.g. 'http://...')
  --interval INTERVAL   interval (s) for connectivity check / retry
  --debug               enable debug output
  --silent              disable output in shell
  --logfile LOGFILE     log file location
```

### 直接部署

<details> 

<summary>Requirements</summary>

```sh
requests
argparse
python >= 3.10
selenium >= 3.141.0
```

</details> 

<details> 

<summary>Linux 下的 chrome for testing 的依赖问题</summary>

在Linux下，直接下载的Chrome for testing 及 chromedriver二进制，需手动配置依赖库，详见 https://stackoverflow.com/a/76734752

```sh
apt-get install -y unzip xvfb libxi6 libgconf-2-4 jq libjq1 libonig5 libxkbcommon0 libxss1 libglib2.0-0 libnss3 \
  libfontconfig1 libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0 libpango-1.0-0 libgdk-pixbuf2.0-0 libxcomposite1 \
  libxcursor1 libxdamage1 libxtst6 libappindicator3-1 libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libxfixes3 \
  libdbus-1-3 libexpat1 libgcc1 libnspr4 libgbm1 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxext6 \
  libxrandr2 libxrender1 gconf-service ca-certificates fonts-liberation libappindicator1 lsb-release xdg-utils
```

</details> 

#### Unix

```sh
# Clone this project to local
git clone https://github.com/coolmoon327/UESTC-QingShuiHe-SRUN-TELECOM.git 
cd "./UESTC-QingShuiHe-SRUN-TELECOM"

# Install chrome for testing and its chrome driver (optional, needed for using brower login mode)
# the previledge is for automatic granting of excutable permission
sudo python3 uestc_telecom/cli.py -u

# Run autologin
python3 uestc_telecom/cli.py --method request --userid 19912344321 --password 12345678
```

#### Windows

```powershell
# Clone this project to local
git clone "https://github.com/coolmoon327/UESTC-QingShuiHe-SRUN-TELECOM.git"
Set-Location ".\UESTC-QingShuiHe-SRUN-TELECOM"

# Install chrome for testing and its chrome driver (optional, needed for using brower login mode)
python3 uestc_telecom\cli.py -u

# Run autologin
python3 uestc_telecom\cli.py --method request --userid 19912344321 --password 12345678
```
<details> 

<summary>Chrome for Testing / Chromedriver 配置</summary>

#### Chrome for Testing / Chromedriver 二进制获取

**方法 A**： Chrome for testing 及 Chrome driver 可通过 `python .\setup_cft.py`, `auto_login.py` 自动获取。获取到的 `./webdriver/chromedriver-xxx/chromedriver` 与 `./webdriver/chrome-headless-shell-xxx/chrome-headless-shell` 文件需要设置权限（如 chmod 777）。

**方法 B**：（不推荐）手动从 [googlechromelabs](https://googlechromelabs.github.io/chrome-for-testing/) 下载。需将对应平台、相互匹配的 `chrome-headless-shell.zip` 及 `chromedriver.zip` 下载并解压至 ./webdriver/。 

在Linux下，通过方法 A 或方法 B 完成 Chrome for testing 及 Chrome driver 的下载后，需配置 Chrome for testing 的依赖库。详见前文 “Linux 下的 chrome for testing 的依赖问题”

</details> 

### 作为服务部署

#### Windows 后台运行

```powershell
pythonw auto_login.py
```

#### Unix 后台运行

```sh
nohup python3 auto_login.py 2>&1 &
```

#### Winsw

详见 https://github.com/winsw/winsw 

<details>

```xml
-- uestc_telecom.xml --
<service>
  <id>uestc-telecom-autologin</id>
  <name>Uestc Telecom Autologin</name>
  <description>Auto login for China Telecom APs in UESTC</description>
  <executable>C:\Directory\To\Your\Python\Excutable</executable>
  <workingdirectory>%BASE%</workingdirectory>
  <arguments>%BASE%\uestc_telecom\cli.py --userid "19912344321" --password "12345678" --silent</arguments>

  <onfailure action="restart" delay="2 sec" />
  <onfailure action="restart" delay="10 sec" />
  <onfailure action="none" />

  <delayedAutoStart>true</delayedAutoStart>

  <logpath>%BASE%\log\service</logpath>
  <log mode="roll" />
</service>
```

</details>

#### Systemd

<details>

```ini
[Unit]
Description=Uestc Telecom Autologin
Documentation=https://github.com/coolmoon327/UESTC-QingShuiHe-SRUN-TELECOM
After=network.target nss-lookup.target

[Service]
User=nobody
NoNewPrivileges=true
ExecStart=/usr/local/bin/python3 /dir/to/uestc_telecom/cli.py --userid "19912344321" --password "12345678" --silent
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

</details>


### 使用 docker 容器部署

#### A. 下载 docker 镜像
*注：由于镜像中需要完整的 Chrome 环境，体积为 ~1450 MB。 如果不需要 `browser` 登录方式，SLIM 镜像体积可减至 ~700 MB*

```sh
# x86-64 完整版，体积较大，可以指定 `method` 为 `request` 与 `browser`，适用于大多数场景
docker pull coolmoon327/uestc-srun-telecom

# x86-64 精简版，体积较小，只能指定 `method` 为 `request`
docker pull coolmoon327/uestc-srun-telecom-slim

# arm-64 完整版，体积较大，可以指定 `method` 为 `request` 与 `browser`，适用于苹果设备与大多数 arm 设备
docker pull coolmoon327/uestc-srun-telecom-arm64

# arm-64 精简版，体积较小，只能指定 `method` 为 `request`
docker pull coolmoon327/uestc-srun-telecom-arm64-slim
```

#### B. 使用 dockerfile 自动部署

*注： 构建过程需要完整的国际互联网环境，或国内镜像源。如果构建过慢，或出现网络相关错误，你可能需要检查以上条件是否生效。详见 [awesome-mirrors#docker](https://github.com/pengisgood/awesome-mirrors#docker)*

```sh
# 构建命令
docker build -t uestc-srun-telecom:latest .

# 构建命令（不含 Chrome 环境，无 browser 登录支持）
# 在 Dockerfile 设置 ARG SLIM=1
docker build -t uestc-srun-telecom:latest .
```

#### 运行镜像

运行镜像时至少需提供 `SRUN_USERNAME` 和 `SRUN_PASSWORD` 两个环境变量，分别为你的手机号和密码。
`SRUN_METHOD` 指定登录方式（精简 `request` 或基于浏览器 `browser`）。

```sh
# 运行自行构建的镜像
docker run -e SRUN_USERNAME='手机号' -e SRUN_PASSWORD='默认为12345678' -e SRUN_METHOD='request | browser' uestc-srun-telecom

# 运行预构建镜像：将上述命令中 uestc-srun-telecom 改为你下载的预构建镜像名
```

#### NAS 部署（*预构建镜像尚未更新）
1. 在 NAS 的 docker 软件中找到本项目上传到 Hub 的 uestc-srun-telecom 镜像：
<div align="center"><img src="https://gitee.com/coolmoon327/picBed/raw/master/pictures/20220110165355.png" style="zoom: 20%;"></div>
2. 只需要修改两条环境变量即可使用：
<div align="center"><img src="https://gitee.com/coolmoon327/picBed/raw/master/pictures/20220110165127.png" style="zoom: 30%;"></div>

## 更新日志
- 2023.11.27: 重构了项目结构。添加了更轻量的构造登录请求的自动登录方式（可能随电信登录前端更新而失效，但他们更新的概率很低……）。

- 2023.11.7: 转为使用[独立的无头chrome for testing及chromedriver](https://developer.chrome.com/blog/chrome-for-testing/)，不再需要完整的chrome环境或配置对应版本的webdriver。

- 2023.6.23: [@yao-yun](https://github.com/yao-yun) 提供了 chromium 内核的自动检测与下载的更新，无需用户自行配置驱动。

- 2022.12.12: 修复 issue #2 提到的 dockerfile 的问题。

- 2022.9.30: 电信入网登陆地址发生变动 172.25.249.8 -> 172.25.249.64
  
> 如何查看入网地址? 当无法正常使用该工具时, 请手动在浏览器进入入网登陆页面, 然后在命令行中传入 `--login-gateway "http://*.*.*.*"` 参数。


## 使用须知

### What's new
1. 参考了 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) 中基于 selenium 的浏览器自动登录方法
2. 相对之前的 UESTC SRUN 项目，本项目重新在 2022 年测试电子科技大学清水河校区电信网络的接入网页，网址和 id 均有变化（经测试，在清水河校区无法使用旧的项目）
3. 在清水河校区的电信认证网页下，本项目为 input 修改 value 值，更改代码为 ` driver.execute_script(f'document.getElementById("username").value={self.username}')`
4. 额外提供了构造登录请求认证的自动登录方法
5. 转为使用[独立的无头chrome for testing及chromedriver](https://developer.chrome.com/blog/chrome-for-testing/)，不再需要完整的chrome环境或手动配置对应版本的webdriver。


### Dockerfile Build
1. 在本项目的根目录下使用 `docker build -t uestc-srun-telecom:latest .` 命令可自动生成 docker 镜像，运行容器将直接开启全自动的 SRUN 服务
2. 若使用 docker，推荐直接在容器中设置环境变量 SRUN_USERNAME 和 SRUN_PASSWORD 的值：`docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' uestc-srun-telecom:latest`
3. 自行构建dockerfile时，可以在 dockerfile 中修改上述环境变量的值为你的账号和密码
4. 由于使用了官方的 Chrome 镜像，需要在 build 之前设置终端代理，这里以本地 Clash 为例： `export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890`
5. 整个 build 过程需要约10min，如果网速较快建议直接 [下载 image](https://hub.docker.com/repository/docker/coolmoon327/uestc-srun-telecom) 使用

## Author / Collaborator

👤 Author: **coolmoon327** 

* Github: [@coolmoon327](https://github.com/coolmoon327)

👤 Collaborator: **yao-yun** 

* Github: [@yao-yun](https://github.com/yao-yun)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2022 [@coolmoon327](https://github.com/coolmoon327).<br/>
This project is [MIT License](https://mit-license.org/)licensed.
