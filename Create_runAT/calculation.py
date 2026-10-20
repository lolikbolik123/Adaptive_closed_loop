import pandas as pd

# Define a function named 'amount' to calculate the amount of each chemicals we need to dispense


def amount(all_att_DOE):
    """
    This function calculate the amount of each chemical we need to dispense ( volumetrical dipense or gravimetrical dispense).

    Parameters:
    - all_att_DOE (dataframe): Dataframe that describe all experiments ("Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",dispense tool)

    Returns:
    - all_att_DOE (dataframe): Dataframe that describe all experiments with the amount (g or ml) of each chemicals
    """

    all_columns = [
        "Melting point",
        "Molar mass",
        "Density",
        "Molar Concentration",
        "ChemBeads Factor",
        "Volume",
        "Mass",
        "Dispense Tool Volumetric",
        "Dispense Tool Gravimetric",
        "Density",
    ]
    # Create empty columns if it doesn't exist

    for column in all_columns:
        if column not in all_att_DOE.columns:
            all_att_DOE[column] = ""

    # Change numerical to colum to numeric
    list_columns_num = [
        "Melting point",
        "Molar mass",
        "Density",
        "Molar Concentration",
        "ChemBeads Factor",
        "Volume",
        "Mass",
    ]

    for columns in list_columns_num:
        all_att_DOE[columns].apply(pd.to_numeric)

    # Replace nan values - for creating the json file later
    all_att_DOE["Dispense Tool Volumetric"].fillna("", inplace=True)
    all_att_DOE["Dispense Tool Gravimetric"].fillna("", inplace=True)
    all_att_DOE["Molar Concentration"].fillna("", inplace=True)
    all_att_DOE["Mass"].fillna("", inplace=True)

    for i in range(0, len(all_att_DOE)):
        if (
            all_att_DOE["Dispense Tool Volumetric"][i] == ""
            and all_att_DOE["CAS Number"][i] != "-"
        ):
            if (
                all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-S"
                or all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            ):
                if all_att_DOE.loc[i, "Mass"] != "":
                    continue
                else:

                    all_att_DOE.loc[i, "Mass"] = round(
                        (all_att_DOE["Molar mass"][i])
                        * 1000
                        * float(all_att_DOE["reaction scale (mmol)"][i])
                        * float(all_att_DOE["Equivalent"][i])
                        * (all_att_DOE["ChemBeads Factor"][i]),
                        3,
                    )

            elif all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-V":

                all_att_DOE.loc[i, "Mass"] = round(
                    (all_att_DOE["Molar mass"][i])
                    * 1000
                    * float(all_att_DOE["reaction scale (mmol)"][i])
                    * float(all_att_DOE["Equivalent"][i]),
                    3,
                )
            else:
                continue
        else:

            if all_att_DOE["Property"].str.match("solvent")[i]:
                continue
            elif (
                all_att_DOE["Property"].str.match("monomer")[i]
                and all_att_DOE["Volume"][i] != ""
            ):
                continue
            elif all_att_DOE["Molar Concentration"][i] != "":
                all_att_DOE.loc[i, "Volume"] = (
                    all_att_DOE["reaction scale (mmol)"][i]
                    * all_att_DOE["Equivalent"][i]
                    * (1 / float(all_att_DOE["Molar Concentration"][i])),
                )
            else:
                print(i)
                print(float(all_att_DOE["Density"][i]))
                all_att_DOE.loc[i, "Volume"] = (
                    (1 / (float(all_att_DOE["Density"][i]) * 0.001))
                    * (all_att_DOE["Molar mass"][i])
                    * 1000
                    * float(all_att_DOE["reaction scale (mmol)"][i])
                    * 0.001
                    * float(all_att_DOE["Equivalent"][i]),
                )
    """
    try:
        all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",
                "Mass",
            ]
        ] = all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",
                "Mass",
            ]
        ].apply(
            pd.to_numeric
        )

        all_att_DOE["Dispense Tool Volumetric"].fillna("", inplace=True)
        all_att_DOE["Molar Concentration"].fillna("", inplace=True)

        for i in range(0, len(all_att_DOE)):
            if (
                all_att_DOE["Dispense Tool Volumetric"][i] == ""
                and all_att_DOE["CAS Number"][i] != "-"
            ):
                if (
                    all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-S"
                    or all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-PFD"
                ):
                    if all_att_DOE.loc[i, "Mass"] != "":
                        continue
                    else:
                        all_att_DOE.loc[i, "Mass"] = round(
                            all_att_DOE["Molar mass"][i]
                            * 1000
                            * all_att_DOE["reaction scale (mmol)"][i]
                            * all_att_DOE["Equivalent"][i]
                            * all_att_DOE["ChemBeads Factor"][i],
                            3,
                        )

                else:
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i],
                        3,
                    )
            else:
                continue

        for i in range(0, len(all_att_DOE)):
            if all_att_DOE["Property"].str.match("solvent")[i]:
                continue
            elif (
                all_att_DOE["Property"].str.match("monomer")[i]
                and all_att_DOE["Volume"][i] != ""
            ):
                continue
            elif all_att_DOE["Molar Concentration"][i] != "":
                all_att_DOE.loc[i, "Volume"] = (
                    all_att_DOE["reaction scale (mmol)"][i]
                    * all_att_DOE["Equivalent"][i]
                    * (1 / all_att_DOE["Molar Concentration"][i]),
                )
            else:
                all_att_DOE.loc[i, "Volume"] = (
                    (1 / (all_att_DOE["Density"][i] * 0.001))
                    * all_att_DOE["Molar mass"][i]
                    * 1000
                    * all_att_DOE["reaction scale (mmol)"][i]
                    * 0.001
                    * all_att_DOE["Equivalent"][i],
                )
    except:  # noqa: E722
        pass

    try:
        all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "Volume",
                "Mass",
            ]
        ] = all_att_DOE[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "Volume",
                "Mass",
            ]
        ].apply(
            pd.to_numeric
        )

        all_att_DOE["Dispense Tool Volumetric"].fillna("", inplace=True)
        all_att_DOE["Molar Concentration"].fillna("", inplace=True)

        for i in range(0, len(all_att_DOE)):
            if (
                all_att_DOE["Dispense Tool Volumetric"][i] == ""
                and all_att_DOE["CAS Number"][i] != "-"
            ):
                if all_att_DOE["Dispense Tool Gravimetric"][i] == "GDU-S":
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i],
                        3,
                    )

                elif all_att_DOE.loc[i, "Mass"] != "":
                    continue
                else:
                    all_att_DOE.loc[i, "Mass"] = round(
                        all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i],
                        3,
                    )
            else:
                continue
            for i in range(0, len(all_att_DOE)):
                if all_att_DOE["Property"].str.match("solvent")[i]:
                    continue
                elif all_att_DOE["Property"].str.match("monomer")[i]:
                    continue
                elif all_att_DOE["Molar Concentration"][i] != "":
                    all_att_DOE.loc[i, "Volume"] = (
                        all_att_DOE["reaction scale (mmol)"][i]
                        * all_att_DOE["Equivalent"][i]
                        * (1 / all_att_DOE["Molar Concentration"][i]),
                    )
                else:
                    all_att_DOE.loc[i, "Volume"] = (
                        (1 / (all_att_DOE["Density"][i] * 0.001))
                        * all_att_DOE["Molar mass"][i]
                        * 1000
                        * all_att_DOE["reaction scale (mmol)"][i]
                        * 0.001
                        * all_att_DOE["Equivalent"][i],
                    )
    except:  # noqa: E722
        pass
    """
    all_att_DOE_sorted = all_att_DOE.sort_values(
        by=["Property", "Experiment No."], ascending=[False, True]
    )

    return all_att_DOE_sorted


