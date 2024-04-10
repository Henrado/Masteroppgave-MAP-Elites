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
            print(i, diff)
            kutt = i
            break
    return csv.iloc[kutt:]

def prepare_sim(csv):
    csv.loc[:,"X_pos_sim"] = -csv.loc[:,"X_pos_sim"]*10
    csv.loc[:,"Z_pos_sim"] = csv.loc[:,"Z_pos_sim"]*10
    return csv

def do_it_all(base_dir_real, base_dir_sim, ex_name):
    real_dir = base_dir_real + ex_name + "/"
    csv_files = [f for f in os.listdir(real_dir) if f.endswith('.csv')]
    sim_filename = base_dir_sim + ex_name + "_exLimit_utenkuber.csv"

    sim_rename_dict = {"x": "X_pos_sim", "z": "Z_pos_sim", "y_rot": "Y_rot_sim"}
    real_rename_dict = {"X":"X_rot", "Y":"Y_rot", "Z":"Z_rot", "X.1":"X_pos", "Y.1": "Y_pos", "Z.1": "Z_pos"}
    

    fig, ax = plt.subplots(figsize=(5.5, 4))
    sim_csv = read_csv(sim_filename, index_col=0, rename=sim_rename_dict)
    sim_csv = prepare_sim(sim_csv)
    ax.plot(sim_csv.loc[:,"Z_pos_sim"], sim_csv.loc[:,"X_pos_sim"], label="Simulering")
    all_csvs = []
    for ind, i in enumerate(csv_files):
        csv = read_csv(os.path.join(real_dir,i), index_col="Frame", skiprows=6, rename=real_rename_dict)
        csv = set_to_origin(csv, real_rename_dict.values())
        csv = cut_begining(csv=csv)
        all_csvs.append(csv)
        ax.plot(csv.loc[:,"Z_pos"], csv.loc[:,"X_pos"], label="Kjøring nr: " + str(ind))
    #sns.lineplot(sim, y="X_pos_sim", x="Z_pos_sim", hue="ind")
    #sns.lineplot(lest, y="X_pos", x="Z_pos")
    ax.set_title(ex_name)
    ax.legend(fontsize=4)
    ax.set_xlabel("Z retning", fontdict=dict(fontsize=12))
    ax.set_ylabel("X retning", fontdict=dict(fontsize=12))
    ax.grid()
    fig.autofmt_xdate()
    plt.tight_layout()
    ax.axis('scaled')


if __name__ == "__main__":
    ex_names = ["CS0", "CS1","CS2","CS5","HCS1","HCS2","HCS5"]
    base_dir_real = "result/FysiskTest/Miljo/Mocap/Miljo_"
    base_dir_sim  = "result/FysiskTest/Miljo/Sim/Z_TWoff_B_"

    ex_names = ["G_S_B", "G_SUfq_B", "G_T_B", "G_TWoff_B", "G_TWoffFq_B"]
    ex_names = ["T_S_B", "T_SUfq_B", "T_TWoff_B", "T_TWoffFq_B"]
    ex_names = ["Z_S_B", "Z_SUfq_B", "Z_T_B", "Z_TWoff_B", "Z_TWoffFq_B"]
    base_dir_real = "result/FysiskTest/Determ/Mocap/"
    base_dir_sim  = "result/FysiskTest/Determ/Sim/"
    for i in ex_names:
        do_it_all(base_dir_real, base_dir_sim, i)
    plt.show()