import requests
import credentials

# Define a function named 'login' to log in Arksuite API


def login(base_URL):
    """
    This function log into the server and generate a token for API Call.

    Parameters:
    - base_URL (str): The server url.

    Returns:
    - token: A string that will be need for all API request.
    """

    URL = base_URL + "cst-api/v1/infrastructure/authorization/login"

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    Credentials = {
        "Credentials": {
            "Username": credentials.username,
            "Password": credentials.password,
        }
    }

    resp = requests.post(URL, headers=headers, json=Credentials)

    j = resp.json()
    token = j["authorizationContext"]["accessToken"]

    if resp.status_code != 200:
        print("error: " + str(resp.status_code))
    else:

        print("Success")

    return token
