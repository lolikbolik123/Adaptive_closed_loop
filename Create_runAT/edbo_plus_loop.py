import pandas as pd

from edbo.plus.optimizer_botorch import EDBOplus
from edbo.plus import scope_generator
import seaborn as sns

def create_chemical_space(data_raw, path):
    """
    This function select

    Parameters:
    - chemical_space (dataframe): Data that define the chemical space with the corresponding descriptors for each chemical
    - batch_size (int): number of experiment by run

    Returns:
    - optimization (dataframe): A dataframe with a priority list where priority=1 significate that the reaction need to be perform on the platform
    - select_experiment(list): list of experiement selected by the algorithm
    """
    DF = data_raw.dropna(axis=1, how="all")
    DF = DF.fillna("-")
    dict_scope = DF.to_dict("list")
    cleaned_data = {k: [bb for bb in b if bb != "-"] for k, b in dict_scope.items()}

    scope = scope_generator.create_reaction_scope(cleaned_data, directory=path)
    scope.insert(
        loc=0, column="Experiment No.", value=list(range(1, len(scope.index) + 1))
    )
    # scope.rename(columns={ scope.columns[1]: "Experiment No." }, inplace = True)

    return scope

def create_chemical_space_with_obj(data_raw, path):
    """
    This function generates a structured chemical space from raw data.
    It cleans the dataset, organizes reaction components, and integrates objective values.

    Parameters:
    - data_raw (DataFrame): Raw input data containing chemical space details.
    - path (str): Directory path where output files will be saved.

    Returns:
    - scope (DataFrame): A structured dataframe defining the chemical space,
      with reaction conditions, experiment numbers, and processing methods.
    - list_substrate (list): A list of unique substrates extracted from the data.
    - list_objectives (list): A list of objective values associated with reactions.
    """
    
    # ----------------------------------------------
    # Data Preprocessing: Clean and Structure the Chemical Space
    # ----------------------------------------------

    
    # Step 1: Identify all columns that end with "_extended"
    extended_columns = [col for col in data_raw.columns if col.endswith('_Extended')]
    
    # Step 2: Find columns to delete (six columns to the left of each "_extended" column)
    columns_to_delete = set()  # Using a set to avoid duplicates
    
    for col in extended_columns:
        col_index = data_raw.columns.get_loc(col)  # Get index position of the "_extended" column
        if col_index >= 7:  # Ensure there are at least 7 columns before it
            columns_to_delete.update(data_raw.columns[col_index-7:col_index])
        else:  # If less than 6 columns exist before, remove all available ones
            columns_to_delete.update(data_raw.columns[:col_index])
    
    # Step 3: Drop identified columns
    DF_essential_raw = data_raw.drop(columns=columns_to_delete)
    
    # Remove columns that contain only NaN values.
    DF = data_raw.dropna(axis=1, how="all")
    DF_essential = DF_essential_raw.dropna(axis=1, how="all")
    
    # Drop specific columns that are not needed for chemical space creation.
    DF = DF.drop(['Objective', 'Processing_method'], axis=1)
    DF_essential = DF_essential.drop(['Objective', 'Processing_method'], axis=1)
    
    # Replace all remaining NaN values with "-" to ensure uniformity.
    DF = DF.fillna("-")
    DF_essential = DF_essential.fillna("-")
    
    
    

 

    # Convert dataframe to a dictionary with column names as keys and lists as values.
    dict_scope = DF_essential.to_dict("list")
    

    # Remove all instances of "-" from the lists to clean the dataset.
    cleaned_data = {k: [bb for bb in b if bb != "-"] for k, b in dict_scope.items()}
    
    # ----------------------------------------------
    # Generate the Reaction Scope
    # ----------------------------------------------
    # Create the reaction scope using the cleaned dataset.
    scope = scope_generator.create_reaction_scope(cleaned_data, directory=path)
    
    # Insert an experiment number column, starting from 1 to the total number of experiments.
    scope.insert(
        loc=0, column="Experiment No.", value=list(range(1, len(scope.index) + 1))
    )
    
    # ----------------------------------------------
    # Extract Key Lists for Further Processing
    # ----------------------------------------------
    # Extract the list of unique substrates (SM1 column) from the raw data.
    list_substrate = DF_essential_raw["SM1_Extended"].dropna().to_list()
    
    # Extract the list of objective values from the raw data.
    list_objectives = DF_essential_raw["Objective"].dropna().to_list()
    
    # ----------------------------------------------
    # Integrate Processing Method Information
    # ----------------------------------------------
    # Merge the reaction scope with the 'Processing_method' from the original dataset.
    merged_df = scope.merge(DF_essential_raw[['SM1_Extended', 'Processing_method']], on='SM1_Extended', how='left')
    
    # Update the 'Processing_method' column in the scope DataFrame.
    scope['Processing_method'] = merged_df['Processing_method']
    
    # ----------------------------------------------
    # Return the Processed Data
    # ----------------------------------------------
    return scope, list_substrate, list_objectives


