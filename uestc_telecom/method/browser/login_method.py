from ..common import AutoLogin as BaseAutoLogin
from time import sleep
from selenium.webdriver.common.by import By
import logging

from .util import get_cft_driver

logger = logging.getLogger(__name__)


class AutoLogin(BaseAutoLogin):
    def __init__(self, username: str, password: str, login_gateway: str):
        """Get a PortalBrowserAutoLogin instance

        Args:
            username (str): username for login
            password (str): password for login
            login_gateway (str): gateway for login
        """
        super().__init__(username, password)
        self.login_gateway: str = login_gateway
        self.logger = logger

    def login(self) -> bool:
        driver = get_cft_driver(
            "start-maximized enable-automation --headless --disable-gpu --disable-browser-side-navigation --no-sandbox window-size=1920x1080 --hide-scrollbars --disable-dev-shm-usage"
        )
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)

        try:
            driver.get(self.login_gateway)
        except:
            logger.info("Portal auth page unreachable")
            return False

        try:
            js_config_usr = (
                'document.getElementById("username").value="' + str(self.username) + '"'
            )
            js_config_pwd = (
                'document.getElementById("pwd").value="' + str(self.password) + '"'
            )
            driver.execute_script(js_config_usr)
            driver.execute_script(js_config_pwd)
            driver.find_element(by=By.ID, value="SLoginBtn_1").click()
            sleep(1)  # for login request to complete
            driver.quit()
        except Exception as exception:
            self.logger.debug(exception)
            self.logger.warning("Login error")
            driver.quit()
            return False

        return True
