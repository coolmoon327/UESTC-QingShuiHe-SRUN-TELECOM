# 使用须知
## What's new
1. 本项目基于 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) 开发
2. 相对之前的 UESTC SRUN 项目，本项目重新在 2022 年测试电子科技大学清水河校区电信网络的接入网页，网址和 id 均有变化（经测试，在清水河校区无法使用旧的项目）
3. 在清水河校区的接入网页下，本项目为 input 修改 value 值，更改代码为 ` driver.execute_script(f'document.getElementById("username").value={self.username}')`
4. web driver 在 [google 官方 api 仓库](http://chromedriver.storage.googleapis.com/index.html) 下载，请下载等于或低于本机 chrome 版本的 driver，下载后替换 webdriver 目录下的对应驱动文件
5. 如何使用请参考 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) ，或直接用 python 工具运行 auto_login.py 脚本
6. 在使用该脚本之前，请确保已经安装 chrome，尤其是 linux 用户需要检查依赖是否都安装完成
7. 该项目对 macOS 的支持存在兼容性问题，arm Mac 用户需要去 [仓库](http://chromedriver.storage.googleapis.com/index.html) 下载 arm macOS 对应的 Chrome 内核，并手动将 self.path 指定到该内核的位置（或者直接替换 chromedriver_mac64）

## Docker 构建
1. 在本项目的根目录下使用 `docker build -t UESTC-QingShuiHe-SRUN-TELECOM:lastest .` 命令可自动生成 docker 镜像，运行容器将直接开启全自动的 SRUN 服务
2. 若使用 docker，推荐直接在容器中设置环境变量 SRUN_USERNAME 和 SRUN_PASSWORD 的值：`docker run -e SRUN_USERNAME='your_username' -e SRUN_PASSWORD='your_password' your_docker_name`
3. 如果希望自行构建 docker，可以在 dockerfile 中修改上述环境变量的值为你的账号和密码