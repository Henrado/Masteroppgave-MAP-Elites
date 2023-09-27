using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.SideChannels;
using System.Text;
using System;

public class RobotParameterChannel : SideChannel
{
    // Start is called before the first frame update
    public int parameter_length;
    public RobotParameterChannel()
    {
        ChannelId = new Guid("621f0a70-4f87-11ea-a6bf-784f4387d1f8");
    }

    protected override void OnMessageReceived(IncomingMessage msg)
    {
        //var receivedString = msg.ReadString();
        // Debug.Log("From Python : " + receivedString);

        string type = msg.ReadString();
        switch (type)
        {
            case "String":
                //Debug.Log(msg.ReadString());
                break;
            case "config":
                parameter_length = msg.ReadInt32(); // read_float23()
                float[] parameters = new float[parameter_length];
                for (int i = 0; i < parameter_length; i++)
                    parameters[i] = msg.ReadFloat32();
                Debug.Log(parameters);
                break;
            default:
                Debug.Log("Vet ikke hva dette er " + type.ToString());
                break;
        }
    }
}
