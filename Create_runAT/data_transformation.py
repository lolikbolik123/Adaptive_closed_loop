import pandas as pd
import numpy as np


# Define a function named 'DT' to transform the data from the user to data readeable by Arksuite


def check_and_select_columns(df, columns_to_check):
    """
    Checks for columns in 'columns_to_check' present in the DataFrame 'df'
    and returns a new DataFrame containing only the found columns.

    Args:
        df (pandas.DataFrame): The DataFrame to check and select columns from.
        columns_to_check (list): A list of column names to check for presence.

    Returns:
        pandas.DataFrame: A new DataFrame containing only the found columns.
    """

    selected_columns = list(set(columns_to_check) & set(df.columns))
    return df[selected_columns]


def DT(data_raw, reactiontype):
    """
    This function transform the data to use it to create run on Arksuite.

    Parameters:
    - data_raw (dataframe): Data from the user -
        CAS Number
        Equivalent
        Reaction conditions
    - reactiontype (str): Htemperature or photochemistry

    Returns:
    - DF (dataframe): A dataframe -
        Experiment No.
        CAS Number
        Wavelength
        reaction scale (mmol)
        time (h)
        Temperature (C )
        Equivalent
        Property
        pressure (bar)


    """

    ### This two lines need to be uncomment when we use the main_ML.py  ###
    """
    data_raw.insert(
        loc=0, column="Experiment No.", value=list(range(1, len(data_raw.index) + 1))
    )
    """
    # data_raw.columns = data_raw.columns.str.replace("\_(.*)", "")

    # Select the columns until the reaction scale - name of the reagent
    columns_select = data_raw.loc[:, "Experiment No.":"reaction scale (mmol)"]
    columns_list = columns_select.columns

    columns_name = columns_list[1:-1]
    df = []
    DF = pd.DataFrame()

    # Return the number of solvent or monomer because it doesn't have equivalent but directly mass or volume input by the user
    number_solvent = 0
    number_monomer = 0
    for ele in list(columns_name):
        if ele.startswith("solvent"):
            number_solvent = number_solvent + 1
        if ele.startswith("monomer"):
            number_solvent = number_solvent + 1

    # transfrom the dataframe to have only one reagent by rows
    for i in range(0, len(columns_name)):
        if i in range(0, len(columns_name) - number_solvent - number_monomer):

            columns_to_check = [
                "Experiment No.",
                "Temperature (C )",
                "pressure (bar)",
                "time (h)",
                "Wavelength",
                "reaction scale (mmol)",
                columns_name[i],
                columns_name[i] + " equivalent",
            ]
            df = check_and_select_columns(data_raw.copy(), columns_to_check)

            df = df.rename(
                columns={
                    columns_name[i]: "CAS Number",
                    columns_name[i] + " equivalent": "Equivalent",
                }
            )
            df["Property"] = columns_name[i]
            DF = pd.concat([DF, df])
        else:
            columns_to_check = [
                "Experiment No.",
                columns_name[i],
                "Temperature (C )",
                "pressure (bar)",
                "time (h)",
                "Wavelength",
                "reaction scale (mmol)",
            ]
            df = check_and_select_columns(data_raw.copy(), columns_to_check)
            df = df.rename(columns={columns_name[i]: "CAS Number"})
            df["Property"] = columns_name[i]
            DF = pd.concat([DF, df])

    DF.reset_index(drop=True, inplace=True)
    # DF.to_csv("C:/Users/TERRIEAI/OneDrive - KAUST/Files_generated_python/DT.csv")

    # Add the volume to add for the solvent and the monomer ( value in the DOE input user)
    property_to_check = [
        "solvent",
        "solvent B",
        "solvent A",
        "monomer",
        "monomer 1",
        "monomer 2",
    ]
    mask = DF["Property"].isin(property_to_check)
    new_DF = DF[mask]
    new_DF.reset_index(inplace=True)

    for i in range(0, len(new_DF)):
        prop = new_DF.loc[i, "Property"]
        new_DF.loc[i, "Volume"] = data_raw.loc[
            new_DF.loc[i, "Experiment No."] - 1, prop + " amount (ml)"
        ]

    columns_merge = list(DF.columns)
    merge_DF_volume = pd.merge(
        DF,
        new_DF,
        how="outer",
        on=columns_merge,
    )

    # Add the mass to add for all columns if needed ( value in the DOE input user)

    for i in range(0, len(DF)):
        prop = DF.loc[i, "Property"]
        if prop + " mass (mg)" in data_raw.columns:
            merge_DF_volume.loc[i, "Mass"] = data_raw.loc[
                merge_DF_volume.loc[i, "Experiment No."] - 1, prop + " mass (mg)"
            ]
        else:
            continue
    merge_DF_volume_sorted = merge_DF_volume.sort_values(
        by=["Property", "Experiment No."], ascending=[False, True]
    )

    return merge_DF_volume_sorted

