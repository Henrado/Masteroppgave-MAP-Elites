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


def prepare_sim(csv):
    csv.loc[:,"X_pos_sim"] = -csv.loc[:,"X_pos_sim"]*10
    csv.loc[:,"Z_pos_sim"] = csv.loc[:,"Z_pos_sim"]*10
    return csv

def do_it_all(sim1, sim2, endepunkt, ex_name):

    sim_rename_dict = {"x": "X_pos_sim", "z": "Z_pos_sim", "y_rot": "Y_rot_sim"}    

    fig, ax = plt.subplots(figsize=(5.5, 4))
    
    sim1_csv = read_csv(sim1, index_col=0, rename=sim_rename_dict)
    sim1_csv = prepare_sim(sim1_csv)
    ax.plot(sim1_csv.loc[:,"Z_pos_sim"], sim1_csv.loc[:,"X_pos_sim"], label="Sim med ekstra kommando")

    sim2_csv = read_csv(sim2, index_col=0, rename=sim_rename_dict)
    sim2_csv = prepare_sim(sim2_csv)
    
    ax.plot(sim2_csv.loc[:,"Z_pos_sim"], sim2_csv.loc[:,"X_pos_sim"], label="Sim uten ekstra kommando")

    #plt.plot([6.9774365*10], [0.6545745*10], 'o', label="Skulle ha endt") #Dette er for løsning (10,16)
    ax.plot([endepunkt[0]*10], [-endepunkt[1]*10], 'o', label="Skulle ha endt") #Dette er for løsning (16,11)

    ax.set_title(ex_name)
    ax.legend(fontsize=8)
    ax.set_xlabel("Z retning", fontdict=dict(fontsize=12))
    ax.set_ylabel("X retning", fontdict=dict(fontsize=12))
    ax.grid()
    fig.autofmt_xdate()
    plt.tight_layout()
    #ax.axis('scaled')
    ax.set_aspect('equal', 'datalim')
    output_filename = ex_name + "_real.svg"
    #fig.savefig(output_filename)
    #plt.close(fig)


if __name__ == "__main__":
    sim1 = "../../Master_Resultater/ResattTest/0_gang.csv"
    sim2 = "../../Master_Resultater/ResattTest/1_gang.csv"
    endepunkt = [6.9774365, 0.6545745]

    sim1 = "../../Master_Resultater/ResattTest/0_gang_scaletime.csv"
    sim2 = "../../Master_Resultater/ResattTest/1_gang_scaletime.csv"
    endepunkt = [1.7211264, 6.4646335]

    do_it_all(sim1, sim2, endepunkt, "Sammenligning")
    plt.show()