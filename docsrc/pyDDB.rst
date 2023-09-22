.. code:: ipython3

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import gro_exp

Example Notebook for pyDB
=========================

Read the density data from two components from a DDB Data Excel File
over a specified temperature area for a pressure of 1 bar

.. code:: ipython3

    # Set the tempature area
    temp_vec = np.linspace(280.15,300.15,21)
    
    # Read the data with the following function
    data, prop_dict = gro_exp.ddb.read_exp_temp_vec("benzene_exp_density.xls", temp_vec, "DEN", 
                            press=101325.000,tol_p=10000, p_nan=False, is_plot=True, is_display=False)




.. image:: pics/output_2_0.png


The data dictionary contains the Mean properties, standard deviation and
number of data points at the specified temperatures. The prop_dict
dictonary contains the data points which are used to calculate the mean
values at the specified temperature. In the following cell shows some
content for these dictonarys

.. code:: ipython3

    # Define the temperature which you would like consider
    temp = 288.15
    
    # Data frames 
    df_mean = pd.DataFrame(data)
    display(df_mean)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Temperature (K)</th>
          <th>DEN (kg/m3)</th>
          <th>STD (kg/m3)</th>
          <th>Number of data points</th>
          <th>References</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>280.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>1</th>
          <td>281.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>2</th>
          <td>282.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>3</th>
          <td>283.15</td>
          <td>889.606250</td>
          <td>0.208877</td>
          <td>12.0</td>
          <td>[Sun T.F., Schouten J.A., Trappeniers N.J., Bi...</td>
        </tr>
        <tr>
          <th>4</th>
          <td>284.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>5</th>
          <td>285.15</td>
          <td>887.500000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>6</th>
          <td>286.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>7</th>
          <td>287.15</td>
          <td>885.400000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>8</th>
          <td>288.15</td>
          <td>884.275056</td>
          <td>0.154745</td>
          <td>18.0</td>
          <td>[Nowak J., Malecki J., Thiebaut J.-M., Rivail ...</td>
        </tr>
        <tr>
          <th>9</th>
          <td>289.15</td>
          <td>883.340000</td>
          <td>0.140000</td>
          <td>2.0</td>
          <td>[Meyer J., Mylius B., Z.Phys.Chem.(Leipzig), 9...</td>
        </tr>
        <tr>
          <th>10</th>
          <td>290.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>11</th>
          <td>291.15</td>
          <td>881.100000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>12</th>
          <td>292.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>13</th>
          <td>293.15</td>
          <td>878.951217</td>
          <td>0.657108</td>
          <td>69.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>14</th>
          <td>294.15</td>
          <td>876.400000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Golubev I.F., Frolova M.G., Trudy Gos.NIPI In...</td>
        </tr>
        <tr>
          <th>15</th>
          <td>295.15</td>
          <td>876.900000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>16</th>
          <td>296.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>17</th>
          <td>297.15</td>
          <td>873.600000</td>
          <td>0.778888</td>
          <td>3.0</td>
          <td>[Hayworth K.E., Lenoir J.M., Hipkin H.G., J.Ch...</td>
        </tr>
        <tr>
          <th>18</th>
          <td>298.15</td>
          <td>873.548792</td>
          <td>0.825668</td>
          <td>197.0</td>
          <td>[Nowak J., Malecki J., Thiebaut J.-M., Rivail ...</td>
        </tr>
        <tr>
          <th>19</th>
          <td>299.15</td>
          <td>872.600000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>20</th>
          <td>300.15</td>
          <td>871.500000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Singh S., Sivanarayana K., Kushwaha R., Praka...</td>
        </tr>
      </tbody>
    </table>
    </div>


It is possible to plot the data points at a temperature to see the
outliers

.. code:: ipython3

    # Plot data for a specified temperature
    temp=298.15
    temp_off = gro_exp.ddb.plot_data(prop_dict,temp)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Mean</th>
          <th>STD</th>
          <th>Number of data points</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>298.15</th>
          <td>873.548792</td>
          <td>0.825668</td>
          <td>197</td>
        </tr>
      </tbody>
    </table>
    </div>



.. image:: pics/output_6_1.png


If you specified the outliers you can drop these and calculate a new
data dictonary

.. code:: ipython3

    # Drop outliers for the considered temperature
    df_mean = pd.DataFrame(data)
    data = gro_exp.ddb.drop_outliers(data,prop_dict,temp, [872,876])
    display(df_mean)
    




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Temperature (K)</th>
          <th>DEN (kg/m3)</th>
          <th>STD (kg/m3)</th>
          <th>Number of data points</th>
          <th>References</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>280.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>1</th>
          <td>281.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>2</th>
          <td>282.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>3</th>
          <td>283.15</td>
          <td>889.606250</td>
          <td>0.208877</td>
          <td>12.0</td>
          <td>[Sun T.F., Schouten J.A., Trappeniers N.J., Bi...</td>
        </tr>
        <tr>
          <th>4</th>
          <td>284.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>5</th>
          <td>285.15</td>
          <td>887.500000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>6</th>
          <td>286.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>7</th>
          <td>287.15</td>
          <td>885.400000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>8</th>
          <td>288.15</td>
          <td>884.275056</td>
          <td>0.154745</td>
          <td>18.0</td>
          <td>[Nowak J., Malecki J., Thiebaut J.-M., Rivail ...</td>
        </tr>
        <tr>
          <th>9</th>
          <td>289.15</td>
          <td>883.340000</td>
          <td>0.140000</td>
          <td>2.0</td>
          <td>[Meyer J., Mylius B., Z.Phys.Chem.(Leipzig), 9...</td>
        </tr>
        <tr>
          <th>10</th>
          <td>290.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>11</th>
          <td>291.15</td>
          <td>881.100000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>12</th>
          <td>292.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>13</th>
          <td>293.15</td>
          <td>878.951217</td>
          <td>0.657108</td>
          <td>69.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>14</th>
          <td>294.15</td>
          <td>876.400000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Golubev I.F., Frolova M.G., Trudy Gos.NIPI In...</td>
        </tr>
        <tr>
          <th>15</th>
          <td>295.15</td>
          <td>876.900000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>16</th>
          <td>296.15</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[]</td>
        </tr>
        <tr>
          <th>17</th>
          <td>297.15</td>
          <td>873.600000</td>
          <td>0.778888</td>
          <td>3.0</td>
          <td>[Hayworth K.E., Lenoir J.M., Hipkin H.G., J.Ch...</td>
        </tr>
        <tr>
          <th>18</th>
          <td>298.15</td>
          <td>873.548792</td>
          <td>0.825668</td>
          <td>197.0</td>
          <td>[Nowak J., Malecki J., Thiebaut J.-M., Rivail ...</td>
        </tr>
        <tr>
          <th>19</th>
          <td>299.15</td>
          <td>872.600000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Wang F., Evangelista R.F., Threatt T.J., Tava...</td>
        </tr>
        <tr>
          <th>20</th>
          <td>300.15</td>
          <td>871.500000</td>
          <td>0.000000</td>
          <td>1.0</td>
          <td>[Singh S., Sivanarayana K., Kushwaha R., Praka...</td>
        </tr>
      </tbody>
    </table>
    </div>


Now you can plot and display the new mean values after the adjustment

.. code:: ipython3

    gro_exp.ddb.plot_means(data)



.. image:: pics/output_10_0.png


After all you can save the data in a obj file and reload at and plot it
again

.. code:: ipython3

    gro_exp.utils.save_data("test.obj",data)
    data = gro_exp.utils.load_data("test.obj")
    gro_exp.ddb.plot_means(data)



.. image:: pics/output_12_0.png

