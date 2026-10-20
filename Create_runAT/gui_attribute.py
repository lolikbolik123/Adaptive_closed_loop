import tkinter as tk
from tkinter import ttk
import pandas as pd

import sys
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

### class GUI###


class App(tk.Tk):

    def __init__(self, data_dict, cas_number):
        super().__init__()
        self.geometry("500x300")
        self.title("Create a new article")

        # initialize data
        self.languages = ("4NH", "GDU-PFD", "GDU-S", "GDU-V")
        self.stocksolution = ("Yes", "No")

        # set up variable
        self.option_var1 = tk.StringVar(self)
        self.option_var2 = tk.StringVar(self)
        self.entry_MolarConcentration = tk.StringVar(self)
        self.entry_chembeads = tk.StringVar(self)

        # create widget
        self.create_wigets_tool()

        # create an the variable dictionnary
        self.dict_var = data_dict

        # create name of Article
        self.create_name_article(cas_number)

    def create_wigets_tool(self):
        # padding for widgets using the grid layout
        paddings = {"padx": 5, "pady": 5}

        # label - Dispense tool
        label = ttk.Label(self, text="Select the tool to dispense the product")
        label.grid(column=0, row=1, sticky=tk.W, **paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var1,
            self.languages[1],
            *self.languages,
            command=self.option_changed_tool,
        )

        option_menu.grid(column=1, row=1, sticky=tk.W, **paddings)

        # output label
        self.output_label = ttk.Label(self, foreground="red")
        self.output_label.grid(column=0, row=3, sticky=tk.W, **paddings)

    def create_name_article(self, cas_number):
        paddings = {"padx": 5, "pady": 5}
        # Create a label to display the article name
        self.label_name = ttk.Label(self, text=f"Article Name: {cas_number}")
        self.label_name.config(font=("arial", 12))
        self.label_name.grid(
            column=0, row=0, sticky=tk.W, **paddings
        )  # Position the label (right-aligned)

    def create_wigets_StockSolution(self):
        # padding for widgets using the grid layout
        paddings = {"padx": 5, "pady": 5}

        # label - Stock solution ?
        label2 = ttk.Label(self, text="Is it a stock solution ?")
        label2.grid(column=0, row=5, sticky=tk.W, **paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var2,
            self.stocksolution[1],
            *self.stocksolution,
            command=self.option_changed_StockSolution,
        )

        option_menu.grid(column=1, row=5, sticky=tk.W, **paddings)

        # output label
        self.output_label2 = ttk.Label(self, foreground="red")
        self.output_label2.grid(column=0, row=6, sticky=tk.W, **paddings)

    def create_wigets_MolarConcentration(self):
        # padding for widgets using the grid layout
        paddings = {"padx": 5, "pady": 5}

        # label - Stock solution
        label3 = ttk.Label(self, text="What is the concentration in mol/l")
        label3.grid(column=0, row=7, sticky=tk.W, **paddings)

        # option menu
        entry_concentration = ttk.Entry(
            self, textvariable=self.entry_MolarConcentration
        )

        entry_concentration.grid(column=1, row=7, sticky=tk.W, **paddings)

        sub_btn = tk.Button(
            self, text="Submit", command=self.option_changed_MolarConcentration
        )

        sub_btn.grid(column=2, row=7, sticky=tk.W, **paddings)

        # output label
        self.output_label3 = ttk.Label(self, foreground="red")
        self.output_label3.grid(column=0, row=8, sticky=tk.W, **paddings)

    def create_wigets_Chembeads(self):
        # padding for widgets using the grid layout
        paddings = {"padx": 5, "pady": 5}

        # label - Chembeads
        label3 = ttk.Label(
            self,
            text="What is the chembeads factor ( if mix 20% reagents - factor =100/20=5) ?",
        )
        label3.grid(column=0, row=9, sticky=tk.W, **paddings)

        # option menu
        entry_chembeads = ttk.Entry(self, textvariable=self.entry_chembeads)

        entry_chembeads.grid(column=0, row=10, sticky=tk.W, **paddings)

        sub_btn = tk.Button(self, text="Submit", command=self.option_changed_Chembeads)

        sub_btn.grid(column=1, row=10, sticky=tk.W, **paddings)

        # output label
        self.output_label4 = ttk.Label(self, foreground="red")
        self.output_label4.grid(column=0, row=11, sticky=tk.W, **paddings)

    def option_changed_tool(self, *args):

        self.output_label["text"] = f"You selected: {self.option_var1.get()}"
        if self.option_var1.get() == "4NH":
            self.dict_var["Dispense Tool Volumetrically"] = self.option_var1.get()
            self.create_wigets_StockSolution()

        elif self.option_var1.get() == "GDU-PFD" or self.option_var1.get() == "GDU-S":
            self.dict_var["Dispense Tool Gravimetrically"] = self.option_var1.get()
            self.create_wigets_Chembeads()

        else:
            self.dict_var["Dispense Tool Gravimetrically"] = self.option_var1.get()

    def option_changed_StockSolution(self, *args):
        self.output_label2["text"] = f"You selected: {self.option_var2.get()}"
        if self.option_var2.get() == "Yes":
            self.dict_var["Stock solution"] = self.option_var2.get()
            self.create_wigets_MolarConcentration()
        else:
            self.dict_var["Stock solution"] = self.option_var2.get()

    def option_changed_MolarConcentration(self, *args):
        self.output_label3["text"] = (
            f"The concentration of the stock solution is : {self.entry_MolarConcentration.get()} mol/l"
        )
        self.dict_var["Molar concentration"] = self.entry_MolarConcentration.get()

    def option_changed_Chembeads(self, *args):
        self.output_label4["text"] = (
            f"The chembead factor is : {self.entry_chembeads.get()}"
        )
        self.dict_var["ChemBeads Factor"] = self.entry_chembeads.get()

    def run(self):
        """Starts the main event loop to display the app."""
        self.mainloop()


