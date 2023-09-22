import glob                        # use linux wildcard syntax
import numpy as np
import sys
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_exp(filename, prop, temp, press=None, tol_temp=0, tol_p=0, p_nan=False, is_plot=False, is_print=False, area=[], is_ref=True):
    """
    This function can read a DBB Excel file and returns the desired mean
    property at the specified temperature.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    prop : string
        property which you would like consider [DEN,DIF]
    temp : float
        desired temperature
    press : float
        desired pressure
    tol_temp : float, optional
        tolerance for the target temperature
    tol_p : float, optional
        tolerance for target pressure
    p_nan : bool, optional
        consider all data points which has no specified pressure
    is_plot : bool, optional
        plot the values
    is_print : bool, optional
        print mean value, standard deviation and amount of data
    area : list, optional
        consider only the data in the specified area [a,b]

    Returns
    -------
    mean : list
        mean value of the considered property by the
    std : list
        standard deviation of the considered property
    unit : string
        string with the unit of the property
    data_amount : integer
        number of data points of the considered property
    prop_vec : list
        list of all data points
    ref_vec : list
        reference of the data points
    table : obj
        Pandas DataFrame with the selected data points
    """

    # Read excel data file
    df_all = pd.read_excel(filename)

    # Read unit and drop first row
    unit = df_all[prop][0]
    df_all = df_all.drop(index=0)

    # Cut off references
    rows_with_nan = df_all[df_all['T'].isnull()].index.tolist()

    # Reference Table
    df_ref = df_all.truncate(before=int(rows_with_nan[0]))

    # Valbool, optionalues table
    df = df_all.truncate(after=int(rows_with_nan[0]))
    pd.to_numeric(df['T'])

    # Search for the desired temperature
    df_woT = df[df['T'] <= (temp + tol_temp)]
    df_woT = df_woT[df_woT['T'] >= (temp - tol_temp)]
    if area:
        df_woT = df_woT[df_woT[prop] <= area[1]]
        df_woT = df_woT[df_woT[prop] >= area[0]]

    # Search for the desired pressure
    if press:
        if "P" in df_woT:
            pd.to_numeric(df['P'])
            if p_nan:
                df_woT['P'] = df_woT['P'].fillna(press)
            df_woT = df_woT[df_woT['P'] <= (press + tol_p)]
            df_woT = df_woT[df_woT['P'] >= (press - tol_p)]

    # Write the prop in vector
    data = df_woT.to_dict()
    prop_vec = []
    ref_vec = []

    # Read reference of the choosen data points
    if is_ref:
        for i in (data[prop]):
            print(data[prop][i])
            prop_vec.append(float(data[prop][i]))
            ref = df_ref[df_ref['PCP Data Set#'] == (data['Ref. Number'][i])]
            ref = ref['T'].values[0]
            ref_vec.append(ref.split("] ")[1])
    else:
        ref_vec = []

    # Save table with data points
    table = df_woT

    # Plot selected data points
    if is_plot:
        plt.figure(figsize=(13, 4))
        plt.title(filename)
        plt.subplot(1, 2, 1)
        sns.scatterplot(x=a['T'], y=prop_vec)
        plt.xlabel("T (K)")
        plt.ylabel(str(prop + " (" + unit + ")"))
        if press:
            if "P" in df_woT:
                plt.subplot(1, 2, 2)
                sns.scatterplot(x=df_woT['P'], y=prop_vec)
                plt.xlabel("p (bar)")
                plt.ylabel(str(prop + " (" + unit + ")"))

    # Calculate mean and std
    if prop_vec:
        data_amount = len(prop_vec)
        mean = np.mean(prop_vec)
        std = np.std(prop_vec)
    else:
        data_amount = None
        mean = None
        std = None

    # Print results
    if is_print:
        print("Mean (" + prop + ") : " + str(mean))
        print("Std  (" + prop + ") : " + str(std))
        print("Amount of data : " + str(len(prop_vec)))

    #Return results
    return mean, std, unit, data_amount, prop_vec, ref_vec, table

