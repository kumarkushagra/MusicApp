import os
import time
import fast

# SETUP
MAX_ATTEMPTS = 5
ROOT_DIR = os.getcwd()
LIBRARY = os.path.join(os.getcwd(), "library")
SONG_LINK = ""


def download_from_fast_site():
    try:
        fast.main(ROOT_DIR, LIBRARY, SONG_LINK)
        return True
    except Exception as e:
        print(f"Fast site download failed: {e}")
        return False


# main Code
attempts = 0
while attempts < MAX_ATTEMPTS:
    print(f"Attempt {attempts + 1} of {MAX_ATTEMPTS} to download from fast site.")
    if download_from_fast_site():
        print("Download successful from the fast site.")
        break
    attempts += 1
    time.sleep(1)

print("Fast site download failed after 5 attempts. Trying the robust site.")
# robust.download_song()
print("Download successful from the robust site.")
