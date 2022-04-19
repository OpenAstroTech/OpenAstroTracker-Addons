# AutoPA:
- Ensure OAT is connected via ASCOM/INDI prior to starting AutoPA. 
  - For ASCOM this can be done using OATcontrol, NINA, Sharpcap, ASCOM Hub, etc.
  - For INDI, this is done using Ekos.
- This program currently does not take into account any limitations on the range of movement. If it thinks you need to move 15 deg to align, it will attempt to and will cause the alt/az systems to collide. 

### To run on Windows:
1. Download `AutoPA_v2.x.x.zip` and extract.
1. Run `autopa_v2.x.x.exe`
1. Enter required settings if necessary. Do not start AutoPA yet.
1. Open your polar alignment software (Sharpcap, NINA, etc) and start the polar alignment routine.
1. Once a solution is shown for adjusting azimuth/altitude, start AutoPA and the mount will start adjusting automatically until aligned within the target accuracy.

### To run on Linux (Astroberry, Stellarmate, etc.):
## NOTE: This is untested and likely does not work yet.
1. Install prerequisites:
   - `sudo apt-get install python3-dev swig libindi-dev g++ libnova-dev libcfitsio-dev zlib1g-dev`
   - `pip3 install pyindi-client`
1. Download `autopa_v2.x.x.py` and `indi.py` from `source` to the same folder.
1. Run `python3 ./autopa_v2.x.x.py`
1. Enter required settings if necessary. Do not start AutoPA yet.
1. Open your polar alignment software (Ekos) and start the polar alignment routine.
1. Once a solution is shown for adjusting azimuth/altitude, start AutoPA and the mount will start adjusting automatically until aligned within the target accuracy.

### To build (On Windows):
1. Download source files
1. `pip install -r requirements.txt`
1. Change to source directory
1. `python setup.py build`

