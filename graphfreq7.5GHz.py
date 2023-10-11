import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import matplotlib.cm as cm
import matplotlib.patches as mpatches

# Read in data from files with a header, ignoring the first few lines
def readfromseventh(filename):
    skip_func = lambda x: (x<6 or x==1008)
    df = pd.read_csv(filename, skiprows = skip_func)
    return df

dir_path = '7.5 GHz/'
file_extension = '.csv'

11.223544/15.468312


df = readfromseventh(dir_path + "7.5GHz 39 cm gain bandwidth.csv")
df = df.rename(columns={'Freq(Hz)': 'freq', 'S21 Log Mag(dB)': 'mag'})
df = df.div({"freq": 10**9, "mag": 1})
df = df[(df["freq"] >= 4.5) & (df["freq"] <= 10.5)]
fig, ax = plt.subplots()
ax.plot(df["freq"],df["mag"]*11.223544/15.468312, marker='.', markersize=3)
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Gain Enhancement (dB)")
ax.text(.01, .99, 'd)', ha='left', va='top', transform=ax.transAxes)
plt.savefig("7.5GHzGainEnhancement.svg")
# plt.show()