def amount_ML(all_att_DOE, selected_experiment_list):
    """
    This function calculate the amount of each chemical we need to dispense ( volumetrical dipense or gravimetrical dispense).

    Parameters:
    - all_att_DOE (dataframe): Dataframe that describe all experiments ("Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",dispense tool)

    Returns:
    - all_att_DOE (dataframe): Dataframe that describe all experiments with the amount (g or ml) of each chemicals
    """
    # select rows where we have to write the yield
    mask = all_att_DOE["Experiment No."].isin(selected_experiment_list)
    data_select = all_att_DOE[mask]
    data_select.reset_index(inplace=True, drop=True)

    all_columns = [
        "Melting point",
        "Molar mass",
        "Density",
        "Molar Concentration",
        "ChemBeads Factor",
        "Volume",
        "Mass",
        "Dispense Tool Volumetric",
        "Dispense Tool Gravimetric",
        "Density",
    ]
    # Create empty columns if it doesn't exist

    for column in all_columns:
        if column not in data_select.columns:
            data_select[column] = ""

    # Change numerical to colum to numeric
    list_columns_num = [
        "Melting point",
        "Molar mass",
        "Density",
        "Molar Concentration",
        "ChemBeads Factor",
        "Volume",
        "Mass",
    ]

    for columns in list_columns_num:
        data_select[columns].apply(pd.to_numeric)

    # Replace nan values - for creating the json file later
    data_select["Dispense Tool Volumetric"].fillna("", inplace=True)
    data_select["Dispense Tool Gravimetric"].fillna("", inplace=True)
    data_select["Molar Concentration"].fillna("", inplace=True)
    data_select["Mass"].fillna("", inplace=True)

    for i in range(0, len(data_select)):
        if (
            data_select["Dispense Tool Volumetric"][i] == ""
            and data_select["CAS Number"][i] != "-"
        ):
            if (
                data_select["Dispense Tool Gravimetric"][i] == "GDU-S"
                or data_select["Dispense Tool Gravimetric"][i] == "GDU-PFD"
            ):
                if data_select.loc[i, "Mass"] != "":
                    continue
                else:

                    data_select.loc[i, "Mass"] = round(
                        (data_select["Molar mass"][i])
                        * 1000
                        * float(data_select["reaction scale (mmol)"][i])
                        * float(data_select["Equivalent"][i])
                        * float(data_select["ChemBeads Factor"][i]),
                        3,
                    )

            elif data_select["Dispense Tool Gravimetric"][i] == "GDU-V":

                data_select.loc[i, "Mass"] = round(
                    (data_select["Molar mass"][i])
                    * 1000
                    * float(data_select["reaction scale (mmol)"][i])
                    * float(data_select["Equivalent"][i]),
                    3,
                )
            else:
                continue
        else:
            for i in range(0, len(data_select)):
                if data_select["Property"].str.match("solvent")[i]:
                    continue
                elif (
                    data_select["Property"].str.match("monomer")[i]
                    and data_select["Volume"][i] != ""
                ):
                    continue
                elif data_select["Molar Concentration"][i] != "":
                    data_select.loc[i, "Volume"] = (
                        data_select["reaction scale (mmol)"][i]
                        * data_select["Equivalent"][i]
                        * (1 / float(data_select["Molar Concentration"][i])),
                    )

                else:
                    data_select.loc[i, "Volume"] = (
                        (1 / (float(data_select["Density"][i]) * 0.001))
                        * (data_select["Molar mass"][i])
                        * 1000
                        * float(data_select["reaction scale (mmol)"][i])
                        * 0.001
                        * float(data_select["Equivalent"][i]),
                    )

    """
    try:
        data_select[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",
            ]
        ] = data_select[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "ChemBeads Factor",
                "Volume",
            ]
        ].apply(
            pd.to_numeric
        )

        data_select["Dispense Tool Volumetric"].fillna("", inplace=True)
        data_select["Molar Concentration"].fillna("", inplace=True)

        for i in range(0, len(data_select)):
            if (
                data_select["Dispense Tool Volumetric"][i] == ""
                and data_select["CAS Number"][i] != "-"
            ):
                if (
                    data_select["Dispense Tool Gravimetric"][i] == "GDU-S"
                    or data_select["Dispense Tool Gravimetric"][i] == "GDU-PFD"
                ):
                    data_select.loc[i, "Mass"] = round(
                        data_select["Molar mass"][i]
                        * 1000
                        * data_select["reaction scale (mmol)"][i]
                        * data_select["Equivalent"][i]
                        * data_select["ChemBeads Factor"][i],
                        3,
                    )

                else:
                    data_select.loc[i, "Mass"] = round(
                        data_select["Molar mass"][i]
                        * 1000
                        * data_select["reaction scale (mmol)"][i]
                        * data_select["Equivalent"][i],
                        3,
                    )
            else:
                continue

    except:  # noqa: E722
        pass

    try:
        data_select[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "Volume",
            ]
        ] = data_select[
            [
                "Melting point",
                "Molar mass",
                "Density",
                "Molar Concentration",
                "Volume",
            ]
        ].apply(
            pd.to_numeric
        )

        data_select["Dispense Tool Volumetric"].fillna("", inplace=True)
        data_select["Molar Concentration"].fillna("", inplace=True)

        for i in range(0, len(data_select)):
            if (
                data_select["Dispense Tool Volumetric"][i] == ""
                and data_select["CAS Number"][i] != "-"
            ):
                if data_select["Dispense Tool Gravimetric"][i] == "GDU-S":
                    data_select.loc[i, "Mass"] = round(
                        data_select["Molar mass"][i]
                        * 1000
                        * data_select["reaction scale (mmol)"][i]
                        * data_select["Equivalent"][i],
                        3,
                    )

                else:
                    data_select.loc[i, "Mass"] = round(
                        data_select["Molar mass"][i]
                        * 1000
                        * data_select["reaction scale (mmol)"][i]
                        * data_select["Equivalent"][i],
                        3,
                    )
            else:
                continue
    except:  # noqa: E722
        pass

    for i in range(0, len(data_select)):
        if data_select["Property"].str.match("solvent")[i]:
            continue
        elif data_select["Property"].str.match("monomer")[i]:
            continue
        elif data_select["Molar Concentration"][i] != "":
            data_select.loc[i, "Volume"] = (
                data_select["reaction scale (mmol)"][i]
                * data_select["Equivalent"][i]
                * (1 / data_select["Molar Concentration"][i]),
            )
        else:
            data_select.loc[i, "Volume"] = (
                (1 / (data_select["Density"][i] * 0.001))
                * data_select["Molar mass"][i]
                * 1000
                * data_select["reaction scale (mmol)"][i]
                * 0.001
                * data_select["Equivalent"][i],
            )
    """
    data_select_sorted = data_select.sort_values(
        by=["Property", "Experiment No."], ascending=[False, True]
    )
    return data_select_sorted


