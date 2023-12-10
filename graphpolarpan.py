from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
import numpy as np
import mpl_toolkits.axisartist.angle_helper as angle_helper
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist.grid_finder import (FixedLocator, MaxNLocator,
                                                 DictFormatter)
import matplotlib.pyplot as plt
import pandas as pd
import math
import os
import matplotlib.patches as mpatches


freq = 6

def getControl():
    dir_path = 'controldata/'
    file = f'{freq}_pan_control.xlsx'
    df = pd.read_excel(dir_path + file)
    df = df.rename(columns={f'Angle (deg) - {freq} GHz': 'pan', f'Amplitude (dB) - {freq} GHz': 'amp'})
    df = df[['pan','amp']]
    df = df.sort_values(by=['pan'])
    return df

def getLens():
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
    df = df[df["tilt"] == 0]
    df = df[['pan', 'amp']]
    df = df.sort_values(by=['pan'])
    return df

controlDf = getControl()
controlTilt = controlDf['pan']
controlAmp = controlDf['amp']
controlTilt = controlTilt.multiply(np.pi/180)

lensDf = getLens()
lensTilt = lensDf['pan']
lensAmp = lensDf['amp']
lensTilt = lensTilt.multiply(np.pi/180)


fig = plt.figure()
ax = fig.add_subplot(projection='polar')
ax.plot(lensTilt, lensAmp, color='red')
ax.plot(controlTilt, controlAmp, color='blue')

ax.set_thetamin(-30)
ax.set_thetamax(30)
ax.set_theta_offset(math.pi/2)
ax.set_rlabel_position
patches = []
patch = mpatches.Patch(color="blue", label="w/ metalens")
patches.append(patch)
patch = mpatches.Patch(color="red", label="w/o metalens")
patches.append(patch)
ax.legend(handles=patches)
# ax.set_ylim([-70,-50])

plt.show()