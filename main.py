import updater
import cas


# Check for updates
updater.checkForUpdates()

# Run the program
while True:
    exitCode = cas.calculate()

    if not exitCode:
        break
    
