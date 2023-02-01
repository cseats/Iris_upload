import requests
import os
import json
import pandas as pd
import copy
# from . import get_base_asset
from asset import get_base_asset

def add_asset_to_group(auth_dict,
    iris_id: str,group_id
):
    ASSET_URL = auth_dict["asset_url"]
    add_detail = {
      "added_by": auth_dict["name"]
    }

# ASSIGN TO GROUP
    response = requests.post(
        f"{ASSET_URL}/groups/{group_id}/assets/{iris_id}",
        headers=auth_dict["headers"],
        data=json.dumps(add_detail)
    )

    if response.status_code != 200:
          raise Exception(f">> Failed to add to group")

    return response.json()
#_______________________________________________________________________________


def append_asset2groups(auth_dict,iris_id,city_region,group_dfs):

  group_id = group_dfs["group_name"].tolist()
  for i in range(len(group_id)):
    if group_id[i] == city_region:
      add_asset_to_group(auth_dict,iris_id,group_dfs["group_id"][i])
#_______________________________________________________________________________


def update_asset_dict(asset_id: str,asset_hc: int,
    asset_sqft: float,asset_country: str,asset_type: str,
    asset_address: str,asset_zip: str,asset_city: str,
    asset_state: str,asset_lat: float,asset_lon: float,
    city_region:str, asset_des : str, asset_yoc : str, asset_org,asset_floors,asset_nickname,description
    ):
    # from get_base_asset import get_base_asset_dict
    asset_dict = get_base_asset.get_base_asset_dict()
    # asset_dict = copy.deepcopy(asset_base_dict)

    asset_dict["name"] = asset_id
    asset_dict["nickname"] = asset_nickname
    asset_dict["geo_location"] = [ asset_lat,asset_lon]
    asset_dict["city"] = asset_city
    asset_dict["state"] = asset_state
    asset_dict["country"] = asset_country
    asset_dict["street_address"] = asset_address
    asset_dict["zip_code"] = asset_zip
    asset_dict["total_area"] = asset_sqft
    asset_dict["primary_use"] = [asset_type]
    asset_dict["total_building_population"] = asset_hc
    asset_dict["n_floors"] = None
    asset_dict["business_group"] = asset_org
    asset_dict["occ_area"] = asset_sqft
    asset_dict["description"] = "City Region: "+city_region + ", Building type: "+asset_des
    asset_dict["year_of_construction"] = asset_yoc
    asset_dict["n_floors"] = asset_floors

    asset_dict["description"] = description

    return asset_dict
#_______________________________________________________________________________


def update_asset(auth_dict,
    iris_id: str,
    asset_id: str,
    asset_hc: int,
    asset_sqft: float,
    asset_country: str,
    asset_type: str,
    asset_address: str,
    asset_zip: str,
    asset_city: str,
    asset_state: str,
    asset_lat: float,
    asset_lon: float, city_region:str, asset_des : str, asset_yoc : str,asset_org,asset_floors,asset_nickname,description
):
    ASSET_URL = auth_dict["asset_url"]
    asset_dict = update_asset_dict(asset_id,asset_hc,asset_sqft,asset_country,
    asset_type,asset_address,asset_zip,asset_city, asset_state,asset_lat,
    asset_lon, city_region, asset_des, asset_yoc,asset_org,asset_floors,asset_nickname,description)


    # Create the asset1
    response = requests.post(
        f"{ASSET_URL}/assets/{iris_id}",
        headers=auth_dict["headers"],
        data=json.dumps(asset_dict)
    )

    if response.status_code != 200:
          raise Exception(f">> Failed to update: {response.json()}")
          print(response.json()['detail'])
    else:
          print("    ID: {}".format(response.json()["id"]))

    return response.json()["organization_id"]
#_______________________________________________________________________________


