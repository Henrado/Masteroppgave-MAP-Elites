using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.SideChannels;
using System.Text;
using System;
using System.Collections.Generic;

public class ConfigSideChannel : SideChannel
{
    public IList<float> jointDriveSettings;
    public IList<float> legAngularLimits;
    public IList<float> robotMassPart;
    public float groundContactPenaltyPart = 0;
    public ConfigSideChannel()
    {
        ChannelId = new Guid("621f0a70-4f87-11ea-a6bf-784f4387d1f8");
    }

    protected override void OnMessageReceived(IncomingMessage msg)
    {
        string type = msg.ReadString();
        switch (type)
        {
            case "jointDriveSettings":
                jointDriveSettings = msg.ReadFloatList(); // read_float23()
                break;
            case "legAngularLimits":
                legAngularLimits = msg.ReadFloatList(); // read_float23()
                break;
            case "robotMassPart":
                robotMassPart = msg.ReadFloatList(); // read_float23()
                break;
            case "groundContactPenaltyPart":
                groundContactPenaltyPart = msg.ReadFloat32(); // read_float23()
                break;
            default:
                Debug.Log("Vet ikke hva dette er " + type.ToString());
                break;
        }
    }
}
