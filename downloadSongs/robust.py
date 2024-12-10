# Robust site, but the download is slow

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import downloadSongs.functions as functions

MAX_FILE_SIZE_MB = 10  
WEB_SITE_LINK = "https://ytmp3.la/en-yMP0/"

def main(ROOT_DIR, LIBRARY, SONG_LINK):
    driver = functions.setup_driver(ROOT_DIR)

    try:
        # Open the site
        driver.get(WEB_SITE_LINK)
        
        # Find the Input field and enter the song
        input_field =  driver.find_element(By.ID, "video")
        input_field.send_keys(SONG_LINK)
        
        # Wait and press the convert button
        convert_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Convert']")))
        convert_button.click()

        # Wait for the Download button to appear after conversion
        download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Download']")))
        download_button.click()

        # Wait for the download to complete and move the file
        functions.wait_for_download(ROOT_DIR)
        downloaded_file = functions.get_most_recent_file(ROOT_DIR)
            
        file_size = os.path.getsize(downloaded_file) / (1024 * 1024)  # Convert bytes to MB
        print(f"Downloaded file size: {file_size:.2f} MB")

        # If the file is larger than 10 MB, delete it and abort the operation
        if file_size > MAX_FILE_SIZE_MB:
            print("File size exceeds 10 MB. Aborting download.")
            os.remove(downloaded_file)  # Remove the large file
        else:
            # Move the file to the library if it's under the size limit
            functions.move_file_to_library(ROOT_DIR, LIBRARY)

    except Exception as e:
        print(e)
        raise
    
    finally:
        driver.quit()


if __name__ == "__main__":
    ROOT_DIR = os.getcwd()
    LIBRARY = os.path.join(os.getcwd(), "library")
    SONG_LINK = ""
    main(ROOT_DIR, LIBRARY, SONG_LINK)
