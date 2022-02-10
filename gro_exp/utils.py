import glob                        # use linux wildcard syntax
import numpy as np
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def bench_plot(ns_day, cpus, nodes=False):
    """
    Function to plot speedup and cpu efficieny over the CPUs.

    Parameters
    ----------
    ns_day : list
        list with ns/day
    cpus : list or int
        list with used cpus or number of cpus per node if ns_day list is over nodes
    nodes : bool
        if ns_day list is over nodes

    Returns
    -------
    speedup : list
        speedup over the cpus or nodes
    efficieny : list
        efficieny over cpus
    """
    efficieny = []
    speedup = []
    speedup_ideal = []
    #if not cpus:
    if nodes:
        cpus = [cpus* (node+1) for node in range(len(ns_day)) ]
        nodes = [node+1 for node in range(len(ns_day)) ]
        for node,nd in zip(nodes,ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(node))
            speedup_ideal.append(1/(ns_day[0]/((node)*ns_day[0])))
    else:
        for cpu,nd in zip(cpus,ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(cpu))
            speedup_ideal.append(1/(ns_day[0]/((cpu)*ns_day[0])))

    plt.figure(figsize=(15,8))
    plt.subplot(2,2, 1)
    plt.plot(cpus,speedup, linestyle="-", marker= '*')
    plt.plot(cpus,speedup_ideal)
    plt.legend(["Speedup","Speedup (ideal)"])
    plt.xlabel("CPUs")
    plt.ylabel("SpeedUp")

    plt.subplot(2,2, 2)
    plt.plot(cpus,efficieny)
    plt.plot(cpus,[1 for i in range(len(cpus))])
    plt.legend(["Efficieny","Efficieny (ideal)"])
    plt.xlabel("CPUs")
    plt.ylabel("Efficiency")

    return speedup, efficieny

def bench_table(ns_day, cpus, ns, nodes=False, print_con=False):
    """
    Function to plot speedup and cpu efficieny over the CPUs.

    Parameters
    ----------
    ns_day : list
        list with ns/day
    cpus : list or int
        list with used cpus or number of cpus per node if ns_day list is over nodes
    ns : float
        time which has to simulated to caculate the simulation time
    nodes : bool
        if ns_day list is over nodes
    print_con : bool
        if True to print in console

    Returns
    -------
    data : dictonary
        dictonary of the table
    """
    efficieny = []
    speedup = []
    speedup_ideal = []

    if nodes:
        cpus = [cpus * (node+1) for node in range(len(ns_day))  ]
        nodes = [node+1 for node in range(len(ns_day)) ]
        for node,nd in zip(nodes,ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(node))
            speedup_ideal.append(1/(ns_day[0]/((node)*ns_day[0])))
    else:
        for cpu,nd in zip(cpus,ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(cpu))
            speedup_ideal.append(1/(ns_day[0]/((cpu)*ns_day[0])))

    data = {"CPUs": cpus, "Speedup": speedup, "Efficieny": efficieny, "ns/day": ns_day, "Simulation time (days)": [ns/i for i in ns_day]}
    df = pd.DataFrame(data)

    if print_con:
        print(df)
    else:
        display(df)

    return data

def msd(filename, is_print=False, is_plot=False):
    """
    The function enables a display of the MSD history calculated by Gromacs by
    reading out a Gromacs xvg output file.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    is_print : bool, optional
        True to print msd diffusion coefficient
    is_plot : bool, optional
        True to plot the msd value over the time

    Returns
    -------
    time : list
        list with the time values
    msd : list
        list with the msd Values
    msd_diff : float
        msd diffusion calculated by GROMACS
    msd_diff_std : float
        standard deviation on msd diffusion calculated by gromacs
    """

    # Read data and ste lists
    data_file = glob.glob(filename)
    time = []
    msd = []

    # Open file
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#"):
                words = line.split()

    # Print MSD value
    if is_print:
        print("MSD Diffusion: "
              + str(words[4]) + ' ' + str(words[5]) + str(words[6]) + "e-9 m s^-2")

    # Read data
    for i, file in enumerate(data_file):
        time = np.genfromtxt(file, skip_header=20, usecols=0)
        msd = np.genfromtxt(file, skip_header=20, usecols=1)

    # Plot msd
    if is_plot:
        plt.title("MSD")
        sns.lineplot(x=time, y=msd)
        plt.xlabel("time")
        plt.ylabel("MSD")

    # Return data
    return time, msd, str(words[4]), str(words[5])


