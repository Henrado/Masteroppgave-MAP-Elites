using System.Collections;
using System.Collections.Generic;
using Unity.MLAgents;
using UnityEngine;
using Unity.MLAgents.SideChannels;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;
using UnityEngine.SceneManagement;




public class Agent_Master : Agent
{
    private ConfigSideChannel parameterChannel;

    private GameObject robot;

    private Robot robot_script;
    public void Awake()
    {
        // We create the Side Channel
        parameterChannel = new ConfigSideChannel();

        // The channel must be registered with the SideChannelManager class
        SideChannelManager.RegisterSideChannel(parameterChannel);
    }

    public override void Initialize()
    {

    }


    public override void OnEpisodeBegin()
    {
        SceneManager.UnloadSceneAsync("SampleScene");
        
        SceneManager.LoadScene("SampleScene", LoadSceneMode.Additive);
        GameObject[] respawns = GameObject.FindGameObjectsWithTag("Qutee");
        robot = respawns[0];
        Debug.Log("Ny scene");
        robot_script = robot.GetComponent<Robot>();
        //robot_script.Initialize_NY();
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        robot_script.OnActionReceived(actions);
    }

    public override void CollectObservations(VectorSensor sensor){
        // Observe the agent's local rotation (3 observations)
        // sensor.AddObservation(Center.localRotation.eulerAngles);

        // Observe the agent local position (3 observations)
        //sensor.AddObservation(Center.localPosition);

        // Observe the agent local rotation in eulerangels (3 observations)
        //sensor.AddObservation(Center.localRotation.eulerAngles);
        // Get a vector from the startposition to the currentposition
        // Vector3 distanceWalked = Center.localPosition - startPosition;
        // Observe a vector pointing from start position to where it is (3 observations)
        // sensor.AddObservation(distanceWalked);

        // Observe a dot product that indicates whether the beak tip is in front of the flower (1 observation)
        // (+1 means that the beak tip is directly in front of the flower, -1 means directly behind)
        //sensor.AddObservation(Vector3.Dot(toFlower.normalized, -nearestFlower.FlowerUpVector.normalized));

        // Observe a dot product that indicates whether the beak is pointing toward the flower (1 observation)
        // (+1 means that the beak is pointing directly at the flower, -1 means directly away)
        //sensor.AddObservation(Vector3.Dot(beakTip.forward.normalized, -nearestFlower.FlowerUpVector.normalized));

        // Observe the relative distance from the beak tip to the flower (1 observation)
        sensor.AddObservation(0);
        sensor.AddObservation(0);
        sensor.AddObservation(0);
        sensor.AddObservation(0);
        sensor.AddObservation(0);
        sensor.AddObservation(0);
        sensor.AddObservation(0);

        // 7 total observations
    }
    public void OnDestroy()
    {
        if (Academy.IsInitialized){
            SideChannelManager.UnregisterSideChannel(parameterChannel);
        }
    }
}
