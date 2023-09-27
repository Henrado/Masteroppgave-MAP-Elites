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
class StringLogChannel(SideChannel):

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
try:
    # Create the channel
    string_log = StringLogChannel()

    # We start the communication with the Unity Editor and pass the string_log side channel as input
    print("Laget String")
    env = UnityEnvironment(side_channels=[string_log])
    print("opprettet env")
    string_log.send_string("The environment was reset")
    time.sleep(0.1)
    string_log.send_string("Test 2")
    print("String was sendt")
    time.sleep(0.1)

    #group_name = list(env.behavior_specs.keys())[0]  # Get the first group_name
    #group_spec = env.behavior_specs[group_name]
    for i in range(1000):
        #decision_steps, terminal_steps = env.get_steps(group_name)
        # We send data to Unity : A string with the number of Agent at each
        string_log.send_string(
            f"Step {i} occurred with {i} deciding agents and "
            f"{i} terminal agents"
        )
        env.step()  # Move the simulation forward
finally:
    env.close()