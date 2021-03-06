# CheckMate2.0

### Overview
This project is a cross discipline capstone at BYU within the School of Technology. It is a self contained chess playing robot built with a custom board and enclosure. It is intended to be used as a recruiting tool for the school of Technology. 

#### File Structure
* run.py - Start of the main program. 
* killSwitch.py - Background script used to shutdown PI when finished with the display.
* *.py - The supporting classes used to run the chess game.
* config.ini - Robot settings and offsets to the board 
* config - Doxygen config file to generate documentation
* GameScripts/ - PGN files that will be used to play each chess game
* html/ - Documentation generated by doxygen 
* extra/ - Additional features that need further development
* tests/ - Tests written for classes. (most will need to be moved in main folder to run)
* notes/ - Additional notes

### Adding Games
To add additional games add PGN files to the GameScripts folder

### Autostart
Python has as trouble running scripts on boot so a few hacks need to be made in order for it to work
* Set up a cronjob by running `crontab -e` and adding the line `@reboot python3 /path/to/run.py`
* In run.py change line 5 set Autostart to True
* In run.py change line 6 set ProjectPath to the path of run.py in the project
* In config.ini set autostart to True

### Debugging
In order to debug the run the program without the robots make the following changes
* In run.py change the global testMode variable to True
* In board.py change comment out the line `from gpio import GPIOBOARD`

### Hardware
The following hardware components were used to build this project
* Raspberry Pi
* Two UArm Swift Pro Robots
* Reed switches
* Custom chess pieces
* Custom enclosure

### Documentation 
To regenerate the source code documentation run `doxygen config`

### Running Test
Many of the classes have test built into them and by running the classes on their own will run the test.
Several other miscellaneous tests can be found in the test folder.