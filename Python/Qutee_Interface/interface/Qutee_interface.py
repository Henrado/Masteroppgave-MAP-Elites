#!/usr/bin/env python

import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library
from XL330 import XL330

# For å finne ut om  det er windows eller Linux
if os.name == 'nt':
    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    DEVICENAME          = 'COM3'
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    DEVICENAME          = '/dev/ttyUSB0'
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    

#********* DYNAMIXEL Model definition *********
#***** (Use only one definition at a time) *****
MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
LEN_GOAL_POSITION           = 4         # Data Byte Length
ADDR_PRESENT_POSITION       = 132
LEN_PRESENT_POSITION        = 4         # Data Byte Length
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 57600
ADDR_MINIMUM_POSITION_VALUE = 52
ADDR_MAXIMUM_POSITION_VALUE = 48
TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Make sure that each DYNAMIXEL ID should have unique ID.
DXL01_ID                    = 1                 # Dynamixel#1 ID : 1
DXL02_ID                    = 2                 # Dynamixel#1 ID : 2
DXL03_ID                    = 3                 # Dynamixel#1 ID : 3
DXL04_ID                    = 4                 # Dynamixel#1 ID : 4
DXL05_ID                    = 5                 # Dynamixel#1 ID : 5
DXL06_ID                    = 6                 # Dynamixel#1 ID : 6
DXL07_ID                    = 7                 # Dynamixel#1 ID : 7
DXL08_ID                    = 8                 # Dynamixel#1 ID : 8
DXL09_ID                    = 9                 # Dynamixel#1 ID : 9
DXL10_ID                    = 10                # Dynamixel#1 ID : 10
DXL11_ID                    = 11                # Dynamixel#1 ID : 11
DXL12_ID                    = 12                # Dynamixel#1 ID : 12

DXL_ALL_ID =        [DXL01_ID, DXL02_ID, DXL03_ID, DXL04_ID, DXL05_ID, DXL06_ID, DXL07_ID, DXL08_ID, DXL09_ID, DXL10_ID, DXL11_ID, DXL12_ID]
DXL_BASE_ID =       [DXL01_ID, DXL04_ID, DXL07_ID, DXL10_ID]
DXL_UPPERLEG_ID =   [DXL02_ID, DXL05_ID, DXL08_ID, DXL11_ID]
DXL_LOWERLEG_ID =   [DXL03_ID, DXL06_ID, DXL09_ID, DXL12_ID]
DXL_ALL_LIST =      []
DXL_ALL_DICT =      {}

for i in DXL_ALL_ID:
    servo = XL330(i)
    DXL_ALL_LIST.append(servo)
    DXL_ALL_DICT[i] = servo

def setMinMaxValue(Dict:dict, IDs:list, min:int, max:int):
    for i in IDs:
        Dict[i].setMinMaxPositionValue(min, max)

def getAllGoalPos(Dict:dict, IDs: list, input: list):
    allGolPos = []
    for i, ID in enumerate(IDs):
        allGolPos.append(Dict[ID].getGoalPos(input[i]))
    return allGolPos

def _sendPacketTxRx(packetHandler:PacketHandler, portHandler: PortHandler, ID:int, ADDr: int, command: int, com_len: int):
    if com_len == 1:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDr, command)
    elif com_len == 2:
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, ID, ADDr, command)
    elif com_len == 4:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID, ADDr, command)
    else:
        print("No data lenght")
        quit()
    if dxl_comm_result != COMM_SUCCESS:
        print("%d:%s" % ID,packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%d:%s" % ID,packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel ID:%d has been successfully connected" % ID)

def setTorque(packetHandler:PacketHandler, portHandler: PortHandler, IDs:list, command: int):
    for i in IDs:
        _sendPacketTxRx(packetHandler, portHandler, i, ADDR_TORQUE_ENABLE, command, 1)

if __name__ == "__main__":
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    print(DEVICENAME)
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

        # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()


    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()
    setTorque(packetHandler, portHandler, [DXL02_ID, DXL03_ID], TORQUE_DISABLE)