using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.SideChannels;
using System.Text;
using System;

public class RobotParameterChannel : SideChannel
{
    // Start is called before the first frame update
    public float[][,] allParameters;

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
                Debug.Log(msg.ReadString());
                break;
            case "config":
                int countLegs = msg.ReadInt32(); // read_float23()
                int countJoints = msg.ReadInt32();
                int countParams = msg.ReadInt32();
                allParameters = new float[countLegs][,];
                for (int i = 0; i < countLegs; i++)
                {
                    allParameters[i] = new float[countJoints, countParams];
                }
                for (int leg_i = 0; leg_i < countLegs; leg_i++)
                {
                    for (int joint = 0; joint < countJoints; joint++)
                    {
                        for (int param = 0; param < countParams; param++)
                        {
                            allParameters[leg_i][joint, param] = msg.ReadFloat32();
                        }
                    }
                }
                break;
            default:
                Debug.Log("Vet ikke hva dette er " + type.ToString());
                break;
        }
    }
}