class ExpIDPopup(QWidget):
    def __init__(self, exp_id, ID2Remove, new_rows):
        super().__init__()

        self.exp_id = exp_id
        self.ID2Remove = ID2Remove
        self.new_rows = new_rows

        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Experiment ID {self.exp_id} - Missing Data")
        self.setGeometry(400, 200, 350, 250)

        layout = QVBoxLayout()

        label = QLabel(f"Experiment ID {self.exp_id} is missing 'Dodecane'.")
        layout.addWidget(label)

        self.dodecane_label = QLabel("Dodecane Peak Areas:")
        layout.addWidget(self.dodecane_label)
        self.dodecane_input = QLineEdit()
        layout.addWidget(self.dodecane_input)

        self.product_label = QLabel("Product Peak Areas:")
        layout.addWidget(self.product_label)
        self.product_input = QLineEdit()
        layout.addWidget(self.product_input)

        self.update_button = QPushButton("Update")
        self.update_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.update_button.clicked.connect(self.update_exp)
        layout.addWidget(self.update_button)

        self.remove_button = QPushButton("Ignore")
        self.remove_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.remove_button.clicked.connect(self.remove_exp)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

    def update_exp(self):
        try:
            dodecane_peak = float(self.dodecane_input.text())
            product_peak = float(self.product_input.text())

            self.new_rows.append({
                'attributeDefinitionLabel': 'Peak Areas',
                'attributeValueIndex': 0,
                'value': dodecane_peak,
                'expID': self.exp_id
            })
            self.new_rows.append({
                'attributeDefinitionLabel': 'Peak names',
                'attributeValueIndex': 0,
                'value': 'Dodecane',
                'expID': self.exp_id
            })
            self.new_rows.append({
                'attributeDefinitionLabel': 'Peak Areas',
                'attributeValueIndex': 1,
                'value': product_peak,
                'expID': self.exp_id
            })
            self.new_rows.append({
                'attributeDefinitionLabel': 'Peak names',
                'attributeValueIndex': 1,
                'value': 'Product',
                'expID': self.exp_id
            })

            self.close()
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numbers for peak areas!")

    def remove_exp(self):
        self.ID2Remove.append(self.exp_id)
        self.close()





