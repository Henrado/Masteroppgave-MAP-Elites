using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.SideChannels;
using UnityEngine.SceneManagement;

public class RobotManager : MonoBehaviour
{
    // singleton
    private static RobotManager instance;
    public static RobotManager Instance { get { return instance; } }


    [Tooltip("Makes sure the physics start after n fixed updates")]
    [SerializeField] int warmupFixedUpdates = 80;

    [Tooltip("Prefab som skal brukes som grus")]
    public GameObject cubePrefab;

    // Side channel
    public ConfigSideChannel rc;
    public void Awake() {
        if (instance != null && instance != this) {
            this.gameObject.SetActive(false);
            Destroy(this.gameObject);
            return;
        }
        else if (instance == null) {
            instance = this;
        }
        DontDestroyOnLoad(this.gameObject);
        if (rc == null) {
            rc = new ConfigSideChannel();
            SideChannelManager.RegisterSideChannel(rc);
            Unity.MLAgents.Academy.Instance.OnEnvironmentReset += ResetScene;
        }
    }

    public void ResetScene() {
        SceneManager.LoadScene("SampleScene");
        StartCoroutine(SpawnENV());
    }

    IEnumerator SpawnENV() {
        // Wait for scene to load properly
        for (int i = 0; i < warmupFixedUpdates; i++)
            yield return new WaitForFixedUpdate();
        
        if (rc.CubeCount > 0)
        {
            CreateCubes(rc.CubeCount);
        } 
    }

    public void CreateCubes(int n)
    {
        Random.InitState(0);
        for (int i = 0; i < n; i++)
        {
            Vector3 randomPos = new Vector3(Random.Range(-10.0f, 10.0f), -0.5f, Random.Range(-10.0f, 10.0f));
            Quaternion randomRot = Quaternion.identity;
            randomRot.eulerAngles = new Vector3(Random.Range(0.0f, 360.0f),Random.Range(0.0f, 360.0f),Random.Range(0.0f, 360.0f));
            Instantiate(cubePrefab, randomPos, randomRot);
        }
    }

    public void OnDestroy(){
        if (Academy.IsInitialized && rc != null)
            SideChannelManager.UnregisterSideChannel(rc);
    }
}