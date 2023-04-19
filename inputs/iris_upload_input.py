import requests
import os
import pandas as pd
def iris_upload_input(INPUT_PATH,dir_path, asset_sheet,group_sheet,risk_rating_sheet,hazard_name):

    all_sites = all_sites = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = asset_sheet,engine="openpyxl")

    all_groups = all_groups = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = group_sheet,engine='openpyxl')

    all_risks = all_risks = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = risk_rating_sheet,engine='openpyxl')
    risk_rating_dict = {}   

    t = all_risks["Flood"][0]
    time_hor = all_risks["Time Horizon"].tolist()
    hazards = hazard_name.keys()

    for i in range(len(time_hor)):

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
                        con_dict["summary"] = h + " Executive Summary "+str(int(all_risks["Time Horizon"][i]))
                
                    risk_haz[hazard_name[h]]=con_dict

        risk_rating_dict[str(int(all_risks["Time Horizon"][i]))] = {"RCP":all_risks["Scenario"][i],"risk_ratings":risk_haz}
    print(risk_rating_dict)

    for x in risk_rating_dict:
        print(x)

    return all_sites, all_groups, risk_rating_dict
