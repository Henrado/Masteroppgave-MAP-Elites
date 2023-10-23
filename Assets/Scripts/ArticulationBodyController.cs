using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Serialization;
using Unity.MLAgents;

namespace Unity.MLAgentsExamples
{
    /// <summary>
    /// Used to store relevant information for acting and learning for each body part in agent.
    /// </summary>
    [System.Serializable]
    public class BodyPart_ny
    {
        [Header("Body Part Info")][Space(10)] public ArticulationBody joint;
        public ArticulationBody ab;
        [HideInInspector] public Vector3 startingPos;
        [HideInInspector] public Quaternion startingRot;

        [Header("Ground & Target Contact")]
        [Space(10)]
        // public GroundContact groundContact;

        //public TargetContact targetContact;

        [FormerlySerializedAs("thisJDController")]
        [HideInInspector] public ArticulationBodyController thisJdController;

        [Header("Current Joint Settings")]
        [Space(10)]
        public Vector3 currentEularJointRotation;

        [HideInInspector] public float currentStrength;
        public float currentXNormalizedRot;
        public float currentYNormalizedRot;
        public float currentZNormalizedRot;

        [Header("Other Debug Info")]
        [Space(10)]
        public Vector3 currentJointForce;

        public float currentJointForceSqrMag;
        public Vector3 currentJointTorque;
        public float currentJointTorqueSqrMag;
        public AnimationCurve jointForceCurve = new AnimationCurve();
        public AnimationCurve jointTorqueCurve = new AnimationCurve();

        /// <summary>
        /// Reset body part to initial configuration.
        /// </summary>
        public void Reset(BodyPart_ny bp)
        {
            bp.ab.transform.position = bp.startingPos;
            bp.ab.transform.rotation = bp.startingRot;
            bp.ab.velocity = Vector3.zero;
            bp.ab.angularVelocity = Vector3.zero;
            // if (bp.groundContact)
            // {
            //     bp.groundContact.touchingGround = false;
            // }

            //if (bp.targetContact)
            //{
            //    bp.targetContact.touchingTarget = false;
            //}
        }

        /// <summary>
        /// Apply torque according to defined goal `x, y, z` angle and force `strength`.
        /// </summary>
        public void SetJointTargetRotation(float x, float y, float z)
        {
            x = (x + 1f) * 0.5f;
            y = (y + 1f) * 0.5f;
            z = (z + 1f) * 0.5f;

            var xRot = Mathf.Lerp(joint.xDrive.lowerLimit, joint.xDrive.upperLimit, x);
            var yRot = Mathf.Lerp(-joint.yDrive.lowerLimit, joint.yDrive.upperLimit, y);
            var zRot = Mathf.Lerp(-joint.zDrive.lowerLimit, joint.zDrive.upperLimit, z);

            currentXNormalizedRot =
                Mathf.InverseLerp(joint.xDrive.lowerLimit, joint.xDrive.upperLimit, xRot);
            currentYNormalizedRot = Mathf.InverseLerp(-joint.yDrive.lowerLimit, joint.yDrive.upperLimit, yRot);
            currentZNormalizedRot = Mathf.InverseLerp(-joint.zDrive.lowerLimit, joint.zDrive.upperLimit, zRot);

            joint.xDrive = new ArticulationDrive{target = xRot};
            joint.yDrive = new ArticulationDrive{target = yRot};
            joint.zDrive = new ArticulationDrive{target = zRot};
            currentEularJointRotation = new Vector3(xRot, yRot, zRot);
        }

        public void SetJointStrength(float strength)
        {
            var rawVal = (strength + 1f) * 0.5f * thisJdController.maxJointForceLimit;
            var ad = new ArticulationDrive
                {
                    stiffness = thisJdController.maxJointSpring,
                    damping = thisJdController.jointDampen,
                    forceLimit = thisJdController.maxJointForceLimit,
                    targetVelocity = rawVal
                };
            joint.xDrive = ad;
            joint.yDrive = ad;
            joint.zDrive = ad;
            currentStrength = ad.forceLimit;
        }
    }

    public class ArticulationBodyController : MonoBehaviour
    {
        [Header("Joint Drive Settings")]
        [Space(10)]
        public float maxJointSpring;

        public float jointDampen;
        public float maxJointForceLimit;

        [HideInInspector] public Dictionary<Transform, BodyPart_ny> bodyPartsDict = new Dictionary<Transform, BodyPart_ny>();

        [HideInInspector] public List<BodyPart_ny> bodyPartsList = new List<BodyPart_ny>();
        const float k_MaxAngularVelocity = 10.47f; // 100 RPM = 10.471976 rad/s

        /// <summary>
        /// Create BodyPart object and add it to dictionary.
        /// </summary>
        public void SetupBodyPart(Transform t)
        {
            var bp = new BodyPart_ny
            {
                ab = t.GetComponent<ArticulationBody>(),
                //joint = t.GetComponent<ConfigurableJoint>(),
                startingPos = t.position,
                startingRot = t.rotation
            };
            Debug.Log(bp.ab);
            bp.ab.maxAngularVelocity = k_MaxAngularVelocity;

            if (bp.ab)
            {
                var ad = new ArticulationDrive
                {
                    stiffness = maxJointSpring,
                    damping = jointDampen,
                    forceLimit = maxJointForceLimit,
                    targetVelocity = k_MaxAngularVelocity
                };
                bp.joint.xDrive = ad;
                bp.joint.yDrive = ad;
                bp.joint.zDrive = ad;
                Debug.Log("Satt drivere");
            }

            bp.thisJdController = this;
            bodyPartsDict.Add(t, bp);
            bodyPartsList.Add(bp);
        }

        public void GetCurrentJointForces()
        {
        }
    }
}
