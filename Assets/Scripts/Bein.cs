using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgentsExamples;
using Random = UnityEngine.Random;

[RequireComponent(typeof(JointDriveController))] // Required to set joint forces
public class Bein : Agent
{

    JointDriveController m_JdController;

    [Header("Body Parts")][Space(10)] public Transform body;
    public Transform leg0Upper;

    public AnimationCurve forceCurve;
    public AnimationCurve torqueCurve;
    private float t = 0f;
    public float angle = 0f;
    
    public override void Initialize()
    {
        m_JdController = GetComponent<JointDriveController>();

        //Setup each body part
        m_JdController.SetupBodyPart(body);
        m_JdController.SetupBodyPart(leg0Upper);
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
        t+=0.01f;
        m_JdController.GetCurrentJointForces();
        forceCurve = bpDict[leg0Upper].jointForceCurve;
        torqueCurve = bpDict[leg0Upper].jointTorqueCurve;

        //float vinkel_X = A*Mathf.Sin(2*Mathf.PI*f_X*t + phi) + theta;
        //float vinkel_Z = A*Mathf.Sin(2*Mathf.PI*f_Z*t + phi) + theta;
        //Debug.Log(vinkel);
        bpDict[leg0Upper].SetJointTargetRotation(angle, 0, 0);
        //Debug.Log(bpDict[leg0Upper].joint.currentTorque);
        //Debug.Log(bpDict[leg0Upper].joint.currentTorque.magnitude);
    }
}
