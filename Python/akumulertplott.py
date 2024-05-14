from Plot.akumulering_utils import *



#container_shape = config["containers"][config["algorithms"]["container"]]["shape"]

determ = [
    {"path": "../../Master_Resultater/Determ/T_S_B_exLimit", "label": "T_S_B_exLimit", "color": "black"},
    {"path": "../../Master_Resultater/Determ/Z_S_B_exLimit", "label": "Z_S_B_exLimit", "color": "grey"},
    {"path": "../../Master_Resultater/Determ/G_S_B_exLimit", "label": "G_S_B_exLimit", "color": "magenta"},

    {"path": "../../Master_Resultater/Determ/T_SUfq_B_exLimit", "label": "T_SUfq_B_exLimit", "color": "red"},
    {"path": "../../Master_Resultater/Determ/Z_SUfq_B_exLimit", "label": "Z_SUfq_B_exLimit", "color": "lightcoral"},
    {"path": "../../Master_Resultater/Determ/G_SUfq_B_exLimit", "label": "G_SUfq_B_exLimit", "color": "peru"},

    {"path": "../../Master_Resultater/Determ/T_T_B_exLimit", "label": "T_T_B_exLimit", "color": "royalblue"},
    {"path": "../../Master_Resultater/Determ/Z_T_B_exLimit", "label": "Z_T_B_exLimit", "color": "navy"},
    {"path": "../../Master_Resultater/Determ/G_T_B_exLimit", "label": "G_T_B_exLimit", "color": "indigo"},

    {"path": "../../Master_Resultater/Determ/T_TWoff_B_exLimit", "label": "T_TWoff_B_exLimit", "color": "gold"},
    {"path": "../../Master_Resultater/Determ/Z_TWoff_B_exLimit", "label": "Z_TWoff_B_exLimit", "color": "orange"},
    {"path": "../../Master_Resultater/Determ/G_TWoff_B_exLimit", "label": "G_TWoff_B_exLimit", "color": "tan"},

    {"path": "../../Master_Resultater/Determ/T_TWoffFq_B_exLimit", "label": "T_TWoffFq_B_exLimit", "color": "forestgreen"},
    {"path": "../../Master_Resultater/Determ/Z_TWoffFq_B_exLimit", "label": "Z_TWoffFq_B_exLimit", "color": "lime"},
    {"path": "../../Master_Resultater/Determ/G_TWoffFq_B_exLimit", "label": "G_TWoffFq_B_exLimit", "color": "palegreen"}
]

