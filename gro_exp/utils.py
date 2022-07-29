import glob                        # use linux wildcard syntax
import numpy as np
import sys
import pickle
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
        cpus = [cpus * (node+1) for node in range(len(ns_day))]
        nodes = [node+1 for node in range(len(ns_day))]
        for node, nd in zip(nodes, ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(node))
            speedup_ideal.append(1/(ns_day[0]/((node)*ns_day[0])))
    else:
        for cpu, nd in zip(cpus, ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(cpu))
            speedup_ideal.append(1/(ns_day[0]/((cpu)*ns_day[0])))

    plt.figure(figsize=(15, 8))
    plt.subplot(2, 2, 1)
    plt.plot(cpus, speedup, linestyle="-", marker='*')
    plt.plot(cpus, speedup_ideal)
    plt.legend(["Speedup", "Speedup (ideal)"])
    plt.xlabel("CPUs")
    plt.ylabel("SpeedUp")

    plt.subplot(2, 2, 2)
    plt.plot(cpus, efficieny)
    plt.plot(cpus, [1 for i in range(len(cpus))])
    plt.legend(["Efficieny", "Efficieny (ideal)"])
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
        cpus = [cpus * (node+1) for node in range(len(ns_day))]
        nodes = [node+1 for node in range(len(ns_day))]
        for node, nd in zip(nodes, ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(node))
            speedup_ideal.append(1/(ns_day[0]/((node)*ns_day[0])))
    else:
        for cpu, nd in zip(cpus, ns_day):
            speed = 1/(ns_day[0]/(nd))
            speedup.append(1/(ns_day[0]/(nd)))
            efficieny.append(speed/(cpu))
            speedup_ideal.append(1/(ns_day[0]/((cpu)*ns_day[0])))

    data = {"CPUs": cpus, "Speedup": speedup, "Efficieny": efficieny,
            "ns/day": ns_day, "Simulation time (days)": [ns/i for i in ns_day]}
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
        sns.lineplot(x=time* 10**-3, y=msd)
        plt.xlabel("time (ns)")
        plt.ylabel("MSD")

    # Return data
    return time, msd, str(words[4]), str(words[6][:-1])


def msd_fit(data_msd, area = [], is_plot = False, is_print = False):
    """
    Function to fit the msd calculated with gromacs by hand. 

    Parameters
    ----------
    data_msd : dictonary
        data dictonary from the function :func:`gro_exp.utils.msd`
    area : list
        area in which the msd will be calculated


    Returns
    -------
    time : float
        self fitted msd value (m^2/s)
    """

    # Read dictonary
    data = data_msd[1]          # read MSD
    time = data_msd[0]          # read time (ps)

    # Area for fitting
    start = area[0] * 10 ** 3   # in ps
    end = area[1] * 10 ** 3     # in ps
    
    # Fit msd value
    msd_fit = (data[int(end/2)]-data[start])*10**-18/(6*(time[int(end/2)]-time[int(start/2)])*10**-12)

    # Plot msd curve from gromacs and shawod the considered area
    if is_plot:
        plt.title("MSD")
        sns.lineplot(x=time* 10**-3, y=data)
        plt.xlabel("time (ns)")
        plt.ylabel("MSD")
        plt.axvspan(xmin=area[0], xmax=area[1], facecolor="grey", alpha=0.3)
    
    # Print self fitted MSD Value
    if is_print:
        print("MSD Diffusion (self): " + "%.4e" % (msd_fit) + " m^2/s")
    
    return msd_fit


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



def save_data(link, data):
    """Save an object files using pickle in the specified link.

    Parameters
    ----------
    data : Object
        Object to be saved
    link : string
        Specific link to save object
    """

    with open(link, "wb") as f:
        pickle.dump(data, f)

def load_data(link):
    """Load an object files using pickle in the specified link.

    Parameters
    ----------
    link : string
        Specific link to load object
    """

    with open(link, 'rb') as f:
        return pickle.load(f)