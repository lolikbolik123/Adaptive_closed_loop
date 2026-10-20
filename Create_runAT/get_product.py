import requests
from Create_runAT import camera_control


def exist_product(base_URL, token, all_att_DOE):

    URL = base_URL + "/cst-api/v1/product-management/products/get-products"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    product_exist = []
    product_tocreate = []

    articleID = all_att_DOE["ArtId"].unique()
    articleID = [x for x in articleID if str(x) != "nan"]

    # change float to int
    articleID = list(map(int, articleID))

    for i in range(0, len(articleID)):

        data = {"ArticleId": articleID[i]}

        resp = requests.post(URL, headers=headersAPI, json=data, verify=True)

        if resp.json()["result"] == []:
            print(" There is no product related to this articleID " + str(articleID[i]))
            product_tocreate.append(articleID[i])
        else:
            product_exist.append((articleID[i]))

    select_producttocreate = all_att_DOE["ArtId"].isin(product_tocreate)
    df_product_tocreate = all_att_DOE[select_producttocreate]

    return df_product_tocreate


def use_barcode(base_URL, token, productID):
    """
    This function return the value of the attribute 'use_barcode' on Arksuite for a vial.
    If it false that means that the transport task to the barcode readear didn't start yet

    Parameters:
    - base_URL (str): The server url.
    - token(str): needed for API request
    - productID (int): Vial experiment product ID

    Returns:
    - use_barcode(bool): transport task to the barcode reader is started or not
    """

    URL = base_URL + "/cst-api/v1/product-management/products/product-attributes/get"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    data_csv = {"ProductIds": [productID]}

    try:
        resp = requests.post(URL, headers=headersAPI, json=data_csv, verify=True)

        j = resp.json()

        product_info = j["result"][0]["attributes"]

        for item in product_info:
            if item["attributeDefinitionLabel"] == "Use_barcode":
                use_barcode = item["value"]

        print(productID)
        print(use_barcode)

    except KeyError:
        print(resp)
        use_barcode = "authentification error"

    return use_barcode
