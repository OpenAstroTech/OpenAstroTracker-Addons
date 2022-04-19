#!/usr/bin/env python3

import PyIndi
import time
import threading
    
class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
    def newDevice(self, d):
        pass
    def newProperty(self, p):
        pass
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        global blobEvent
        blobEvent.set()
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        pass
    def serverDisconnected(self, code):
        pass

def disconnectScope(indiclient, telescope):
    device_telescope=indiclient.getDevice(telescope)
    while not(device_telescope):
        time.sleep(0.5)
        device_telescope=indiclient.getDevice(telescope)
    
    # wait CONNECTION property be defined for telescope
    telescope_connect=device_telescope.getSwitch("CONNECTION")
    while not(telescope_connect):
        time.sleep(0.5)
        telescope_connect=device_telescope.getSwitch("CONNECTION")
     
    # if the telescope device is not connected, we do connect it
    while device_telescope.isConnected():
        # Property vectors are mapped to iterable Python objects
        # Hence we can access each element of the vector using Python indexing
        # each element of the "CONNECTION" vector is a ISwitch
        telescope_connect[1].s=PyIndi.ISS_ON  # the "CONNECT" switch
        telescope_connect[0].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
        indiclient.sendNewSwitch(telescope_connect) # send this new value to the device
    time.sleep(1)

def connectScope(indiclient, telescope):
    device_telescope=indiclient.getDevice(telescope)
    while not(device_telescope):
        time.sleep(0.5)
        device_telescope=indiclient.getDevice(telescope)
    
    # wait CONNECTION property be defined for telescope
    telescope_connect=device_telescope.getSwitch("CONNECTION")
    while not(telescope_connect):
        time.sleep(0.5)
        telescope_connect=device_telescope.getSwitch("CONNECTION")
     
    # if the telescope device is not connected, we do connect it
    if not(device_telescope.isConnected()):
        # Property vectors are mapped to iterable Python objects
        # Hence we can access each element of the vector using Python indexing
        # each element of the "CONNECTION" vector is a ISwitch
        telescope_connect[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
        telescope_connect[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
        indiclient.sendNewSwitch(telescope_connect) # send this new value to the device

def indiserverConnect(hostname="localhost", port="7624"):
    # connect the server
    indiclient=IndiClient()
    indiclient.setServer(hostname,int(port))
    global blobEvent
    blobEvent=threading.Event()

    if (not(indiclient.connectServer())):
         print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Run server in Ekos first.")
         return None
    return (indiclient, blobEvent)

def indiserverDisconnect(indiclient):
    indiclient.disconnectServer()