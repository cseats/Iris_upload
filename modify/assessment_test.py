import requests
import os
import argparse
import json
import logging
import math
from pathlib import Path
import pandas as pd
import numpy as np
import datetime

from get_base_asset import get_base_asset_dict
from get_base_asset_risk import risk_dict_init
from get_base_asset_risk import get_cat_dict
from get_base_asset_risk import update_risk_rating_dicts
from get_base_asset_risk import group_risk_dict_init



from api_update_test import remove_asset
from api_update_test import get_headers
import os
import pandas as pd
import requests
from datetime import datetime
from get_base_asset_risk import group_risk_dict_init
import json

prod_bear = "eyJraWQiOiIrTGR0d3l1VFRNNTRBMFc1ZWk3OVJweUdUeG9OWHlHTEFFaThWRUFicFNZPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiMHFGQXJuRm4xRmFUMUpFTXBhR2thZyIsInN1YiI6ImEzZTFhYjIyLTM5M2ItNDZiNi1iM2E0LWFkMDRlMTRjY2M0OCIsImNvZ25pdG86Z3JvdXBzIjpbIkFkbWluIl0sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY3VzdG9tOm9yZ2FuaXphdGlvbl9pZCI6IjQzMzRmNjVmLWQwY2MtNDYyYi04ODk0LWEyYjFkZTc1ZDliNyIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX1hvUFpmMktnUyIsImNvZ25pdG86dXNlcm5hbWUiOiJhcnVwLWF6dXJlLWFkX29iOTNkenpkcjJmNHN0Njlsdm1sMGVfbm8wd3QteGpyaHI5dmktZHJ5ZGUiLCJvcmlnaW5fanRpIjoiZDUxZDFiZDYtMGJlYS00OTMxLThjMzgtNzk1NTI0NDY1YzZlIiwiYXVkIjoiMWh1cWNwbWU4dHFxOWczOWRpNzV1cDNqbmgiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJvQjkzRHp6ZFIyZjRzdDY5TFZNTDBFX25vMHdULXhKcmhSOVZJLWRSeWRFIiwicHJvdmlkZXJOYW1lIjoiYXJ1cC1henVyZS1hZCIsInByb3ZpZGVyVHlwZSI6Ik9JREMiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjU5NzI0MTc5OTI5In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY3NDY2MDIxOSwibmFtZSI6IkNhbXAgU2VhdHMiLCJleHAiOjE2NzY5OTM1NjAsImlhdCI6MTY3Njk4OTk2MCwianRpIjoiYmVlYmExODktYzBkMC00MTM2LWE5YWMtNWVjN2M4M2NlZjRmIiwiZW1haWwiOiJDYW1wLlNlYXRzQGFydXAuY29tIn0.YVvIxYG7o4Uq-m2iEWrmuWRQiY_SQpvJEgKZ76h1nIptitikAfLjusejIEDGtSWSa2qaym82Nrd01-pj_Q7i1BxwH9gZI2CShewr0JAHcZEN7UdEssWjl513A6qTYVA-YhNHbWr3HBro3RKUhTEzUz-WzHHJcH9-yQNN6yJJO2W15r5Mvu4oXGMzPB6KzmXJo9dCGDDPZ1ZdCQfOOXVO2oqUBgqEUbAOTENG_VgWZPsS2FxIm-s_6jp2emcWLEITtuOUwETjJg6kJJEXOg2_kldBnMGzgcuec9Ostp2GzcZmiCH4ek0RpA-450Qf_CgJ8wPdWwozJD1ZPE36ldhcdA"
test_bear = "eyJraWQiOiJpUG1ab3dwNGlvUm9LRFZ2SW9OXC9SdGM4K1dNdXhIT2FmXC82SXlkWFwvVStVPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicmZULUFGSVMwZE9adXhBdTlBVFRWdyIsInN1YiI6IjljZGFhOThlLWQ1NjYtNDk0MS04ZjViLTAyZjU2YWZlYmIxYSIsImNvZ25pdG86Z3JvdXBzIjpbIkFkbWluIl0sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY3VzdG9tOm9yZ2FuaXphdGlvbl9pZCI6ImQ5NWY5YTY2LWVmYWQtNDk4NS1iNzYxLThlZWVjMTYxYTMyYSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX2ZWNFFiR1BhRiIsImNvZ25pdG86dXNlcm5hbWUiOiJhenVyZS1hcnVwLWFkX3VoMndtaWczMWVoNTVkYmFleDFqbnJlY3hobXdhemtqdXg2b2h1ZHZyNnciLCJvcmlnaW5fanRpIjoiODcxMzg4ZTUtN2ZiZC00MWM5LWEwMDUtZDZlNGRkNzlhZjVmIiwiYXVkIjoiNWUzbGtqdm5zNnQ4bXU3NGExdnFvcDVkcDIiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJ1aDJXbWlnMzFlSDU1ZEJBRVgxak5SZWNYSE1XQXpLSnV4Nk9IdWRWUjZ3IiwicHJvdmlkZXJOYW1lIjoiYXp1cmUtYXJ1cC1hZCIsInByb3ZpZGVyVHlwZSI6Ik9JREMiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjU5NzI0MTAxNjQ4In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY1OTcyNDQ0NSwibmFtZSI6IkNhbXAgU2VhdHMiLCJleHAiOjE2NjIxMjc1NDAsImlhdCI6MTY2MjEyMzk0MCwianRpIjoiNjc3NGEzMDAtMTRlYS00YjkyLWIyNWYtOTE2MzI0ODkzODRhIiwiZW1haWwiOiJDYW1wLlNlYXRzQGFydXAuY29tIn0.FIkiV2Ru9LAIVtrt_YjU8Y9Xcd2I69ccuSTsqtMpDh9gdZuaIrXrpOlq4-8RJTfGHn8FgGtTsDkigbqSWwAr5kt19nyU-624RrMCya5FET2_Q96KoI8OcVk1-rcym8H7rFTKgyYDWToR9fnbnaxU8QvEBhPOdaEtPffvP7Crhmh4n4mJ8_WCCoiCMbEK-WbLAxSyAwPCGBZ-lHg8CH_YU4XkEcAIWOofdUImt2szia6rCArcKS8veyabxexOrUwDB4zz2i_8RXrbNK3lMQU_XCJI6EFLM4KpUQq1_37_c-6fhxGmelmHeRKem9u5nn705LVThbRFCFwvUvYm_8cUhg"

