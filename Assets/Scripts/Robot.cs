using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgentsExamples;
using Random = UnityEngine.Random;

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
    private float t = 0f;
    private float f_X = 1f;
    
    public override void Initialize()
    {
        m_JdController = GetComponent<JointDriveController>();
        leg0List = new Transform[]{leg0, leg0Upper, leg0Lower};
        leg1List = new Transform[]{leg1, leg1Upper, leg0Lower};
        leg2List = new Transform[]{leg2, leg2Upper, leg0Lower};
        leg3List = new Transform[]{leg3, leg3Upper, leg0Lower};

        //Setup each body part
        m_JdController.SetupBodyPart(body);
        SetupBodyPartList(m_JdController, leg0List);
        SetupBodyPartList(m_JdController, leg1List);
        SetupBodyPartList(m_JdController, leg2List);
        SetupBodyPartList(m_JdController, leg3List);
    }
    
    private void SetupBodyPartList(JointDriveController con, Transform[] list)
    {
        foreach (Transform i in list)
        {
            con.SetupBodyPart(i);
        }
    }
    public void SetParameters(float x)
    {
        this.f_X = x;
        Debug.Log("Parametrs satt");
    }

    public override void OnEpisodeBegin()
    {
        foreach (var bodyPart in m_JdController.bodyPartsDict.Values)
        {
            bodyPart.Reset(bodyPart);
        }
    }

    void FixedUpdate()
    {
        var bpDict = m_JdController.bodyPartsDict;

        // Pick a new target joint rotation
        float A = 1f;
        float f_X = 1f;
        float f_Z = 0.1f;
        float theta = 0f;
        float phi = 0f;
        t+=0.01f;

        float vinkel_X = A*Mathf.Sin(2*Mathf.PI*f_X*t + phi) + theta;
        float vinkel_Z = A*Mathf.Sin(2*Mathf.PI*f_Z*t + phi) + theta;
        //Debug.Log(vinkel);
        bpDict[leg0].SetJointTargetRotation(0, vinkel_Z, 0);
        bpDict[leg0Upper].SetJointTargetRotation(vinkel_X, 0, 0);
        bpDict[leg0Lower].SetJointTargetRotation(vinkel_Z, 0, 0);
    }
}
