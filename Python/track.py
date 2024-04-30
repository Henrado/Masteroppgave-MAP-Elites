import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def read_csv(filname, index_col, skiprows=0, rename=None):
    csv = pd.read_csv(filname, skiprows=skiprows, index_col=index_col)
    if rename != None:
        csv = csv.rename(columns=rename, errors="raise")
    return csv

def set_to_origin(csv, keywords):
    for key in keywords:
        csv.loc[:,key] = csv.loc[:,key] - csv.loc[0, key] 
    return csv

def cut_begining(csv):
    start_pos = np.array([csv.loc[0, "X_pos"], csv.loc[0, "Y_pos"], csv.loc[0, "Z_pos"]])
    start_rot = np.array([csv.loc[0, "X_rot"], csv.loc[0, "Y_rot"], csv.loc[0, "Z_rot"]])
    kutt = 0
    for i in range(len(csv)):
        line_pos = np.array([csv.loc[i, "X_pos"], csv.loc[i, "Y_pos"], csv.loc[i, "Z_pos"]])
        line_rot = np.array([csv.loc[i, "X_rot"], csv.loc[i, "Y_rot"], csv.loc[i, "Z_rot"]])
        diff = start_pos-line_pos
        
        if np.sqrt(diff.dot(diff)) > 0.2:
            #print(i, diff)
            kutt = i
            break
    return csv.iloc[kutt:]

def prepare_sim(csv):
    csv.loc[:,"X_pos_sim"] = -csv.loc[:,"X_pos_sim"]*10
    csv.loc[:,"Z_pos_sim"] = csv.loc[:,"Z_pos_sim"]*10
    return csv

def do_it_all(ax, base_dir_real, base_dir_sim, ex_name_tuple):
    ex_name = ex_name_tuple[0]
    ex_title = ex_name_tuple[1]
    real_dir = base_dir_real + ex_name + "/"
    csv_files = [f for f in os.listdir(real_dir) if f.endswith('.csv')]
    sim_filename_uten = base_dir_sim + "" + ex_name + "_exLimit_utenkuber.csv"
    sim_filename_med = base_dir_sim + "" + ex_name + "_exLimit_medkuber.csv"

    sim_rename_dict = {"x": "X_pos_sim", "z": "Z_pos_sim", "y_rot": "Y_rot_sim"}
    real_rename_dict = {"X":"X_rot", "Y":"Y_rot", "Z":"Z_rot", "X.1":"X_pos", "Y.1": "Y_pos", "Z.1": "Z_pos"}
    

    #fig, ax = plt.subplots(figsize=(5.5, 4))
    sim_med_csv = read_csv(sim_filename_med, index_col=0, rename=sim_rename_dict)
    sim_med_csv = prepare_sim(sim_med_csv)

    sim_uten_csv = read_csv(sim_filename_uten, index_col=0, rename=sim_rename_dict)
    sim_uten_csv = prepare_sim(sim_uten_csv)
    
    color = next(ax._get_lines.prop_cycler)['color']
    ax.plot(sim_med_csv.loc[:,"Z_pos_sim"], sim_med_csv.loc[:,"X_pos_sim"], label="Simulering med kuber", color=color, zorder=9)
    xy = (sim_med_csv.loc[:,"Z_pos_sim"].iloc[-1], sim_med_csv.loc[:,"X_pos_sim"].iloc[-1])
    ax.plot([xy[0]], [xy[1]], 'o', label="Endepunkt", color=color, zorder=10)
    #ax.annotate('(%.2f, %.2f)' % xy, xy=xy, textcoords='data')

    ax.plot(sim_uten_csv.loc[:,"Z_pos_sim"], sim_uten_csv.loc[:,"X_pos_sim"], label="Simulering uten kuber", zorder=8)
    
    sum_lengde_sim_med = np.sqrt(sim_med_csv.iloc[-1]["X_pos_sim"]**2+sim_med_csv.iloc[-1]["Z_pos_sim"]**2)
    sum_lengde_sim_uten = np.sqrt(sim_uten_csv.iloc[-1]["X_pos_sim"]**2+sim_uten_csv.iloc[-1]["Z_pos_sim"]**2)

    
    all_csvs = []
    sum_lengde_real = 0
    for ind, i in enumerate(csv_files):
        csv = read_csv(os.path.join(real_dir,i), index_col="Frame", skiprows=6, rename=real_rename_dict)
        csv = set_to_origin(csv, real_rename_dict.values())
        csv = cut_begining(csv=csv)
        sum_lengde_real += np.sqrt(csv.iloc[-1]["X_pos"]**2+csv.iloc[-1]["Y_pos"]**2+csv.iloc[-1]["Z_pos"]**2)
        all_csvs.append(csv)
        ax.plot(csv.loc[:,"Z_pos"], csv.loc[:,"X_pos"], label="Kjøring nr: " + str(ind))
    #sns.lineplot(sim, y="X_pos_sim", x="Z_pos_sim", hue="ind")
    #sns.lineplot(lest, y="X_pos", x="Z_pos")
    print("Med", ex_name, sum_lengde_sim_med/(sum_lengde_real/len(csv_files)))
    print("Uten", ex_name, sum_lengde_sim_uten/(sum_lengde_real/len(csv_files)))
    print("Begge", ex_name, ((sum_lengde_sim_uten+sum_lengde_sim_med)/2)/(sum_lengde_real/len(csv_files)))
    ax.set_title(ex_title, fontsize=12)
    ax.legend(fontsize=5)
    ax.set_xlabel("Z retning", fontdict=dict(fontsize=12))
    #ax.set_ylabel("X retning", fontdict=dict(fontsize=12))
    ax.grid()
    #ax.set_aspect('equal', 'datalim')
    ax.set_xlim(-45, 130)
    ax.set_aspect('equal')
    #ax.set_ylim(-100, 100)
    output_filename = ex_name + "_real.svg"
    #fig.savefig(output_filename)
    #plt.close(fig)


