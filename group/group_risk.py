def group_risk():

    asset_url = auth_dict["asset_url"]
    hazard_url = auth_dict["hazard_url"]
    header = auth_dict["headers"]

    groups = all_groups["group"].tolist()
    group_type = all_groups["group_type"].tolist()
    group_ids = all_groups["group_id"].tolist()
    group_names = all_groups["name"].tolist()
      
    for i in range(len(groups)):
        group_risk = group_risk_dict_init()
        group_risk["group_id"] = group_ids[i]
