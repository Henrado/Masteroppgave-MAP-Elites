#!/usr/bin/env python

import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library
from XL330 import XL330
import numpy as np


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

# TODO DISSE MÅ SJEKKES
BASE_MIN_DEGRE = -45
BASE_MAX_DEGRE = 45
UPPERLEG_MIN_DEGRE = -60
UPPERLEG_MAX_DEGRE = 0
LOWERLEG_MIN_DEGRE = 0
LOWERLEG_MAX_DEGRE = 45


for i in DXL_ALL_ID:
    servo = XL330(i)
    DXL_ALL_LIST.append(servo)
    DXL_ALL_DICT[i] = servo

def setMinMaxValue(Dict:dict, IDs:list, min:int, max:int):
    for i in IDs:
        Dict[i].setMinMaxPositionValue(min, max)

def getAllGoalPos(Dict:dict, IDs: list, input: list[float]) -> list[int]:
    allGolPos = []
    for i, ID in enumerate(IDs):
        allGolPos.append(Dict[ID].getGoalPos(input[i]))
    return allGolPos

def initializeGroupSync(packetHandler:PacketHandler, portHandler: PortHandler, ADDR:int, LEN_ADDER: int) -> tuple:
    
    return group_sync_read, group_sync_write

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
        print("%d:%s" % (ID,packetHandler.getTxRxResult(dxl_comm_result)))
    elif dxl_error != 0:
        print("%d:%s" % (ID,packetHandler.getRxPacketError(dxl_error)))
    else:
        print("Dynamixel ID:%d has been successfully connected" % ID)


def setTorqueMode(packetHandler:PacketHandler, portHandler: PortHandler, IDs:list[int], command: int):
    for i in IDs:
        _sendPacketTxRx(packetHandler, portHandler, i, ADDR_TORQUE_ENABLE, command, 1)

        
def setMaxMinPosLimitDegre(packetHandler:PacketHandler, portHandler: PortHandler, IDs:list, minLimitDegre: float, maxLimitDegre: float):
    for i in IDs:
        vServo = DXL_ALL_DICT[i]
        vServo.setMinMaxPositionDegre(minLimitDegre, maxLimitDegre)
        minLimit, maxLimit = vServo.getMinMaxPosValue() 
        _sendPacketTxRx(packetHandler, portHandler, i, ADDR_MAXIMUM_POSITION_VALUE, maxLimit, 4)
        _sendPacketTxRx(packetHandler, portHandler, i, ADDR_MINIMUM_POSITION_VALUE, minLimit, 4)

def setupGroupRead(groupSyncRead : GroupSyncRead, IDs:list) -> bool:
    for i in IDs:
        # Add parameter storage for Dynamixel#1 present position value
        dxl_addparam_result = groupSyncRead.addParam(i)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead addparam failed" % i)
            quit()

def sendGroupWrite(packetHandler:PacketHandler, groupSyncWrite:GroupSyncWrite, IDs: list[int], dxl_goal_position: list[int]):
    if len(IDs) != len(dxl_goal_position):
        raise Exception("ID-listen og Goal-listen er ikke like lange! ID:", len(IDs), "Goal:", len(dxl_goal_position))
    # Allocate goal position value into byte array
    for index, id in enumerate(IDs):
        param_goal_position = [DXL_LOBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position[index]))]

        # Add Dynamixel#1 goal position value to the Syncwrite parameter storage
        dxl_addparam_result = groupSyncWrite.addParam(id, param_goal_position)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % id)
            quit()

    # Syncwrite goal position
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # Clear syncwrite parameter storage
    groupSyncWrite.clearParam()

def readGroupUntilDone(packetHandler:PacketHandler, groupSyncRead: GroupSyncRead, ADDR_POS: int, Len_ADDR: int, IDs: list):
    while 1:
        # Syncread present position
        dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupsyncread data of Dynamixel#i is available
        for i in IDs:
            dxl_getdata_result = groupSyncRead.isAvailable(i, ADDR_POS, Len_ADDR)
            if dxl_getdata_result != True:
                print("[ID:%03d] groupSyncRead getdata failed" % i)
                quit()

        # Get Dynamixel#i present position value
        for i in IDs:
            dxl1_present_position = groupSyncRead.getData(i, ADDR_POS, Len_ADDR)
            print("[ID:%03d]  PresPos:%03d\t" % (i, dxl1_present_position))

        #if not ((abs(dxl_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD) and (abs(dxl_goal_position[index] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD)):
        #    break

        

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
    # Initialize GroupSyncWrite instance
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
    # Initialize GroupSyncRead instace for Present Position
    groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    setMaxMinPosLimitDegre(packetHandler, portHandler, DXL_BASE_ID, BASE_MIN_DEGRE, BASE_MAX_DEGRE)
    setMaxMinPosLimitDegre(packetHandler, portHandler, DXL_UPPERLEG_ID, UPPERLEG_MIN_DEGRE, UPPERLEG_MAX_DEGRE)
    setMaxMinPosLimitDegre(packetHandler, portHandler, DXL_LOWERLEG_ID, LOWERLEG_MIN_DEGRE, LOWERLEG_MAX_DEGRE)
    setTorqueMode(packetHandler, portHandler, DXL_ALL_ID, TORQUE_ENABLE)
    for i in range(3):
        l = [0,-1,-1,0,1,1,0,-1,-1,0,1,1]
        l = getAllGoalPos(DXL_ALL_DICT, DXL_ALL_ID, l)
        print("Går til", l)
        sendGroupWrite(packetHandler, groupSyncWrite, DXL_ALL_ID, l)
        time.sleep(2)
        l = [0,1,1,0,-1,-1,0,1,1,0,-1,-1]
        l = getAllGoalPos(DXL_ALL_DICT, DXL_ALL_ID, l)
        sendGroupWrite(packetHandler, groupSyncWrite, DXL_ALL_ID, l)
        time.sleep(2)
    setTorqueMode(packetHandler, portHandler, DXL_ALL_ID, TORQUE_DISABLE)
    quit()
