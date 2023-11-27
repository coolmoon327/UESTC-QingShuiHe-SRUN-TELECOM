import logging

logger = logging.getLogger(__name__)

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from .download_cft import fetch_cft, search_cft


def get_cft_driver(
    chrome_options: str,
    cft_ver: str | None = None,
    target_dir: str = "./webdriver",
):
    """Get a chrome webdriver instance with automatically managed backend

    Args:
        chrome_options (str): arguments for chrome.
        cft_ver (str | None, optional): version of cft/driver. Defaults to None (latest).
        target_dir (str, optional): directory for the cft/driver. Defaults to "./webdriver".

    Returns:
        WebDriver: a new instance of the chrome driver
    """
    logging.debug("Start constructing chrome driver")
    webdriver_options = Options()
    for arg in chrome_options.split():
        webdriver_options.add_argument(arg)
    logging.debug(f"Options: {chrome_options}")

    chrome_dir, driver_dir = search_cft(target_dir)
    if chrome_dir == "" and driver_dir == "":
        logging.warning(f"No current installed chrome in {target_dir}, try downloading")
        chrome_dir, driver_dir = fetch_cft(target_dir, cft_ver)

    logging.debug(f"Chrome binary:{chrome_dir}")
    logging.debug(f"Chromedriver binary:{driver_dir}")
    webdriver_options.binary_location = chrome_dir

    driver = Chrome(service=Service(driver_dir), options=webdriver_options)

    return driver
