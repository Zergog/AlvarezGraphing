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

# Match slider values to the closest values in the frequency list
def find_closest_values(s, x):
    idx = (np.abs(s - x)).argmin()
    return s.iloc[idx]

# Given a specific frequency, scatter plot the data
def plot_dfs(separation_list, frequency):
    colors = cm.rainbow(np.linspace(0, 1, len(separation_list)))
    patches = []
    for df, c, foldername in zip(separation_list, colors, foldernames):
        df_temp = df[df["freq"] == frequency]
        ax.plot(df_temp["dist"],df_temp["mag"], marker='.', markersize=3, color=c)
        patch = mpatches.Patch(color=c, label=foldername)
        patches.append(patch)
    ax.legend(handles=patches)

# The function to be called anytime a slider's value changes
def update(val):
    df = separation_list[0]
    frequency = find_closest_values(df["freq"], val)
    ax.clear()
    plot_dfs(separation_list, frequency)
    ax.set_ylim(-20, 20)

# Create a dataset corresponding to a specific frequency
def createseparationdf(foldername):
    filenames = [file for file in os.listdir(foldername)]
    file_list = []
    for file in filenames:
        if file.endswith(file_extension):
            file_list.append(file)

    df_list = []
    for file in file_list:
        df = readfromseventh(foldername + file)
        df = df.assign(dist=int(file[:-4]))
        df_list.append(df)
    big_df = pd.concat(df_list)
    df = big_df.rename(columns={'Freq(Hz)': 'freq', 'S21 Log Mag(dB)': 'mag'})
    df = df.div({"freq": 10**9, "mag": 1, "dist": 1})
    df = df.sort_values(by=['freq', 'dist'])
    return df


dir_path = 'Variable Lens Distance Data/'
file_extension = '.csv'
separation_list = []
foldernames = [folder for folder in os.listdir(dir_path)]
# Iterate through  each frequency folder, then create a list of datasets corresponding to each frequency
for folder in foldernames:
    df = createseparationdf(dir_path + folder + '/')
    separation_list.append(df)
fig, ax = plt.subplots()

# set initial frequency and plot values
initfreq = 7
initfreq = find_closest_values(separation_list[0]["freq"], initfreq)
plot_dfs(separation_list, initfreq)

# Make a horizontally oriented slider to control the frequency
axb = plt.axes([0.1, 0.05, 0.8, 0.05])
slider = Slider(
    ax=axb,
    label="Frequency",
    valmin=0,
    valmax=15,
    valinit=initfreq,
    orientation="horizontal"
)
slider.on_changed(update)
ax.set_ylim(-20, 20)
plt.show()