import os
import pandas as pd
import numpy as np
import matplotlib
import tkinter
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Slider, Button
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np
from scipy.interpolate import griddata

freq = 6
dir_path = f'{freq} GHz Data/tiltpandata/'
file_extension = '.xlsx'
filenames = [file for file in os.listdir(dir_path)]
file_list = []
for file in filenames:
    if file.endswith(file_extension):
        file_list.append(file)
df_list = []
for file in file_list:
    df = pd.read_excel(dir_path + file)
    df = df.rename(columns={f'Angle (deg) - {freq} GHz': 'pan', f'Amplitude (dB) - {freq} GHz': 'amp'})
    df = df[['pan','amp']]
    df = df.assign(tilt=float(file[:-5]))
    df_list.append(df)
df = pd.concat(df_list)


X = df["tilt"]
Y = df["pan"]
Z = df["amp"]
yg = np.linspace(-30, 30, 51)
xg = np.linspace(-10, 9.6, 50)
xgrid, ygrid = np.meshgrid(xg, yg)
ctr_f = griddata((X, Y), Z, (xgrid, ygrid), method='linear')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
extent = (-30, 30, -10, 10)
im = ax.imshow(ctr_f.T, extent=extent, cmap=cm.gist_rainbow, interpolation = 'gaussian')
# ax.contourf(xgrid, ygrid, ctr_f, cmap=cm.coolwarm)
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.5)
cbar.ax.set_ylabel("dBm", rotation=-90)
ax.set_xlabel("Pan Angle (degree)")
ax.set_ylabel("Tilt Angle (Degree)")
ax.text(.01, .99, 'c)', ha='left', va='top', transform=ax.transAxes, color="#FF1441")
plt.savefig("6GHzheatmap.svg")
# plt.show()