header = {'accept': 'application/json', 'authorization': f'Bearer {prod_bear}'}
# dicttest= {
#     "assessment_type": "CURRENT",
#
#     "group_id": "61456c48-5275-4d1f-9f81-ccf114f9e772",
#     "status" : "IN-PROGRESS",
#     "version":1,
#   "display_economic_loss": False,
#   "display_inventory_loss": False,
#   "display_downtime": False,
#   "display_life_safety": True,
#   "display_siteaccess_roads": False,
#   "display_siteaccess_bridges": False,
#   "display_siteaccess_rail": False,
#   "display_utility_power": False,
#   "display_utility_water": False,
#   "display_utility_waste": False,
#   "display_utility_telecom": False,
#   "display_utility_fiber": False,
#   "display_health_and_wellness": False,
#   "display_damage": True,
#   "display_aggregate_life_safety": True,
#   "executive_summary": "Test",
#    "ratings": {
#     "meteorological_tornado": {
#       "negligible": true,
#       "further_analysis_needed": true,
#       "further_analysis_explanation": "Further analysis need to be performed for the following reasons: ....",
#       "assessment_update": "48 months",
#
#       "life_safety": {
#         "confidence": 1.2,
#         "risk_rating": "Medium",
#         "apetite": "neutral",
#         "likelihood": "0.3.1",
# #         "consequence": "1.1"
# #       },
# # "aggregate_life_safety": {
# #         "confidence": 1.2,
# #         "risk_rating": "Medium",
# #         "apetite": "neutral",
# #         "likelihood": "0.3.1",
# #         "consequence": "1.1"
# #       },
# # "damage": {
# #         "confidence": 1.2,
# #         "risk_rating": "Medium",
# #         "apetite": "neutral",
# #         "likelihood": "0.3.1",
# #         "consequence": "1.1"
# #       }
# #     }
# #    }
# # }
# id = "71c7ff98-a344-4fea-834a-927bd64cbb8a"
# # ASSET_URL = "https://asset.dev.iris.arup.com"
ASSET_URL = "https://asset.test.iris.arup.com"
ASSET_URL = "https://asset.iris.arup.com"
# #
# # # hz_URL = "https://hazard.dev.iris.arup.com"
HAZARD_URL = "https://hazard.test.iris.arup.com"
HAZARD_URL = "https://hazard.iris.arup.com"
# #
# #ID: 8227ba94-95bf-40e0-bc4c-1ad8b5f21139
# <Response [200]>
#     ID: db475fd0-9919-4263-b903-23204ff7277b
# <Response [200]>
#     ID: b350cde2-6619-4a31-baf4-8e8aa3b6a993
# <Response [200]>
#     ID: 5541e974-3959-4ce7-afff-a8ece5ce300a
# <Response [200]>
#     ID: ddb2de49-6a5e-49c1-a50e-0f6227e48e67
# <Response [200]>
#     ID: ce8cb26a-2610-43ab-8de1-9d52d64d5bd3
# # #
# #
# # group_risk = group_risk_dict_init()
# # group_risk["group_id"] = "1e4da211-1f92-4002-ad61-3a9c3d2c1a4f"#response.json()["id"]
# # group_risk["ratings"]["meteorological_tornado"]["life_safety"]["risk-rating"] = "Medium"#group_indv_aal[i]
# # group_risk["ratings"]["meteorological_tornado"]["aggregate_life_safety"]["risk-rating"] ="High"# group_agg_aal[i]
# # group_risk["ratings"]["meteorological_tornado"]["damage"]["risk-rating"] = "Low"#group_dam[i]
# #
# #
# # response = requests.post(
# #     f"{HAZARD_URL}/risk-ratings/group",
# #     headers=get_headers(),
# #     data=json.dumps(group_risk)
# # )
# # if response.status_code != 200:
# #       raise Exception(f">> Failed to add: {response.status_code} { response.json()}")
# # else:
# #       print(response)
# # #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # # # file = "20220823_site_details.csv"
# # # # file = "20220824-00-00-00_site_details__ss.csv"
# # # # dir_path = os.path.dirname(os.path.realpath(__file__))
# # # # print(dir_path)
# # # # post_assessment(id,1,2.3,3)
# # # # df= pd.read_excel(os.path.join("C:\Users\camp.seats\OneDrive - Arup\PROJ\Projects\Amazon_T\Scripts Area\_iris_Dev\cs_iris-scripts\cs_iris_Dev\iris-scripts-main\projects\AWS\outputs",file))
# # # # df= pd.read_csv(os.path.join(dir_path,"outputs",file))
# # # #
# # #
# # #
# # #
# # # group_id = "974902af-5780-4d0b-af1f-fff740aa4057"
# # # currentDateAndTime = datetime.now()
# # # # print(currentDateAndTicurrentDateAndTime = datetime.now()me)
# # # # currentTime = currentDateAndTime.strftime("%Y-%m-%d-%H-%M-%S")
# # # # print("The current time is", currentTime)
# # # # time_stamp = date.today().strftime("%H:%M:%S")
# # # # print(time_stamp)
# # # # print(datetime.now())


