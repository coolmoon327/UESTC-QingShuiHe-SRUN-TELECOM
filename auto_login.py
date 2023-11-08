import os
import argparse
import config
import time
import logging
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from setup_cft import fetch_cft, get_platform


class AutoLogin(object):
    def __init__(self, username, password):
        self.portal_test_host: str = "1.1.1.1"
        self.login_gateway: str = "http://172.25.249.64"

        if "SRUN_USERNAME" in os.environ:
            SRUN_USERNAME = os.environ["SRUN_USERNAME"]
            if len(SRUN_USERNAME) > 3:
                self.username = SRUN_USERNAME
            else:
                self.username = username
        else:
            self.username = username
        if "SRUN_PASSWORD" in os.environ:
            SRUN_PASSWORD = os.environ["SRUN_PASSWORD"]
            if len(SRUN_PASSWORD) > 3:
                self.password = SRUN_PASSWORD
            else:
                self.password = password
        else:
            self.password = password

        if config.log:  # 记录log
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(level=logging.INFO)
            handler = logging.FileHandler(os.path.join(config.log_path, "log.txt"))
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            if config.debug:  # debug 在控制台输出
                console = logging.StreamHandler()
                console.setLevel(logging.INFO)
                self.logger.addHandler(console)

        self.options = Options()
        arguments = "--headless --disable-gpu --no-sandbox window-size=1920x1080 --hide-scrollbars"
        for arg in arguments.split():
            self.options.add_argument(arg)

        chrome_platform = get_platform()
        filename_ext = ".exe" if "win" in chrome_platform else ""
        self.path = (
            f"webdriver/chromedriver-{chrome_platform}/chromedriver{filename_ext}"
        )
        self.options.binary_location = f"webdriver/chrome-headless-shell-{chrome_platform}/chrome-headless-shell{filename_ext}"

    def _check_network(self):
        """
        检查网络是否畅通
        :return: Ture为畅通, False为不畅通。
        """
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (self.portal_test_host, 53)
            )
            return True
        except socket.error as exception:
            return False

    def _login_srun(self):
        s = Service(self.path)
        driver = webdriver.Chrome(service=s, options=self.options)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)  # 超时
        try:
            driver.get(self.login_gateway)
        except:
            self.logger.warning("Get gateway out of time....try again soon")
            return
        time.sleep(3)
        # username_box = driver.find_element(by=By.ID, value="username")
        # password_box = driver.find_element(by=By.ID, value="pwd")
        # username_box.send_keys(self.username)
        # password_box.send_keys(self.password)
        try:
            js_config_usr = (
                'document.getElementById("username").value="' + str(self.username) + '"'
            )
            js_config_pwd = (
                'document.getElementById("pwd").value="' + str(self.password) + '"'
            )
            driver.execute_script(js_config_usr)
            driver.execute_script(js_config_pwd)
            driver.find_element(by=By.ID, value="SLoginBtn_1").click()  # �~Y��~U
        except:
            self.logger.warning("Login error")
            driver.quit()
            return
        time.sleep(3)
        driver.quit()
        return

    def _login(self):
        """
        登录网络
        :return: 成功返回True 失败返回 False
        """
        i = 1
        while i <= config.retry:
            self.logger.info("Start trying times: {}".format(i))
            self._login_srun()
            time.sleep(10)
            status = self._check_network()
            if status:
                self.logger.info("Loging success")
                return True
            else:
                i += 1
                time.sleep(10)  # 等10秒再尝试
        if i > config.retry:
            self.logger.warning("Out of trying times")
            raise Exception("Out of trying times")

    def start(self):
        self.logger.info("Start watching network status")
        while True:
            # check是否掉线
            # self.logger.info("Checking network")
            if self._check_network():
                # self.logger.info("Network is good")
                pass
            else:
                self.logger.info("Network is disconnected. Try login now.")
                self._login()  # 重新登录
            time.sleep(config.check_time)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Parse arguments
    parser = argparse.ArgumentParser(
        prog="auto_login.py",
        description="Automated logging in for China Telecom's portal authentication in UESTC student apartments.",
    )
    parser.add_argument(
        "-u",
        "--update-cft",
        required=False,
        action="store_true",
        help="download/update chrome for test",
    )

    args = parser.parse_args()
    logger.debug(args)

    if args.update_cft:
        try:
            fetch_cft()
        except Exception:
            logger.error("Update chrome for test failed")

    login = AutoLogin(config.username, config.passowrd)
    login.start()
