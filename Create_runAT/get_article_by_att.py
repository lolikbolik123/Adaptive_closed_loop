import requests

# Define a function named exist_article to check if an article is already registered to Arksuite via the API


def exist_article(base_URL, token, compounds_cas):

    URL_4 = (
        base_URL
        + "/cst-api/v1/product-management/articles/get-articles-by-attributes-values"
    )

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    CASNumber_exist = []
    print(compounds_cas)

    for i in range(0, len(compounds_cas)):

        data_csv_4 = [
            {
                "AttributeDefinition": {
                    "CstId": "AF9D2CD3-EEF4-445A-99E6-54B82FE36768"  
                },
                "Values": [{"String": compounds_cas[i]}],
            }
        ]

        resp_4 = requests.post(URL_4, headers=headersAPI, json=data_csv_4, verify=True)

        if resp_4.json()["result"] == []:
            print(compounds_cas[i] + " The article is not register")
        else:
            CASNumber_exist.append((compounds_cas[i]))

    return CASNumber_exist


"""
def new_article_t(CASNumber_exist, data_csv_csv):

    list_CASNumber = set(data_csv_csv["CAS Number"])

    for i in CASNumber_exist:
        if i in list_CASNumber:
            data_csv_csv.drop(
                data_csv_csv[data_csv_csv["CAS Number"] == i].index, inplace=True
            )
        else:
            continue

"""
# Define a function named new_article to create a list of new article needed to be created


def new_article(CASNumber_exist, compounds_cas):
    """
    create a list of the new article to create on Arksuite

    Parameters:
    - CASNumber_exist(list): lsit of CAS Number that already exist
    - compounds_cas(list): list of unique CAS Number that are on DOE (input user)

    returns:
    - compounds_cas (list): list of article that would need to be created on Arksuite

    """

    for i in range(0, len(CASNumber_exist)):
        if bool(CASNumber_exist[i] in compounds_cas) is True:
            compounds_cas.remove(CASNumber_exist[i])
        else:
            continue

    return compounds_cas


# Define a function named get_att_byCASNumber to get the attribute of a chemical registered in Arksuite


def get_att_byCASNumber(base_URL, token, data_csv):
    """
    Request  send to the API to get the attribute of a chemical registered in Arksuite

    Parameters:
    - base_URL (str): The server url.
    - token(str): token to do a request on Arksuite
    - data_csv (dataframe): dataframe with all the chemicals that will be used for the run (one row, one chemical)

    returns:
    - data_csv (dataframe): dataframe with all attibute registered on Arksuite (Melting point, Molar Mass,
    Dispense Tool Volumetric, Dispense Tool Gravimetric, Internal Standard, Dispensable, Density, ChemBeads Factor,
    Molar Concentration)

    """

    URL_2 = (
        base_URL
        + "/cst-api/v1/product-management/articles/get-articles-by-attributes-values"
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    # request on the API for each row on the dataframe
    for i in data_csv["CAS Number"]:
        if i != "-":
            data = [
                {
                    "AttributeDefinition": {
                        "CstId": "AF9D2CD3-EEF4-445A-99E6-54B82FE36768"
                    },
                    "Values": [{"String": i}],
                }
            ]

            resp_2 = requests.post(URL_2, headers=headersAPI, json=data, verify=True)

            # Add the attributes on the dataframe
            if resp_2.status_code == 200:
                tk_2 = resp_2.json()
                ex = tk_2["result"][0]
                ex_2 = ex["attributes"]

                index = data_csv[data_csv["CAS Number"].isin([i])].index

                data_csv.loc[index, "ArtId"] = ex["id"]
                data_csv.loc[index, "IUPAC Name"] = ex = tk_2["result"][0]["label"]

                for j in range(0, len(ex_2)):

                    if ex_2[j]["attributeDefinition"]["id"] == 95:
                        data_csv.loc[index, "Melting point"] = ex_2[j]["flattenedValue"]

                    elif ex_2[j]["attributeDefinition"]["id"] == 169:
                        data_csv.loc[index, "Molar mass"] = ex_2[j]["flattenedValue"]

                    # elif ex_2[i]['attributeDefinition']['id'] == 33:
                    #  data_csv['CAS NUMBER']= ex_2[i]['flattenedValue']

                    elif ex_2[j]["attributeDefinition"]["id"] == 139:
                        data_csv.loc[index, "Dispense Tool Volumetric"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 138:
                        data_csv.loc[index, "Dispense Tool Gravimetric"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 254:
                        data_csv.loc[index, "Internal Standard"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 28:
                        data_csv.loc[index, "Dispensable"] = ex_2[j]["flattenedValue"]

                    elif ex_2[j]["attributeDefinition"]["id"] == 59:
                        data_csv.loc[index, "Density"] = ex_2[j]["flattenedValue"]

                    elif ex_2[j]["attributeDefinition"]["id"] == 294:
                        data_csv.loc[index, "ChemBeads Factor"] = ex_2[j][
                            "flattenedValue"
                        ]

                    elif ex_2[j]["attributeDefinition"]["id"] == 293:
                        data_csv.loc[index, "Molar Concentration"] = ex_2[j][
                            "flattenedValue"
                        ]

                    else:
                        continue
            else:
                pass
        else:
            pass

    return data_csv

def get_att_byCASNumber_test(base_URL, token, data_csv):
    """
    Request  send to the API to get the attribute of a chemical registered in Arksuite

    Parameters:
    - base_URL (str): The server url.
    - token(str): token to do a request on Arksuite
    - data_csv (dataframe): dataframe with all the chemicals that will be used for the run (one row, one chemical)

    returns:
    - data_csv (dataframe): dataframe with all attibute registered on Arksuite (Melting point, Molar Mass,
    Dispense Tool Volumetric, Dispense Tool Gravimetric, Internal Standard, Dispensable, Density, ChemBeads Factor,
    Molar Concentration)

    """

    URL_2 = (
        base_URL
        + "/cst-api/v1/product-management/articles/get-articles-by-attributes-values"
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }
    
    attribute_map = {
    95: "Melting point",
    169: "Molar mass",
    139: "Dispense Tool Volumetric",
    138: "Dispense Tool Gravimetric",
    254: "Internal Standard",
    28: "Dispensable",
    59: "Density",
    294: "ChemBeads Factor",
    293: "Molar Concentration"
}
    
    

   
    
    # request on the API for each row on the dataframe
    for i in data_csv["CAS Number"].unique():
        if i != "-":
            data = [
                {
                    "AttributeDefinition": {
                        "CstId": "AF9D2CD3-EEF4-445A-99E6-54B82FE36768"
                    },
                    "Values": [{"String": i}],
                }
            ]

            resp_2 = requests.post(URL_2, headers=headersAPI, json=data, verify=True)

            # Add the attributes on the dataframe
            if resp_2.status_code == 200:
                tk_2 = resp_2.json()
                ex = tk_2["result"][0]
                att = ex["attributes"]
                data_csv.loc[data_csv['CAS Number'] == i, ['ArtId', 'IUPAC Name']] = [ex['id'], tk_2['result'][0]['label']]

                for j in range(0, len(att)):
                    attribute_id = att[j]["attributeDefinition"]["id"]
                    if attribute_id in attribute_map:
                        column_name = attribute_map[attribute_id]
                        data_csv.loc[data_csv['CAS Number'] == i, column_name] = att[j]["flattenedValue"]

 

    return data_csv