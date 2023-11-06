import requests
import json
from zipfile import ZipFile
from typing import Tuple
import os
import platform
import logging

logger = logging.getLogger(__name__)

cft_driver_repo = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"


# platform: linux64, mac-arm64, mac-x64, win32, win64
def get_target_url(platform: str) -> Tuple[str, str]:
    session = requests.session()
    good_ver_json = session.get(cft_driver_repo).text
    target_ver = json.loads(good_ver_json)["versions"][-1]

    headless_chrome_url: str = ""
    chromedriver_url: str = ""

    for entry in target_ver["downloads"]["chrome-headless-shell"]:
        if entry["platform"] == platform:
            headless_chrome_url = entry["url"]
    if headless_chrome_url == "":
        raise ValueError("Headless chrome N/A")

    for entry in target_ver["downloads"]["chromedriver"]:
        if entry["platform"] == platform:
            chromedriver_url = entry["url"]
    if chromedriver_url == "":
        raise ValueError("Chromedriver N/A")

    return headless_chrome_url, chromedriver_url


def download_unzip(target_path: str, url: str):
    # create dir

    if not os.path.exists(target_path):
        logger.info(f"Create dir: {target_path}")
        os.makedirs(target_path)

    # download
    logger.info(f"Downloading {url.split('/')[-1]} ver. {url.split('/')[-3]}")
    session = requests.session()
    response = session.get(url)
    filename = url.split("/")[-1]
    file = os.path.join(target_path, filename)

    r = requests.get(url, stream=True)
    with open(file, "wb") as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)

    # decompress
    logger.info(f"Decompressing to {target_path}")
    with ZipFile(file, "r") as f:
        f.extractall(target_path)

    # cleanup
    logger.info(f"Clean up: {file}")
    os.remove(file)


def get_platform() -> str:
    system = platform.system()
    arch = platform.architecture()
    machine = platform.machine()

    logger.debug(f"System: {system}")
    logger.debug(f"Architecture: {arch}")

    platform_both = "unknown"

    match system:
        case "Windows":
            match arch[0]:
                case "64bit":
                    platform_both = "win64"
                case "32bit":
                    platform_both = "win32"
        case "Darwin":
            match machine:
                case "aarch64":
                    platform_both = "mac-arm64"
                case "AMD64":
                    platform_both = "mac-x64"
        case "Linux":
            match arch[0]:
                case "64bit":
                    platform_both = "linux64"
        case _:
            logger.error(
                f"Unsupported Platform: {'\t'.join([system,arch[0],arch[1],machine])}"
            )

    return platform_both


def fetch_cft():
    # for test
    """
    for platform_chrome in ["linux64", "mac-arm64", "mac-x64", "win32", "win64"]:
        headless_chrome_url, chromedriver_url = get_target_url(platform_chrome)

        download_unzip('./webdriver', headless_chrome_url)
        download_unzip('./webdriver', headless_chrome_url)
    """

    platform_both = get_platform()

    logger.info(f"Chrome Platform: {platform_both}")

    logger.info(f"Geting Target")
    headless_chrome_url, chromedriver_url = get_target_url(platform_both)

    logger.info(f"Retriving")
    download_unzip("./webdriver", headless_chrome_url)
    download_unzip("./webdriver", chromedriver_url)


if __name__ == "__main__":
    fetch_cft()