class CanceledRunPopup(QDialog):
    def __init__(self, runID):
        super().__init__()
        self.new_runID = None
        self.runID = runID  # Store the current Run ID
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Run Canceled")
        self.setGeometry(100, 100, 400, 220)

        layout = QVBoxLayout()

        # Message Label (Show current runID in the popup)
        self.label = QLabel(
            f"The current run (ID: {self.runID}) has been CANCELED.\n"
            "Do you want to continue with a new Run ID?", self
        )
        self.label.setFont(QFont("Arial", 12))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Input Field for New Run ID
        self.runID_input = QLineEdit(self)
        self.runID_input.setPlaceholderText("Enter new Run ID here")
        layout.addWidget(self.runID_input)

        # Replace Button (Normal)
        self.replace_button = QPushButton("Replace", self)
        self.replace_button.clicked.connect(self.replace_runID)
        layout.addWidget(self.replace_button)

        # Terminate Button (Red)
        self.terminate_button = QPushButton("Terminate", self)
        self.terminate_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.terminate_button.clicked.connect(self.terminate_program)
        layout.addWidget(self.terminate_button)

        self.setLayout(layout)

    def replace_runID(self):
        self.new_runID = self.runID_input.text().strip()
        if self.new_runID:
            self.accept()  # Close the dialog with a successful result

    def terminate_program(self):
        print("Terminated", "Error: The process has been terminated by the user.")
        sys.exit()  # Exit script with an error code



####################################


def value_gui_to_dataframe(data_raw):
    """
    This function processes a DataFrame containing CAS Numbers and extracts
    relevant information about dispense tools, chembeads factor, stock solution,
    solvent, and molar concentration. The values are extracted based on specific
    naming conventions in the CAS Number and stored in a structured DataFrame.

    Parameters:
    - data_raw (DataFrame): A DataFrame containing only the CAS Number
      of the articles that need to be created.

    Returns:
    - merge_data (DataFrame): A DataFrame containing extracted information
      merged with the original dataset.
    """


    
    # Define an empty DataFrame with required columns to store extracted values.
    df = pd.DataFrame(columns=[
        "CAS Number",
        "Dispense Tool Gravimetrically",
        "Dispense Tool Volumetrically",
        "ChemBeads Factor",
        "Molar concentration",
        "Stock Solution",
        "Solvent",
    ])
    
    # Initialize iteration counter
    iteration = 0

    # ----------------------------------------------
    # Iterate Over Unique CAS Numbers and Extract Information
    # ----------------------------------------------
    for i in data_raw["CAS Number"].unique():
        
        # Extract the CAS number for the current iteration as a string.
        cas_number = str(data_raw["CAS Number"].unique()[iteration])
        print(f'Processing CAS Number: {cas_number}')
        
        # Store CAS number in the DataFrame.
        df.loc[iteration, "CAS Number"] = cas_number

        # Split the CAS number string by "_" to extract relevant sections.
        split_parts = cas_number.split("_")
        
        # ----------------------------------------------
        # Processing for Solid ('S') Compounds
        # ----------------------------------------------
        if split_parts[1] == 'S':
            if split_parts[2] == 'P':  # Solid - Powder Form
                df.loc[iteration, "ChemBeads Factor"] = 1.00
                if split_parts[-1] in ['GDU-PFD', 'GDU-S']:
                    df.loc[iteration, "Dispense Tool Gravimetrically"] = split_parts[-1]
                else:
                    raise ValueError(f'Invalid dispense tool selection for {cas_number}')
            
            elif split_parts[2] == 'S':  # Solid - Solution Form
                if split_parts[-1] in ['GDU-PFD', 'GDU-S']:
                    df.loc[iteration, "Dispense Tool Gravimetrically"] = split_parts[-1]
                else:
                    raise ValueError(f'Invalid dispense tool selection for {cas_number}')
                
                df.loc[iteration, "Solvent"] = "ChemBeads"
                concentration_str = split_parts[-2][:-1]  # Extract numeric concentration
                concentration_int = int(concentration_str)
                if not (0 < concentration_int <= 100):
                    raise ValueError(f"Invalid Weight Percentage for {cas_number}: {concentration_int}")

                
                
                df.loc[iteration, "ChemBeads Factor"] = 100.0 / concentration_int
        
        # ----------------------------------------------
        # Processing for Liquid ('L') Compounds
        # ----------------------------------------------
        elif split_parts[1] == 'L':
            if split_parts[2] == 'P':  # Liquid - Powder Form
                df.loc[iteration, "Stock Solution"] = 'No'
                if split_parts[-1] in ['GDU-V', '4NH']:
                    df.loc[iteration, "Dispense Tool Volumetrically"] = split_parts[-1]
                else:
                    raise ValueError(f'Invalid dispense tool selection for {cas_number}')
            
            elif split_parts[2] == 'S':  # Liquid - Solution Form
                df.loc[iteration, "Stock Solution"] = 'Yes'
                if split_parts[-1] in ['GDU-V', '4NH']:
                    df.loc[iteration, "Dispense Tool Volumetrically"] = split_parts[-1]
                else:
                    raise ValueError(f'Invalid dispense tool selection for {cas_number}')
                
                # Ensure valid solvent selection
                if split_parts[3] == 'XXX':
                    raise ValueError(f'Invalid solvent selection for {cas_number}')
                
                df.loc[iteration, "Solvent"] = split_parts[3]
                
                # Extract and store molar concentration
                concentration_str = split_parts[-2][:-1]
                concentration = float(concentration_str)
                
                if not (00.01 <= concentration <= 55.00):
                    raise ValueError(f"Invalid Molar Concentration for {cas_number}: {concentration_int}")
                    
                df.loc[iteration, "Molar concentration"] = concentration
        
        # ----------------------------------------------
        # Error Handling for Unexpected Cases
        # ----------------------------------------------
        else:
            raise ValueError(f'Invalid selection for Solid/Liquid form for {cas_number}')
        
        # Increment the iteration counter.
        iteration += 1

    # ----------------------------------------------
    # Merge Extracted Data with Original DataFrame
    # ----------------------------------------------
    merge_data = pd.merge(data_raw, df, how="inner", on="CAS Number")
    
    # ----------------------------------------------
    # Return the Processed DataFrame
    # ----------------------------------------------
    return merge_data




