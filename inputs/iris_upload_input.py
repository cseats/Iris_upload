import requests
import os
import pandas as pd
def iris_upload_input(INPUT_PATH,dir_path, asset_sheet,group_sheet,risk_rating_sheet):

    all_sites = all_sites = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = asset_sheet,engine="openpyxl")

    all_groups = all_groups = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = group_sheet,engine='openpyxl')

    all_risks = all_risks = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = risk_rating_sheet,engine='openpyxl')
    risk_rating_dict = {}
    hazard_name = {"Flood":"hydrological_riverine_flooding",
                    "Wildfire":"climatological_wildfire",
                    "Seismic":"geophysical_seismic"}
    print(list(all_risks.columns))
    print(len(list(all_risks.columns)))
    haz_num = len(list(all_risks.columns))
    print(all_risks["Wildfire"][1])
    print(all_risks["Seismic"][1])
    print(all_risks)
    print(all_risks["Seismic"][0])
    t = all_risks["Flood"][0]
    print(t[0])
    print(t[-1])
    print(list(t.split(",")))
    print(all_risks["Time Horizon"].tolist())
    time_hor = all_risks["Time Horizon"].tolist()
    hazards = hazard_name.keys()
    print(hazards)

    if all_risks["Wildfire"][1]==all_risks["Wildfire"][1]:
        print("evil plan works bb")
    for i in range(len(time_hor)):
        # risk_rating_dict[i]
        risk_haz = {}
        for h in hazards:
            con_dict = {}
            if True:
                # risk_name = h+"_consequence"

                haz_consq = all_risks[h][i]
                if haz_consq==haz_consq:
                    haz_consq = list(all_risks[h][i].split(","))
                    for c in haz_consq:
                        con_dict[c] = h+" Risk "+str(int(all_risks["Time Horizon"][i]))
                        con_dict["haz_name"] = h+" Hazard "+str(int(all_risks["Time Horizon"][i]))
                    # print(all_risks[i][hazards[h]])
                    risk_haz[hazard_name[h]]=con_dict

        risk_rating_dict[str(int(all_risks["Time Horizon"][i]))] = {"RCP":all_risks["Scenario"][i],"risk_ratings":risk_haz}
    print(risk_rating_dict)







    print(risk_rating_dict)

    for x in risk_rating_dict:
        print(x)

    return all_sites, all_groups, risk_rating_dict