if __name__ == "__main__":
    ex_names_base = {"X-retning":"X-retning", 
                     "Z-retning":"Z-retning"
                     }
    base_dir_real_base = "../../Master_Resultater/FysiskTest/Baseline/Mocap/"
    base_dir_sim_base  = "../../Master_Resultater/FysiskTest/Baseline/Sim/"

    miljo_ex_names1 = {
        "CS0": "Cubesize=0 0 kuber"
    }

    miljo_ex_names2 = {"CS1":"Cubesize=1 10k kuber", 
                      "CS2":"Cubesize=2 10k kuber", 
                      "CS5":"Cubesize=5 10k kuber", 
                      "HCS1":"Cubesize=1 5k kuber", 
                      "HCS2":"Cubesize=2 5k kuber",
                      "HCS5":"Cubesize=5 5k kuber"
                      }
    miljo_base_dir_real = "../../Master_Resultater/FysiskTestTimescale/Miljo/Mocap/"
    miljo_base_dir_sim  = "../../Master_Resultater/FysiskTestTimescale/Miljo/Sim/"

    ex_names1 = {"G_S_B":       "Fullt delt SinFreq", 
                "G_SUfq_B":     "Fullt delt Sin", 
                "G_T_B":        "Fullt delt Tan", 
                "G_TWoff_B":    "Fullt delt TanOff", 
                "G_TWoffFq_B":  "Fullt delt TanOffFreq",
                "T_S_B":        "Segment delt SinFreq"}
    ex_names2 = {
                "T_SUfq_B":     "Segment delt Sin",
                "T_T_B":        "Segment delt Tan", 
                "T_TWoff_B":    "Segment delt TanOff", 
                "T_TWoffFq_B":  "Segment delt TanOffFreq",
                "Z_S_B":        "Ikke delt SinFreq", 
                "Z_SUfq_B":     "Ikke delt Sin", 
                }
    ex_names3 = {
                "Z_T_B":        "Ikke delt Tan", 
                "Z_TWoff_B":    "Ikke delt TanOff", 
                "Z_TWoffFq_B":  "Ikke delt TanOffFreq"
                }
    kontroller_base_dir_real = "../../Master_Resultater/FysiskTestTimescale/Determ/Mocap/"
    kontroller_base_dir_sim  = "../../Master_Resultater/FysiskTestTimescale/Determ/Sim/"

    fig, axs = plt.subplots(3, 2,figsize=(5.3, 8.5),  sharex=True, sharey=True)
    #axs = axs.reshape(-1)
    ex_names = miljo_ex_names1
    for i, ax in zip(ex_names.items(), axs.flat):
        do_it_all(ax, miljo_base_dir_real, miljo_base_dir_sim, i)
    
    """ #For å fylle på med x og z retning
    do_it_all(axs.flat[4], base_dir_real_base, base_dir_sim_base, ("X-retning","X-retning"))
    do_it_all(axs.flat[5], base_dir_real_base, base_dir_sim_base, ("Z-retning","Z-retning"))
    """
    axs.flat[0].set_ylabel("X retning", fontdict=dict(fontsize=12))
    axs.flat[2].set_ylabel("X retning", fontdict=dict(fontsize=12))
    axs.flat[4].set_ylabel("X retning", fontdict=dict(fontsize=12))

    ## access each axes object via axs.flat
    for ax in axs.flat:
        ## check if something was plotted 
        if not bool(ax.has_data()):
            fig.delaxes(ax) ## delete if nothing is plotted in the axes obj

    fig.autofmt_xdate()
    plt.tight_layout()
    #fig.savefig("real_ex3_2.pdf")
    plt.show()