def density(filename, is_print=False, is_plot=False):
    """
    The function enables a calculation of the mean density in as simulation box
    and can plot the density over the box. As input file a gromacs xvg has to use.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    is_print : bool, optional
        True to print the mean density
    is_plot : bool, optional
        True to plot the density over the box length

    Returns
    -------
    length : list
        list over box length
    density : list
        list with the density
    dens_mean : float
        mean density in the simulation Box
    """
    # Read data and set list
    data_file = glob.glob(filename)
    length = []
    density = []

    # Read data
    for i, file in enumerate(data_file):
        length = np.genfromtxt(file, skip_header=24, usecols=0)
        density = np.genfromtxt(file, skip_header=24, usecols=1)

    # Calculate density
    density_mean = np.mean(density)

    # Print density
    if is_print:
        print("Density: " + str(density_mean) + " kg m^-3")

    if is_plot:
        plt.title("Density")
        sns.lineplot(x=length, y=density)
        plt.xlabel("Box length")
        plt.ylabel("Density")

    # Return results
    return length, density, density_mean


def read_exp(filename, prop, temp, press=None, tol_temp=0, tol_p=0, p_nan=False, is_plot=False, is_print=False, area=[]):
    """
    This function can read a DBB Excel file and returns the desired mean
    property at the specified temperature.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    prop : string
        property which you would like consider
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
    a = df[df['T'] <= (temp + tol_temp)]
    a = a[a['T'] >= (temp - tol_temp)]
    if area:
        a = a[a[prop] <= area[1]]
        a = a[a[prop] >= area[0]]

    # Search for the desired pressure
    if press:
        if "P" in a:
            pd.to_numeric(df['P'])
            if p_nan:
                a['P'] = a['P'].fillna(press)
            a = a[a['P'] <= (press + tol_p)]
            a = a[a['P'] >= (press - tol_p)]

    # Write the prop in vector
    data = a.to_dict()
    prop_vec = []
    ref_vec = []

    # Read reference of the choosen data points
    for i in (data[prop]):
        prop_vec.append(float(data[prop][i]))
        ref = df_ref[df_ref['PCP Data Set#'] == (data['Ref. Number'][i])]
        ref = ref['T'].values[0]
        ref_vec.append(ref.split("] ")[1])

    # Save table with data points
    table = a

    # Plot selected data points
    if is_plot:
        plt.figure(figsize=(13, 4))
        plt.title(filename)
        plt.subplot(1, 2, 1)
        sns.scatterplot(x=a['T'], y=prop_vec)
        plt.xlabel("T (K)")
        plt.ylabel(str(prop + " (" + unit + ")"))
        if press:
            if "P" in a:
                plt.subplot(1, 2, 2)
                sns.scatterplot(x=a['P'], y=prop_vec)
                plt.xlabel("p (bar)")
                plt.ylabel(str(prop + " (" + unit + ")"))

    # Calculate mean and std
    data_amount = len(prop_vec)
    mean = np.mean(prop_vec)
    std = np.std(prop_vec)

    # Print results
    if is_print:
        print("Mean (" + prop + ") : " + str(mean))
        print("Std  (" + prop + ") : " + str(std))
        print("Amount of data : " + str(len(prop_vec)))

    #Return results
    return mean, std, unit, data_amount, prop_vec, ref_vec, table
