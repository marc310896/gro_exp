import glob                        # use linux wildcard syntax
import numpy as np
import sys
import scipy.stats as stats
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def cut_gro(filename, output, direction='z', area = [], mol={}, remove=False):
    """
    Function to cut into  Gromacs structure files or to remove molecules in specific areas.

    Parameters
    ----------
    filename : string
        string to gro file
    output : string
        name of the output gro file
    direction : string
        direction (x,y or z)
    area : list
        list [a,b] area which you want to have
    mol : dictonary
        key as the molecules name and value is a list c=[a,b]
        Remove the specified molecules in the area c
    remove: bool
        remove molecules specified in the mol dictonary
    """


    # Read filled structure
    with open(filename, "r") as file_in:
        counter = 0
        data = []
        for line in file_in:
            if counter < 2:
                if counter == 0:
                    title = line
                counter += 1
            elif not len(line.split()) == 3:
                atom = []
                atom.append(int(line[0:5]))
                atom.append(line[5:10])
                atom.append(line[10:15])
                atom.append(int(line[15:20]))
                atom.append(float(line[20:28]))
                atom.append(float(line[28:36]))
                atom.append(float(line[36:44]))

                data.append(atom)
            else:
                box = line

    if direction == "x":
        i = 4
    elif direction == "y":
        i = 5 
    elif direction == "z":
        i = 6

    # Create molecule lists
    mols = {}
    mol_names = []
    last_atom = None
    for atom in data:
        if (atom[1] in mol) and remove:
            if (mol[atom[1]][0]<atom[i]<mol[atom[1]][1]):
                pass
            elif (area[0]<atom[i]<area[1]):

                # Create new dictionary entry
                if not atom[1] in mols:
                    mols[atom[1]] = []
                    mol_names.append(atom[1])

                # Create new molecule
                if last_atom is None or not atom[0]==last_atom:
                    mols[atom[1]].append([])

                # Add atom
                mols[atom[1]][-1].append(atom)
                last_atom = atom[0]

        elif (area[0]<atom[i]<area[1]):
            # Create new dictionary entry
            if not atom[1] in mols:
                mols[atom[1]] = []
                mol_names.append(atom[1])

            # Create new molecule
            if last_atom is None or not atom[0]==last_atom:
                mols[atom[1]].append([])

            # Add atom
            mols[atom[1]][-1].append(atom)
            last_atom = atom[0]


    # Create new gro file
    with open(output, "w") as file_out:
        # Set title
        file_out.write(title)

        # Number of atoms
        num_atoms = sum([sum([len(mol) for mol in mols[mol_name]]) for mol_name in mol_names])
        file_out.write("%i" % num_atoms+"\n")

        # Atoms
        num_a = 0
        num_m = 0
        for mol_name in mol_names:
            for mol in mols[mol_name]:
                num_m = num_m+1 if num_m < 99999 else 0
                for atom in mol:
                    # Set ids
                    num_a = num_a+1 if num_a < 99999 else 0

                    # Write atom string
                    out_string  = "%5i" % num_m  #  1- 5 (5)    Residue number
                    out_string += atom[1]        #  6-10 (5)    Residue short name
                    out_string += atom[2]        # 11-15 (5)    Atom name
                    out_string += "%5i" % num_a  # 16-20 (5)    Atom number
                    for j in range(3):           # 21-44 (3*8)  Coordinates
                        out_string += "%8.3f" % atom[4+j]

                    file_out.write(out_string+"\n")

        # Box
        file_out.write(box)

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


def msd(filename, is_print=False, is_plot=False, kwargs_line={}):
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
    kwargs_line: dict, optional
        Dictionary with plotting parameters for the line plot

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
        sns.lineplot(x=time* 10**-3, y=msd, **kwargs_line)
        plt.xlabel("time (ns)")
        plt.ylabel("MSD")

    # Return data
    return time, msd, str(words[4]), str(words[6][:-1])


def msd_fit(data_msd, area = [], is_plot = False, is_print = False, kwargs_line={}):
    """
    Function to fit the msd calculated with gromacs by hand. 

    Parameters
    ----------
    data_msd : dictonary
        data dictonary from the function :func:`gro_exp.utils.msd`
    area : list
        area in which the msd will be calculated
    is_print : bool, optional
        True to print msd diffusion coefficient
    is_plot : bool, optional
        True to plot the msd value over the time
    kwargs_line: dict, optional
        Dictionary with plotting parameters for the line plot

    Returns
    -------
    msd_fit : float
        self fitted msd value (m^2/s)
    """

    # Read dictonary
    data = data_msd[1]          # read MSD
    time = data_msd[0]          # read time (ps)

    # Area for fitting
    start = area[0] * 10 ** 3   # in ps
    end = area[1] * 10 ** 3     # in ps
    
    # Fit msd value
    msd_fit = (data[int(end/2)]-data[int(start/2)])*10**-18/(6*(time[int(end/2)]-time[int(start/2)])*10**-12)

    # Plot msd curve from gromacs and shawod the considered area
    if is_plot:
        plt.title("MSD")
        sns.lineplot(x=time* 10**-3, y=data, **kwargs_line)
        plt.xlabel("time (ns)")
        plt.ylabel("MSD")
        plt.axvspan(xmin=area[0], xmax=area[1], facecolor="grey", alpha=0.3)
    
    # Print self fitted MSD Value
    if is_print:
        print("MSD Diffusion (self): " + "%.4e" % (msd_fit) + " m^2/s")
    
    return msd_fit


