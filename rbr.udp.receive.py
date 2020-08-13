#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rbr.udp.receive.py
#  
#  Copyright 2020  <>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 6776

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    var, adress = sock.recvfrom(664) # buffer size is 664 bytes
    
    ControlThrottle = int(round(struct.unpack_from('<f', var , offset=28)[0] * 100))
    ControlBrake = int(round(struct.unpack_from('<f', var , offset=32)[0] * 100))
    ControlClutch = int(round(struct.unpack_from('<f', var , offset=40)[0] * 100))
    TotalSteps = struct.unpack_from('<l', var , offset=0)[0]
    StageRaceTime = struct.unpack_from('<f', var , offset=12)[0]
    RaceHr = int(StageRaceTime / 60 )
    RaceMin = (StageRaceTime / 60 - int(StageRaceTime / 60))*60
    ControlGear = struct.unpack_from('<l', var , offset=44)[0] - 1 # minus 1 because neutral is 1
    EngineCoolantTemperature = int(round(struct.unpack_from("<f", var , offset=144)[0] - 273.15)) # minus 273.15 to convert from kelvin
    RadiatorCoolantTemperature = int(round(struct.unpack_from("<f", var , offset=140)[0] - 273.15))
    LFBrakeDiskTemp = int(round(struct.unpack_from("<f", var , offset=188)[0] - 273.15))
    RFBrakeDiskTemp = int(round(struct.unpack_from("<f", var , offset=316)[0] - 273.15))
    LBBrakeDiskTemp = int(round(struct.unpack_from("<f", var , offset=444)[0] - 273.15))
    RBBrakeDiskTemp = int(round(struct.unpack_from("<f", var , offset=572)[0] - 273.15))
    EngineRpm = int(round(struct.unpack_from("<f", var , offset=136)[0]))

    
    print(chr(27) + "[2J") # clear screen using escape sequences
    print(chr(27) + "[H")  # return to home using escape sequences
    
    print("Total Steps: %s	Race Time: %s:%s" %(TotalSteps, RaceHr , RaceMin))
    print("Engine: %s RPM   Gear: %s   Throttle: %s   Brake: %s   Clutch: %s" %(EngineRpm , ControlGear, ControlThrottle , ControlBrake, ControlClutch))
    print("Coolant Temp: %s°C" % EngineCoolantTemperature)
    print("")
    print("Brake Disk Temp")
    print("LF: %s°C	RF: %s°C" % (LFBrakeDiskTemp , RFBrakeDiskTemp))
    print("LB: %s°C	RB: %s°C" % (LBBrakeDiskTemp , RBBrakeDiskTemp))
