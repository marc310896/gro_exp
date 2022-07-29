import os
import sys

import copy
import shutil
import unittest

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import gro_exp


class UserModelCase(unittest.TestCase):
    #################
    # Remove Output #
    #################
    @classmethod
    def setUpClass(self):
        if os.path.isdir("tests"):
            os.chdir("tests")

        folder = "output"
        if not os.path.exists('output'):
            os.makedirs('output')
        if not os.path.exists("output/temp"):
            os.makedirs("output/temp")
        open(folder+"/temp.txt", 'a').close()

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # Test functions to read msd and
    def test_gromacs_analyse(self):

        gro_exp.utils.density("data/density.xvg", is_print=True, is_plot=True)
        data_msd = gro_exp.utils.msd("data/msd.xvg", is_print=True, is_plot=True)
        gro_exp.utils.msd_fit(data_msd, area=[0,5], is_print=True, is_plot=True)

    # Test function to read DDB Data Bank
    def test_ddb(self):
        # Set the tempature area
        temp_vec = np.linspace(280.15,300.15,21)

        # Read the data with the following function
        data, prop_dict = gro_exp.ddb.read_exp_temp_vec("data/benzene_exp_density.xls", temp_vec, "DEN", press=101325.000, p_nan=False, is_plot=True, is_display=False)

        # Plot data for a specified temperature
        temp = 288.15
        gro_exp.ddb.plot_data(prop_dict,temp)

        # Drop outliers for the considered temperature
        data = gro_exp.ddb.drop_outliers(data,prop_dict,temp, [810,820])

        # Plot new data dictonary
        gro_exp.ddb.plot_means(data)

    def utils(self):
        data = gro_exp.utils.load_data("data/test.obj")
        gro_exp.utils.save_data("output/test.obj", data)


    def test_benchmark_function(self):
        ns_h_1core = [0.762,1.344,2.045,2.755,3.448,4.013,4.199,4.518]
        cpus_1core = [1,2,3,4,5,6,7,8]

        gro_exp.utils.bench_plot(ns_h_1core, cpus_1core)
        gro_exp.utils.bench_table(ns_h_1core, cpus_1core, 200, print_con=True)

        ns_h = [ 31.297,51.343,40.657,44.627,46.823,46.984,47.606,43.642,44.444,43.502,42.243,41.988,39.320,27.012,38.910,34.992,34.540,23.975,34.915,34.435]
        gro_exp.utils.bench_plot(ns_h, 75, nodes=True)
        gro_exp.utils.bench_table(ns_h, 75, 200, nodes=True, print_con=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
