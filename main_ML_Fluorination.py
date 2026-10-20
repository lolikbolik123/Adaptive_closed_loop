import requests
import pandas as pd
import sys
from Create_runAT import (
    authorization,
    calculation,
    create,
    create_json,
    data_transformation,
    automation_PubChem,
    get_article_by_att,
    get_product,
    run,
    edbo_plus_loop,
    gui_attribute,
)

import datetime
import time
import os


################ User Inputs ####################################### 
####################################################################


# Define user-specific variables such as the username, file name, and workflow type.
user_name = "Aidana"  # The name of the user running this script.
file_name = "new_ML_1-4"  # Name of the experiment or project file.
Workflow = "WF44"  # Workflow identifier, specifying the type of process being executed.

# Define the batch size, which determines how many experiments will be optimized in parallel.
batch_size = 6

# Define the maximum number of substrates to optimize in a single iteration.
max_substrate = 4

####################################################################


# ANSI escape codes for bold colored text
RED_BOLD = "\033[1;31m"   # Bold Red
GREEN_BOLD = "\033[1;32m" # Bold Green
BLUE_BOLD = "\033[1;34m"  # Bold Blue
RESET = "\033[0m"         # Reset to default color

# ----------------------------------------------
# Server Connection and Authentication
# ----------------------------------------------
# Define the base URL for the API server, which will be used for making HTTP requests.
base_URL = "http://10.73.58.47/"

# Send a request to the API server to check if it is accessible and responding.
response_API = requests.get(base_URL)
# Print the status code of the response; should be 200 if successful.
response_API.status_code  

# Authenticate the user by obtaining an authorization token.
# This token is required for subsequent API interactions.
token = authorization.login(base_URL)

# ----------------------------------------------
# Define File Paths and User Configuration
# ----------------------------------------------
# Determine the system type to set the correct path for file storage.
# If running on a workstation, store in 'Documents'. Otherwise, use OneDrive.


# Load the input data file containing the chemical space from an Excel spreadsheet.
# The file is expected to be inside the 'Input_user' directory under the user's folder.
data_raw = pd.read_excel(
    "Input_user/"
    + user_name
    + "/"
    + "Edbo_"
    + file_name
    + "/"
    + file_name
    + ".xlsx"
)

# Define labels and paths for output files.
# These paths specify where processed files will be saved.
label = Workflow + "Test_parallelization_" + file_name  # Unique label for experiment output files.

# Main directory for storing input and output files related to this experiment.
path = (
    "Input_user/"
    + user_name
    + "/"
    + "Edbo_"
    + file_name
    + "/"
)

# Directory for storing computed descriptors related to Density Functional Theory (DFT) calculations.
path_dft = (
    "Input_user/"
    + user_name
    + "/"
    + "Edbo_"
    + file_name
    + "/descriptors/"
)

# ----------------------------------------------
# Generate the Chemical Space for Optimization
# ----------------------------------------------
# This function generates the chemical space by identifying possible 
# reaction components and conditions that can be optimized.
# It takes the input dataset and processes it into a structured format
# that can be used for further machine learning-based optimization.
edbo_chemical_space, list_substrate, list_objectives = (edbo_plus_loop.create_chemical_space_with_obj(data_raw, path))

# Save the generated chemical space as a CSV file.
# This file will store all the possible reaction conditions in a tabular format
# and will be referenced later in the workflow.
edbo_chemical_space.to_csv(path + "chemical_space.csv", index=False)

# ----------------------------------------------
# Check for Existing Articles
# ----------------------------------------------
# This section checks if the chemical articles (compounds) required for the experiments
# already exist in the database or if they need to be retrieved from external sources (e.g., PubChem).

# Transform the raw dataset based on the selected workflow type.
# Different workflows might require different data transformations.
data_T = data_transformation.DT_with_processing_method(edbo_chemical_space, Workflow)

# Save the transformed dataset to a CSV file for future reference.
data_T.to_csv(path + "Data_T.csv", index=False)

# Reload the transformed data into a pandas DataFrame for further processing.
test_1 = pd.read_csv(path + "Data_T.csv")

# Remove duplicate compound entries from the dataset to prevent redundant processing.
compounds_cas = data_transformation.DT_filtered(data_T)

