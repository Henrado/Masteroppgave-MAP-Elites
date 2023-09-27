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
    private Transform[][] allLegList;
    private float t = 0f;
    private float[,] leg0Params;
    private float[,] leg1Params;
    private float[,] leg2Params;
    private float[,] leg3Params;
    private float[][,] allLegParams;
    
    public override void Initialize()
    {
        m_JdController = GetComponent<JointDriveController>();
        leg0List = new Transform[]{leg0, leg0Upper, leg0Lower};
        leg1List = new Transform[]{leg1, leg1Upper, leg0Lower};
        leg2List = new Transform[]{leg2, leg2Upper, leg0Lower};
        leg3List = new Transform[]{leg3, leg3Upper, leg0Lower};
        allLegList = new Transform[][]{leg0List, leg1List, leg2List, leg3List};

        int countJoint = 3;
        int countVars = 5;
        leg0Params = new float[countJoint,countVars];
        leg1Params = new float[countJoint,countVars];
        leg2Params = new float[countJoint,countVars];
        leg3Params = new float[countJoint,countVars];
        allLegParams = new float[][,]{leg0Params, leg1Params, leg2Params, leg3Params};

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
    public void SetParameters(float[][,] newParamsList)
    {
        for (int leg_i = 0; leg_i < allLegParams.Length; leg_i++)
        {
            for (int joint = 0; joint < allLegParams[leg_i].GetLength(0); joint++)
            {
                for (int param = 0; param < allLegParams[leg_i].GetLength(1); param++)
                {
                    allLegParams[leg_i][joint,param] = newParamsList[leg_i][joint, param];
                }
            }
        }
    }

    public override void OnEpisodeBegin()
    {
        foreach (var bodyPart in m_JdController.bodyPartsDict.Values)
        {
            bodyPart.Reset(bodyPart);
        }
    }

    private float GetWantedAngle(float A, float f, float t, float phi, float theta)
    {
        return A*Mathf.Sin(2*Mathf.PI*f*t + phi) + theta;
    }

    void FixedUpdate()
    {
        var bpDict = m_JdController.bodyPartsDict;
        t+=0.01f;
        for (int leg_i = 0; leg_i < allLegList.Length; leg_i++)
        {
            float[,] jWP = allLegParams[leg_i]; // jointsWithParams
            int countAngels = allLegParams[leg_i].GetLength(0);
            float[] angels = new float[countAngels];
            for (int i = 0; i < angels.Length; i++)
            {
                angels[i] = GetWantedAngle(jWP[i,0], jWP[i,1], jWP[i,2], jWP[i,3], jWP[i,4]);
            }
            bpDict[allLegList[leg_i][0]].SetJointTargetRotation(0, angels[0], 0);
            bpDict[allLegList[leg_i][1]].SetJointTargetRotation(angels[1], 0, 0);
            bpDict[allLegList[leg_i][2]].SetJointTargetRotation(angels[2], 0, 0);
        }
    }
}
