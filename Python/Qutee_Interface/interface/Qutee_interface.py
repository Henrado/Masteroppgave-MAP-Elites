#!/usr/bin/env python

import os
from Qutee_Interface.interface.dynamixel_sdk  import *                    # Uses Dynamixel SDK library
from Qutee_Interface.interface.XL330 import XL330
import numpy as np


# For å finne ut om  det er windows eller Linux
if os.name == 'nt':
    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    DEVICENAME          = 'COM3'
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    def getch():
        return None
    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    """DEVICENAME          = '/dev/ttyUSB0'
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
        """
    

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

BASE_MIN_DEGRE = -45
BASE_MAX_DEGRE = 45
UPPERLEG_MIN_DEGRE = -60
UPPERLEG_MAX_DEGRE = 60
LOWERLEG_MIN_DEGRE = 0
LOWERLEG_MAX_DEGRE = 100


for i in DXL_ALL_ID:
    servo = XL330(i)
    DXL_ALL_LIST.append(servo)
    DXL_ALL_DICT[i] = servo



class Qutee_interface:
    def __init__(self):
        self.setUpPort()
        self.firstTimeSetUp()
        self.setReversed(DXL_ALL_DICT, DXL_UPPERLEG_ID, True)
        # Initialize GroupSyncWrite instance
        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        # Initialize GroupSyncRead instace for Present Position
        self.groupSyncRead = GroupSyncRead(self.portHandler, self.packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        

    def setUpPort(self):
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        print(DEVICENAME)
        self.portHandler = PortHandler(DEVICENAME)

        # Initialize PacketHandler instance
        # Set the protocol version
        # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        #self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        self.packetHandler = Protocol2PacketHandler()

            # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()

        # Set port baudrate
        if self.portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

    def firstTimeSetUp(self):
        self.setMaxMinPosLimitDegre(self.packetHandler, self.portHandler, DXL_BASE_ID, BASE_MIN_DEGRE, BASE_MAX_DEGRE)
        self.setMaxMinPosLimitDegre(self.packetHandler, self.portHandler, DXL_UPPERLEG_ID, UPPERLEG_MIN_DEGRE, UPPERLEG_MAX_DEGRE)
        self.setMaxMinPosLimitDegre(self.packetHandler, self.portHandler, DXL_LOWERLEG_ID, LOWERLEG_MIN_DEGRE, LOWERLEG_MAX_DEGRE)

    def EnableTorqueALL(self):
        self.setTorqueMode(self.packetHandler, self.portHandler, DXL_ALL_ID, TORQUE_ENABLE)
        
        
    def DisableTorqueALL(self):
        self.setTorqueMode(self.packetHandler, self.portHandler, DXL_ALL_ID, TORQUE_DISABLE)


    def setAction(self, action:list[float]):
        l = self.getAllGoalPos(DXL_ALL_DICT, DXL_ALL_ID, action)
        #print("Går til", l)
        self.sendGroupWrite(self.packetHandler, self.groupSyncWrite, DXL_ALL_ID, l)


    def setMaxMinValue(self,Dict:dict[int,XL330], IDs:list[int], max:int, min:int) -> None:
        """Tar inn ordbok med alle servoene og liste med hvilke servoer som skal 
        settes med maximum og minimum pwm"""
        for i in IDs:
            Dict[i].setMinMaxPositionValue(min, max)

    def setReversed(self,Dict:dict[int,XL330], IDs:list[int], reversed:bool) -> None:
        """Tar inn ordbok med alle servoene og liste med hvilke servoer som skal 
        reversere input"""
        for i in IDs:
            Dict[i].setReverseInputDirection(reversed)

    def getAllGoalPos(self, Dict:dict[int, XL330], IDs: list[int], input: list[float]) -> list[int]:
        """
        Går gjennom valgt ordbok og henter ut servoens pwm basert på input mellom -1, 1
        input: list[float] er liste med input fra -1 til 1
        return: list[int] med pwm sinaler 0-4090
        """
        allGolPos = []
        for i, ID in enumerate(IDs):
            allGolPos.append(Dict[ID].getGoalPos(input[i]))
        return allGolPos


    def _sendPacketTxRx(self,packetHandler:Protocol2PacketHandler, portHandler: PortHandler, ID:int, ADDr: int, command: int, com_len: int) -> None:
        """
        Send en enslig pakke til en valgt servo med ID
        ID[int]: ID til servoen som skal modta commandoen 
        ADDr[int]: Adressen til kommandoen 
        command[int]: Kommandoen som skal sendes
        com_len[int]: Lengden på kommandoen som skal sendes 
        """
        if com_len == 1:
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDr, command)
        elif com_len == 2:
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, ID, ADDr, command)
        elif com_len == 4:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID, ADDr, command)
        else:
            print("Wrong data lenght")
            quit()
        if dxl_comm_result != COMM_SUCCESS:
            print("%d:%s" % (ID,packetHandler.getTxRxResult(dxl_comm_result)))
        elif dxl_error != 0:
            print("%d:%s" % (ID,packetHandler.getRxPacketError(dxl_error)))


    def setTorqueMode(self,packetHandler:Protocol2PacketHandler, portHandler: PortHandler, IDs:list[int], command: int) -> None:
        """
        Skal sette torque moden til en liste med servoer
        IDs:list[int]: Liste med IDer som skal settes mode 
        command: int: Moden som skal settes: 1=Enable, 0=Disable
        """
        for i in IDs:
            self._sendPacketTxRx(packetHandler, portHandler, i, ADDR_TORQUE_ENABLE, command, 1)

        
    def setMaxMinPosLimitDegre(self,packetHandler:Protocol2PacketHandler, portHandler: PortHandler, IDs:list[int], minLimitDegre: float, maxLimitDegre: float):
        """
        Skal sette min og max vinkel til servoer i IDs
        IDs: Liste med valgte servoer
        minLimitDegre:[float] Minimum vinkel den skal kunne gå
        maxLimitDegre:[float] Maximum vinkel den skal kunne gå
        """
        for i in IDs:
            vServo = DXL_ALL_DICT[i]
            vServo.setMinMaxPositionDegre(minLimitDegre, maxLimitDegre)
            minLimit, maxLimit = vServo.getMinMaxPosValue() 
            self._sendPacketTxRx(packetHandler, portHandler, i, ADDR_MAXIMUM_POSITION_VALUE, maxLimit, 4)
            self._sendPacketTxRx(packetHandler, portHandler, i, ADDR_MINIMUM_POSITION_VALUE, minLimit, 4)


    def setupGroupRead(self,groupSyncRead : GroupSyncRead, IDs:list[int]):
        """
        Setter opp hvilke servoer man skal hente data fra
        """
        for i in IDs:
            # Add parameter storage for Dynamixel#1 present position value
            dxl_addparam_result = groupSyncRead.addParam(i)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncRead addparam failed" % i)
                quit()


    def sendGroupWrite(self,packetHandler:Protocol2PacketHandler, groupSyncWrite:GroupSyncWrite, IDs: list[int], dxl_goal_position: list[int]):
        """
        Skal sende en bolk med samme type data (goal_position) til servoene i listen IDs
        IDs list[int]: Liste med servoer 
        dxl_goal_position list[int]: Liste med pwm signaler som skal sendes til servoene 
        """
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


    def readGroupUntilDone(self,packetHandler:Protocol2PacketHandler, groupSyncRead: GroupSyncRead, ADDR_POS: int, Len_ADDR: int, IDs: list):
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

    def quit(self):
        quit()
        

if __name__ == "__main__":
    Q = Qutee_interface()
    Q.EnableTorqueALL()
    for i in range(3):
        l = [0,-1,-1,0,1,1,0,-1,-1,0,1,1]
        Q.setAction(l)
        time.sleep(2)
        l = [0,1,1,0,-1,-1,0,1,1,0,-1,-1]
        Q.setAction(l)
        time.sleep(2)
    Q.DisableTorqueALL()
    Q.quit()
