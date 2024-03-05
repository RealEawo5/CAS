from packaging import version
import multiprocessing
import subprocess
import requests
import argparse
import shutil
import psutil
import time
import sys
import os


CURRENT_VERSION = 'v2.1.0'


def downloadUpdate(downloadURL):
    response = requests.get(downloadURL, stream=True)

    with open('new-cas.exe', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


    createNewUpdater()

    subprocess.Popen(['updater-cas.exe', '--updater-install'])

    sys.exit()


def installUpdate():
    # Wait for cas.exe to exit
    while 'cas.exe' in (p.name() for p in psutil.process_iter()):
        time.sleep(1)

    print('Installing update...')

    # Rename the current .exe
    os.rename('cas.exe', 'old-cas.exe')
    
    # Replace the current .exe with the new one
    os.rename('new-cas.exe', 'cas.exe')

    # Restart the application
    subprocess.Popen(['cas.exe', '--updater-cleanup'])
    sys.exit()


def cleanUpInstall():
    # Wait for updater.exe to exit
    while 'updater-cas.exe' in (p.name() for p in psutil.process_iter()):
        time.sleep(1)

    print('Cleaning up...')

    # Delete the updater
    os.remove('updater-cas.exe')

    # Delete the old .exe
    os.remove('old-cas.exe')

    

def createNewUpdater():
    shutil.copyfile('new-cas.exe', 'updater-cas.exe')


def checkForUpdates():
    response = requests.get('https://api.github.com/repos/realeawo5/CAS/releases/latest')
    LATEST_VERSION = response.json()['tag_name']

    if isNewUpdate(LATEST_VERSION, CURRENT_VERSION):
        print('Update available. Updating now...')

        downloadURL = response.json()['assets'][0]['browser_download_url']
        downloadUpdate(downloadURL)
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
