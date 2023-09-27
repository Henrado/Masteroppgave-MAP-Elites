using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.SideChannels;
using UnityEngine.SceneManagement;

using System.Text;
using System;

public class RobotManager : MonoBehaviour
{
    RobotParameterChannel parameterChannel;
    Bein[] robots;
    public void Awake()
    {
        // We create the Side Channel
        parameterChannel = new RobotParameterChannel();

        // When a Debug.Log message is created, we send it to the stringChannel
        // The channel must be registered with the SideChannelManager class
        SideChannelManager.RegisterSideChannel(parameterChannel);
        Debug.Log("Våknet");
    }
    void Start() 
    {
        this.robots = FindObjectsOfType<Bein>();

        foreach (Bein i in this.robots) {
            i.SetParameters(4f);
        }
    }

    public void OnDestroy()
    {
        if (Academy.IsInitialized){
            SideChannelManager.UnregisterSideChannel(parameterChannel);
        }
    }

    public void Update()
    {
        // Optional : If the space bar is pressed, raise an error !
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.LogError("This is a fake error. Space bar was pressed in Unity.");
        }
    }
}
