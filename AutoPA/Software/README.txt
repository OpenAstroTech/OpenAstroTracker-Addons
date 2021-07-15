Sharpcap AutoPA:
-Ensure OAT is connected via ASCOM prior to running script. This can be done using OATcontrol, NINA, Sharpcap, ASCOM Hub, etc.
-This program currently does not take into account any limitations on the range of movement. If it thinks you need to move 15 deg to align, it will attempt to and will cause the alt/az systems to collide. 

To Install:
-Download "requirements.txt" and "sharpcap_autopa_vX.X.py"
-"pip install -r requirements.txt"

To run:
-Open Sharpcap first
-Run "python ./sharpcap_autopa_vX.X.py" from PowerShell
-Start polar alignment routine in Sharpcap. Once a solution is calculated by Sharpcap, the mount should start adjusting on it's own until aligned within 1 arcmin.