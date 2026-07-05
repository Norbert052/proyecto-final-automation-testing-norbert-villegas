from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import platform


def get_driver():
    is_github_actions = os.getenv("GITHUB_ACTIONS", "false").lower() == "true"
    is_linux = platform.system().lower() == "linux"

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if is_github_actions:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    driver_manager = ChromeDriverManager()
    driver_path = driver_manager.install()

    if os.path.isdir(driver_path):
        for candidate in ("chromedriver", "chromedriver.exe"):
            candidate_path = os.path.join(driver_path, candidate)
            if os.path.exists(candidate_path):
                driver_path = candidate_path
                break
    else:
        driver_dir = os.path.dirname(driver_path)
        fallback_name = "chromedriver.exe" if platform.system().lower() == "windows" else "chromedriver"
        fallback_path = os.path.join(driver_dir, fallback_name)
        if os.path.exists(fallback_path):
            driver_path = fallback_path

    service = Service(driver_path)
    options.add_argument("--start-maximized")

    return webdriver.Chrome(service=service, options=options)
