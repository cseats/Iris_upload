def get_cat_dict():
  cat_dict = {
  # '1' : "Very Low",
  '1' : "Low",
  # "3" : "Low-Medium",
  "2" : "Medium",
  # "5" : "Medium-High",
  "3" : "High",
  # "7" : "High-Very High",
  # "8" : "Very High",
  # "9" : "Catastrophic"
  }
  return cat_dict


def group_risk_dict_init():

    group_risk_dict = {
        "assessment_type": "CURRENT",
        "group_id": "d74f4e5d-1c71-4e8d-b5e4-994d41114460",
        "status": "PUBLISHED",
        "version":1,
  "display_economic_loss": False,
  "display_inventory_loss": False,
  "display_downtime": False,
  "display_life_safety": True,
  "display_siteaccess_roads": False,
  "display_siteaccess_bridges": False,
  "display_siteaccess_rail": False,
  "display_utility_power": False,
  "display_utility_water": False,
  "display_utility_waste": False,
  "display_utility_telecom": False,
  "display_utility_fiber": False,
  "display_health_and_wellness": False,
  "display_damage": True,
  "display_aggregate_life_safety": True,

 "executive_summary": "Test executive summary",
  "ratings": {
    "meteorological_tornado": {
      "negligible": True,
      "further_analysis_needed": False,
      "further_analysis_explanation": "Further analysis need to be performed for the following reasons: ....",
      "assessment_update": "48 months",

      "life_safety": {
        "confidence": 1.2,
        "risk_rating": "Medium",
        "apetite": "neutral",
        "likelihood": "0.3.1",
        "consequence": "1.1"
      },
"aggregate_life_safety": {
        "confidence": 1.2,
        "risk_rating": "Medium",
        "apetite": "neutral",
        "likelihood": "0.3.1",
        "consequence": "1.1"
      },
"damage": {
        "confidence": 1.2,
        "risk_rating": "Medium",
        "apetite": "neutral",
        "likelihood": "0.3.1",
        "consequence": "1.1"
      }
    },
        "geophysical_seismic": {
          "negligible": True,
          "further_analysis_needed": False,
          "further_analysis_explanation": "Analysis type has not been performed",
          "assessment_update": None,

          "life_safety": {
            "confidence": 1.2,
            "risk_rating": "Not Assessed",
            "apetite": "neutral",
            "likelihood": "0.3.1",
            "consequence": "1.1"
          },
    "aggregate_life_safety": {
            "confidence": 1.2,
            "risk_rating": "Not Assessed",
            "apetite": "neutral",
            "likelihood": "0.3.1",
            "consequence": "1.1"
          },
    "damage": {
            "confidence": 1.2,
            "risk_rating": "Not Assessed",
            "apetite": "neutral",
            "likelihood": "0.3.1",
            "consequence": "1.1"
          }
        },
                "climatological_wildfire": {
                  "negligible": True,
                  "further_analysis_needed": False,
                  "further_analysis_explanation": "Analysis type has not been performed",
                  "assessment_update": None,

                  "life_safety": {
                    "confidence": 1.2,
                    "risk_rating": "Not Assessed",
                    "apetite": "neutral",
                    "likelihood": "0.3.1",
                    "consequence": "1.1"
                  },
            "aggregate_life_safety": {
                    "confidence": 1.2,
                    "risk_rating": "Not Assessed",
                    "apetite": "neutral",
                    "likelihood": "0.3.1",
                    "consequence": "1.1"
                  },
            "damage": {
                    "confidence": 1.2,
                    "risk_rating": "Not Assessed",
                    "apetite": "neutral",
                    "likelihood": "0.3.1",
                    "consequence": "1.1"
                  }
                }
              }


}

    return group_risk_dict

