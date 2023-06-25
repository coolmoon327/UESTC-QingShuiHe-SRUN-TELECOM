import detect_chrome
import requests
import os 
import zipfile
import platform

def update_chrome_driver():
        
    # obtain installed chrome version

    chrome_version = ".".join(detect_chrome.get_chrome_version().split('.')[:3])
    driver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + chrome_version
    response = requests.get(driver_version_url)
    driver_version = response.text

    # discriminate system and architecture

    system = platform.system()
    machine = platform.machine()

    if system == 'Windows':
        if machine.endswith(('64', '86')):
            platform_driver_zipfilename = "chromedriver_win32.zip"
            platform_driver_filepath = "./webdriver/" + "chromedriver.exe"
        else:
            raise OSError("Unsupported architecture: " + system + machine)
    elif system == 'Linux':
        if machine == 'x86_64':
            platform_driver_zipfilename = "chromedriver_linux64.zip"
            platform_driver_filepath = "./webdriver/" + "chromedriver_linux64"
        else:
            raise OSError("Unsupportedarchitecture: " + system + machine)
    elif system == 'Darwin':
        if machine == 'arm64':
            platform_driver_zipfilename = "chromedriver_mac64.zip"
            platform_driver_filepath = "./webdriver/" + "chromedriver_mac64"
        elif machine == 'x86_64':
            platform_driver_zipfilename = "chromedriver_mac_arm64.zip"
            platform_driver_filepath = "./webdriver/" + "chromedriver_mac64_m1"
        else:
            raise OSError("Unsupported architecture: " + system + machine)
    else:
        raise OSError("Unsupported operating system: " + system)

    # download corresponding chrome driver

    driver_file_url = "/".join(["https://chromedriver.storage.googleapis.com",
                                driver_version,
                                platform_driver_zipfilename])
    platform_driver_zipfilepath = "./webdriver/" + driver_version + "." + platform_driver_zipfilename
    if not os.path.exists("./webdriver"): os.makedirs("./webdriver")
    with open(platform_driver_zipfilepath, "wb") as file:
        file.write(requests.get(driver_file_url).content)
        
    # extract the driver file

    with zipfile.ZipFile(platform_driver_zipfilepath, 'r') as driver_file:
        for file in driver_file.namelist():
            if file == 'chromedriver.exe' if system == 'Windows' else 'chromedriver' and file != 'LICENSE.chromedriver':
                driver_file.extract(file, "./webdriver/")
                if system != 'Windows':
                    if os.path.exists(platform_driver_filepath): os.remove(platform_driver_filepath)
                    os.rename("./webdriver/" + file, platform_driver_filepath)

    os.remove(platform_driver_zipfilepath)

if __name__ == '__main__':
    update_chrome_driver()