def DT_with_processing_method(data_raw, reactiontype):
    """
    This function transform the data to use it to create run on Arksuite.

    Parameters:
    - data_raw (dataframe): Data from the user -
        CAS Number
        Equivalent
        Reaction conditions
    - reactiontype (str): Htemperature or photochemistry

    Returns:
    - DF (dataframe): A dataframe -
        Experiment No.
        CAS Number
        Wavelength
        reaction scale (mmol)
        time (h)
        Temperature (C )
        Equivalent
        Property
        pressure (bar)


    """

    ### This two lines need to be uncomment when we use the main_ML.py  ###
    """
    data_raw.insert(
        loc=0, column="Experiment No.", value=list(range(1, len(data_raw.index) + 1))
    )
    """
    # data_raw.columns = data_raw.columns.str.replace("\_(.*)", "")
    
    # Step 1: Identify all columns that end with "_extended"    
    # Step 2: Find columns to delete (six columns to the left of each "_extended" column)


    # Select the columns until the reaction scale - name of the reagent
    columns_select = data_raw.loc[:, "Experiment No.":"reaction scale (mmol)"]
    columns_list = columns_select.columns

    columns_name = columns_list[1:-1]
    df = []
    DF = pd.DataFrame()

    # Remove "_Extended" and keep only unique column names
    columns_cleaned = list(dict.fromkeys([col.replace("_Extended", "") for col in columns_name]))
    

    # Return the number of solvent or monomer because it doesn't have equivalent but directly mass or volume input by the user
    number_solvent = 0
    number_monomer = 0
    for ele in list(columns_name):
        if ele.startswith("solvent"):
            number_solvent = number_solvent + 1
        if ele.startswith("monomer"):
            number_solvent = number_solvent + 1

    # transfrom the dataframe to have only one reagent by rows
    for i in range(0, len(columns_name)):
        if i in range(0, len(columns_name) - number_solvent - number_monomer):

            columns_to_check = [
                "Experiment No.",
                "Temperature (C )",
                "pressure (bar)",
                "time (h)",
                "Wavelength",
                "reaction scale (mmol)",
                'Processing_method',
                columns_name[i],
                columns_cleaned[i] + " equivalent",
            ]
            df = check_and_select_columns(data_raw.copy(), columns_to_check)

            df = df.rename(
                columns={
                    columns_name[i]: "CAS Number",
                    columns_cleaned[i] + " equivalent": "Equivalent",
                }
            )
            df["Property"] = columns_name[i]
            DF = pd.concat([DF, df])
        else:
            columns_to_check = [
                "Experiment No.",
                columns_name[i],
                "Temperature (C )",
                "pressure (bar)",
                "time (h)",
                "Wavelength",
                "reaction scale (mmol)",
                'Processing_method',
            ]
            df = check_and_select_columns(data_raw.copy(), columns_to_check)
            df = df.rename(columns={columns_name[i]: "CAS Number"})
            df["Property"] = columns_name[i]
            DF = pd.concat([DF, df])

    DF.reset_index(drop=True, inplace=True)
    # DF.to_csv("C:/Users/TERRIEAI/OneDrive - KAUST/Files_generated_python/DT.csv")

    # Add the volume to add for the solvent and the monomer ( value in the DOE input user)
    property_to_check = [
        "solvent_Extended",
        "solvent B",
        "solvent A",
        "monomer",
        "monomer 1",
        "monomer 2",
    ]
    mask = DF["Property"].isin(property_to_check)
    new_DF = DF[mask]
    new_DF.reset_index(inplace=True)

    for i in range(0, len(new_DF)):
        prop = new_DF.loc[i, "Property"]
        prop_cleaned = prop.replace('_Extended', '')
        del prop

        new_DF.loc[i, "Volume"] = data_raw.loc[
            new_DF.loc[i, "Experiment No."] - 1, prop_cleaned + " amount (ml)"
        ]

    columns_merge = list(DF.columns)
    merge_DF_volume = pd.merge(
        DF,
        new_DF,
        how="outer",
        on=columns_merge,
    )

    # Add the mass to add for all columns if needed ( value in the DOE input user)

    for i in range(0, len(DF)):
        prop = DF.loc[i, "Property"]
        prop_cleaned = prop.replace('_Extended', '')
        del prop

        if prop_cleaned + " mass (mg)" in data_raw.columns:
            merge_DF_volume.loc[i, "Mass"] = data_raw.loc[
                merge_DF_volume.loc[i, "Experiment No."] - 1, prop_cleaned + " mass (mg)"
            ]
        else:
            continue
    merge_DF_volume_sorted = merge_DF_volume.sort_values(
        by=["Property", "Experiment No."], ascending=[False, True]
    )

    return merge_DF_volume_sorted
    


