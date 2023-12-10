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

dir_path = '6 GHz Data/'
file_extension = '.csv'

df = readfromseventh(dir_path + "6 GHz 24 cm gain bandwidth.csv")
df = df.rename(columns={'Freq(Hz)': 'freq', 'S21 Log Mag(dB)': 'mag'})
df = df.div({"freq": 10**9, "mag": 1})
df = df[(df["freq"] >= 4) & (df["freq"] <= 8)]
fig, ax = plt.subplots()
ax.plot(df["freq"],df["mag"], marker='.', markersize=3)
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Gain Enhancement (dB)")
ax.text(.01, .99, 'd)', ha='left', va='top', transform=ax.transAxes)
plt.savefig("6GHzGainEnhancement.svg")
# plt.show()