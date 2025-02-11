from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

# Ensure SBR_WEBDRIVER is set correctly
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER", "http://localhost:4444/wd/hub")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional
chrome_options.add_argument("--disable-gpu")

# Use local ChromeDriver instead of Remote WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def scrape_website(website):
    print("Connecting to Scraping Browser...")
    
    if not SBR_WEBDRIVER:
        raise ValueError("SBR_WEBDRIVER is not set. Check your WebDriver path.")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    chrome_options.add_argument("--disable-gpu")
    
    # Use WebDriver Remote properly
    driver = webdriver.Remote(command_executor=SBR_WEBDRIVER, options=chrome_options)

    try:
        driver.get(website)
        print("Waiting for captcha to solve...")
        
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html

    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove scripts and styles
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Clean text
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
