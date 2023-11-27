from ..common import AutoLogin as BaseAutoLogin
from typing import Tuple
from urllib.parse import urlparse, quote_plus
import requests
import logging
from json import loads


logger = logging.getLogger(__name__)


class NoInfoforLogin(Exception):
    def __init__(self):
        super().__init__(f"Info needed for constructing request can not be fetched")


class AutoLogin(BaseAutoLogin):
    def __init__(self, username: str, password: str, login_gateway: str):
        super().__init__(username, password)

        self.login_gateway = login_gateway
        self.header = None
        self.loginpayload = None
        self.logger = logger

    def login(self) -> bool:
        self.logger.info("Logging via constructing POST")
        try:
            self.logger.debug(f"Getting necessary info from {self.login_gateway + '/eportal/redirectortosuccess.jsp'}")
            self.__get_info(self.login_gateway + "/eportal/redirectortosuccess.jsp")
            self.logger.debug(f"Info got: {self.query_string}")
        except NoInfoforLogin:
            self.logger.warning("Failed to fetch connection info")
            return False
        except Exception as exception:
            self.logger.warning(f"Unknown error: {exception}")
            return False
        self.header = self.__construct_request_header(
            self.login_gateway, self.query_string
        )
        self.logger.debug(f"Header constructed: {self.header}")
        e, m = (
            0x10001,
            0x94DD2A8675FB779E6B9F7103698634CD400F27A154AFA67AF6166A43FC26417222A79506D34CACC7641946ABDA1785B7ACF9910AD6A0978C91EC84D40B71D2891379AF19FFB333E7517E390BD26AC312FE940C340466B4A5D4AF1D65C3B5944078F96A1A51A5A53E4BC302818B7C9F63C4A1B07BD7D874CEF1C3D4B2F5EB7871,
        )
        self.encrypted_passwd = self.__encrypt_passwd(m, e, self.password)
        self.loginpayload = self.__construct_login_payload(
            self.username, self.encrypted_passwd, self.query_string
        )
        self.logger.debug(f"Login Payload constructed: {self.loginpayload}")

        try:
            response = requests.post(
                self.login_gateway + "/eportal/InterFace.do?method=login",
                headers=self.header,
                data=self.loginpayload,
            )
        except Exception as exception:
            self.logger.warning(
                f"Error when sending POST request to log in: {exception}"
            )
            return False

        if response.status_code == 200:
            self.logger.info("POST login successful")
            self.logger.debug("Response content:", response.text.encode("uft-8"))
            return True
        else:
            self.logger.info(
                "POST request failed with status code:", response.status_code
            )
            return False

    def __get_info(
        self,
        redirect_startpoint: str,
    ) -> None:
        """Get querystring, which includes info on the AP to be authenticated

        Args:
            redirect_startpoint (str): the starting point of redirection
        Raises:
            NoInfoforLogin: when connection to redirect_startpoint failed
        """
        resp = requests.get(
            redirect_startpoint,
            allow_redirects=False,
        )
        next = resp.headers.get("Location")
        if next == None or resp.status_code != 302:
            raise NoInfoforLogin()

        resp = requests.get(next, allow_redirects=False)
        self.referer = resp.headers.get("Location")
        if self.referer == None:
            raise NoInfoforLogin()
        self.logger.debug(self.referer)
        self.logger.debug(f"referer: {self.referer}")

        parsed_url = urlparse(self.referer)
        self.query_string = str(parsed_url.query)
        self.logger.debug(f"quert_string: {self.query_string}")

        return

    def __construct_request_header(self, login_gateway: str, query_string: str) -> dict:
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": urlparse(login_gateway).hostname,
            "Origin": login_gateway,
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Referer": "http://172.25.249.64/eportal/index.jsp?" + query_string,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }

    def __construct_login_payload(
        self, username: str, encrypted_passwd: str, query_string: str
    ):
        payload = {
            "userId": username,
            "password": encrypted_passwd,
            "service": "",
            "queryString": quote_plus(query_string),
            "operatorPwd": "",
            "operatorUserId": "",
            "validcode": "",
            "passwordEncrypt": "true",
        }

        return payload

    def __get_pubkey(self) -> Tuple[int, int]:
        response = requests.get(
            self.login_gateway + "/eportal/InterFace.do?method=pageInfo",
            headers=self.header,
            data={"queryString": quote_plus(self.query_string)},
        )
        resp_json = loads(response.text)
        e = int(resp_json["publicKeyExponent"], 16)
        m = int(resp_json["publicKeyModulus"], 16)

        return (e, m)

    def __encrypt_passwd(self, m: int, e: int, passwd: str) -> str:
        passwdwithmac = passwd + ">111111111"
        ## self.logger.debug(f"Encrypting passwd: {passwdwithmac}")
        encoded = int.from_bytes(passwdwithmac.encode("utf-8"), byteorder="big")
        ## self.logger.debug(format(encoded, "x"))
        crypt = pow(encoded, e, m)
        encrypted_pass = format(crypt, "x")
        ## self.logger.debug(encrypted_pass)

        return encrypted_pass
