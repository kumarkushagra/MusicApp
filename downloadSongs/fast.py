# Downloads from the fast website, but it has ads and is slighlty error prone.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import downloadSongs.functions as functions

WEB_SITE_LINK = "https://yt.savetube.me/14-youtube-music-downloader-5djdh6"

def main(ROOT_DIR, LIBRARY, SONG_LINK):
    driver = functions.setup_driver(ROOT_DIR)
    wait = WebDriverWait(driver, 10)

    try:
        # Open the site
        driver.get(WEB_SITE_LINK)

        # Find the Input field and enter the song
        input_field = driver.find_element(By.CSS_SELECTOR, 'input.search-input')
        input_field.send_keys(SONG_LINK)

        # Wait and press the get link button on the site
        
        get_link_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get Link')]")))
        get_link_button.click()

        # Wait for the download button to be clickable
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Download']/parent::button")))
        download_button.click()

        # Wait for the download to complete and move the file
        functions.wait_for_download(ROOT_DIR)
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
