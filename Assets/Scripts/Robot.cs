using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgentsExamples;
using Unity.MLAgents.SideChannels;
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
    public AnimationCurve forceCurve;
    public AnimationCurve torqueCurve;
    private ConfigSideChannel parameterChannel;

    [Tooltip("Prefab som skal brukes som grus")]
    public GameObject cubePrefab;
    public GroundContact GC;

    
    public void Awake()
    {
    }
    public override void Initialize()
    {
        parameterChannel = FindObjectOfType<RobotManager>().rc;
        m_JdController = GetComponent<JointDriveController>();
        leg0List = new Transform[]{leg0, leg0Upper, leg0Lower};
        leg1List = new Transform[]{leg1, leg1Upper, leg1Lower};
        leg2List = new Transform[]{leg2, leg2Upper, leg2Lower};
        leg3List = new Transform[]{leg3, leg3Upper, leg3Lower};
        allLegList = new Transform[][]{leg0List, leg1List, leg2List, leg3List};

        IList<float> jointDriveSettings = parameterChannel.jointDriveSettings;
        if (jointDriveSettings != null){
            m_JdController.maxJointSpring = jointDriveSettings[0];
            m_JdController.jointDampen = jointDriveSettings[1];
            m_JdController.maxJointForceLimit = jointDriveSettings[2];
        }

        IList<float> legAngularLimits = parameterChannel.legAngularLimits;
        List<List<float>> limitsArray = MakeAngularLimitsArray(legAngularLimits);
        //Setup each body part
        m_JdController.SetupBodyPart(body, new List<float>());
        SetupBodyPartList(m_JdController, leg0List, limitsArray);
        SetupBodyPartList(m_JdController, leg1List, limitsArray);
        SetupBodyPartList(m_JdController, leg2List, limitsArray);
        SetupBodyPartList(m_JdController, leg3List, limitsArray);

        Center = transform.Find("Center");
        startPosition = Center.localPosition;
        startRotation = Center.localRotation;

        if (parameterChannel.robotMassPart != null){
            SetPartMass(this.transform, parameterChannel.robotMassPart, 0);
        }

        if (parameterChannel.groundContactPenaltyPart != 0){
            GC.groundContactPenalty = parameterChannel.groundContactPenaltyPart;
            GC.penalizeGroundContact = true;
        }
        if (parameterChannel.CubeCount > 0)
        {
            CreateCubes(parameterChannel.CubeCount, parameterChannel.CubeSize);
        } 
    }
    
    private void SetupBodyPartList(JointDriveController con, Transform[] list, List<List<float>> limits)
    {
        for (int i = 0; i < list.Length; i++)
        {
            con.SetupBodyPart(list[i], limits[i]);
        }
    }

    public override void OnEpisodeBegin()
    {
        Random.InitState(0);
        return;
        //foreach (var bodyPart in m_JdController.bodyPartsDict.Values)
        //{
        //    bodyPart.Reset(bodyPart);
        //}
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        var bpDict = m_JdController.bodyPartsDict;

        for (int leg_i = 0; leg_i < allLegList.Length; leg_i++)
        {
            bpDict[allLegList[leg_i][0]].SetJointTargetRotation(0, actions.ContinuousActions[3*leg_i+0], 0); //leg0
            bpDict[allLegList[leg_i][1]].SetJointTargetRotation(actions.ContinuousActions[3*leg_i+1], 0, 0); //upperleg0
            bpDict[allLegList[leg_i][2]].SetJointTargetRotation(actions.ContinuousActions[3*leg_i+2], 0, 0); //forleg0
        }
    }
    void FixedUpdate()
    {
        var bpDict = m_JdController.bodyPartsDict;

        m_JdController.GetCurrentJointForces();
        forceCurve = bpDict[leg0Upper].jointForceCurve;
        torqueCurve = bpDict[leg0Upper].jointTorqueCurve;
    }

    private List<List<float>> MakeAngularLimitsArray(IList<float> list){
        if (list == null){
            return new List<List<float>>
            {
                new(),
                new(),
                new()
            };
        }
        List<List<float>> myList = new()
        {
            new List<float> { list[0] },
            new List<float> { list[1], list[2] },
            new List<float> { list[3], list[4] }
        };
        return myList;
    } 

    private void SetPartMass(Transform part, IList<float> masses, int dept){
        foreach (Transform child in part)
        {
            if (child.TryGetComponent<Rigidbody>(out var rb) & masses.Count >= dept)
            {
                rb.mass = masses[dept];
                SetPartMass(child, masses, dept+1);
            }
        }
    }

    public void CreateCubes(int n, float scale)
    {
        Random.InitState(0);
        for (int i = 0; i < n; i++)
        {
            Vector3 randomPos = new Vector3(Random.Range(-10.0f, 10.0f), -0.5f, Random.Range(-10.0f, 10.0f));
            Quaternion randomRot = Quaternion.identity;
            randomRot.eulerAngles = new Vector3(Random.Range(0.0f, 360.0f),Random.Range(0.0f, 360.0f),Random.Range(0.0f, 360.0f));
            GameObject go = Instantiate(cubePrefab, randomPos, randomRot);
            if (scale != 1){
                go.transform.localScale = new Vector3(scale, scale, scale);
            }
        }
    }

    public override void CollectObservations(VectorSensor sensor){
        // Observe the agent's local rotation (3 observations)
        // sensor.AddObservation(Center.localRotation.eulerAngles);

        // Observe the agent local position (3 observations)
        sensor.AddObservation(Center.localPosition);

        // Observe the agent local rotation in eulerangels (3 observations)
        sensor.AddObservation(Center.localRotation.eulerAngles);
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
        sensor.AddObservation(GetCumulativeReward());

        // 7 total observations
    }
    public void OnDestroy()
    {
        if (Academy.IsInitialized){
            SideChannelManager.UnregisterSideChannel(parameterChannel);
        }
    }
}