# Define a function named 'DT_filtered' to select unique chemicals - it will be use later to check if this chemicals are registered on Arksuite


def DT_filtered(main_df):
    """
    This function select the row to have unique chemical based on the column CAS Number.

    Parameters:
    - data_raw (dataframe): Data from the user -
        CAS Number
        Equivalent
        Reaction conditions


    Returns:
    - compounds_cas (list): The list of unique CAS Number
    """

    data_f = main_df[["CAS Number", "Property"]]
    data_f = data_f.drop_duplicates()
    data_f = data_f[data_f["CAS Number"] != "-"]
    compounds_cas = data_f["CAS Number"].to_list()
    return compounds_cas


# Define a function named 'read_excel' to read an Excel file and filter specific columns
def read_excel(filename):
    """
    This function reads an Excel file and filters specific columns.

    Parameters:
    - filename (str): The path to the Excel file extracted from Arksuite to be read.

    Returns:
    - pd.DataFrame: A DataFrame containing the selected columns from the Excel file.
    """

    # Read the Excel file into a DataFrame using pandas.
    # The third row (0-indexed) in the Excel file is used as column names.
    df = pd.read_excel(filename, header=2)

    # Filter rows containing the string "Analyse GC" using a lambda function.
    # The lambda function checks if the string is present in any row of the DataFrame.
    filtered_rows = df[df.apply(lambda row: "Analyse GC" in str(row), axis=1)]

    # Select specific columns from the filtered rows.
    selected_columns = filtered_rows[
        [
            "Run ID",
            "Trial",
            "Trial State",
            "Experiment",
            "Node",
            "Peak Areas",
            "Peak names",
        ]
    ]

    # Return the DataFrame containing the selected columns.
    return selected_columns


def split_columns_on_max_values(df, value_column_name, description_column_name):
    """
    This subroutine takes a DataFrame with two adjacent columns (value and description).
    If the cells in these columns contain multiple data separated by '\n', it splits
    the columns into multiple columns based on the maximum number of combined data.

    Parameters:
    - df (pd.DataFrame): The input DataFrame with two adjacent columns.
    - value_column_name (str): The name of the column containing values.
    - description_column_name (str): The name of the column containing descriptions.

    Returns:
    - pd.DataFrame: A new DataFrame with split columns for values and descriptions.
    """

    # Drop the existing value and description columns from the output DataFrame
    df_output = df.drop(columns=[value_column_name, description_column_name])

    # Get the DataFrame index
    dd = df_output.index

    # Extract value and description columns
    value_column = df[value_column_name]
    description_column = df[description_column_name]

    # Get the number of rows in the DataFrame
    noRows = len(value_column)

    maxCount = 0

    # Determine the maximum number of values in a cell
    for nn in range(noRows):
        if str(value_column.iloc[nn]) != "nan":
            # Split the cell values using '\n' and calculate the count
            cell_values = str(value_column.iloc[nn]).split("\n")
            count = len(cell_values)
            maxCount = max(maxCount, count)

    # Add new columns to the output DataFrame based on the maximum count
    for nn in range(maxCount):
        df_output[f"value_{nn+1}"] = np.nan  # Create new value columns
        df_output[f"description_{nn+1}"] = None  # Create new description columns

    # Populate the new columns with values and descriptions
    for nn in range(noRows):
        if str(value_column.iloc[nn]) != "nan":
            cell_values = str(value_column.iloc[nn]).split("\n")
            cell_description = str(description_column.iloc[nn]).split("\n")
            count = len(cell_values)
            for ii in range(count):
                df_output.loc[dd[nn], f"value_{ii+1}"] = float(cell_values[ii])
                df_output.loc[dd[nn], f"description_{ii+1}"] = cell_description[ii]

    return df_output


