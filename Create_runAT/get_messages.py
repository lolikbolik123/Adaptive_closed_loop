import numpy as np

import pandas as pd

import requests
import datetime
import os

# Define a function named get_messafge to get the messages posted on Arksuite


def get_messages_started(base_URL, token,now,future_date_str,start_app,base_path):

    URL = base_URL + "/cst-api/v1/infrastructure/environment/logging/get-messages"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    

    data ={
            "Timeframe": {
                "From": str(now),
                "Until": str(future_date_str),
            },
            "MessageContext": {"ModuleId": 3},
        }
    

    resp = requests.post(URL, headers=headersAPI, json=data, verify=True)

    message = resp.json()
    
    word_to_check1='Aqueous'
    word_to_check2='Started'
    word_to_check3='Membrane_app_closed'
    
  
    started_list=[]  
    for i in range (0,len(message['result'])):
        text=message['result'][i]['messageText']
        if word_to_check1 and  word_to_check2 in text:
            # Extract keywords using string manipulation or regular expressions
            keywords = ["Aqueous", "Organic", "Started"]
            extracted_numbers = [int(word.split()[-1]) for word in text.split(",") if any(kw in word for kw in keywords)]
            
            # Create folder name
            today = datetime.datetime.now().strftime("%Y_%m_%d")
            folder_name = f"{today}_{'_'.join(str(num) for num in extracted_numbers)}"
            full_path = os.path.join(base_path, folder_name)
            
            # Create the folder
            os.makedirs(full_path, exist_ok=True)
            
            started_list.append(True)
        elif word_to_check3 in text:
            start_app=False
        
        else:
            started_list.append(False)
            
    if any(started_list):
        started=True
    else:
        started=False

    return started,start_app


def get_messages_finished(base_URL, token,now,future_date_str,start_app):

    URL = base_URL + "/cst-api/v1/infrastructure/environment/logging/get-messages"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }



    data ={
            "Timeframe": {
                "From": str(now),
                "Until": str(future_date_str),
            },
            "MessageContext": {"ModuleId": 3},
        }
    

    resp = requests.post(URL, headers=headersAPI, json=data, verify=True)

    message = resp.json()
    
    word_to_check1='Aqueous'
    word_to_check2='Finished'
    word_to_check3='Membrane_app_closed'
    
  
    started_list=[]
    
    for i in range (0,len(message['result'])):
        text=message['result'][i]['messageText']
        if word_to_check1 and  word_to_check2 in text:
            started_list.append(False)
        elif word_to_check3 in text:
            start_app=False
        else:
            started_list.append(True)
            start_app=True
            
    if any(value == False for value in started_list):
        started=False
    else:
        started=True

    return started,start_app