# this script is used to upload assets to the Iris platform from CSV input using
# Requests to access the REST API
import requests
import os
import argparse
import json
import logging
import math
from pathlib import Path
import pandas as pd
import numpy as np
import sys
import copy
import dotenv


from authentication import get_auth
from group import *
from inputs import iris_upload_input
from outputs import write_results
from asset import *

print(pd.__version__)

if __name__ == "__main__":
    print("starting upload")
    group_update = True
    group_risk_rating = False
    group_risk_quant = False

    asset_update = True
    asset_risk_rating = True
    asset_risk_quant = False

    write_Results = True
    OUTPUT_FOLDER = "outputs"


#_______________________________________________________________________________
# Determine which environment we are going to use (test/prod/dev)
    print(os.getcwd())
    env = "test" #(test,prod,dev)
    env = "prod"
    # env = "dev"

    ASSET_URL,HAZARD_URL,header = get_auth.get_auth(env,os.getcwd())
    auth_dict= {"asset_url": ASSET_URL,
                "hazard_url": HAZARD_URL,
                "headers": header,
                "name": "Camp Seats"
    }
    print("Authentification: ", auth_dict)
    print("Uploading to "+env+" environment")
    print(auth_dict["asset_url"])
#_______________________________________________________________________________
# Fxn to bring in upload csv (select file if time)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    INPUT_PATH = "inputs\\eqr_iris_upload_full.xlsx"
    INPUT_PATH = "inputs\\AllSites_scripted_04132023.xlsx"
    asset_sheet = "upload"
    asset_sheet = "2.1 to_iris"
    group_sheet = "groups"
    risk_rating_sheet = "2.2 iris_scenarios"

    #Hazards to be condsidered in data upload
    hazard_name = {
                    "Wildfire":"climatological_wildfire",
                    "Seismic":"geophysical_seismic",
                    "Extreme Heat": "climatological_extreme_heat",
                    "Flood":"hydrological_flooding",
                    "Drought":"climatological_drought"
                    }


    all_sites, all_groups, risk_rating_dict = iris_upload_input.iris_upload_input(INPUT_PATH,dir_path,asset_sheet,group_sheet,risk_rating_sheet,hazard_name)

    print("________________________________________________")
    print(all_sites)
    print("________________________________________________")
#_______________________________________________________________________________
# Add or update Groups
    if group_update:
        group_df = create_groups.create_groups(auth_dict,all_groups)


        print("Writing group results...\n")
        file_name =  "_group_data.csv"
        write_results.write_results(dir_path,group_df,OUTPUT_FOLDER,file_name)
        print("Results written.\n")
#_______________________________________________________________________________
# Add or update Group risk rating
    if group_risk_rating:
        #dictionary calling out the GROUOP hazards their consequences and the csv headers of the consequence risk ratings
        group_hazard_conseq = {"geophysical_seismic":[{"economic_loss":None}],
                               "climatological_wildfire":[{"economic_loss":None}],
                               "hydrological_stormwater_flooding":[{"economic_loss":None}],
                               "hydrological_riverine_flooding":[{"economic_loss":None}],
                               "hydrological_coastal_flooding_and_sea_level_rise":[{"economic_loss":None}],
                               "climatological_extreme_heat":[{"economic_loss":None}]
                              }

# Add or update assets in xlsx
    if asset_update:
        # asset_base_dict = get_base_asset.get_base_asset_dict()
        print("Uploading/updating assets...\n")
        risk_len = len(list(risk_rating_dict.keys()))
        all_sites = iris_asset.iris_asset(all_sites,auth_dict,group_df)
        print("Assets updated.\n")
        print("************************")
        print(all_sites)
# Add or update asset risk ratings (specify if quantitative ratings are wanted)
    if asset_risk_rating:
        #dictionary calling out the GROUOP hazards their consequences and the csv headers of the consequence risk ratings
        c = 0
        for y in risk_rating_dict:
            c+=1
            print("************************")
            print("Starting the next assessment post\n")
            if risk_rating_dict[y]["RCP"] == "Current":

                assessment_type = {"version":1,"assessment_type": "CURRENT","year":str(y)}

            else:
                assessment_type = {"version":1,  "rcp_scenario": str(risk_rating_dict[y]["RCP"]),"time_horizon": str(y),"assessment_type": "FUTURE","year":str(y)}

            # assessment_type = {"version":c,  "rcp_scenario": "8.5","time_horizon": str(y),"assessment_type": "FUTURE"}

            print("Uploading/updating asset risk ratings...\n")
            asset_hazard_conseq = {"geophysical_seismic":[{"economic_loss":"Seismic Risk"}],
                                   "climatological_wildfire":[{"economic_loss":"Wildfire Risk"}],
                                   "hydrological_stormwater_flooding":[{"economic_loss":"Flood Risk"}],
                                   "hydrological_riverine_flooding":[{"economic_loss":"Flood Risk"}],
                                   "hydrological_coastal_flooding_and_sea_level_rise":[{"economic_loss":"Flood Risk"}],
                                   "climatological_extreme_heat":[{"economic_loss":"Extreme Heat Risk"}]}



           
            _risk_key = "Risk ID "+str(c)

            all_sites = asset_risk.asset_risk(all_sites,risk_rating_dict[y]["risk_ratings"],auth_dict,assessment_type,_risk_key)

#_______________________________________________________________________________



        print("Risk ratings updated.\n")
# write results
    if write_Results:
        print("Writing results...\n")
        file_name =  "_site_details.csv"
        write_results.write_results(dir_path,all_sites,OUTPUT_FOLDER,file_name)
        print("Results written.\n")
