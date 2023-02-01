import requests
import os
import pandas as pd
def iris_upload_input(INPUT_PATH,dir_path, asset_sheet,group_sheet):

    all_sites = all_sites = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = asset_sheet,engine="openpyxl")

    all_groups = all_groups = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = group_sheet,engine='openpyxl')

    return all_sites, all_groups
