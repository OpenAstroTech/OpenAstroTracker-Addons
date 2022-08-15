#!/usr/bin/env python3
import curses
import time
import sys
import indi, serial
import re

def clearline(screen, line):
    screen.move(line, 0)
    screen.clrtoeol();

def keypress(screen, altaz, value):
    if value > 0:
        line = f"{altaz} raising by {value}"
    elif value < 0:
        line = f"{altaz} lowering by {value}"
    elif value == 0:
        line = ""
    clearline(screen, 3)
    screen.addstr(3, 0, line)
    return True

def sendCommand(command, telescope="LX200 GPS"):
    #Connect to indi server
    indiclient, blobEvent = indi.indiserverConnect()

    #Disconnect OAT from indi to free up serial port
    indi.disconnectScope(indiclient, telescope)

    #Send command     
    ser = serial.Serial(serialport, baudrate, timeout = 0.2)
    ser.flush()
    ser.write(str.encode(command))
    result = ser.readline()
    result = result[:-1].decode('utf-8')
    
    #Reconnect OAT to indi and disconnect from server
    indi.connectScope(indiclient, telescope)
    indi.indiserverDisconnect(indiclient)
    return result
            
def altaz(axis, errorvalue, serialport):
	if not re.match(r"^[-+]?([0-9]*\.[0-9]+|[0-9]+)$", str(errorvalue)):
		print("Error value not valid")
		return
		
	errorvalue = float(errorvalue)
	if axis.lower() == "alt":
		commandToSend = f":MAL{errorvalue}#"
	elif axis.lower() == "az":
		commandToSend = f":MAZ{errorvalue}#"
	else:
		print("Axis input not correct")
		return

	result = sendCommand(commandToSend)
	return

if len(sys.argv) >= 2:
    serialport = sys.argv[1]
else:
    serialport = "/dev/ttyACM0"

#screen = curses.filter()
# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)
screen.nodelay(1)
screen.addstr(0, 0, 'Up/Down arrow keys to raise/lower altitude.')
screen.addstr(1, 0, 'Right/Left arrow keys to increase/decrease azimuth.')
screen.addstr(2, 0, 'Press \'q\' to exit.')

keypress_timeout = time.time()
status_timeout = time.time()
keypress_shown = False
status_shown = False

azimuth = 0
altitude = 0
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_RIGHT:
            keypress_timeout = time.time()
            altitude = 0
            azimuth += 1
            keypress_shown = keypress(screen, "Azimuth", azimuth)
        elif char == curses.KEY_LEFT:
            keypress_timeout = time.time()
            altitude = 0
            azimuth -= 1
            keypress_shown = keypress(screen, "Azimuth", azimuth)        
        elif char == curses.KEY_UP:
            keypress_timeout = time.time()
            azimuth = 0
            altitude += 1
            keypress_shown = keypress(screen, "Altitude", altitude) 
        elif char == curses.KEY_DOWN:
            keypress_timeout = time.time()
            azimuth = 0
            altitude -= 1
            keypress_shown = keypress(screen, "Altitude", altitude)
        if time.time() - keypress_timeout > 1 and keypress_shown:
            keypress_shown = False
            if altitude != 0:
                statusline = f"Adjusting altitude by {altitude} arcminutes"
                screen.addstr(4, 0, statusline)
                status_shown = True
                altaz("alt", altitude, serialport)
            if azimuth != 0:
                statusline = f"Adjusting azimuth by {azimuth} arcminutes"
                screen.addstr(4, 0, statusline)
                status_shown = True
                altaz("az", azimuth, serialport)
            azimuth = 0
            altitude = 0
            status_timeout = time.time()
            clearline(screen, 3)
        if time.time() - status_timeout > 3 and status_shown:
            status_shown = False
            clearline(screen, 4)
finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