def optimization_multiple(chemical_space, batch_size, columns_to_drop, iteration, path,csv_name):
    """
    This function use the bayesian optimisation (EDBO plus package from Doyle's group) to optimize the yield of the reaction

    Parameters:
    - chemical_space (dataframe): Data that define the chemical space with the corresponding descriptors for each chemical
    - batch_size (int): number of experiment by run
    - columns_to_drop(list): columns that we don't want to use for the bayesian optimization
    - path(string); path to save the excel file after each iteration of the optimization

    Returns:
    - optimization (dataframe): A dataframe with a priority list where priority=1 significate that the reaction need to be perform on the platform
    - select_experiment(list): list of experiement selected by the algorithm
    """

    df_to_opt = chemical_space
    regression_columns = df_to_opt.columns.drop(columns_to_drop).values.tolist()

    opt = EDBOplus()
    """
        Parameters
        ----------
        objectives: list
            list of string containing the name for each objective.
            Example:
                objectives = ['yield', 'cost', 'impurity']

        objective_mode: list
            list to select whether the objective should be maximized or minimized.
            Examples:
                A) Example for single-objective optimization:
                    objective_mode = ['max']
                B) Example for multi-objective optimization:
                    objective_mode = ['max', 'min', 'min']

        objective_thresholds: list
            List of worst case values for each objective.
            Example:
                objective_threshold = [50.0, 10.0, 10.0]

        columns_features: list
            List containing the names of the columns to be included in the regression model. By default set to
            'all', which means the algorithm will automatically select all the columns that are not in
            the *objectives* list.

        batch: int
            Number of experiments that you want to run in parallel. For instance *batch = 5* means that you
            will run 5 experiments in each EDBO+ run. You can change this number at any stage of the optimization,
            so don't worry if you change  your mind after creating or initializing the reaction scope.

        get_predictions: boolean
            If True it will print out a *csv file* with the predictions.
            You can also access the *predicted_mean* and *predicted_variance* through the EDBOPlus class.

        directory: string
            name of the directory to save the results of the optimization.

        filename: string
            Name of the file to save a *csv* with the priority list. If *get_predictions=True* EDBO+ will automatically
            save a second file including the predictions (*pred_filename.csv*).

        init_sampling_method: string:
            Method for selecting the first samples in the scope (in absence)  Choices are:
            - 'seed' : Random seed (as implemented in Pandas).
            - 'lhs' : LatinHypercube sampling.
            - 'cvtsampling' : CVT sampling.

        scaler_features: sklearn class
            sklearn.preprocessing class for transforming the features.
            Example:
                sklearn.preprocessing.MinMaxScaler()

        scaler_objectives: sklearn class
            sklearn.preprocessing class for transforming the objective values.
            Examples:
                - sklearn.preprocessing.StandardScaler()
            Default:
                EDBOStandardScaler()

        seed: int
            Seed for the random initialization.

        acquisition_function_sampler: string
            Options are: 'SobolQMCNormalSampler' or 'IIDNormalSampler'.

        """
    opt.run(
        filename=csv_name,
        objectives=["yield"],
        objective_mode=["max"],
        objective_thresholds=[None],
        batch=batch_size,
        init_sampling_method="seed",
        columns_features=regression_columns,
        directory=path,
    )

    optimization = pd.read_csv(path + csv_name)
    select_experiment = optimization.loc[optimization["priority"] == 1]
    selected_experiment_list = list(select_experiment["Experiment No."])

    return optimization, selected_experiment_list
# Define a function named optimization that use the bayesian optimization from edboplus package to predict the new run of a reaction


