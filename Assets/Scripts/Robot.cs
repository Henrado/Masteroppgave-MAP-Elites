using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgentsExamples;
using Random = UnityEngine.Random;
using System;

[RequireComponent(typeof(JointDriveController))] // Required to set joint forces
public class Robot : Agent
{

    JointDriveController m_JdController;

    [Header("Body Parts")][Space(10)] 
    public Transform body;
    public Transform leg0;
    public Transform leg0Upper;
    public Transform leg0Lower;
    public Transform leg1;
    public Transform leg1Upper;
    public Transform leg1Lower;
    public Transform leg2;
    public Transform leg2Upper;
    public Transform leg2Lower;
    public Transform leg3;
    public Transform leg3Upper;
    public Transform leg3Lower;
    private Transform[] leg0List;
    private Transform[] leg1List;
    private Transform[] leg2List;
    private Transform[] leg3List;
    private Transform[][] allLegList;
    private Vector3 startPosition;
    private Quaternion startRotation;
    private Transform Center;
    
    public override void Initialize()
    {
        m_JdController = GetComponent<JointDriveController>();
        leg0List = new Transform[]{leg0, leg0Upper, leg0Lower};
        leg1List = new Transform[]{leg1, leg1Upper, leg1Lower};
        leg2List = new Transform[]{leg2, leg2Upper, leg2Lower};
        leg3List = new Transform[]{leg3, leg3Upper, leg3Lower};
        allLegList = new Transform[][]{leg0List, leg1List, leg2List, leg3List};

        //Setup each body part
        m_JdController.SetupBodyPart(body);
        SetupBodyPartList(m_JdController, leg0List);
        SetupBodyPartList(m_JdController, leg1List);
        SetupBodyPartList(m_JdController, leg2List);
        SetupBodyPartList(m_JdController, leg3List);

        Center = transform.Find("Center");
        startPosition = Center.localPosition;
        startRotation = Center.localRotation;
    }
    
    private void SetupBodyPartList(JointDriveController con, Transform[] list)
    {
        foreach (Transform i in list)
        {
            con.SetupBodyPart(i);
        }
    }

    public override void OnEpisodeBegin()
    {
        foreach (var bodyPart in m_JdController.bodyPartsDict.Values)
        {
            bodyPart.Reset(bodyPart);
        }
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        var bpDict = m_JdController.bodyPartsDict;

        for (int leg_i = 0; leg_i < allLegList.Length; leg_i++)
        {
            bpDict[allLegList[leg_i][0]].SetJointTargetRotation(0, actions.ContinuousActions[3*leg_i+0], 0);
            bpDict[allLegList[leg_i][1]].SetJointTargetRotation(actions.ContinuousActions[3*leg_i+1], 0, 0);
            bpDict[allLegList[leg_i][2]].SetJointTargetRotation(actions.ContinuousActions[3*leg_i+2], 0, 0);
        }
    }

    public override void CollectObservations(VectorSensor sensor){
        // Observe the agent's local rotation (3 observations)
        // sensor.AddObservation(Center.localRotation.eulerAngles);

        // Observe the agent local position (3 observations)
        sensor.AddObservation(Center.localPosition);
        // Get a vector from the startposition to the currentposition
        Vector3 distanceWalked = Center.localPosition - startPosition;
        // Observe a vector pointing from start position to where it is (3 observations)
        sensor.AddObservation(distanceWalked);

        // Observe a dot product that indicates whether the beak tip is in front of the flower (1 observation)
        // (+1 means that the beak tip is directly in front of the flower, -1 means directly behind)
        //sensor.AddObservation(Vector3.Dot(toFlower.normalized, -nearestFlower.FlowerUpVector.normalized));

        // Observe a dot product that indicates whether the beak is pointing toward the flower (1 observation)
        // (+1 means that the beak is pointing directly at the flower, -1 means directly away)
        //sensor.AddObservation(Vector3.Dot(beakTip.forward.normalized, -nearestFlower.FlowerUpVector.normalized));

        // Observe the relative distance from the beak tip to the flower (1 observation)
        sensor.AddObservation(1);

        // 7 total observations
    }
}
