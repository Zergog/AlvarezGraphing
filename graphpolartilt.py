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

freq = 6

def getControl():
    dir_path = 'Control Data/'
    file = f'{freq}_tilt_control.xlsx'
    df = pd.read_excel(dir_path + file)
    df = df.rename(columns={f'Angle (deg) - {freq} GHz': 'tilt', f'Amplitude (dB) - {freq} GHz': 'amp'})
    df = df[['tilt','amp']]
    df = df.sort_values(by=['tilt'])
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
    df = df[df["pan"] == 0]
    df = df[['tilt', 'amp']]
    df = df.sort_values(by=['tilt'])
    return df

controlDf = getControl()
controlTilt = controlDf['tilt']
controlAmp = controlDf['amp']
controlTilt = controlTilt.multiply(np.pi/180)

lensDf = getLens()
lensTilt = lensDf['tilt']
lensAmp = lensDf['amp']
lensTilt = lensTilt.multiply(np.pi/180)

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
ax.plot(lensTilt, lensAmp, color='red')
ax.plot(controlTilt, controlAmp, color='blue')

ax.set_thetamin(-10)
ax.set_thetamax(10)
# ax.set_ylim([-70,-50])

plt.show()