def add_asset(auth_dict,asset_id: str,
        asset_hc: int,
        asset_sqft: int,
        asset_country: str,
        asset_type: str,
        asset_address: str,
        asset_zip: str,
        asset_city: str,
        asset_state: str,
        asset_lat: float,
        asset_lon: float, city_region:str, asset_des : str, asset_yoc : str,asset_org,asset_floors,asset_nickname,description
        ):
    ASSET_URL = auth_dict["asset_url"]
    asset_dict = update_asset_dict(asset_id,asset_hc,asset_sqft,asset_country,
    asset_type,asset_address,asset_zip,asset_city, asset_state,asset_lat,
    asset_lon, city_region, asset_des, asset_yoc,asset_org,asset_floors,asset_nickname,description)

    response = requests.post(
        f"{ASSET_URL}/assets/",
        headers=auth_dict["headers"],
        data=json.dumps(asset_dict))
    if response.status_code != 200:
          raise Exception(f">> Failed to add: {response.status_code} { response.json()}")
    else:
          print("    ID: {}".format(response.json()["id"]))

    return response.json()["id"]
#_______________________________________________________________________________


def iris_asset(all_sites,auth_dict,group_df):

  n_assets = len(all_sites["Ledger"])
  print(" * {} assets in file".format(n_assets))

  # Data columns to be checked
  site_cols = ["Property Name","Ledger","lat","long","City","State","Address",'ZIP','rentable_sqft','number_of_beds','Construction Type','Year Built','Market','Submarket',"Units"]

  for asset_index in range(n_assets):

    asset_type = all_sites["type"][asset_index]
    asset_lat = float(all_sites["lat"][asset_index])
    asset_lon = float(all_sites["long"][asset_index])
    asset_city = all_sites["City"][asset_index]
    asset_state = all_sites["State"][asset_index]
    asset_country = "USA"
    asset_address = all_sites["Address"][asset_index]
    asset_zip = str(all_sites["ZIP"][asset_index])
    asset_sqft = int(all_sites["rentable_sqft"][asset_index])
    asset_hc = int(all_sites["number_of_beds"][asset_index])
    asset_org = str(all_sites["Submarket"][asset_index])
    city_region = all_sites["Market"][asset_index]
    asset_des = all_sites["Construction Type"][asset_index]
    asset_yoc = int(all_sites["Year Built"][asset_index])
    asset_floors = int(all_sites["Units"][asset_index])

    asset_id = str(all_sites["Property Name"][asset_index])
    asset_nickname = str(all_sites["Property Name"][asset_index])
    iris_id = all_sites["Iris ID"][asset_index]
    risk_id = all_sites["Risk ID"][asset_index]
    asset_assess_id =all_sites["Assessment ID"][asset_index]
    description = "Market: "+city_region+" | Submarket: "+asset_org+" | Acquired year: "+str(all_sites["Acquired Year"][asset_index])+" | Construction type: "+asset_des+" | Executive summary: "+all_sites["Executive Summary"][asset_index]#number of buildings

#-------------------------------------------------------------------------------
              #                      Asset attributes
    print("_______________________________________________________________________")
    print("Updating Iris for " + asset_id)
    print(" ")

    if pd.isnull(all_sites["Iris ID"][asset_index]):
      print(" * No Iris ID exists for asset, initializing asset")
      print("  1/3 Creating asset")

      iris_id = add_asset(auth_dict,asset_id,asset_hc,asset_sqft,asset_country,asset_type,asset_address,asset_zip,asset_city,asset_state,asset_lat,asset_lon,city_region,asset_des,asset_yoc,asset_org,asset_floors,asset_nickname,description)

      print("  2/3 Adding asset to group")
      append_asset2groups(iris_id,city_region,group_df)

      print("  3/3 Initializing risk ratings")
      iris_id_str = str(iris_id)
      all_sites.loc[asset_index,"Iris ID"] = iris_id_str

    else:
      print(" * Iris ID exists for asset, {}".format(all_sites["Iris ID"][asset_index]))
      print("  1/2 Updating asset")
      group_id = update_asset(auth_dict,all_sites["Iris ID"][asset_index],asset_id,asset_hc,asset_sqft,asset_country,asset_type,asset_address,asset_zip,asset_city,asset_state,asset_lat,asset_lon,city_region,asset_des,asset_yoc,asset_org,asset_floors,asset_nickname,description)
      append_asset2groups(auth_dict,all_sites["Iris ID"][asset_index],city_region,group_df)

# Add asset to group portfolio
    add_asset_to_group(auth_dict,iris_id,group_df["group_id"][0])
    return all_sites
