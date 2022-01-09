# 使用须知
## What's new
1. 本项目基于 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) 开发
2. 相对之前的 URESTC SRUN 项目，本项目重新在 2022 年测试电子科技大学清水河校区电信网络的接入网页，网址和 id 均有变化（经测试，在清水河校区无法使用旧的项目）
3. 在清水河校区的接入网页下，需要为 input 修改 value 值，更改代码为 ` driver.execute_script(f'document.getElementById("username").value={self.username}')`
4. web driver 在 [google 官方 api 仓库](http://chromedriver.storage.googleapis.com/index.html) 下载，请下载等于或低于本机 chrome 版本的 driver
5. 如何使用请参考 [SRUN 项目](https://github.com/RManLuo/srun_auto_login) ，或直接用 python 工具运行