def diff_inf_fit(diff_vec, x_vec, x="box", area = [], is_plot = False, is_print = False, kwargs_line={}, kwargs_scatter = {}):
    """
    Fuction to fit diffusion coefficient at an inifinite box size.

    Parameters
    ----------
    diff_vec : list
        list with diffusion coefficients
    box_vec : list 
        list with the box size
    area : list
        x axis limit
    is_print : bool, optional
        True to print msd diffusion coefficient
    is_plot : bool, optional
        True to plot the msd value over the time
    kwargs_line: dict, optional
        Dictionary with plotting parameters for the line plot

    Returns
    -------
    intercept : float
        diffusion coefficient for an inifinite box size
    error : float 
        error of intercept
    """

    

    # Fit to an infinite box size
    if x == "box":
        x_vec = [1/box for box in x_vec]
        if not area:
            area = [0, 1.05 * max(x_vec)]    
    elif x == "number":
        x_vec = [(1/n)**(1/3) for n in x_vec]
        if not area:
            area = [0, 1.05 * max(x_vec)]  

    reg = stats.linregress(x_vec,diff_vec)
    print(reg.slope)
    print(len([(reg.slope*x + reg.intercept)  for x in np.arange(area[0], area[1] + 0.01, 0.01)]))
    print(len(np.arange(area[0], area[1]+ 0.01, 0.01)))
    # Plot msd curve from gromacs and shawod the considered area
    if is_plot:
        sns.lineplot(x=[x for x in np.arange(area[0], area[1]+ 0.01, 0.01)], y= [(reg.slope*x + reg.intercept)  for x in np.arange(area[0], area[1] + 0.01, 0.01)],**kwargs_line)                   
        sns.scatterplot(x=x_vec,y=diff_vec, **kwargs_scatter)
        plt.xlabel("Inverse box (1/nm)")
        plt.ylabel("Diffusion (m^2/s)")
        plt.xlim(area)
   

    
    # Print self fitted MSD Value
    if is_print:
        print("Diffusion (inifinite box): " + "%.4e" % (reg.intercept) + " m^2/s")
        print("Diffusion (inifinite box): " + "%.4e" % (reg.intercept_stderr) + " m^2/s")
    
    return reg.intercept, reg.intercept_stderr


def density(filename, area = [], is_print=False, is_plot=False, kwargs_line={}):
    """
    The function enables a calculation of the mean density in as simulation box
    and can plot the density over the box. As input file a gromacs xvg has to use.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    area : array
        calculate the density between [a,b], default whole box
    is_print : bool, optional
        True to print the mean density
    is_plot : bool, optional
        True to plot the density over the box length
    kwargs_line: dict, optional
        Dictionary with plotting parameters for the line plot

    Returns
    -------
    length : list
        list over box lengthden
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
    if area:
        idx_1 = np.digitize(area[0],length)
        idx_2 = np.digitize(area[1],length)
        density_area_mean = np.mean(density[idx_1:idx_2])
        
    # Print density
    if is_print:            
        print("Density: " + str(density_mean) + " kg m^-3")
        if area:
            print("Density ["+ str(area[0])+","+str(area[1])+"]: " + str(density_area_mean) + " kg m^-3")
    if is_plot:
        plt.title("Density")
        sns.lineplot(x=length, y=density, **kwargs_line)
        if area:
            plt.axvspan(xmin=area[0], xmax=area[1], facecolor="grey", alpha=0.3)
        plt.xlabel("Box length")
        plt.ylabel("Density")

    # Return results
    return length, density, density_mean


def gyrate(filename, is_print=False, is_plot=False, kwargs_line={}):
    """
    The function enables a calculation of the gyration radius for a molcule in a simulation box
    and can plot the gyration over the box. As input file a gromacs xvg has to use.

    Parameters
    ----------
    filename : string
        Link to gromacs analyse output file
    is_print : bool, optional
        True to print the gyration radius
    is_plot : bool, optional
        True to plot the density over the box length
    kwargs_line: dict, optional
        Dictionary with plotting parameters for the line plot

    Returns
    -------
    length : list
        list over box length
    gyrate : list
        list with the gyration radius
    gyrate : float
        mean gyration radius in the simulation Box
    """
    # Read data and set list
    data_file = glob.glob(filename)
    length = []
    gyrate = []

    # Read data
    for i, file in enumerate(data_file):
        length = np.genfromtxt(file, skip_header=28, usecols=0)
        gyrate = np.genfromtxt(file, skip_header=28, usecols=1)

    # Calculate gyrate
    gyrate_mean = np.mean(gyrate)

    # Print gyrate
    if is_print:
        print("gyrate: " + str(gyrate_mean) + " nm")

    if is_plot:
        plt.title("gyrate")
        sns.lineplot(x=length, y=gyrate, **kwargs_line)
        plt.xlabel("Box length")
        plt.ylabel("gyrate")

    # Return results
    return length, gyrate, gyrate_mean



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