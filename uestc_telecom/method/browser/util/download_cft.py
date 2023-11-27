from genericpath import isfile
import requests, json, logging, os, ctypes
from zipfile import ZipFile
from typing import Tuple
from .get_platform import get_platform

cft_json_endpoint = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"

logger = logging.getLogger(__name__)


def __isAdmin() -> bool:
    try:
        return os.getuid() == 0  # type: ignore
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


class VersionNotFoundError(Exception):
    def __init__(self, version, endpoint):
        self.version = version
        self.endpoint = endpoint
        super().__init__(f"{version} was not found in endpoint {endpoint}")


class PlatformNotFoundError(Exception):
    def __init__(self, platform, endpoint):
        self.version = platform
        self.endpoint = endpoint
        super().__init__(f"{platform} was not found in endpoint {endpoint}")


# platform: linux64, mac-arm64, mac-x64, win32, win64
def get_target_url(platform: str, version: str | None = None) -> Tuple[str, str]:
    """Get the url of cft/driver bin zip for specified platform and version

    Args:
        platform (str): can be
        version (str | None, optional): target version. Defaults to None (get the latest).

    Raises:
        VersionNotFoundError: target version not found in cft endpoint
        PlatformNotFoundError: cft/driver of target platform not found in cft endpoint

    Returns:
        Tuple[str, str]: url for (headless cft, chromedriver)
    """
    session = requests.session()
    good_ver_json = session.get(cft_json_endpoint).text

    if version == None:
        target_ver = json.loads(good_ver_json)["versions"][-1]
    else:
        target_ver = None
        for versions in json.loads(good_ver_json)["versions"]:
            if versions["version"] == version:
                target_ver = versions
                break
        if target_ver == None:
            raise VersionNotFoundError(version, cft_json_endpoint)

    headless_chrome_url: str = ""
    chromedriver_url: str = ""

    for entry in target_ver["downloads"]["chrome-headless-shell"]:
        if entry["platform"] == platform:
            headless_chrome_url = entry["url"]
    if headless_chrome_url == "":
        raise PlatformNotFoundError(platform, cft_json_endpoint)
    for entry in target_ver["downloads"]["chromedriver"]:
        if entry["platform"] == platform:
            chromedriver_url = entry["url"]
    if chromedriver_url == "":
        raise PlatformNotFoundError(platform, cft_json_endpoint)

    return headless_chrome_url, chromedriver_url


def download_unzip(target_path: str, url: str):
    """Download a zip file from given url to target path

    Args:
        target_path (str): Where to store the unziped files
        url (str): Url for the zip file
    """
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


def search_cft(target_dir: str = "./webdriver") -> tuple[str, str]:
    platform_both = get_platform()

    filename_ext = ".exe" if "win" in platform_both else ""
    hdless_cft_dir = f"webdriver/chrome-headless-shell-{platform_both}/chrome-headless-shell{filename_ext}"
    driver_cft_dir = (
        f"webdriver/chromedriver-{platform_both}/chromedriver{filename_ext}"
    )

    if isfile(hdless_cft_dir) and isfile(driver_cft_dir):
        return (hdless_cft_dir, driver_cft_dir)
    else:
        return ("", "")


def fetch_cft(
    target_dir: str = "./webdriver", version: str | None = None
) -> tuple[str, str]:
    """Download Chrome for Testing and its webdriver of given version in target_dir, and returns the excutable dir for both

    Args:
        target_dir (str, optional): location of chrome(driver) bin. Defaults to "./webdriver".
        version (str | None, optional): version, e.g. 114.0.5713.0. Defaults to None (get the latest).

    Returns:
        tuple[str, str]: (Chrome excutable dir, Chromedriver excutable dir)
    """

    platform_both = get_platform()

    logger.info(f"Chrome Platform: {platform_both}")

    logger.info(f"Getting Target")
    headless_chrome_url, chromedriver_url = get_target_url(platform_both, version)

    logger.info(f"Retriving")
    download_unzip(target_dir, headless_chrome_url)
    download_unzip(target_dir, chromedriver_url)

    # filename_ext = ".exe" if "win" in platform_both else ""
    hdless_cft_dir = (
        f"webdriver/chrome-headless-shell-{platform_both}/chrome-headless-shell"
    )
    driver_cft_dir = f"webdriver/chromedriver-{platform_both}/chromedriver"

    ## Automactically grant the permission if ran privileged, else return a warning
    if platform_both in ["linux64", "mac-x64", "mac-arm64"]:
        if __isAdmin():
            os.chmod(hdless_cft_dir, 777)
            os.chmod(driver_cft_dir, 777)
            logger.info(f"Granted permission to {hdless_cft_dir} {driver_cft_dir}`")
        else:
            logger.warning(
                f"For unix, run `chmod 777 {hdless_cft_dir} {driver_cft_dir}`"
            )

    return (hdless_cft_dir, driver_cft_dir)
