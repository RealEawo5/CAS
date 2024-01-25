# Import updater
import updater

import argparse
import sys

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--version', action='store_true', help='Program version')
parser.add_argument('--updater-install', action='store_true', help='Install new updates running as the program updater')
parser.add_argument('--updater-cleanup', action='store_true', help='Clean up after installing updates')
args = parser.parse_args()

if args.version:
    print(updater.CURRENT_VERSION)
    sys.exit()

if args.updater_install:
    updater.installUpdate()

if args.updater_cleanup:
    updater.cleanUpInstall()


# Check for updates
updater.checkForUpdates()


# Import modules
import cas


# Run the program
while True:
    exitCode = cas.calculate()

    if not exitCode:
        break
    