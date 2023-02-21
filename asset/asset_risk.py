#functions containted to update/create the risk ratings of assets
import json
import requests
import pandas as pd
import copy

from asset import get_base_asset_risk

def asset_risk_post(base_risk_dict,auth_dict,all_sites,asset_indx,_risk_key,version_):
    print("")
    HAZARD_URL = auth_dict["hazard_url"]
    print(all_sites[_risk_key][asset_indx])
    print(base_risk_dict)
    print("____________________________________________")
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
        print("This is the risk key "+_risk_key)
        risk_id = all_sites[_risk_key][asset_indx]

        print(f"Risk rating exists, updating existing risk rating for asset...\n")
        print("Unpublishing exsiting rating...\n")
        print("Risk rating version "+str(version_))
# UNPUBLISH risk rating
        response = requests.patch(f"{HAZARD_URL}/risk-ratings/{risk_id}/status?status=IN-PROGRESS&version={1}",headers=auth_dict["headers"])
        if response.status_code != 200:
            print(response)
            # print(response.json())
            raise Exception(f">> Failed to change risk rating status")
        else:
            print("")
            print("Existing rating has been unpublished!\n")
            print("Updating risk rating...\n")
# Update risk rating
        response = requests.patch(
          f"{HAZARD_URL}/risk-ratings/{risk_id}?version={1}",
          headers=auth_dict["headers"],
          data=json.dumps(base_risk_dict))

        if response.status_code != 200:
            print("")
            print(response)
            print(response.json()['detail'])
            raise Exception(f">> Failed to UPDATE risk ratings")
        else:
            print("Risk rating has been updated and published!\n")

# PUBLISH risk rating
        response_ = requests.patch(f"{HAZARD_URL}/risk-ratings/{risk_id}/status?status=PUBLISHED&version={1}",headers=auth_dict["headers"])
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
            print(haz)
            print(asset_hazard_conseq)
            print(all_sites[asset_hazard_conseq[haz]["haz_name"]][asset_indx])
            # print(_o)
            haz_dict[haz]={
            "negligible": True,
            "further_analysis_needed": False,
            "further_analysis_explanation": None,
            "assessment_update": None,
            "hazard_source": "MunichRe",
            "hazard_rating": {
                "confidence": 0,
                "risk_rating": all_sites[asset_hazard_conseq[haz]["haz_name"]][asset_indx],
                "apetite": "",
                "likelihood": "",
                "consequence": ""
      }}

            for consq in asset_hazard_conseq[haz]:

                data_frame_key = asset_hazard_conseq[haz][consq]  #[list(consq.keys())[0]]
                print("Hazard: "+haz+"  | Consequence: "+consq+"  | Rating: "+all_sites[data_frame_key][asset_indx])
                haz_dict[haz][consq] = {
                                            "confidence": 0,
                                            "risk_rating": all_sites[data_frame_key][asset_indx],
                                            "apetite": "",
                                            "likelihood": "",
                                            "consequence": ""}

        base_risk_dict["ratings"] = haz_dict
        base_risk_dict["asset_id"] = all_sites["Iris ID"][asset_indx]
        base_risk_dict["ref_id"] = all_sites["Iris ID"][asset_indx]

        if assessment_type["assessment_type"] == "CURRENT":


            base_risk_dict["name"] = assessment_type["assessment_type"] + " Scenario"
        else:
            base_risk_dict["name"] = assessment_type["assessment_type"] + " Scenario RCP"+assessment_type["rcp_scenario"]+" "+ assessment_type["time_horizon"]


        for keys in list(assessment_type.keys()):
            base_risk_dict[keys] = assessment_type[keys]

        version_ = assessment_type["version"]
        all_sites[_risk_key][asset_indx] = asset_risk_post(base_risk_dict,auth_dict,all_sites,asset_indx,_risk_key,version_)
        print(" ")

    return all_sites
