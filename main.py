import os
import time
import fast
import robust

# SETUP
MAX_ATTEMPTS = 2
ROOT_DIR = os.getcwd()
LIBRARY = os.path.join(os.getcwd(), "library")
SONG_LINK = ""

# main code
def main():
    attempts = 0
    donwloaded = False

    while attempts < MAX_ATTEMPTS:
        print(f"Attempt {attempts + 1} of {MAX_ATTEMPTS} to download from fast site.")
        try:
            fast.main(ROOT_DIR, LIBRARY, SONG_LINK)
            print("Download successful from the fast site.")
            donwloaded = True
            break
        except Exception as e:
            print(f"Fast site download failed: {e}")
            
        attempts += 1
        time.sleep(1)

    if not donwloaded:
        print(f"Fast site download failed after {MAX_ATTEMPTS} attempts. Trying the robust site.")
        robust.main(ROOT_DIR, LIBRARY, SONG_LINK)
        print("Download successful from the robust site.")

if __name__ == "__main__":
    main()
