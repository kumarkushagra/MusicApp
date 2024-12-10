import os
import time
import downloadSongs.fast as fast
import downloadSongs.robust as robust

# SETUP
MAX_ATTEMPTS = 2
ROOT_DIR = os.getcwd()
LIBRARY = os.path.join(os.getcwd(), "library")

# main code
def main(SONG_LINK):
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        print(f"Attempt {attempts + 1} of {MAX_ATTEMPTS} to download from fast site.")
        try:
            fast.main(ROOT_DIR, LIBRARY, SONG_LINK)
            print("Download successful from the fast site.")
            return True
        except Exception as e:
            print(f"Fast site download failed: {e}")
            
        attempts += 1
        time.sleep(1)

    try:
        print(f"Fast site download failed after {MAX_ATTEMPTS} attempts. Trying the robust site.")
        robust.main(ROOT_DIR, LIBRARY, SONG_LINK)
        print("Download successful from the robust site.")
        return True
    except:
        return False


if __name__ == "__main__":
    SONG_LINK = ""
    main(SONG_LINK)