def risk_dict_init():

    risk_dict = {
  "display_economic_loss": True,
  "display_inventory_loss": False,
  "display_downtime": False,
  "display_life_safety": True,
  "display_siteaccess_roads": False,
  "display_siteaccess_bridges": False,
  "display_siteaccess_rail": False,
  "display_utility_power": False,
  "display_utility_water": False,
  "display_utility_waste": False,
  "display_utility_telecom": False,
  "display_utility_fiber": False,
  "display_health_and_wellness": False,
  "display_damage": False,
  "display_aggregate_life_safety": False,

 "executive_summary": "Test executive summary",
  "ratings": {

        "geophysical_seismic": {
          "negligible": True,
          "further_analysis_needed": False,
          "further_analysis_explanation": None,
          "assessment_update": None,

              "economic_loss": {
                "confidence": 1.2,
                "risk_rating": "Not Assessed",
                "apetite": "neutral",
                "likelihood": "0.3.1",
                "consequence": "1.1"}
        },

          "climatological_wildfire": {
            "negligible": True,
            "further_analysis_needed": False,
            "further_analysis_explanation": None,
            "assessment_update": None,

                "economic_loss": {
                  "confidence": 1.2,
                  "risk_rating": "Not Assessed",
                  "apetite": "neutral",
                  "likelihood": "0.3.1",
                  "consequence": "1.1"}

          },

            "hydrological_stormwater_flooding": {
              "negligible": True,
              "further_analysis_needed": False,
              "further_analysis_explanation": None,
              "assessment_update": None,

                  "economic_loss": {
                    "confidence": 1.2,
                    "risk_rating": "Medium",
                    "apetite": "neutral",
                    "likelihood": "0.3.1",
                    "consequence": "1.1"}
                },

              "hydrological_riverine_flooding": {
                "negligible": True,
                "further_analysis_needed": False,
                "further_analysis_explanation": None,
                "assessment_update": None,

                    "economic_loss": {
                      "confidence": 1.2,
                      "risk_rating": "Medium",
                      "apetite": "neutral",
                      "likelihood": "0.3.1",
                      "consequence": "1.1"}
                },

                "hydrological_coastal_flooding_and_sea_level_rise": {
                  "negligible": True,
                  "further_analysis_needed": False,
                  "further_analysis_explanation": None,
                  "assessment_update": None,

                      "economic_loss": {
                        "confidence": 1.2,
                        "risk_rating": "Medium",
                        "apetite": "neutral",
                        "likelihood": "0.3.1",
                        "consequence": "1.1"}
                  },
                  "climatological_extreme_heat": {
                    "negligible": True,
                    "further_analysis_needed": False,
                    "further_analysis_explanation": None,
                    "assessment_update": None,

                        "economic_loss": {
                          "confidence": 1.2,
                          "risk_rating": "Medium",
                          "apetite": "neutral",
                          "likelihood": "0.3.1",
                          "consequence": "1.1"}
                    }
    },

    "assessment_type": "CURRENT",
    "asset_id": "d74f4e5d-1c71-4e8d-b5e4-994d41114460",
    "status": "PUBLISHED",
    "version":1}
    print(risk_dict)
    return risk_dict



def risk_dict_base():
  risk_dict = {
      "display_economic_loss": True,
      "display_inventory_loss": False,
      "display_downtime": False,
      "display_life_safety": False,
      "display_siteaccess_roads": False,
      "display_siteaccess_bridges": False,
      "display_siteaccess_rail": False,
      "display_utility_power": False,
      "display_utility_water": False,
      "display_utility_waste": False,
      "display_utility_telecom": False,
      "display_utility_fiber": False,
      "display_health_and_wellness": False,
      "display_damage": False,
      "display_aggregate_life_safety": False,
      "executive_summary": "Test executive summary",
      "assessment_type": "CURRENT",
      "asset_id": "d74f4e5d-1c71-4e8d-b5e4-994d41114460",
      "status": "PUBLISHED",
      "version":1,
      "ref_id": "string",
      "ref_type": "ASSET"}
  # print(risk_dict)
  return risk_dict