# Query the database to check if these compounds already exist.
# This function returns a list of existing compounds based on their CAS numbers.
CASNumber_exist = get_article_by_att.exist_article(base_URL, token, compounds_cas)

# Identify the compounds that are missing and need to be fetched from external sources.
add_article = get_article_by_att.new_article(CASNumber_exist, compounds_cas)

# If new compounds are required, fetch their attributes from PubChem and store them in a file.
if add_article != []:
    # Retrieve compound attributes such as molecular weight, formula, etc.
    att_new_article = automation_PubChem.attributes_PubChem(add_article)
    
    # Merge the retrieved attributes with the transformed dataset to ensure consistency.
    att_new_article = pd.merge(att_new_article, data_T, how="inner", on="CAS Number")
    
    # Save the retrieved attributes to a CSV file for further use.
    att_new_article.to_csv(path + "new_article.csv")

    # Use a graphical user interface (GUI) to manually input missing attributes if needed.
    attribute_GUI = gui_attribute.value_gui_to_dataframe(att_new_article)

    # Create new articles in the database using the retrieved attributes.
    no_add, new_article = create.create_article(base_URL, token, attribute_GUI)
    
    print('***********New articles are added****************')
    raise ValueError('Re-run after adding the density values')
    
    

# Retrieve attributes for all compounds present in the Design of Experiments (DOE).
all_att_DOE = get_article_by_att.get_att_byCASNumber_test(base_URL, token, test_1)

# Save the DOE attributes to a CSV file for use in experiment planning.
all_att_DOE.to_csv(path + "DOE_ready_run_before_calc/" + label + ".csv")

# ----------------------------------------------
# Check and Create Missing Products
# ----------------------------------------------
# This section checks if the required products already exist in the database and
# creates new ones if they are missing.

# Query the database to check for existing products.
product_tocreate = get_product.exist_product(base_URL, token, all_att_DOE)

# If missing products are identified, create them in the database.
new_product = create.create_product(base_URL, token, product_tocreate)

# Log the newly created products to the console for verification.
print(new_product)

# If no new products were created, inform the user.
if new_product.empty:
    print("There is no new product")
else:
    # Save the details of newly created products to a CSV file.
    # The file is named using the current date to maintain version control.
    new_product.to_csv(
        path+"New_product/"+ datetime.date.today().strftime("%Y%m%d")+ ".csv"
    )

# ----------------------------------------------
# Generate the Chemical Space for Optimization
# ----------------------------------------------
# This function generates the chemical space by identifying possible 
# reaction components and conditions that can be optimized.
# It takes the input dataset and processes it into a structured format
# that can be used for further machine learning-based optimization.
edbo_chemical_space, list_substrate, list_objectives = (
    edbo_plus_loop.create_chemical_space_with_obj(data_raw, path)
)

# Save the generated chemical space as a CSV file.
# This file will store all the possible reaction conditions in a tabular format
# and will be referenced later in the workflow.
edbo_chemical_space.to_csv(path + "chemical_space.csv", index=False)

# ----------------------------------------------
# Bayesian Optimization Loop
# ----------------------------------------------
# Define the number of different substrates present in the dataset
number_subrate = len(list_substrate)

# Initialize an array to store the maximum yield obtained for each substrate.
# Initially, all values are set to zero, meaning no optimization has been performed yet.
max_yield = [0] * number_subrate

# Initialize iteration counters for each substrate.
# This tracks how many rounds of optimization have been performed.
iteration = [1] * number_subrate



# ANSI escape codes for red bold text
RED_BOLD = "\033[1;31m"
RESET = "\033[0m"

# Flag to track if user input is already provided
user_decision = None  