# Define a reaction named 'ratio_analytic' to calculate the ratio/yield of each experiement in a run


def ratio_analysis(analytic_result, list_expID):
    """
    This function calculate the ratio of product compare to the internal standard injected after the reaction.

    Parameters:
    - analytic_result (dataframe): Dataframe with the peak area of each product and internal standard for each experiment extract from
      the report in Arksuite

    Returns:
    - ratio_analytic (dataframe): Dataframe with the ratio of each product regardinf the internal standard
    """

    list_peak_name = list(analytic_result["Peak name"])
    list_peak_name_noduplicate = list(dict.fromkeys(list_peak_name))
    list_peak_name_noduplicate.remove("Dodecane")
    print(list_peak_name_noduplicate)

    analytic_result["ratio"] = 0

    ratio_analytic = analytic_result.pivot(
        index=["expID", "Experiment No._CAS_Number", "ratio"], columns="Peak name"
    )["Peak area"]
    ratio_analytic.reset_index(inplace=True)

    if list_peak_name_noduplicate == []:
        ratio_analytic[["Product", "Dodecane"]] = 0
        print("empty")
    else:

        # Change column Product and Dodecane's values to a numeric type
        ratio_analytic[["Product", "Dodecane"]] = ratio_analytic[
            ["Product", "Dodecane"]
        ].apply(pd.to_numeric)

        for i in list_expID:
            if ratio_analytic["Product"].loc[ratio_analytic["expID"] == i].isna().any():
                ratio_analytic["ratio"].loc[ratio_analytic["expID"] == i] = 0

            else:
                ratio_analytic["ratio"].loc[ratio_analytic["expID"] == i] = (
                    ratio_analytic["Product"].loc[ratio_analytic["expID"] == i]
                    / ratio_analytic["Dodecane"].loc[ratio_analytic["expID"] == i]
                )

    return ratio_analytic