def show_popup(message):
    popup = tk.Tk()
    popup.wm_title("Notification")
    popup.geometry("600x100")
    label = tk.Label(popup, text=message)
    label.pack(side="top", fill="x", pady=10, padx=10)
    B1 = tk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()






def verify_experiment_data(df):
    app = QApplication(sys.argv)
    ID2Remove = []  # List to store expIDs to remove
    new_rows = []  # List to collect new rows for updating the DataFrame

    # Identify unique experiment IDs using the "Timestamp Stored" rows.
    experiment_ids = df.loc[df['attributeDefinitionLabel'] == "Timestamp Stored", 'expID'].unique()
    
    # Check each experiment for a corresponding 'Dodecane' row.
    missing_expIDs = [exp_id for exp_id in experiment_ids if df[(df['expID'] == exp_id) & (df['value'] == 'Dodecane')].empty]

    # If there are no missing experiments, return the original DataFrame.
    if not missing_expIDs:
        return df, ID2Remove

    # Iterate over each missing experiment ID
    for exp_id in missing_expIDs:
        popup = ExpIDPopup(exp_id, ID2Remove, new_rows)
        popup.show()
        app.exec_()  # Ensures window stays open

    # Remove the chosen expIDs from the DataFrame
    updated_df = df[~df['expID'].isin(ID2Remove)]

    # If there are new rows, append them to the DataFrame
    if new_rows:
        new_rows_df = pd.DataFrame(new_rows)
        updated_df = pd.concat([updated_df, new_rows_df], ignore_index=True)

    return updated_df, ID2Remove



def prompt_new_runID(runID):
    app = QApplication(sys.argv)
    popup = CanceledRunPopup(runID)
    result = popup.exec_()  # Show the modal dialog
    return popup.new_runID if result == QDialog.Accepted else None  # Return new Run ID