# INPUT_PATH = "inputs\\eqr_iris_upload_full.xlsx"
# sheet_title = "upload"
# dir_path = os.path.dirname(os.path.realpath(__file__))
# all_sites = all_sites = pd.read_excel(os.path.join(dir_path,INPUT_PATH),sheet_name = sheet_title)
#
# # path = os.path.join(dir_path,"""_site_details-ERASE.csv")
# # Df = pd.read_csv(path)
# #
# # # print(Df["Asset ID"])
# id = all_sites["Iris ID"].tolist()
# # print(id)
#
group_id = "1ac1077d-ff47-4860-8e58-a985548951f7"
# #
# print(f"{ASSET_URL}/groups/{group_id}/assets")
response1 = requests.get(f"{ASSET_URL}/groups/{group_id}/assets",
            headers=header)

# print(response1)

# kill_groups = ["d309a29d-d0bf-4764-b391-5764780328c0"]
# print(response1)
# print(response1)
print(response1.json())
# # #
results = response1.json()
# print(results)
for asset in results["results"]:

# # #     print(asset["id"])
    asset_id =  asset["id"]
    print(asset)
    print(asset_id)
# # #     # response = requests.get(f"{hz_URL}/assessments/?limit=10&asset_id={asset_id}/",
# #     #             headers=get_headers())
# #     # # print(response.json()['detail'])
# #     # print(response.json())
# #     # assess = response.json()
# #     # print(assess["results"])
# #     # print(response.json()["results"]["id"])
    # print(asset["id"])
    # asset_id = asset["id"]

    # remove_asset(asset["id"],ASSET_URL)


