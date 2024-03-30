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
    {"CubeSize": 0, "CubeCount": "Ingen"    ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_CS0", "label": "CubeSize=0", "color": "lime"},
    {"CubeSize": 1, "CubeCount": "Full"     ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_CS1", "label": "CubeSize=1", "color": "magenta"},
    {"CubeSize": 2, "CubeCount": "Full"     ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_CS2", "label": "CubeSize=2", "color": "red"},
    {"CubeSize": 5, "CubeCount": "Full"     ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_CS5", "label": "CubeSize=5", "color": "navy"},
    {"CubeSize": 1, "CubeCount": "Halvert"  ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_HCS1", "label": "CubeSize=1 Half", "color": "gold"},
    {"CubeSize": 2, "CubeCount": "Halvert"  ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_HCS2", "label": "CubeSize=2 Half", "color": "forestgreen"},
    {"CubeSize": 5, "CubeCount": "Halvert"  ,"path": "../../Master_Resultater/Miljo/Z_TWoff_B_HCS5", "label": "CubeSize=5 Half", "color": "black"}
]

gruppert = [
    {"Individ": "Global","Kontroller": "Sin",       "label": "G_S_B_exLimit",       "path":"../../Master_Resultater/Determ/G_S_B_exLimit"},
    {"Individ": "Global","Kontroller": "SUfq",      "label": "G_SUfq_B_exLimit",    "path":"../../Master_Resultater/Determ/G_SUfq_B_exLimit"},
    {"Individ": "Global","Kontroller": "Tanh",      "label": "G_T_B_exLimit",       "path":"../../Master_Resultater/Determ/G_T_B_exLimit"},
    {"Individ": "Global","Kontroller": "TWoff",     "label": "G_TWoff_B_exLimit",   "path":"../../Master_Resultater/Determ/G_TWoff_B_exLimit"},
    {"Individ": "Global","Kontroller": "TWoffFq",   "label": "G_TWoffFq_B_exLimit", "path":"../../Master_Resultater/Determ/G_TWoffFq_B_exLimit"},

    {"Individ": "Two","Kontroller": "Sin",          "label": "T_S_B_exLimit",       "path":"../../Master_Resultater/Determ/T_S_B_exLimit"},
    {"Individ": "Two","Kontroller": "SUfq",         "label": "T_SUfq_B_exLimit",    "path":"../../Master_Resultater/Determ/T_SUfq_B_exLimit"},
    {"Individ": "Two","Kontroller": "Tanh",         "label": "T_T_B_exLimit",       "path":"../../Master_Resultater/Determ/T_T_B_exLimit"},
    {"Individ": "Two","Kontroller": "TWoff",        "label": "T_TWoff_B_exLimit",   "path":"../../Master_Resultater/Determ/T_TWoff_B_exLimit"},
    {"Individ": "Two","Kontroller": "TWoffFq",      "label": "T_TWoffFq_B_exLimit", "path":"../../Master_Resultater/Determ/T_TWoffFq_B_exLimit"},

    {"Individ": "Zero","Kontroller": "Sin",         "label": "Z_S_B_exLimit",       "path":"../../Master_Resultater/Determ/Z_S_B_exLimit"},
    {"Individ": "Zero","Kontroller": "SUfq",        "label": "Z_SUfq_B_exLimit",    "path":"../../Master_Resultater/Determ/Z_SUfq_B_exLimit"},
    {"Individ": "Zero","Kontroller": "Tanh",        "label": "Z_T_B_exLimit",       "path":"../../Master_Resultater/Determ/Z_T_B_exLimit"},
    {"Individ": "Zero","Kontroller": "TWoff",       "label": "Z_TWoff_B_exLimit",   "path":"../../Master_Resultater/Determ/Z_TWoff_B_exLimit"},
    {"Individ": "Zero","Kontroller": "TWoffFq",     "label": "Z_TWoffFq_B_exLimit", "path":"../../Master_Resultater/Determ/Z_TWoffFq_B_exLimit"}
]

two  = [gruppert[0], gruppert[3], gruppert[6], gruppert[9] , gruppert[12]]
zero = [gruppert[1], gruppert[4], gruppert[7], gruppert[10], gruppert[13]]
glob = [gruppert[2], gruppert[5], gruppert[8], gruppert[11], gruppert[14]]

s       = [gruppert[0], gruppert[1], gruppert[2]]
sufq    = [gruppert[3], gruppert[4], gruppert[5]]
t       = [gruppert[6], gruppert[7], gruppert[8]]
tWoff   = [gruppert[9], gruppert[10], gruppert[11]]
tWoffFq = [gruppert[12], gruppert[13], gruppert[14]]
ex_lost_dict = gruppert
#do_it_all_boxsplot(gruppert, "iterations.csv", key="qd_score", key_gruppe="Individ", key_type="Kontroller", title="QD score", output_filename="QD_score_box.svg")


#do_it_all_stdline(ex_lost_dict, "iterations.csv", "qd_score", title="QD_score", scale=True, output_filename="QD_score.svg")
#do_it_all_stdline(ex_lost_dict, "evals.csv", "cont_size", title="Konteiner fylt")



#do_it_all_stdline(miljo, "iterations.csv", "qd_score", title="QD_score", scale=True, output_filename="QD_score_miljo.svg")
do_it_all_boxsplot(miljo, "iterations.csv", key="qd_score", key_gruppe="CubeCount", key_type="CubeSize", title="QD score", output_filename="QD_score_miljo_box.svg")
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