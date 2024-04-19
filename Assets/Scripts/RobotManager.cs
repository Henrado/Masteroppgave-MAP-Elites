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
        Random.InitState(0);
        SceneManager.LoadScene("SampleScene");
        Random.InitState(0);
        StartCoroutine(SpawnENV());
        Random.InitState(0);
    }

    IEnumerator SpawnENV() {
        // Wait for scene to load properly
        for (int i = 0; i < warmupFixedUpdates; i++)
            yield return new WaitForFixedUpdate();
        
    }

    public void OnDestroy(){
        if (Academy.IsInitialized && rc != null)
            SideChannelManager.UnregisterSideChannel(rc);
    }
}