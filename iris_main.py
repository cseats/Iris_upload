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


from authentication import *
from group import *
from inputs import *
from outputs import *
from asset import *

print(pd.__version__)
# import venv
# from asset import get_base_asset

# global pd,np

# # import authentication as auth
# import group
# import inputs
# import outputs

# print("starting upload")
# print(__name__)
if __name__ == "__main__":
    print("starting upload")
    group_update = True
    group_risk_rating = False
    group_risk_quant = False

    asset_update = False
    asset_risk_rating = False
    asset_risk_quant = False

    write_Results = False
    OUTPUT_FOLDER = "outputs"


#_______________________________________________________________________________
# Determine which environment we are going to use (test/prod/dev)
    print(os.getcwd())
    env = "test" #(test,prod,dev)
    # env = "prod"
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
    asset_sheet = "upload"
    group_sheet = "groups"
    all_sites, all_groups = iris_upload_input.iris_upload_input(INPUT_PATH,dir_path,asset_sheet,group_sheet)

#_______________________________________________________________________________
# Add or update Groups
    if group_update:
        group_df = create_groups.create_groups(auth_dict,all_groups)

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
        all_sites = iris_asset.iris_asset(all_sites,auth_dict,group_df)
        print("Assets updated.\n")
# Add or update asset risk ratings (specify if quantitative ratings are wanted)
    if asset_risk_rating:
        #dictionary calling out the GROUOP hazards their consequences and the csv headers of the consequence risk ratings
        print("Uploading/updating asset risk ratings...\n")
        asset_hazard_conseq = {"geophysical_seismic":[{"economic_loss":"Seismic Risk"}],
                               "climatological_wildfire":[{"economic_loss":"Wildfire Risk"}],
                               "hydrological_stormwater_flooding":[{"economic_loss":"Flood Risk"}],
                               "hydrological_riverine_flooding":[{"economic_loss":"Flood Risk"}],
                               "hydrological_coastal_flooding_and_sea_level_rise":[{"economic_loss":"Flood Risk"}],
                               "climatological_extreme_heat":[{"economic_loss":"Extreme Heat Risk"}]}

        assessment_type = {"version":1,  "rcp_scenario": "8.5","time_horizon": "2100","assessment_type": "FUTURE"}
        _risk_key = "Risk ID 1"
        all_sites = asset_risk.asset_risk(all_sites,asset_hazard_conseq,auth_dict,assessment_type,_risk_key)

#_______________________________________________________________________________

        asset_hazard_conseq = {"geophysical_seismic":[{"economic_loss":"Seismic Risk"}],
                               "climatological_wildfire":[{"economic_loss":"Wildfire Risk"}],
                               "hydrological_stormwater_flooding":[{"economic_loss":"Flood Risk"}],
                               "hydrological_riverine_flooding":[{"economic_loss":"Flood Risk"}],
                               "hydrological_coastal_flooding_and_sea_level_rise":[{"economic_loss":"Flood Risk"}],
                               "climatological_extreme_heat":[{"economic_loss":"Extreme Heat Risk"}]}

        assessment_type = {"version":2,"assessment_type": "CURRENT"}
        _risk_key = "Risk ID 2"
        all_sites = asset_risk.asset_risk(all_sites,asset_hazard_conseq,auth_dict,assessment_type,_risk_key)


        print("Risk ratings updated.\n")
# write results
    if write_Results:
        print("Writing results...\n")
        write_results.write_results(dir_path,all_sites,OUTPUT_FOLDER)
        print("Results written.\n")