# Define a function named 'transform_data_statistic' to transfrom a dataframe an use it to calculate the ratio/yield of a reaction


def transform_data_statistic(statistic, selected_experiment_list):
    """
    This takes a DataFrame with  peak area and peak names in the same columns and transform in a table with 2 columns named Peak area and Peak names.

    Parameters:
    - statistic (DataFrame): The input DataFrame with peak area and peak names in the same columns.
    - selected_experiment_list (list): list of experiment selected from the chemical space


    Returns:
    - analytic_result (Dataframe): A new DataFrame with 2 columns for Peak area and Peak names.
    """
    # the selected_experiment number is Experiment No._CAS_Number from the chemical space
    selected_experiment_list.sort()
    print(selected_experiment_list)
    # expID is ID that Arksuite gave automatically
    list_expID = statistic["expID"].to_list()
    list_expID_unique = sorted(set(list_expID))

    y = 0
    # creation of an empty columns name "Experiment No._CAS_Number"
    statistic["Experiment No._CAS_Number"] = 0
    for i in list_expID_unique:
        statistic["Experiment No._CAS_Number"].loc[statistic["expID"] == i] = (
            selected_experiment_list[y]
        )
        y += 1

    Peak_area = statistic.loc[statistic["attributeDefinitionLabel"] == "Peak Areas"]
    Peak_name = statistic.loc[statistic["attributeDefinitionLabel"] == "Peak names"]

    Peak_area.rename(columns={"value": "Peak area"}, inplace=True)
    Peak_name.rename(columns={"value": "Peak name"}, inplace=True)

    Peak_area_S = Peak_area[
        ["attributeValueIndex", "Peak area", "expID", "Experiment No._CAS_Number"]
    ]
    Peak_name_s = Peak_name[
        ["attributeValueIndex", "Peak name", "expID", "Experiment No._CAS_Number"]
    ]

    analytic_result = pd.merge(
        Peak_area_S,
        Peak_name_s,
        on=["expID", "attributeValueIndex", "Experiment No._CAS_Number"],
    )

    return analytic_result


def remove_experiments(statistic: pd.DataFrame, ID2Remove: list, selected_experiment_list: list):
    """
    Removes experiments from the statistic DataFrame based on a list of IDs and updates experiment numbering.
    Also updates and returns the selected_experiment_list after removal.

    Parameters:
    - statistic (pd.DataFrame): The DataFrame containing experimental results.
    - ID2Remove (list): List of experiment IDs to be removed.
    - selected_experiment_list (list): List of new experiment names to be mapped to the remaining expIDs.


    Returns:
    - updated_selected_experiment_list (list): The filtered list of selected experiment names.
    """

    if not ID2Remove:
        return selected_experiment_list  # No change if nothing to remove

    # Ensure input validation
    if not isinstance(statistic, pd.DataFrame):
        raise ValueError("Expected 'statistic' to be a pandas DataFrame.")

    if not isinstance(ID2Remove, list):
        raise ValueError("Expected 'ID2Remove' to be a list.")

    if not isinstance(selected_experiment_list, list):
        raise ValueError("Expected 'selected_experiment_list' to be a list.")


    if "expID" not in statistic.columns:
        raise KeyError("Column 'expID' not found in the statistic DataFrame.")


    # Extract unique expID values from statistic before removal
    list_expID_unique = sorted(set(statistic["expID"].to_list()))

    # Sort selected_experiment_list to ensure order
    selected_experiment_list_sorted = sorted(selected_experiment_list)

    # Ensure mapping lengths match
    if len(list_expID_unique) != len(selected_experiment_list_sorted):
        raise ValueError(f"Mismatch in mapping lengths: {len(list_expID_unique)} unique expIDs vs {len(selected_experiment_list_sorted)} selected experiments.")

    # Create a mapping dictionary {expID: selected_experiment_name}
    expID_to_experiment_map = dict(zip(list_expID_unique, selected_experiment_list_sorted))


    # Remove corresponding experiments from selected_experiment_list
    updated_selected_experiment_list = [exp for expID, exp in expID_to_experiment_map.items() if expID not in ID2Remove]


    return updated_selected_experiment_list 
