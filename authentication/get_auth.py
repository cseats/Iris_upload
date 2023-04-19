# from dotenv import load_dotenv
import dotenv
from dotenv import load_dotenv
import os



def get_auth(env,dir_path):
    print("In authentication...\n")
    load_dotenv()
    if env == "test":
        _bearer = os.getenv("iris_test_auth")
        print("Bearer found! \n")
        ASSET_URL = "https://asset.test.iris.arup.com"
        HAZARD_URL = "https://hazard.test.iris.arup.com"

    elif env == "prod":
        _bearer = os.getenv("iris_prod_auth")
        print("Bearer found! \n")
        ASSET_URL = "https://asset.iris.arup.com"
        HAZARD_URL = "https://hazard.iris.arup.com"


    # ASSET_URL = "https://asset.test.iris.arup.com"
    # HAZARD_URL = "https://hazard.test.iris.arup.com"
    header = {'accept': 'application/json', 'authorization': f'Bearer {_bearer}'}
    return ASSET_URL,HAZARD_URL,header
