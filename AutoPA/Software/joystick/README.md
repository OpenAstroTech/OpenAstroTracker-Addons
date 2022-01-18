# AutoPA Joystick (Linux Only):
- This script allows manual control of each axis using keyboard arrow keys. Hold down and release left/right/up/down to adjust azimuth/altitude.
- The OAT can be remotely and precisely polar aligned using AutoPA and Ekos' polar alignment module.

### To run on Linux (Astroberry, Stellarmate, etc.):
1. Install prerequisites:
   - `sudo apt-get install python3-dev swig libindi-dev g++ libnova-dev libcfitsio-dev zlib1g-dev`
   - `pip3 install pyindi-client`
1. Download `joystick_INDI.py` and `indi.py` to the same folder.
1. Run `python3 ./joystick_INDI.py`