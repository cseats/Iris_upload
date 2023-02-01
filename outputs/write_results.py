import datetime
import os
import pandas as pd

def write_results(dir_path,all_sites,OUTPUT_FOLDER):

    Now = datetime.datetime.now()
    now_str=Now.strftime("%d%m%Y%H%M%S")
    os.mkdir(os.path.join(dir_path,"outputs","results",now_str))
    file_name =  "_site_details.csv"
    print_path = os.path.join(dir_path, OUTPUT_FOLDER,"results",now_str, file_name)
    print(print_path)
    all_sites.to_csv(path_or_buf=print_path)