def optimization(chemical_space, batch_size, columns_to_drop, iteration, path):
    """
    This function use the bayesian optimisation (EDBO plus package from Doyle's group) to optimize the yield of the reaction

    Parameters:
    - chemical_space (dataframe): Data that define the chemical space with the corresponding descriptors for each chemical
    - batch_size (int): number of experiment by run
    - columns_to_drop(list): columns that we don't want to use for the bayesian optimization
    - path(string); path to save the excel file after each iteration of the optimization

    Returns:
    - optimization (dataframe): A dataframe with a priority list where priority=1 significate that the reaction need to be perform on the platform
    - select_experiment(list): list of experiement selected by the algorithm
    """

    df_to_opt = chemical_space
    regression_columns = df_to_opt.columns.drop(columns_to_drop).values.tolist()

    opt = EDBOplus()
    """
        Parameters
        ----------
        objectives: list
            list of string containing the name for each objective.
            Example:
                objectives = ['yield', 'cost', 'impurity']

        objective_mode: list
            list to select whether the objective should be maximized or minimized.
            Examples:
                A) Example for single-objective optimization:
                    objective_mode = ['max']
                B) Example for multi-objective optimization:
                    objective_mode = ['max', 'min', 'min']

        objective_thresholds: list
            List of worst case values for each objective.
            Example:
                objective_threshold = [50.0, 10.0, 10.0]

        columns_features: list
            List containing the names of the columns to be included in the regression model. By default set to
            'all', which means the algorithm will automatically select all the columns that are not in
            the *objectives* list.

        batch: int
            Number of experiments that you want to run in parallel. For instance *batch = 5* means that you
            will run 5 experiments in each EDBO+ run. You can change this number at any stage of the optimization,
            so don't worry if you change  your mind after creating or initializing the reaction scope.

        get_predictions: boolean
            If True it will print out a *csv file* with the predictions.
            You can also access the *predicted_mean* and *predicted_variance* through the EDBOPlus class.

        directory: string
            name of the directory to save the results of the optimization.

        filename: string
            Name of the file to save a *csv* with the priority list. If *get_predictions=True* EDBO+ will automatically
            save a second file including the predictions (*pred_filename.csv*).

        init_sampling_method: string:
            Method for selecting the first samples in the scope (in absence)  Choices are:
            - 'seed' : Random seed (as implemented in Pandas).
            - 'lhs' : LatinHypercube sampling.
            - 'cvtsampling' : CVT sampling.

        scaler_features: sklearn class
            sklearn.preprocessing class for transforming the features.
            Example:
                sklearn.preprocessing.MinMaxScaler()

        scaler_objectives: sklearn class
            sklearn.preprocessing class for transforming the objective values.
            Examples:
                - sklearn.preprocessing.StandardScaler()
            Default:
                EDBOStandardScaler()

        seed: int
            Seed for the random initialization.

        acquisition_function_sampler: string
            Options are: 'SobolQMCNormalSampler' or 'IIDNormalSampler'.

        """
    opt.run(
        filename="data_with_dft.csv",
        objectives=["yield"],
        objective_mode=["max"],
        objective_thresholds=[None],
        batch=batch_size,
        init_sampling_method="seed",
        columns_features=regression_columns,
        directory=path,
    )

    optimization = pd.read_csv(path + "data_with_dft.csv")
    select_experiment = optimization.loc[optimization["priority"] == 1]
    selected_experiment_list = list(select_experiment["Experiment No._CAS_Number"])

    return optimization, selected_experiment_list


# Define a function named add_yield to add the yield of reactions run on the platform


def add_yield(optimization, analytic_result, iteration, path):
    """
    This function add yield of the reaction that have a priority =1 in the dataframe generate after using the function optimization.

    Parameters:
    - optimization (dataframe): A dataframe with a priority list where priority=1 significate that the reaction need to be perform on the platform
    - analytic_result (dataframe); A dataframe with the run ID, experiments ID and analytical result
    - iteration (int) : loop iteration, starting from 1 - to see the improvemnt through the iteration

    Returns:
    - optimization (dataframe): A dataframe with the yield added for the experiement that have a priority=1
    """

    index = []
    max_obs = []

    # select rows where we have to write the yield
    data_select = optimization.loc[optimization["priority"] == 1]
    list_exp = data_select["Experiment No._CAS_Number"]

    optimization["iteration"] = 0

    # transform the dataframe analytic_resutl to dictionnary
    analytic_result = analytic_result.set_index("Experiment No._CAS_Number")
    dict_analytic_result = analytic_result["ratio"].to_dict()

    for y in list_exp.to_list():
        
       
        
        
        optimization["yield"].loc[optimization["Experiment No._CAS_Number"] == y] = (
            dict_analytic_result[y]
        )

        optimization.loc[optimization["Experiment No._CAS_Number"] == y, "iteration"] = iteration

    # plot the data - max yield observed versus the iteration of the Bayesian algorithm

    reduce_opt = optimization[optimization["iteration"] > 0]

    reduce_opt["yield"] = reduce_opt["yield"].astype(float)
    current_max = reduce_opt["yield"].max()
    max_obs.append(current_max)
    index.append(iteration)
    print(current_max)
    """
    dict = {"max_obs": max_obs, "iteration": index}
    df = pd.DataFrame(dict)

    sns.scatterplot(
        data=df.groupby("iteration")["max_obs"].max().to_frame(),
        x="iteration",
        y="max_obs",
    )
    """

    return optimization, current_max 


