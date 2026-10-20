import requests


def run_processing_holder(base_URL, token, list_holder):

    URL = base_URL + "/cst-api/v1/production/experimentation/inventory-infos/get"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    for i in list_holder:

        data = {
            "FilterAndOrderDefinition_v1": {
                "Context": {
                    "UseCase": "GetProducts",
                    "ParentProductId": i,
                    "SearchDepth": 3,
                    "IncludeExperimentInfo": True,
                }
            },
        }

        resp = requests.post(URL, headers=headersAPI, json=data, verify=True)
        inventory_info = resp.json()["result"]

        runIDs = []
        for i in range(0, len(inventory_info)):

            for item in inventory_info[i]:
                if item["articleId"] == 5:
                    runID = item["runId"]
                    runIDs.append(runID)

    return runIDs
