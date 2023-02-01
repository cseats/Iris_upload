#functions containted to update/create the risk ratings of assets
import json
import requests
import pandas as pd
import copy

from asset import get_base_asset_risk

def asset_risk_post(base_risk_dict,auth_dict,all_sites,asset_indx,_risk_key,version_):
    print("")
    HAZARD_URL = auth_dict["hazard_url"]

    if all_sites[_risk_key][asset_indx] != all_sites[_risk_key][asset_indx]: #if there is no risk rating
      print(f"Risk rating has not been created yet, adding rating now...")
      response = requests.post(
          f"{HAZARD_URL}/risk-ratings/",
          headers=auth_dict["headers"],
          data=json.dumps(base_risk_dict))

      if response.status_code != 200:
            print(response)
            print(response.json())
            raise Exception(f">> Failed to add risk ratings")
      else:
            print("")
            print("Risk rating has been posted!")

    else:
        iris_id = base_risk_dict["asset_id"]
        risk_id = all_sites[_risk_key][asset_indx]

        print(f"Risk rating exists, updating existing risk rating for asset...\n")
        print("Unpublishing exsiting rating...\n")
# UNPUBLISH risk rating
        response = requests.patch(f"{HAZARD_URL}/risk-ratings/{risk_id}/status?status=IN-PROGRESS&version={version_}",headers=auth_dict["headers"])
        if response.status_code != 200:
            print(response)
            raise Exception(f">> Failed to change risk rating status")
        else:
            print("")
            print("Existing rating has been unpublished!\n")
            print("Updating risk rating...\n")
# Update risk rating
        response = requests.patch(
          f"{HAZARD_URL}/risk-ratings/{risk_id}?version={version_}",
          headers=auth_dict["headers"],
          data=json.dumps(base_risk_dict))

        if response.status_code != 200:
            print("")
            print(response.json()['detail'])
            raise Exception(f">> Failed to UPDATE risk ratings")
        else:
            print("Risk rating has been updated and published!\n")

# PUBLISH risk rating
        response_ = requests.patch(f"{HAZARD_URL}/risk-ratings/{risk_id}/status?status=PUBLISHED&version={version_}",headers=auth_dict["headers"])
        if response_.status_code != 200:
            print(response_)
            raise Exception(f">> Failed to change risk rating status")
        else:
            print("")
            print("Existing rating has been unpublished!\n")
            print("Updating risk rating...\n")
    return response.json()["id"]




def asset_risk(all_sites,asset_hazard_conseq,auth_dict,assessment_type,_risk_key):

    for asset_indx in range(len(all_sites[_risk_key])):
        base_risk_dict = copy.deepcopy(get_base_asset_risk.risk_dict_base())
        haz_dict = dict()
        print("________________________________________________________________")
        print(" ")
        print("Posting risk rating for  "+str(all_sites["Property Name"][asset_indx])+ " , IRIS ID:"+ str(all_sites["Iris ID"][asset_indx])+",  Risk ID : "+str(all_sites[_risk_key][asset_indx]))
        print(" ")

        for haz in asset_hazard_conseq.keys():
            haz_dict[haz]={
            "negligible": True,
            "further_analysis_needed": False,
            "further_analysis_explanation": None,
            "assessment_update": None}

            for consq in asset_hazard_conseq[haz]:

                data_frame_key = consq[list(consq.keys())[0]]
                print("Hazard: "+haz+"  | Consequence: "+list(consq.keys())[0]+"  | Rating: "+all_sites[data_frame_key][asset_indx])
                haz_dict[haz][list(consq.keys())[0]] = {
                                            "confidence": 1.2,
                                            "risk_rating": all_sites[data_frame_key][asset_indx],
                                            "apetite": "neutral",
                                            "likelihood": "0.3.1",
                                            "consequence": "1.1"}

        base_risk_dict["ratings"] = haz_dict
        base_risk_dict["asset_id"] = all_sites["Iris ID"][asset_indx]
        base_risk_dict["ref_id"] = all_sites["Iris ID"][asset_indx]

        for keys in list(assessment_type.keys()):
            base_risk_dict[keys] = assessment_type[keys]
        version_ = assessment_type["version"]
        all_sites[_risk_key][asset_indx] = asset_risk_post(base_risk_dict,auth_dict,all_sites,asset_indx,_risk_key,version_)
        print(" ")

    return all_sites
