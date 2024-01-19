import subprocess
import os

def checkUpdates():
    # Navigate to the directory where your program is located
    os.chdir('.')

    # Fetch the latest updates from the remote repository
    subprocess.call(['git', 'fetch'])

    # Check if there are any updates
    result = subprocess.check_output(['git', 'status', '-uno'])

    if 'Your branch is behind' in result.decode('utf-8'):
        print('Update available. Updating now...')
        # Pull the latest updates
        subprocess.call(['git', 'pull'])
    else:
        print('Your program is up to date.')