miljo = [
    {"CubeSize": 0, "CubeCount": "Ingen"    ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_CS0", "label": "CubeSize=0 10000 kuber", "color": "lime"},
    {"CubeSize": 1, "CubeCount": "Full"     ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_CS1", "label": "CubeSize=1 10000 kuber", "color": "magenta"},
    {"CubeSize": 2, "CubeCount": "Full"     ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_CS2", "label": "CubeSize=2 10000 kuber", "color": "red"},
    {"CubeSize": 5, "CubeCount": "Full"     ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_CS5", "label": "CubeSize=5 10000 kuber", "color": "navy"},
    {"CubeSize": 1, "CubeCount": "Halvert"  ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_HCS1", "label": "CubeSize=1 5000 kuber", "color": "gold"},
    {"CubeSize": 2, "CubeCount": "Halvert"  ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_HCS2", "label": "CubeSize=2 5000 kuber", "color": "forestgreen"},
    {"CubeSize": 5, "CubeCount": "Halvert"  ,"path": "../../Master_Resultater/timescale1/miljo_timescale/Z_TWoff_B_HCS5", "label": "CubeSize=5 5000 kuber", "color": "black"}
]

gruppert = [
    {"Individ": "Fullt delt","Kontroller": "SinFreq",     "label": "Fullt delt SinFreq",      "path":"../../Master_Resultater/timescale1/kontrollers_timescale/G_S_B_exLimit"},
    {"Individ": "Fullt delt","Kontroller": "Sin",         "label": "Fullt delt Sin",          "path":"../../Master_Resultater/timescale1/kontrollers_timescale/G_SUfq_B_exLimit"},
    {"Individ": "Fullt delt","Kontroller": "Tan",         "label": "Fullt delt Tan",          "path":"../../Master_Resultater/timescale1/kontrollers_timescale/G_T_B_exLimit"},
    {"Individ": "Fullt delt","Kontroller": "TanOff",      "label": "Fullt delt TanOff",       "path":"../../Master_Resultater/timescale1/kontrollers_timescale/G_TWoff_B_exLimit"},
    {"Individ": "Fullt delt","Kontroller": "TanOffFreq",  "label": "Fullt delt TanOffFreq",   "path":"../../Master_Resultater/timescale1/kontrollers_timescale/G_TWoffFq_B_exLimit"},

    {"Individ": "Segment delt","Kontroller": "SinFreq",   "label": "Segment delt SinFreq",    "path":"../../Master_Resultater/timescale1/kontrollers_timescale/T_S_B_exLimit"},
    {"Individ": "Segment delt","Kontroller": "Sin",       "label": "Segment delt Sin",        "path":"../../Master_Resultater/timescale1/kontrollers_timescale/T_SUfq_B_exLimit"},
    {"Individ": "Segment delt","Kontroller": "Tan",       "label": "Segment delt Tan",        "path":"../../Master_Resultater/timescale1/kontrollers_timescale/T_T_B_exLimit"},
    {"Individ": "Segment delt","Kontroller": "TanOff",    "label": "Segment delt TanOff",     "path":"../../Master_Resultater/timescale1/kontrollers_timescale/T_TWoff_B_exLimit"},
    {"Individ": "Segment delt","Kontroller": "TanOffFreq","label": "Segment delt TanOffFreq", "path":"../../Master_Resultater/timescale1/kontrollers_timescale/T_TWoffFq_B_exLimit"},

    {"Individ": "Ikke delt","Kontroller": "SinFreq",      "label": "Ikke delt SinFreq",       "path":"../../Master_Resultater/timescale1/kontrollers_timescale/Z_S_B_exLimit"},
    {"Individ": "Ikke delt","Kontroller": "Sin",          "label": "Ikke delt Sin",           "path":"../../Master_Resultater/timescale1/kontrollers_timescale/Z_SUfq_B_exLimit"},
    {"Individ": "Ikke delt","Kontroller": "Tan",          "label": "Ikke delt Tan",           "path":"../../Master_Resultater/timescale1/kontrollers_timescale/Z_T_B_exLimit"},
    {"Individ": "Ikke delt","Kontroller": "TanOff",       "label": "Ikke delt TanOff",        "path":"../../Master_Resultater/timescale1/kontrollers_timescale/Z_TWoff_B_exLimit"},
    {"Individ": "Ikke delt","Kontroller": "TanOffFreq",   "label": "Ikke delt TanOffFreq",    "path":"../../Master_Resultater/timescale1/kontrollers_timescale/Z_TWoffFq_B_exLimit"}
]

fult    = [gruppert[0], gruppert[1], gruppert[2], gruppert[3], gruppert[4]]
segment = [gruppert[5], gruppert[6], gruppert[7], gruppert[8] , gruppert[9]]
ikke    = [gruppert[10], gruppert[11], gruppert[12], gruppert[13], gruppert[14]]

sinFreq   = [gruppert[0], gruppert[5], gruppert[10]]
sin       = [gruppert[1], gruppert[6], gruppert[11]]
tan       = [gruppert[2], gruppert[7], gruppert[12]]
tanOff    = [gruppert[3], gruppert[8], gruppert[13]]
tanOffFreq= [gruppert[4], gruppert[9], gruppert[14]]
ex_lost_dict = gruppert
do_it_all_boxsplot(ex_lost_dict, "iterations.csv", key="qd_score", key_gruppe="Individ", key_type="Kontroller", title="QD score", output_filename="QD_score_box.pdf")
#do_it_all_stdline(ex_lost_dict, "iterations.csv", "qd_score", title="QD score per iterasjon", scale=True, output_filename="QD_score.pdf")
for i in ex_lost_dict:
    i["filname"] = i["path"].split("/")[5][10:]

#do_it_all_grid_per_ex(ex_lost_dict, performance=True, activity=False)


#do_it_all_stdline(miljo, "iterations.csv", "qd_score", title="QD score per iterasjon", scale=True, output_filename="QD_score_miljo.pdf")
#do_it_all_boxsplot(miljo, "iterations.csv", key="qd_score", key_gruppe="CubeSize", key_type="CubeCount", title="QD score", output_filename="QD_score_miljo_box.pdf")
""" do_it_all_stdline(zero, "iterations.csv", "qd_score", title="QD_score for Zero", scale=True, output_filename="QD_score_zero.svg")
do_it_all_stdline(two, "iterations.csv", "qd_score", title="QD_score for Two", scale=True, output_filename="QD_score_two.svg")
do_it_all_stdline(glob, "iterations.csv", "qd_score", title="QD_score for Global", scale=True, output_filename="QD_score_global.svg")

do_it_all_stdline(s, "iterations.csv", "qd_score", title="QD_score for Sinus", scale=True, output_filename="QD_score_S.svg")
do_it_all_stdline(sufq, "iterations.csv", "qd_score", title="QD_score for Sinus uten frekvens", scale=True, output_filename="QD_score_SUfq.svg")
do_it_all_stdline(t, "iterations.csv", "qd_score", title="QD_score for Tanh", scale=True, output_filename="QD_score_T.svg")
do_it_all_stdline(tWoff, "iterations.csv", "qd_score", title="QD_score for Tanh med offset", scale=True, output_filename="QD_score_TWoff.svg")
do_it_all_stdline(tWoffFq, "iterations.csv", "qd_score", title="QD_score for Tanh med offset og frekvens", scale=True, output_filename="QD_score_TWoffFq.svg") """



""" d, conf = get_all_dataframes(path, "grid.solutions.csv", parse=True)
arr2 = dataframe2numpy(d, dtype=object)

a = np.empty(shape=arr2.shape)
for i in range(arr2.shape[0]):
    for j in range(arr2.shape[1]):
        for k in range(arr2.shape[2]):
            svar = []
            for liste in (arr2[i][j][k]):
                svar.append(liste["genom"][0])
            if len(svar)>0:
                a[i][j][k] = np.nanmax(svar)
b = a[:][9][:] """