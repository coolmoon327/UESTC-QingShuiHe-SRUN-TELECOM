import logging
from logging.handlers import RotatingFileHandler
import argparse
import os
import sys

logger = logging.getLogger(__name__)

# arguments = {
#     "prog": "auto_login.py",
#     "description": "Automated logging in for China Telecom's portal authentication in UESTC student apartments.",
#     "arguments": [
#         {
#             "flags": ["-u", "--update-cft"],
#             "required": False,
#             "action": "store_true",
#             "help": "download/update chrome for test",
#         }
#     ],
# }


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auto_login.py",
        description="Automated logging in for China Telecom's portal authentication in UESTC student apartments.",
    )
    parser.add_argument(
        "-u",
        "--update-cft",
        required=False,
        action="store_true",
        help="(legacy) download/update newest chrome for test and corresponding driver",
    )
    parser.add_argument(
        "-i",
        "--userid",
        required=False,
        action="store",
        help="username",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=False,
        action="store",
        help="password",
    )
    parser.add_argument(
        "--method",
        required=False,
        default="request",
        action="store",
        help="loging method, available: browser, request",
    )
    parser.add_argument(
        "-g",
        "--login-gateway",
        required=False,
        default="http://172.25.249.64",
        help="address of the portal page, should have scheme (e.g. 'http://...')",
    )
    parser.add_argument(
        "--interval",
        action="store",
        default=10,
        help="interval (s) for connectivity check / retry",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="enable debug output",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        default=False,
        help="disable output in shell",
    )
    parser.add_argument(
        "--logfile",
        action="store",
        default=os.path.dirname(os.path.abspath(__file__)) + "/log/autologin.log",
        help="log file location",
    )

    return parser


if __name__ == "__main__":
    arguments = get_argparser().parse_args()

    ## logging
    logging_level = logging.DEBUG if arguments.debug else logging.INFO
    logging.basicConfig(level=logging_level)
    logging.getLogger("").handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    console_handler.setLevel(logging_level)
    if not arguments.silent:
        logging.getLogger("").addHandler(console_handler)

    if not os.path.exists(os.path.dirname(arguments.logfile)):
        os.mkdir(os.path.dirname(arguments.logfile))
    file_handler = RotatingFileHandler(filename=arguments.logfile, maxBytes=5000000)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    )
    file_handler.setLevel(logging_level)
    logging.getLogger("").addHandler(file_handler)

    ## --update-cft
    if arguments.update_cft:
        from method.browser.util import fetch_cft

        logger.info("Installing CFT")
        try:
            chrome_dir, driver_dir = fetch_cft("./webdriver")
            logger.info(f"CFT installed in {chrome_dir}, {driver_dir}")
            exit(0)
        except Exception as exception:
            logger.error("Error when downloading CFT")

    ## login
    username, password = None, None
    if "SRUN_USERNAME" in os.environ and len(os.environ["SRUN_USERNAME"]) > 3:
        username = os.environ["SRUN_USERNAME"]
    if "SRUN_PASSWORD" in os.environ and len(os.environ["SRUN_PASSWORD"]) > 3:
        password = os.environ["SRUN_PASSWORD"]
    if arguments.userid:
        username = arguments.userid
    if arguments.password:
        password = arguments.password
    if username == None or password == None:
        logger.critical("Username / password not provided", exc_info=True)
        exit(1)

    match str(arguments.method):
        case "request":
            from method import RequestAutoLogin

            auto_login = RequestAutoLogin(
                username, arguments.password, arguments.login_gateway
            )
        case "browser":
            from method import BrowserAutoLogin

            auto_login = BrowserAutoLogin(
                username, arguments.password, arguments.login_gateway
            )
        case _:
            raise ValueError("Invalid login method")

    auto_login.monitor(interval=int(arguments.interval))
