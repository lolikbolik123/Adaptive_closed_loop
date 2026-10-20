import pandas as pd

from bs4 import BeautifulSoup
import pubchempy as pcp
import re
import requests
from . import gui_attribute

# Define a function named 'attributes_PubChem' to search on Pubchem webpage information about chemicals

def print_red_bold(text):
    """
    Prints the input string in red and bold in the terminal.

    Parameters:
    - text (str): The string to be printed in red bold.

    Returns:
    None
    """
    red_bold = "\033[1;31m"  # ANSI escape code for bold red text
    reset = "\033[0m"  # Reset formatting
    print(f"{red_bold}{text}{reset}")



def attributes_PubChem(add_article):
    """
    This function go on Pubchem webpage and extract the molecular weight, the IUPAC name, the SMILES representation, the Pubchem identifier, the density, the boiling point and the melting point.

    Parameters:
    - add_article (str): The CAS number of the chemical to add to Arksutie server.

    Returns:
    - result (dataframe): A dataframe with all the chemicals information for each new chemical.
    """
    MW = []
    IUPAC = []
    SMILES = []
    CID = []

    for i in range(0, len(add_article)):
        CAS_Number_extend = add_article[i]
        z = CAS_Number_extend.split("_")[0]

        if bool(pcp.get_compounds(z, "name")) == False:
            print(z, "is not a correct CAS Number")
            MW.append("nan")
            IUPAC.append("nan")
            SMILES.append("nan")
            CID.append("nan")
            #
        else:
            for compound in pcp.get_compounds(z, "name"):
                MW.append(compound.molecular_weight)
                IUPAC.append(compound.iupac_name)
                SMILES.append(compound.canonical_smiles)
                CID.append(compound.cid)

    rho_DF = []
    MP_DF = []
    MP_unit_DF = []
    BP_DF = []
    BP_unit_DF = []

    for i in range(0, len(CID)):
        Identifier = CID[i]
        data = requests.get(
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"
            + str(Identifier)
            + "/xml"
        )
        html = BeautifulSoup(data.content, "html.parser")

        try:
            rho = html.find(name="TOCHeading", string="Density")
            # rho=rho.find_next_sibling('Information').find(name='String').string
            ex_rho = rho.find_next_sibling("Information").find(name="String").string
            rho_DF.append((re.search("(^[-|\d.]+)", ex_rho).group(1)))
        except AttributeError:
            rho_DF.append("N/A")
            message = f"No density found for {add_article[i]}, with PubChem CID: {str(Identifier)}" 
            print_red_bold(message)
            # gui_attribute.show_popup(message)

        try:
            MP = html.find(name="TOCHeading", string="Melting Point")
            ex_MP = MP.find_next_sibling("Information").find(name="String").string
            MP_DF.append((re.search("(^[-|\d.]+)", ex_MP).group(1)))
            MP_unit_DF.append((re.search("°(.)", ex_MP).group(1)))
        except AttributeError:
            MP_DF.append("N/A")
            MP_unit_DF.append("N/A")

        try:
            BP = html.find(name="TOCHeading", string="Boiling Point")
            ex_BP = BP.find_next_sibling("Information").find(name="String").string
            BP_DF.append((re.search("(^[-|\d.]+)", ex_BP).group(1)))
            BP_unit_DF.append((re.search("°(.)", ex_BP).group(1)))
        except AttributeError:
            BP_DF.append("N/A")
            BP_unit_DF.append("N/A")

    DF = pd.DataFrame(add_article, columns=["CAS Number"])
    DF["Molecular Weight"] = MW
    DF["IUPAC Name"] = IUPAC
    DF["SMILES"] = SMILES
    DF["CID"] = CID
    DF["Density"] = rho_DF
    DF["Melting Point"] = MP_DF
    DF["Boiling Point"] = BP_DF
    DF["Boiling Point Unit"] = BP_unit_DF
    DF["Melting Point Unit"] = MP_unit_DF

    to_remov = {"C": "Celsius", "F": "Fahrenheit"}
    for char in to_remov.keys():
        DF["Boiling Point Unit"] = DF["Boiling Point Unit"].str.replace(
            char, to_remov[char]
        )
        DF["Melting Point Unit"] = DF["Melting Point Unit"].str.replace(
            char, to_remov[char]
        )

    result = DF

    return result
