from packaging import version
import requests
import os
import sys
import subprocess


CURRENT_VERSION = 'v1.1.1'


def checkUpdates():
    response = requests.get('https://api.github.com/repos/realeawo5/CAS/releases/latest')
    LATEST_VERSION = response.json()['tag_name']

    if isNewUpdate(LATEST_VERSION, CURRENT_VERSION):
        print('Update available. Updating now...')
        downloadUrl = response.json()['assets'][0]['browser_download_url']
        response = requests.get(downloadUrl, stream=True)
        with open('new-cas.exe', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # Replace the current .exe with the new one
        os.rename('new-cas.exe', 'cas.exe')

        # Restart the application
        subprocess.Popen(['cas.exe'])
        sys.exit()
    else:
        print('Latest version installed')


def isNewRelease(LATEST_VERSION, CURRENT_VERSION):
    LATEST_VERSION = version.parse(LATEST_VERSION)
    CURRENT_VERSION = version.parse(CURRENT_VERSION)

    if CURRENT_VERSION > LATEST_VERSION:
        return True
    else:
        return False
    
def isNewUpdate(LATEST_VERSION, CURRENT_VERSION):
    LATEST_VERSION = version.parse(LATEST_VERSION)
    CURRENT_VERSION = version.parse(CURRENT_VERSION)

    if LATEST_VERSION > CURRENT_VERSION:
        return True
    else:
        return False


if __name__ == '__main__':
    LATEST_VERSION = requests.get('https://api.github.com/repos/realeawo5/CAS/releases/latest').json()['tag_name']

    print(isNewRelease(LATEST_VERSION, CURRENT_VERSION), end=":")
    # print(LATEST_VERSION, end=":")
    print(CURRENT_VERSION)

    # checkUpdates()