def read_exp_temp_vec(filename,temp_vec, prop, press, tol_temp=0.2,  tol_p = 10000, p_nan=True, is_plot=True, is_display=False):
    """
    This function can read a DBB Excel file and returns the mean property of the specified temperatures.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    temp : float
        desired temperature
    prop : string
        property which you would like consider
    press : float
        desired pressure
    tol_temp : float, optional
        tolerance for the target temperature
    tol_p : float, optional
        tolerance for target pressure
    p_nan : bool, optional
        consider all data points which has no specified pressure
    is_plot : bool, optional
        plot the values
    is_display: bool, optional
        show pandas DataFrame

    Returns
    -------
    data : dictonary
        dictonary with the mean property, standard deviation and number of data points for the specified temperatures
    prop_dict : dictonary
        dictonary with all data points for the specified temperatures
    """

    data_prop = []
    std_prop = []
    num_data = []
    prop_dict = {}
    reference = []
    for temp in temp_vec:
        mean, std, unit, data_amount, prop_vec, ref_vec, table = read_exp(filename, prop, temp, press, tol_temp, tol_p, p_nan)
        prop_dict[str(temp)] = {}
        prop_dict[str(temp)][prop] = prop_vec
        prop_dict[str(temp)]["Reference"] = ref_vec
        data_prop.append(mean)
        num_data.append(data_amount)
        std_prop.append(std)
        reference.append(ref_vec)
    if prop == "DIF":
        prop_dict[str(temp)][prop] = [value * 10 ** (-4) for value in prop_dict[str(temp)][prop]]
        unit = "m^2/s"
        for i in range(len(data_prop)):
            if not data_prop[i] == None:
                data_prop[i] = data_prop[i] * 10 ** (-4)
                std_prop[i] = std_prop[i] * 10 ** (-4)

        

    if is_plot:
        for j in range(len(data_prop)):
            sns.scatterplot(x=[temp_vec[j]], y=data_prop[j]  )
            plt.errorbar(temp_vec[j], data_prop[j], std_prop[j]  )

        plt.xlabel("$\mathrm{Temperature \ (K)}$")
        if prop=="DEN":
            plt.ylabel("$\mathrm{Density} \ (\mathrm{kg \ m^{-2})}$")
        elif prop=="DIF":
            plt.ylabel("$\mathrm{Diffusion} \ (\mathrm{m^{2} \ s^{-1})}$")


    data = {"Temperature (K)": temp_vec, str(prop + " (" + str(unit) + ")"): data_prop, "STD (" + str(unit) + ")": std_prop, "Number of data points": num_data, "References": reference}

    if is_display:
        df = pd.DataFrame(data)
        display(df)

    return data,prop_dict

def drop_outliers(data,prop_dict,temp,area):
    """
    This function can be used remove the specified outliers from the mean property. Therefore, it will be specified a area in which the data points 
    has to be considered. All points outside these area will be removed.

    Parameters
    ----------
    data : dictonary
        dictonary with the mean property, standard deviation and number of data points for the specified temperatures
    prop_dict : dictonary
        dictonary with all data points for the specified temperatures
    temp : string
        consiedered temperature
    area : list
        list with lowest and the highest property

    Returns
    -------
    data : dictonary
        dictonary with the mean property, standard deviation and number of data points for the specified temperatures
    """
    for key in prop_dict[str(temp)].keys():
        if not key=="Reference":
            prop = [prop for prop in prop_dict[str(temp)][key] if area[1] > prop > area[0]]
            prop_ref = [prop_ref for prop,prop_ref in zip(prop_dict[str(temp)][key],prop_dict[str(temp)]["Reference"]) if area[1] > prop > area[0]]
            df = pd.DataFrame(data)
            if ["DEN"] in list(prop_dict[str(temp)].keys()):
                df.loc[df["Temperature (K)"] == temp, ["DEN (kg/m3)"]] = np.mean(prop)
                df.loc[df["Temperature (K)"] == temp, ["STD (kg/m3)"]] = np.std(prop)
                df.loc[df["Temperature (K)"] == temp, ["Number of data points"]] = len(prop)
                df.loc[df["Temperature (K)"] == temp, ["References"]] = prop_ref
            elif ["DIF"] in list(prop_dict[str(temp)].keys()):
                df.loc[df["Temperature (K)"] == temp, ["DIF (m^2/s)"]] = np.mean(prop)
                df.loc[df["Temperature (K)"] == temp, ["STD (m^2/s)"]] = np.std(prop)
                df.loc[df["Temperature (K)"] == temp, ["Number of data points"]] = len(prop)
                df.loc[df["Temperature (K)"] == temp, ["References"]] = prop_ref

    data = df.to_dict()
    return data

