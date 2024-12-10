import time, os, shutil
from selenium import webdriver


def wait_for_download(directory):    
    while True:
        files_in_folder = os.listdir(directory)
        if any(file.endswith('.mp3') for file in files_in_folder):  
            return
        time.sleep(1)


def move_file_to_library(source, target):
    try:
        files_in_folder = os.listdir(source)
        filename = next((file for file in files_in_folder if file.endswith('.mp3')), None)
        src = os.path.join(source, filename)
        dest = os.path.join(target, filename)
        shutil.move(src, dest)
        print("Moved song to the library successfully")

    except Exception as e:
        print(f"Unable to move, exception: {e}")


def setup_driver(download_dir):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--download-default-directory={download_dir}')
    chrome_options.add_argument('--disable-gpu')  
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-application-cache')  
    chrome_options.add_argument('--disk-cache-size=1')  
    chrome_options.add_argument('--disable-logging')  
    chrome_options.add_argument('--disable-extensions') 
    chrome_options.add_argument('--disable-software-rasterizer')  
    chrome_options.add_argument('--headless')  

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver
