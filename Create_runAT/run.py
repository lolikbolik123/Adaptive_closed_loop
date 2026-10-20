import numpy
import json
import pandas as pd
import requests
from Create_runAT import authorization


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def new_run(base_URL, token, json_file, label, path):
    """
    This function return the runID, the list of the experiment and the list of the experiment product ID

    Parameters:
    - base_URL (str): The server url.
    - token(str): needed for API request
    - json_file (dict): a dictionary that follow that the template to create a run via Arksuite API
    - lable (str): name of your run display on Arksuite
    - path (str): general path to be able to open the json file

    Returns:
    - runID (int): run unique ID from Arksuite
    - list_experiment (list): list of unique experiment for a specific run
    - list_product (list): list of unique experiment product ID for a specific run

    """

    with open(path + "data" + label + ".json", "w", encoding="utf-8") as f:
        json.dump(json_file, f, ensure_ascii=False, indent=4, cls=NpEncoder)

    URL = base_URL + "cst-api/v1/production/experimentation/run/create-run"

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    # Opening JSON file
    f = open(path + "data" + label + ".json")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    resp = requests.post(URL, headers=headersAPI, json=data, verify=True)
    print(resp.json())
    j = resp.json()
    runID = j["result"]["runId"]

    list_experiment = []
    list_product = []
    expID = j["result"]["experiments"]
    for i in range(0, len(expID)):
        list_experiment.append(j["result"]["experiments"][i]["experimentId"])
        list_product.append(j["result"]["experimentProducts"][i]["productId"])

    return runID, list_experiment, list_product


def put_in_queue(base_URL, token, runID):
    """
    This function return a bolean - true mean that the run is now in the queue

    Parameters:
    - base_URL (str): The server url.
    - token(str): needed for API request
    - runID (int): run unique ID from Arksuite

    Returns:
    - resp.json() (bolean): True means that the run is now in the queue

    """

    URL = (
        base_URL + "/cst-api/v1/production/experimentation/run/queue-run/" + str(runID)
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    resp = requests.post(URL, headers=headersAPI, verify=True)

    return resp.json()


def status_run(base_URL, token, runID):
    """
    This function return the status of the run (created, queued, completed, canceled, finished)

    Parameters:
    - base_URL (str): The server url.
    - token(str): needed for API request
    - runID (int): run unique ID from Arksuite

    Returns:
    - status (str):  status of the run

    """

    URL = (
        base_URL
        + "/cst-api/v1/production/experimentation/run/get-run-state/"
        + str(runID)
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }
    try:
        resp = requests.post(URL, headers=headersAPI, verify=True)
        j = resp.json()
        status = j["result"]
    except KeyError:
        print(resp)
        status = "not completed - authentification error"

    return status


def statistic(base_URL, token, runID, list_expID, path):
    """
    This function return a dataframe with the GC/UPLC peak area for each experiments in a specific run

    Parameters:
    - base_URL (str): The server url.
    - token(str): needed for API request
    - runID (int): run unique ID from Arksuite
    - list_expID (list): List of unique experiment id for one specific run
    - path (str): general path

    Returns:
    - result_f (dataframe): a dataframe with the peak area of each product + internal standard that where specified in the processing method for each experiment

    """

    df_filtrate_by_expID = {}

    for i in list_expID:
        URL = base_URL + "/cst-api/v1/production/experimentation/run/get-run-statistics"

        headersAPI = {
            "accept": "application/json",
            # "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
            #'authorizationContext': 'accessToken'
        }

        data = {
            "IncludeDocuments": False,
            "RunIds": [runID],
            "ExperimentTrials": [
                {
                    "ExperimentId": i,
                    "TrialNumber": 0,
                    "attributeDefinitionId": 258,
                }
            ],
        }

        resp = requests.post(URL, headers=headersAPI, json=data, verify=True)

        tk = resp.json()
        print(tk)

        df = pd.json_normalize(
            tk["result"][0]["experiments"][0]["trials"][0]["createdProducts"][0][
                "attributes"
            ]
        )

        df_filtrate = df[["attributeDefinitionLabel", "attributeValueIndex", "value"]]
        df_filtrate["expID"] = i

        df_filtrate_by_expID[i] = df_filtrate

    result_f = pd.DataFrame()
    result = pd.DataFrame()

    for i in list_expID:
        result = pd.concat(
            [df_filtrate_by_expID[i], result],
            axis=0,
        )
        result_f = pd.concat([result_f, result], axis=0)
        result = pd.DataFrame()

        result_f.to_csv(path + "statistic" + str(runID) + ".csv")

    return result_f


def verification(df):

    # Find expID groups containing "Dodecane"
    bad_experiments = df[df["value"] == "Dodecane"]["expID"].unique()
    
    # Print messages for incorrect experiments
    if bad_experiments.size > 0:
        for exp in bad_experiments:
            print(f"Experiment {exp} contains 'Dodecane' and is incorrect.")
    else:
        print("All experiments are valid.")
        
    return df