import requests
import pandas as pd
import qrcode


def test(data_raw):
    data_f = data_raw[
        [
            "CAS Number",
            "Property",
            "Molecular Weight",
            "IUPAC Name",
            "SMILES",
            "CID",
            "Density",
            "Melting Point",
            "Boiling Point",
            "Boiling Point Unit",
            "Melting Point Unit",
            "Dispense Tool Volumetrically",
            "Dispense Tool Gravimetrically",
            "Stock solution",
            "Molar concentration",
        ]
    ]
    data_csv = data_f.drop_duplicates()
    data_csv = data_csv.dropna(how="all")
    data_csv = data_csv.fillna("")
    data_csv["IUPAC Name"] = data_csv["IUPAC Name"].str.replace(";", "")
    data_csv = data_csv.replace("N/A", "")
    return data_csv


# Define a function named 'create article' to create new article on Arksuite via API


def create_article(base_URL, token, att_new_article):
    """
    This function create new article into the server via Arksuite's API.

    Parameters:
    - base_URL (str): The server url.
    - token (str): token to be able to log int the server
    - att_new_article (dataframe) : dataframe with article needed to be add to Arksuite -
            "extended CAS Number",
            "CAS Number",
            "Property",
            "Molecular Weight",
            "IUPAC Name",
            "SMILES",
            "CID",
            "Density",
            "Melting Point",
            "Boiling Point",
            "Boiling Point Unit",
            "Melting Point Unit",
            "Dispense Tool Volumetrically",
            "Dispense Tool Gravimetrically",
            "Stock solution",
            "Molar concentration"

    Returns:
    - no_Add (list): A list of CAS Number ( chemicals) that where not added
    - added_DF (dataframe) : A dataframe with article ( dataframe) added to Arksuite
    """

    URL_2 = base_URL + "cst-api/v1/product-management/articles/create-articles"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }
    selected_columns = [
        "CAS Number",
        "Property",
        "Molecular Weight",
        "IUPAC Name",
        "SMILES",
        "CID",
        "Density",
        "Melting Point",
        "Boiling Point",
        "Boiling Point Unit",
        "Melting Point Unit",
        "Dispense Tool Volumetrically",
        "Dispense Tool Gravimetrically",
        "Stock solution",
        "Molar concentration",
    ]
    try:
        data_f = att_new_article[selected_columns]
    except KeyError as e:
        print(f"Error: Missing column(s): {', '.join(e.args)}")
        # Handle missing columns (e.g., select only existing ones)
        print(e.args[0])
        data_f = att_new_article[
            [col for col in selected_columns if col in att_new_article.columns]
        ]

    data_csv = data_f.drop_duplicates()
    data_csv = data_csv.dropna(how="all")
    data_csv = data_csv.fillna("")
    data_csv["IUPAC Name"] = data_csv["IUPAC Name"].str.replace(";", " ")
    data_csv = data_csv.replace("N/A", "")

    for i in data_csv.index:

        data = {
            "Label": data_csv["IUPAC Name"][i],
            "Comment": "creation via API",
            "Attributes": [
                # Melting point
                (
                    {
                        "CategoryId": 30,
                        "CategoryCstIdentifier": "DF8C4505-EEC9-4226-A49B-7A4A350FB381",
                        "AttributeId": 95,
                        "CstIdentifier": "322934DE-1CC3-4DA6-83B0-971831F4FE5F",
                        "Value": data_csv["Melting Point"][i],
                        "Unit": data_csv["Melting Point Unit"][i],
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["Melting Point"][i] != ""
                    else {}
                ),
                # Molar mass
                (
                    {
                        "CategoryId": 30,
                        "CategoryCstIdentifier": "DF8C4505-EEC9-4226-A49B-7A4A350FB381",
                        "AttributeId": 169,
                        "CstIdentifier": "FB93A3DA-1C50-4C68-BF0F-EA0DE99B6CBF",
                        "Value": data_csv["Molecular Weight"][i],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["Molecular Weight"][i] != ""
                    else {}
                ),
                # Density
                (
                    {
                        "CategoryId": 30,
                        "CategoryCstIdentifier": "DF8C4505-EEC9-4226-A49B-7A4A350FB381",
                        "AttributeId": 59,
                        "CstIdentifier": "B942B95D-E489-4864-B4AD-220AADFABE17",
                        "Value": data_csv["Density"][i],
                        # "Unit": 1200,
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["Density"][i] != ""
                    else {}
                ),
                # SMILES
                (
                    {
                        "AttributeId": 283,
                        "CstIdentifier": "DB738391-E68A-4779-B471-11DDF045F890",
                        "Value": data_csv["SMILES"][i],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["SMILES"][i] != ""
                    else {}
                ),
                # Molar Concentration
                (
                    {
                        "CategoryId": 30,
                        "CategoryCstIdentifier": "DF8C4505-EEC9-4226-A49B-7A4A350FB381",
                        "AttributeId": 293,
                        "CstIdentifier": "AAC544F2-D40A-4AB7-82D3-9A3CB880FC44",
                        "Value": data_csv["Molar concentration"][i],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["Molar concentration"][i] != ""
                    else {}
                ),
                # CAS Number
                (
                    {
                        "CategoryId": 30,
                        "CategoryCstIdentifier": "DF8C4505-EEC9-4226-A49B-7A4A350FB381",
                        "AttributeId": 33,
                        "CstIdentifier": "345FAE2E-54E4-4D62-A693-8A8C00A031F8",
                        "Value": data_csv["CAS Number"][i].split("_")[0],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["CAS Number"][i] != ""
                    else {}
                ),
                # Extended CAS number
                (
                    {
                        "AttributeId": 367,
                        "CstIdentifier": "AF9D2CD3-EEF4-445A-99E6-54B82FE36768",
                        "Value": data_csv["CAS Number"][i],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if data_csv["SMILES"][i] != ""
                    else {}
                ),
                # Tag solvent
                (
                    {
                        "AttributeId": 247,
                        "CstIdentifier": "8BF88CC4-77A1-43A6-B49F-F4CF31CB620F",
                        "Value": bool(data_csv["Property"][i] == "solvent"),
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if bool(data_csv["Property"][i] == "solvent") != ""
                    else {}
                ),
                # Tag dispensable or not
                {
                    "AttributeId": 28,
                    "CstIdentifier": "9E61F679-693D-4D72-94A7-B63F7B771175",
                    "Value": True,
                    # "Unit": 'None',
                    "InsertedAt": "2022-11-30T11:41:06.076Z",
                },
                # Volumetric Tool
                (
                    {
                        "AttributeId": 139,
                        "CstIdentifier": "A3662EB7-5735-4CE1-BF41-FFD4160DB057",
                        "Value": data_csv["Dispense Tool Volumetrically"][i],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if "Dispense Tool Volumetrically" in data_csv.columns
                    and data_csv["Dispense Tool Volumetrically"][i] != ""
                    else {}
                ),
                # Gravimetric Tool
                (
                    {
                        "AttributeId": 138,
                        "CstIdentifier": "13196261-41A2-42DB-9F79-82D175396798",
                        "Value": data_csv["Dispense Tool Gravimetrically"][i],
                        # "Unit": 'None',
                        "InsertedAt": "2022-11-30T11:41:06.076Z",
                    }
                    if "Dispense Tool Gravimetrically" in data_csv.columns
                    and data_csv["Dispense Tool Gravimetrically"][i] != ""
                    else {}
                ),
            ],
        }

        #### TRY ####
        if data_csv["Dispense Tool Gravimetrically"][i] == "GDU-S":
            GDUS_parameters = {
                "CategoryId": 42,
                "CategoryCstIdentifier": "507D6137-FD6C-4D08-B9BC-7BCE0B36F14F",
                "AttributeId": 80,
                "CstIdentifier": "B39F0B58-A3F1-4A60-A6A4-4F5ACF574042",
                "Value": 5,
                # "Unit": 'None',
                "InsertedAt": "2022-11-30T11:41:06.076Z",
            }

            data["Attributes"].append(GDUS_parameters)

        elif data_csv["Dispense Tool Gravimetrically"][i] == "GDU-V":
            GDUV_parameters = {
                "CategoryId": 37,
                "CategoryCstIdentifier": "E9CCE9E1-67D6-4F20-90BA-34CE907D3584",
                "AttributeId": 131,
                "CstIdentifier": "641DF186-E5D7-4F56-894A-8F7CBC06834A",
                "Value": "1",
                # "Unit": 'None',
                "InsertedAt": "2022-11-30T11:41:06.076Z",
            }

            data["Attributes"].append(GDUV_parameters)

        elif data_csv["Dispense Tool Gravimetrically"][i] == "GDU-PFD":
            GDUPFd_parameters = {
                "CategoryId": 36,
                "CategoryCstIdentifier": "536D870B-DD1E-4252-9C87-39CA46893C45",
                "AttributeId": 80,
                "CstIdentifier": "B39F0B58-A3F1-4A60-A6A4-4F5ACF574042",
                "Value": "5",
                # "Unit": 'None',
                "InsertedAt": "2022-11-30T11:41:06.076Z",
            }

            data["Attributes"].append(GDUPFd_parameters)

        elif data_csv["Dispense Tool Volumetrically"][i] == "4NH":
            NH_parameters = {
                "CategoryId": 53,
                "CategoryCstIdentifier": "76E84FA6-507B-4084-8825-C66A05F73F2D",
                "AttributeId": 200,
                "CstIdentifier": "7C98E9D3-29E9-4095-B6F2-89A8F5D7C683",
                "Value": "2",
                # "Unit": 'None',
                "InsertedAt": "2022-11-30T11:41:06.076Z",
            }

            data["Attributes"].append(NH_parameters)

        else:
            continue

        #############

        data["Attributes"] = list(filter(None, data["Attributes"]))
        print(data)

        resp_2 = requests.post(URL_2, headers=headersAPI, json=data, verify=True)

        json_response = resp_2.json()

        no_Add = []
        added = []
        added_DF = pd.DataFrame()
        added_IUPAC_Name = []

        if resp_2.status_code != 200:
            print("error: " + str(resp_2.status_code))
            print(resp_2.json())
            no_Add.append(data_csv["CAS Number"][i])
        else:
            print("Success")
            added_DF["CAS Number"] = data_csv["CAS Number"][i]
            added_DF["IUPAC Name"] = data_csv["IUPAC Name"][i]
            added_DF["ArtID"] = json_response["result"]
        # added=added.append(data_csv['CAS Number'][i])
        # added_IUPAC_Name=added_IUPAC_Name.append(data_csv['IUPAC Name'][i])

    return no_Add, added_DF  # added


# Define a function named 'create product' to create new product on Arksuite via API


def create_product(base_URL, token, new_product):
    """
    This function create new product into the server via Arksuite's API.

    Parameters:
    - base_URL (str): The server url.
    - token (str): token to be able to log int the server
    - new_product (dataframe) : dataframe with product needed to be add to Arksuite -
            "CAS Number",
            "Property",
            "Molecular Weight",
            "IUPAC Name",
            "SMILES",
            "CID",
            "Density",
            "Melting Point",
            "Boiling Point",
            "Boiling Point Unit",
            "Melting Point Unit",
            "Dispense Tool Volumetrically",
            "Dispense Tool Gravimetrically",
            "Stock solution",
            "Molar concentration",
            "ArtID"

    Returns:
    - DF_new_product (dataframe): A dataframe with ArtId, IUPAC Name, ProductID

    """

    URL = base_URL + "cst-api/v1/product-management/products/create-product"

    headersAPI = {
        "accept": "application/json",
        # "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #'authorizationContext': 'accessToken'
    }

    new_product_unique = new_product[["ArtId", "IUPAC Name", "CAS Number"]]
    new_product_unique.drop_duplicates(inplace=True)

    list_new_product = []

    for i in new_product_unique.index:
        data = {
            "Label": new_product_unique["IUPAC Name"][i],
            "ArticleId": int(new_product_unique["ArtId"][i]),
        }
        resp = requests.post(URL, headers=headersAPI, json=data, verify=True)

        if resp.status_code != 200:
            print("error: " + str(resp.status_code))

        else:
            print(
                "Success:" + new_product_unique["IUPAC Name"][i] + " have been created"
            )

        json_resp = resp.json()

        print(json_resp)

        productId = json_resp["result"]

        list_new_product.append(
            {
                "ArtId": int(new_product_unique["ArtId"][i]),
                "IUPAC Name": new_product_unique["IUPAC Name"][i],
                "ProductID": productId,
                "CAS Number": new_product_unique["CAS Number"][i],
            }
        )

    DF_new_product = pd.DataFrame.from_dict(list_new_product)

    DF_new_product.to_csv("test_creation_product.csv")

    return DF_new_product


# Define a function named 'qr_code_generator' to create a qr code containing the CAS Number, Aticle ID and Product ID of evry new peroduct created via Arksuite API


def qr_code_generator(new_product):

    path_QrCode = "C:/Users/TERRIEAI/OneDrive - KAUST/Python_Scripts/QrCode/reagents/"

    for i in range(0, len(new_product)):

        content = (
            "C:"
            + str(new_product.loc[i, "CAS Number"])
            + "\n"
            + "A:"
            + str(new_product.loc[i, "ArtId"])
            + "\n"
            + "P:"
            + str(new_product.loc[i, "ProductID"])
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(
            path_QrCode
            + str(new_product.loc[i, "CAS Number"])
            + "_"
            + str(new_product.loc[i, "ProductID"])
            + ".png"
        )
