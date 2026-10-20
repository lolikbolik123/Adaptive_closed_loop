import itertools
import pandas as pd
import os
from pathlib import Path


def create_reaction_scope(
    components,
    directory="./",
    filename="reaction_scope.csv",
    check_overwrite=True,
    chunk_size=1000000,
):
    """
    Reaction scope generator. This function generates all possible combinations of
    reaction parameters and saves them in a CSV file for further processing.

    ----------------------------------------------------------------------
    Example:

    components = {'temperature': [30, 40, 50],
                  'solvent': ['THF', 'DMSO'],
                  'concentration': [0.1, 0.2, 0.3, 0.4, 0.5]}
    ----------------------------------------------------------------------

    ----------------------------------------------------------------------
    Note:
        - All non-numerical choices are encoded using a One-Hot-Encoder.
    ----------------------------------------------------------------------

    ----------------------------------------------------------------------
    Returns:
        A dataframe containing the entire set of reaction conditions (reaction scope),
        saved as a CSV file named *reaction_scope.csv*.
    ----------------------------------------------------------------------
    """
    # Define the full file path for saving the reaction scope.
    filename = directory + "reaction_scope.csv"
    
    # Ensure the components parameter is a dictionary.
    msg = "You need to pass a dictionary for components.\n"
    assert type(components) == dict, msg  # noqa: E721

    print("Generating reaction scope...")
    wdir = Path(directory)  # Convert directory path to a Path object.
    
    # Check if the file already exists and whether to overwrite it.
    if os.path.exists(filename) and check_overwrite is True:
        # print('Sadeed\n')
        # print('Overwriting as of now. Need to confirm from the user usually\n')
        # The usual behavior would be asking the user for confirmation before overwriting.
        overwrite = input("Scope already exists. Overwrite? Y = yes, N = no\n")
        if overwrite.lower() != "y":
            df_scope = pd.read_csv(filename)
            return df_scope

    # ----------------------------------------------
    # Predict the Total Number of Combinations
    # ----------------------------------------------
    # This calculates the total number of unique reaction conditions.
    n_combinations = 0
    for key in list(components.keys()):
        if n_combinations == 0:
            n_combinations = len(components[key])
        else:
            n_combinations *= len(components[key])

    # Calculate the remainder when divided by the chunk size.
    remainder = n_combinations % chunk_size

    # Generate all possible reaction conditions.
    keys = components.keys()  # Extract component names.
    values = (components[key] for key in keys)  # Extract possible values.

    if n_combinations > chunk_size:
        # ----------------------------------------------
        # Handle Large Datasets with Chunking
        # ----------------------------------------------
        # If the number of combinations exceeds the chunk size,
        # process and save them in smaller chunks to optimize memory usage.
        chunck_combination = []  # Store combinations temporarily.
        n_iterations = 0  # Track the number of chunks processed.
        
        for comb in itertools.product(*values):  # Generate all possible combinations.
            chunck_combination.append(comb)
            
            if len(chunck_combination) >= chunk_size:
                # Convert the chunk to a DataFrame.
                df_scope = pd.DataFrame(chunck_combination)
                
                # Save the first chunk with headers, then append subsequent chunks.
                if n_iterations == 0:
                    df_scope.to_csv(
                        filename, index=False, mode="w", header=list(keys)
                    )
                else:
                    df_scope.to_csv(filename, index=False, mode="a", header=False)
                
                # Clear the temporary storage for the next chunk.
                chunck_combination = []
                n_iterations += 1
        
        # Save the last remaining chunk if any combinations are left.
        if remainder > 0:
            df_scope = pd.DataFrame(chunck_combination)
            df_scope.to_csv(filename, index=False, mode="a", header=False)
    
    else:
        # ----------------------------------------------
        # Handle Small Datasets (Single Write)
        # ----------------------------------------------
        # If the number of combinations is small enough, generate all at once.
        scope = [
            dict(zip(keys, combination)) for combination in itertools.product(*values)
        ]

        # Convert to a DataFrame and save it as a CSV file.
        df_scope = pd.DataFrame(scope)
        df_scope.to_csv(filename, index=False, mode="w", header=list(keys))

    # Return the generated reaction scope as a DataFrame.
    return df_scope

