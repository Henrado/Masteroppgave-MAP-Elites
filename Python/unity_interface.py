from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.side_channel import (
    SideChannel,
    IncomingMessage,
    OutgoingMessage,
)
import numpy as np
import uuid
import time


# Create the StringLogChannel class
class RobotParameterChannel(SideChannel):

    def __init__(self) -> None:
        super().__init__(uuid.UUID("621f0a70-4f87-11ea-a6bf-784f4387d1f8"))

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Note: We must implement this method of the SideChannel interface to
        receive messages from Unity
        """
        # We simply read a string from the message and print it.
        print(msg.read_string())

    def send_string(self, data: str) -> None:
        # Add the string to an OutgoingMessage
        msg = OutgoingMessage()
        msg.write_string(data)
        # We call this method to queue the data we want to send
        super().queue_message_to_send(msg)

    def send_config(self, configParams) -> None:
        countLegs = len(configParams)
        countJoints = configParams[0].shape[0]
        countParams = configParams[0].shape[1]
        msg = OutgoingMessage()
        msg.write_string("config")
        msg.write_int32(countLegs)
        msg.write_int32(countJoints)
        msg.write_int32(countParams)
        for leg_i in range(countLegs):
            for joint in range(countJoints):
                for params in range(countParams):
                    msg.write_float32(configParams[leg_i][joint, params])
        super().queue_message_to_send(msg)