# Prepare the data by adding Density Functional Theory (DFT) descriptors.
for i in list_substrate:
    
    dft_file_name = path + "data_with_dft" + i + ".csv"
    dft_file_name_short = "data_with_dft" + i + ".csv"
    
    # Check if any DFT file exists
    file_exists = os.path.exists(dft_file_name)
    
    if file_exists and user_decision is None:
        # Prompt user only once
        user_choice = input(
            f"{RED_BOLD}\nSome DFT files already exist.\n"
            "Do you want to USE the existing files where available? [Yes/No]: " 
            f"{RESET}"
        ).strip().lower()
        
        user_decision = user_choice in ["yes", "y"]  # Convert input to boolean

    # If the file exists and the user chose "Use", skip this substrate
    if file_exists and user_decision:
        print(f"{BLUE_BOLD}Using existing file: {dft_file_name_short}{RESET}")
        
        # retain priority=-1 and reset priority=1 to priority =0
        read_dft = pd.read_csv(dft_file_name)
        
        if "priority" in read_dft.columns:

            # Reset all rows where 'yield' is "PENDING" to have priority=0
            read_dft.loc[read_dft["yield"] == "PENDING", "priority"] = 0
        
            # Check if 'priority' column contains -1
            if not (read_dft["priority"] == -1).any():
                # Drop 'yield' and 'priority' columns if no -1 exists in 'priority'
                read_dft.drop(columns=["yield", "priority"], inplace=True)
        
        columns_to_remove_from_optimization = read_dft.iloc[
            :, : read_dft.columns.get_loc("reaction scale (mmol)")+1
        ]
        
        # Save the updated file
        read_dft.to_csv(dft_file_name, index=False)
        
        continue  # Skip regeneration
            
    # Filter the chemical space to include only data relevant to the current substrate.
    edbo_chemical_space_filtered = edbo_chemical_space[edbo_chemical_space["SM1_Extended"] == i]
    
    # Add DFT descriptors to the filtered dataset.
    add_dft, columns_to_remove_from_optimization = edbo_plus_loop.add_dft2(
        edbo_chemical_space_filtered, path_dft
    )
    
    # Save the updated dataset with DFT descriptors.
    add_dft.to_csv(dft_file_name, index=False)
    
    print(f"{GREEN_BOLD}Generated new file: {dft_file_name_short}{RESET}")

    

