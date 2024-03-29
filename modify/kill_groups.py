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

import os
import pandas as pd
import requests
from datetime import datetime
import json

prod_bear = "eyJraWQiOiIrTGR0d3l1VFRNNTRBMFc1ZWk3OVJweUdUeG9OWHlHTEFFaThWRUFicFNZPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiYW50N0VvdkVDTGpSSHFrRW85RUF0ZyIsInN1YiI6ImEzZTFhYjIyLTM5M2ItNDZiNi1iM2E0LWFkMDRlMTRjY2M0OCIsImNvZ25pdG86Z3JvdXBzIjpbIkFkbWluIl0sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY3VzdG9tOm9yZ2FuaXphdGlvbl9pZCI6IjQzMzRmNjVmLWQwY2MtNDYyYi04ODk0LWEyYjFkZTc1ZDliNyIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX1hvUFpmMktnUyIsImNvZ25pdG86dXNlcm5hbWUiOiJhcnVwLWF6dXJlLWFkX29iOTNkenpkcjJmNHN0Njlsdm1sMGVfbm8wd3QteGpyaHI5dmktZHJ5ZGUiLCJvcmlnaW5fanRpIjoiYmM4OGE0M2UtMDQ4Yy00OGJlLTlkNmYtMzc5YTdiYTc3YTg5IiwiYXVkIjoiMWh1cWNwbWU4dHFxOWczOWRpNzV1cDNqbmgiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJvQjkzRHp6ZFIyZjRzdDY5TFZNTDBFX25vMHdULXhKcmhSOVZJLWRSeWRFIiwicHJvdmlkZXJOYW1lIjoiYXJ1cC1henVyZS1hZCIsInByb3ZpZGVyVHlwZSI6Ik9JREMiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjU5NzI0MTc5OTI5In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY4MTczODQyMywibmFtZSI6IkNhbXAgU2VhdHMiLCJleHAiOjE2ODE3NDYxMjEsImlhdCI6MTY4MTc0MjUyMSwianRpIjoiYjY5MjFmZDctNGQ0NS00YmY5LWI1MzAtN2MwNTVlMzFmZWJlIiwiZW1haWwiOiJDYW1wLlNlYXRzQGFydXAuY29tIn0.LtTpqrfs97vRxalJZZ0RD8vE6ZxxvOBtlROW6AaBqqdHE6yuuQOsxEoFG8UPfnIVH2cQVyAUqR8bYICkIrcDyT_-OGAKmVbJJ6kJv-Zi7yk5bfd2PjbCxv02UOlVY4DBTv0-BUzvVodhQd8oHUqv0kFCDL5mc2dmm1PVzM0paNKIssUdw56pAXHKBXxMF98e9x4RrcCbfJxb9la4xJy2rkWRCqfMCDzQfyc30fGU_fZ_5aelN2lF_bEytiLx1lURs9tuL_nMtu0TQ3_yJMljg2P8H3fhFPh_t7GGlZ1Wzc8XJ2w3pcZd9pB4USVNNI5Z1mlr_iRj1uYISd5ilN4eGg"
test_bear = "eyJraWQiOiJpUG1ab3dwNGlvUm9LRFZ2SW9OXC9SdGM4K1dNdXhIT2FmXC82SXlkWFwvVStVPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicmZULUFGSVMwZE9adXhBdTlBVFRWdyIsInN1YiI6IjljZGFhOThlLWQ1NjYtNDk0MS04ZjViLTAyZjU2YWZlYmIxYSIsImNvZ25pdG86Z3JvdXBzIjpbIkFkbWluIl0sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY3VzdG9tOm9yZ2FuaXphdGlvbl9pZCI6ImQ5NWY5YTY2LWVmYWQtNDk4NS1iNzYxLThlZWVjMTYxYTMyYSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX2ZWNFFiR1BhRiIsImNvZ25pdG86dXNlcm5hbWUiOiJhenVyZS1hcnVwLWFkX3VoMndtaWczMWVoNTVkYmFleDFqbnJlY3hobXdhemtqdXg2b2h1ZHZyNnciLCJvcmlnaW5fanRpIjoiODcxMzg4ZTUtN2ZiZC00MWM5LWEwMDUtZDZlNGRkNzlhZjVmIiwiYXVkIjoiNWUzbGtqdm5zNnQ4bXU3NGExdnFvcDVkcDIiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJ1aDJXbWlnMzFlSDU1ZEJBRVgxak5SZWNYSE1XQXpLSnV4Nk9IdWRWUjZ3IiwicHJvdmlkZXJOYW1lIjoiYXp1cmUtYXJ1cC1hZCIsInByb3ZpZGVyVHlwZSI6Ik9JREMiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNjU5NzI0MTAxNjQ4In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY1OTcyNDQ0NSwibmFtZSI6IkNhbXAgU2VhdHMiLCJleHAiOjE2NjIxMjc1NDAsImlhdCI6MTY2MjEyMzk0MCwianRpIjoiNjc3NGEzMDAtMTRlYS00YjkyLWIyNWYtOTE2MzI0ODkzODRhIiwiZW1haWwiOiJDYW1wLlNlYXRzQGFydXAuY29tIn0.FIkiV2Ru9LAIVtrt_YjU8Y9Xcd2I69ccuSTsqtMpDh9gdZuaIrXrpOlq4-8RJTfGHn8FgGtTsDkigbqSWwAr5kt19nyU-624RrMCya5FET2_Q96KoI8OcVk1-rcym8H7rFTKgyYDWToR9fnbnaxU8QvEBhPOdaEtPffvP7Crhmh4n4mJ8_WCCoiCMbEK-WbLAxSyAwPCGBZ-lHg8CH_YU4XkEcAIWOofdUImt2szia6rCArcKS8veyabxexOrUwDB4zz2i_8RXrbNK3lMQU_XCJI6EFLM4KpUQq1_37_c-6fhxGmelmHeRKem9u5nn705LVThbRFCFwvUvYm_8cUhg"

header = {'accept': 'application/json', 'authorization': f'Bearer {prod_bear}'}
thing = "groups"
ASSET_URL = "https://asset.iris.arup.com"
HAZARD_URL = "https://hazard.iris.arup.com"
done = 0
cnt = 0
while done ==0:
    cnt +=1
    response1 = requests.get(f"{ASSET_URL}/{thing}/",
                headers=header)
    if  cnt==15:
        done = 1
    print(response1)
    print(response1.json())
    groups  = response1.json()
    for group in groups["results"]:
        group_id = group["id"]
        print(group)
        response2 = requests.delete(f"{ASSET_URL}/{thing}/{group_id}",
                    headers=header)
        print(response2)

thing = "assets"
done = 0
cnt = 0
while done ==0:
    cnt +=1
    response1 = requests.get(f"{ASSET_URL}/{thing}/",
                headers=header)
    if  cnt==300:
        done = 1
    print(response1)
    print(response1.json())
    groups  = response1.json()
    for group in groups["results"]:
        group_id = group["id"]
        print(group)
        response2 = requests.delete(f"{ASSET_URL}/{thing}/{group_id}",
                    headers=header)
        print(response2)