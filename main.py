import argparse
import sys

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--version', action='store_true', help='Program version')
args = parser.parse_args()

if args.version:
    print(updater.CURRENT_VERSION)

    sys.exit()


# Import modules
import updater
import cas
    

# Check for updates
updater.checkForUpdates()

# Run the program
while True:
    exitCode = cas.calculate()

    if not exitCode:
        break
    