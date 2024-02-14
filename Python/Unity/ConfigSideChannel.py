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
class ConfigSideChannel(SideChannel):

    def __init__(self) -> None:
        super().__init__(uuid.UUID("621f0a70-4f87-11ea-a6bf-784f4387d1f8"))

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Note: We must implement this method of the SideChannel interface to
        receive messages from Unity
        """
        pass

    def send_config(self, data: dict) -> None:
        for key, value in data.items():
            # Add the string to an OutgoingMessage
            msg = OutgoingMessage()
            msg.write_string(key)
            if type(value) == list: 
                msg.write_float32_list(value)
            elif type(value) == float:
                msg.write_float32(value)
            elif type(value) == int:
                msg.write_int32(value)
            # We call this method to queue the data we want to send
            super().queue_message_to_send(msg)