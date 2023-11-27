from time import sleep
import logging
from requests import head


class AutoLogin(object):
    def __init__(self, username: str, password: str):
        self.logger = logging.getLogger(__name__)
        self.connection_test_host: str = "1.1.1.1"
        self.username = username
        self.password = password

    def _have_internet(self, test_host: str = "1.1.1.1") -> bool:
        """Check if can reach internet via request https header, and return true/false for success/failure
        Args:
            test_host (str, optional): host for connection test. Defaults to 1.1.1.1
        """
        if test_host == "":
            test_host = self.connection_test_host
        url = "https://" + test_host

        try:
            head(url, timeout=3)
            self.logger.debug("Connection Tested OK")
            return True
        except:
            self.logger.info("Internet Connection Test Failed")
            return False

    def login(self) -> bool:
        """Try login for once, and return true/false for success/failure"""
        self.logger.info("Try logging in")
        return False

    def monitor(self, interval: int = 10):
        """Continuously monitor network status, and try login() when disconnected

        Args:
            interval (int, optional): interval between check. Defaults to 10.
        """
        self.logger.info("Start monitoring network status")
        while True:
            self.logger.info("Checking connectivity")
            if self._have_internet():
                self.logger.info("Connected to internet")
                pass
            else:
                self.logger.info("Disconnected to internet")
                try:
                    self.logger.info("Try login")
                    self.login()
                except:
                    pass
            sleep(interval)
