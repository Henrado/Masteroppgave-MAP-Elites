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
    public float groundContactPenaltyPart = 0.0f;
    public int CubeCount = 0;
    public float CubeSize = 1f;
    public ConfigSideChannel()
    {
        ChannelId = new Guid("621f0a70-4f87-11ea-a6bf-784f4387d1f8");
    }

    private object ReadType(IncomingMessage msg, string type){
        switch (type)
        {
            case "int":
                return msg.ReadInt32();
            case "float":
                return msg.ReadFloat32();
            case "list":
                return msg.ReadFloatList();
            default:
                return null;
        }
    }

    protected override void OnMessageReceived(IncomingMessage msg)
    {
        string type = msg.ReadString();
        string castType = msg.ReadString();
        switch (type)
        {
            case "jointDriveSettings":
                jointDriveSettings = (IList<float>)ReadType(msg, castType);
                break;
            case "legAngularLimits":
                legAngularLimits = (IList<float>)ReadType(msg, castType); 
                break;
            case "robotMassPart":
                robotMassPart = (IList<float>)ReadType(msg, castType); 
                break;
            case "groundContactPenaltyPart":
                groundContactPenaltyPart = float.Parse(ReadType(msg, castType).ToString()); // float 
                break;
            case "CubeCount":
                CubeCount = (int)ReadType(msg, castType); // int
                break;
            case "CubeSize":
                CubeSize = float.Parse(ReadType(msg, castType).ToString()); // float
                break;
            default:
                Debug.Log("Vet ikke hva dette er " + type.ToString());
                break;
        }
    }
}