# ##_________________________________________________________________
##                  DELETE ASSET
    response = requests.delete(f"{ASSET_URL}/assets/{asset_id}",
            headers=header
        )
    print("tried to delete asset?")
    print(response)
    print(response.json())

    if response.status_code != 200:
        print("could not delete asset")
        print(response.json()['detail'])
        raise Exception(f">> Failed to change risk rating status")
##_________________________________________________________________
#                   Get risk ID
    try:
        response = requests.get(f'{ASSET_URL}/risk-ratings/?ref_id={asset_id}&ref_type=ASSET',headers=header)
        print("______________")
        print(response)
        print(")))))))))))))))")
        # print(response.results)
        print(response.json())
        print("++++++++++++++++++++")
        risk_id = response.json()[0]["id"]
        print(risk_id)
    #
    #
    # ##_________________________________________________________________
    # #               DELETE RISK RATINGS
    #
    #   Unpublish risk ratings
        response = requests.patch(f"{HAZARD_URL}/risk-ratings/{risk_id}/status?status=IN-PROGRESS&version=2",headers=header)
        if response.status_code != 200:
            print(response)
            raise Exception(f">> Failed to change risk rating status")
        else:
            print("Risk rating unpublished")

    #   Delete risk ratings
        response = requests.delete(
                f"https://hazard.iris.arup.com/risk-ratings/{risk_id}?version=2",
                # f"{HAZARD_URL}/risk-ratings/?asset_id={asset}&assement_type=CURRENT&version=0",
                headers=get_headers()
            )
        print(response)
        # print(response.json())
        if response.status_code != 200:
            raise Exception("COULD NOT DELETE RATING")
            print(response.json()['detail'])
    except:
        print("idk didnt work this time")

##_________________________________________________________________
# ##_________________________________________________________________
##                  DELETE ASSET
    response = requests.delete(f"{ASSET_URL}/assets/{asset_id}",
            headers=header
        )
    print("tried to delete asset?")
    print(response)
    print(response.json())

    if response.status_code != 200:
        print("could not delete asset")
        print(response.json()['detail'])
        # raise Exception(f">> Failed to change risk rating status")
# #
# #
# # # for j in df["Iris ID"].tolist():
# # #     print(j)
# # #     # try:
#     # except:
#     #     print(f"the asset {j} has already been removed")


# time_stamp = date.today().strftime("%Y-%m-%d-)
# time_stamp = date.today().strftime("%H%M%S")
#
# print(time_stamp)
# Now = datetime.now()
# print(Now.strftime("%d%m%Y%H%M%S"))