# Start the Bayesian optimization loop.
# The loop continues until the maximum yield for each substrate meets or exceeds its objective.
while any(element1 < element2 for element1, element2 in zip(max_yield, list_objectives)):
    
    # Identify which substrates have not yet reached their target yield.
    indices = [
        i
        for i, (yield_value, obj_value) in enumerate(zip(max_yield, list_objectives))
        if yield_value < obj_value
    ]
    
    # Limit the number of substrates processed per iteration to `max_substrate`.
    indices = indices[:max_substrate] if len(indices) > max_substrate else indices
    
    # ----------------------------------------------
    # Perform Bayesian Optimization for Each Substrate
    # ----------------------------------------------
    all_selected_experiment = []  # List to store selected experiments across all substrates.
    
    for i in indices:
        current_substrate = list_substrate[i]
        
        # Load the dataset corresponding to the current substrate.
        add_dft = pd.read_csv(path + "data_with_dft" + current_substrate + ".csv")
        csv_name = "data_with_dft" + current_substrate + ".csv"
        
        # Run Bayesian optimization using EDBO+ for the current substrate.
        optimization, selected_experiment = edbo_plus_loop.optimization_multiple(
            add_dft, batch_size, columns_to_remove_from_optimization, iteration, path, csv_name
        )
        
        # Append the selected experiments to the list of all experiments.
        all_selected_experiment = all_selected_experiment + selected_experiment

    # ----------------------------------------------
    # Process Optimization Results
    # ----------------------------------------------
    # Load the DOE (Design of Experiments) dataset.
    all_att_DOE = pd.read_csv(path + "DOE_ready_run_before_calc/" + label + ".csv")
    
    # Calculate the required amount of each chemical for the selected experiments.
    DOE_complete = calculation.amount_ML(all_att_DOE, all_selected_experiment)
    
    # Save the updated DOE dataset containing calculated amounts.
    DOE_complete.to_csv(path + "DOE_ready_run/" + label + str(iteration) + ".csv")
    
    # ----------------------------------------------
    # JSON File Generation Based on Workflow Selection
    # ----------------------------------------------
    # Depending on the workflow type, generate a JSON file with the experiment details.
    if Workflow == "WF44":
        json_file = create_json.WF44_Swing_SP_thermal_reaction(DOE_complete, label)
    elif Workflow == "WF61":
        json_file = create_json.WF61_GC(DOE_complete, label)
    else:
        print("The reaction type is not specified or not recognized, please check again")
    
    # ----------------------------------------------
    # Creation and Execution of a New Experimental Run
    # ----------------------------------------------
    # Start a new run using the generated JSON file.
    runID, list_expID, list_productID = run.new_run(
        base_URL, token, json_file, label, path
    )
    print(runID)  # Print the assigned run ID for tracking.
    
    # Monitor the status of the run to check its progress.
    status_runID = run.status_run(base_URL, token, runID)
    print(status_runID)  # Display the current status of the run.

    """
    ############################################################################################################
    ############################################################################################################
    Now the run is queued in the Arcsuite. We have to wait till the run is executed and analysed
    so that we have the results and move to optimize and calculate the next batch of experiments. 
    ############################################################################################################
    ############################################################################################################
    """

    #sys.exit()

    while status_runID != "Completed":
        # Check the status of the run
        status_runID = run.status_run(base_URL, token, runID)
        print(f"Current Run ID: {runID} - Status: {status_runID}")
    
        # Handle authentication error by regenerating the token
        if status_runID == "not completed - authentification error":
            token = authorization.login(base_URL)
    
        # If the run is canceled, show the popup
        elif status_runID == "Canceled":
            new_runID = gui_attribute.prompt_new_runID(runID)  # Show popup with the current run ID
    
            if new_runID:  # If user provided a new run ID
                try:
                    runID = int(new_runID)  # Convert the new run ID to an integer
                    print(f"Updated run ID: {runID}")
                    status_runID = run.status_run(base_URL, token, runID)  # Check status of the new run ID
                    continue  # Restart the loop with the new run ID
                except ValueError:
                    print("Invalid input! Run ID must be a number. Please enter again.")
                    continue  # Ask for a new input again
    
            else:
                print("No new Run ID provided.")
    
        else:
            time.sleep(10 * 60)  # Wait for 10 minutes before checking again

    # generation of a new token
    token = authorization.login(base_URL)

    # Retrieve the GC/UPLC results from ArcSuite
    statistic = run.statistic(base_URL, token, runID, list_expID, path)
    
    # Make a backup copy of the original statistic DataFrame
    statistic_original = statistic.copy()
    
    # Verify experiment data and get the list of IDs to remove
    statistic, ID2Remove = gui_attribute.verify_experiment_data(statistic)
    
    # ---------------------- Removing Unwanted Experiments ----------------------
    
    # Call the remove_experiments function to clean up and update experiment data
    all_selected_experiment = data_transformation.remove_experiments(statistic_original, ID2Remove, all_selected_experiment)
    
    # if all the experiments were failed, skip furthrer processing and run new experiments
    if statistic.empty:
        print("Statistic DataFrame is empty. Skipping this iteration.")
        continue  # Skip the rest of the iteration and restart the loop
        
    # ---------------------------------------------------------------------------

    # Transform the data extract from arksuite in a dataframe
    data_statistic = data_transformation.transform_data_statistic(
        statistic, all_selected_experiment
    )

    data_statistic.to_csv(path + "data_stat" + str(iteration) + ".csv", index=False)

    # Calculate the ratio between product and internal standard
    ratio = calculation.ratio_analysis(data_statistic, list_expID)

    ratio.to_csv(path + "ratio" + str(iteration) + ".csv", index=False)

    ### Add yield in each optimization dataframe

    for index, i in enumerate(list_substrate):
        # read optimization for each substrate
        optimization = pd.read_csv(path + "data_with_dft" + i + ".csv")
        # take the value of the iteration for each substrate
        iteration_by_subtrate = iteration[index]
        # Add the ratio/yield in the dataframe (chemical space)
        new_yields, current_max = edbo_plus_loop.add_yield(
            optimization, ratio, iteration_by_subtrate, path
        )
        max_yield[iteration_by_subtrate] = current_max
        new_yields.to_csv(
            path + "new_yield_" + i + str(iteration) + ".csv", index=False
        )

        # Drop the columns iteration - otherwise there will be an error when you run the edbo package
        add_dft = new_yields.drop(columns=["iteration"])
        add_dft.to_csv(path + "data_with_dft" + i + ".csv", index=False)
        add_dft.to_csv(
            path + "data_iteration" + i + str(iteration) + ".csv", index=False
        )

    iteration = [x + 1 for x in iteration]

    print(iteration)
    
    print('Reached End')


# print(
#     "Bayesian optimization reach the objective of "
#     + objective
#     + "of yield for the reaction "
#     + label
#     + "after "
#     + iteration
#     + "iterations of "
#     + batch_size
#     + "experiments"
# )
