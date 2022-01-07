AutoPA:
-Ensure OAT is connected via ASCOM prior to starting AutoPA. This can be done using OATcontrol, NINA, Sharpcap, ASCOM Hub, etc.
-This program currently does not take into account any limitations on the range of movement. If it thinks you need to move 15 deg to align, it will attempt to and will cause the alt/az systems to collide. 

To run:
-Run autopa_v2.x.x.exe and enter required settings if necessary. Do not start AutoPA yet.
-Open your polar alignment software (Sharpcap, NINA, etc) and start the polar alignment routine.
-Once a solution is shown for adjusting azimuth/altitude, start AutoPA and the mount will start adjusting automatically until aligned within the target accuracy.

To build:
-Download source files
-pip install -r requirements.txt
-Change to source directory
-python setup.py build