def plot_data(prop_dict, temp, mean=True, std=True, is_display=False):
    """
    This function can be used to find outliers in the data. It is possible to plot the data points for a specified temperature.

    Parameters
    ----------
    prop_dict : dictonary
        dictonary with all data points for the specified temperatures
    temp : string
        consiedered temperature
    mean: bool, optional
        plot the mean values of the property as a line plot
    std: bool, optional
        shows the area of the standard deviation

    Returns
    -------
    data : list
        lit of all data points at the specified temperature
    """
    
    for key in prop_dict[str(temp)].keys():
        if not key=="Reference":
            plt.scatter([i+1 for i in range(len(prop_dict[str(temp)][key]))],prop_dict[str(temp)][key], label="Data Points")
            if mean:
                plt.plot([i for i in range(len(prop_dict[str(temp)][key])+2)],[np.mean(prop_dict[str(temp)][key]) for i in range(len(prop_dict[str(temp)][key])+2)], label="Mean")
            if std:
                plt.axhspan(ymin=np.mean(prop_dict[str(temp)][key])-np.std(prop_dict[str(temp)][key]),ymax=np.mean(prop_dict[str(temp)][key])+np.std(prop_dict[str(temp)][key]),facecolor="grey", alpha=0.3, label="STD")
            plt.xlim([0,len(prop_dict[str(temp)][key])+1])
            plt.legend()
            plt.xlabel("Number of data points")
            plt.ylabel("Property")
            data={"Mean": np.mean(prop_dict[str(temp)][key]), "STD": np.std(prop_dict[str(temp)][key]), "Number of data points": len(prop_dict[str(temp)][key])}
            
            if is_display:
                df = pd.DataFrame(data, index=[str(temp)])
                display(df)
    return prop_dict[str(temp)]


def plot_means(data):
    """
    This function create the plot of the mean property values over the temperature

    Parameters
    ----------
    data : dictonary
        dictonary with the mean property, standard deviation and number of data points for the specified temperatures
    """
    if ["DEN (kg/m3)"] in list(data.keys()):
        for j in range(len(data["DEN (kg/m3)"])):
            sns.scatterplot(x=[data["Temperature (K)"][j]],y=[data["DEN (kg/m3)"][j]]  )
            plt.errorbar(data["Temperature (K)"][j],data["DEN (kg/m3)"][j],data["STD (kg/m3)"][j])

        plt.xlabel("$\mathrm{Temperature \ (K)}$")
        plt.ylabel("$\mathrm{Density} \ (\mathrm{kg \ m^{-2})}$")
    elif ["DIF (m^2/s)"] in list(data.keys()):
        for j in range(len(data["DIF (m^2/s)"])):
            sns.scatterplot(x=[data["Temperature (K)"][j]],y=[data["DIF (m^2/s)"][j]]  )
            plt.errorbar(data["Temperature (K)"][j],data["DIF (m^2/s)"][j],data["STD (m^2/s)"][j])

        plt.xlabel("$\mathrm{Temperature \ (K)}$")
        plt.ylabel("$\mathrm{Diffusion} \ (\mathrm{m^{2} \ s^{-1})}$")

    