# Define a function named add_dft to add dft descriptors on chemicals


def add_dft(chemical_space, path_dft):
    """
    Add the dft calculation contained in different csv files in one dataframe to use it for the Bayesian optimisation

    Parameters:
    - chemical_space(dataframe): dataframe that contains all the combinations possible regarding the differnts components tested
    - path_dft(str): path where the dft csv files are stored

    returns:
    - merged_df (dataframe): dataframe that contains all experiment with all the descriptors for each components

    """

    # Select the columns that can have dft descriptors
    selected_columns = chemical_space.iloc[
        :, : chemical_space.columns.get_loc("reaction scale (mmol)")
    ]

    # Create a list to store the new column names
    new_column_names = []

    # Iterate through existing column names
    for col in chemical_space.columns:
        # Add "_CAS_Number" to column names before "column3", keep others unchanged
        new_column_names.append(
            col + "_CAS_Number" if col in selected_columns.columns else col
        )

    # Rename columns in the DataFrame
    chemical_space.columns = new_column_names

    # Create variables with dynamic name based on column names to be able to read the different csv files
    # In the loop first look if there is a csv files corresponding for the columns present in the selected columns
    # One csv file - dft data related all components in one columns of the chemical space dataframe
    list_df = []
    list_key = []

    for i, col_name in enumerate(selected_columns.columns):
        try:
            col_name_trimmed = col_name[:-9] if col_name.endswith("_Extended") else col_name
            globals()[col_name] = pd.read_csv(path_dft + col_name_trimmed + ".csv")
            list_df.append(globals()[col_name])
            key = [col for col in globals()[col_name].columns if "CAS_Number" in col]
            list_key.append(key[0])
        except:  # noqa: E722
            continue

    merged_df = chemical_space  # Start with the first DataFrame

    for i in range(0, len(list_df)):
        # Access DataFrames by index for clarity (avoid globals)
        current_df = list_df[i]
        # Define key columns based on DataFrame order (assuming appropriate key names)
        key = list_key[i]  # Use f-string for dynamic key column names

        merged_df = merge_dataframes(
            merged_df, current_df, key
        )  # Optional: Use the helper function

    return merged_df, new_column_names


def add_dft2(chemical_space, path_dft):
    """
    Add the dft calculation contained in different csv files in one dataframe to use it for the Bayesian optimisation

    Parameters:
    - chemical_space(dataframe): dataframe that contains all the combinations possible regarding the differnts components tested
    - path_dft(str): path where the dft csv files are stored

    returns:
    - merged_df (dataframe): dataframe that contains all experiment with all the descriptors for each components

    """

    extended_columns = [col for col in chemical_space.columns if col.endswith("_Extended")]
    
    
    # Create a mapping of original column names to their stripped versions
    column_mapping = {col: col.replace("_Extended", "") for col in extended_columns}
    
    # Process each column and merge based on the stripped name
    for extended_col, stripped_col in column_mapping.items():
        
        try:
    
            file2_path = path_dft+stripped_col+".csv"
            df2 = pd.read_csv(file2_path)
            
            # Extract the first part before "_" in "sulfonyl_fluoride_Extended"
            chemical_space = chemical_space.copy()
            chemical_space.loc[:, stripped_col+"_Key"] = chemical_space[extended_col].astype(str).str.split("_").str[0]
        
            # Merge based on the extracted key from df1 and "sulfonyl_fluoride" column in df2
            chemical_space = chemical_space.merge(df2, left_on=stripped_col+"_Key", right_on=stripped_col, how="left")
            
            # Select relevant columns and drop unnecessary ones
            chemical_space = chemical_space.drop(columns=[stripped_col+"_Key", stripped_col])
        except:
        
            continue
        
    # Add two new columns to the dataframe 'chemical_space'
    # chemical_space["yield"] = "PENDING"
    # chemical_space["priority"] = 0
                
    selected_columns = chemical_space.iloc[
        :, : chemical_space.columns.get_loc("reaction scale (mmol)")+1
    ]
    
    return chemical_space, selected_columns.columns



# Define a function named merge_dataframes to merge two dataframes
def merge_dataframes(left_df, right_df, key):
    """
    Merges two DataFrames on specified key columns.

    Args:
        left_df: The left DataFrame for the merge.
        right_df: The right DataFrame for the merge.
        left_key: The key column in the left DataFrame.
        right_key: The key column in the right DataFrame.

    Returns:
        The merged DataFrame.
    """
    return pd.merge(left_df, right_df, on=key)
