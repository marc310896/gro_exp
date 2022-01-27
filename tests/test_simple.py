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

    def test_gromacs_analyse(self):

        gro_exp.utils.density("data/density.xvg", is_print=True)
        gro_exp.utils.msd("data/msd.xvg", is_print=True)
        plt.show()


if __name__ == '__main__':
    unittest.main(verbosity=2)
