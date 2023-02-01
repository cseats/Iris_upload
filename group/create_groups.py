import requests
import os
import json
import pandas as pd

def create_groups(auth_dict:dict, all_groups):

  asset_url = auth_dict["asset_url"]
  header = auth_dict["headers"]

  groups = all_groups["group"].tolist()
  group_type = all_groups["group_type"].tolist()
  group_ids = all_groups["group_id"].tolist()
  group_names = all_groups["name"].tolist()

  group_dict = group_dict = dict()
  group_name = []
  group_id = []
  group_des = []
  group_df = []
  group_risk_id = []

  for i in range(len(groups)):
    if groups[i] == groups[i]:
#Create group (CURRENTLY NOT UPDATING GROUPS)
      if group_ids[i] != group_ids[i]:
        print(auth_dict["asset_url"])

        group_dict[groups[i]] = {"name": group_names[i], "description": group_type[i]}
        responseg = requests.post(
            auth_dict["asset_url"]+"/groups",
            headers=header,
            data=json.dumps(group_dict[groups[i]])
        )

        print("posting the group to Iris")
        if responseg.status_code != 200:
            raise Exception(f">> Failed to add: {responseg.status_code} { responseg.json()}")
        else:
            print("    ID: {}".format(responseg.json()["id"]))

        group_df.append([responseg.json()["id"],groups[i],group_type[i],None])
# Update existing group
      else:
        group_dict[groups[i]] = {"name": group_names[i], "description": group_type[i]}

        responseg = requests.patch(
            auth_dict["asset_url"]+f"/groups/{group_ids[i]}",
            headers=auth_dict["headers"],
            data=json.dumps(group_dict[groups[i]])
            )

        print("Updating group")
        if responseg.status_code != 200:
            raise Exception(f">> Failed to add: {responseg.status_code} { responseg.json()}")
        else:
            print("    ID: {}".format(responseg.json()["id"]))

        group_df.append([group_ids[i],groups[i],group_type[i],0])

    df = pd.DataFrame(group_df,columns=["group_id", "group_name", "group_des","group_risk_id"])

  return df
