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

def getControlPan():
    dir_path = 'controldata/'
    file = f'{freq}_pan_control.xlsx'
    df = pd.read_excel(dir_path + file)
    df = df.rename(columns={f'Angle (deg) - {freq} GHz': 'pan', f'Amplitude (dB) - {freq} GHz': 'amp'})
    df = df[['pan','amp']]
    df = df.sort_values(by=['pan'])
    return df

def getLensPan():
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
def getControlTilt():
    dir_path = 'Control Data/'
    file = f'{freq}_tilt_control.xlsx'
    df = pd.read_excel(dir_path + file)
    df = df.rename(columns={f'Angle (deg) - {freq} GHz': 'tilt', f'Amplitude (dB) - {freq} GHz': 'amp'})
    df = df[['tilt','amp']]
    df = df.sort_values(by=['tilt'])
    return df

def getLensTilt():
    # Interpolate over pan data files, at central pan with specific tilts.
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

controlDf = getControlTilt()
controlTilt = controlDf['tilt']
controlAmpTilt = controlDf['amp']
controlTilt = controlTilt.multiply(np.pi/180)

lensDf = getLensTilt()
lensTilt = lensDf['tilt']
lensAmpTilt = lensDf['amp']
lensTilt = lensTilt.multiply(np.pi/180)


controlDf = getControlPan()
controlPan = controlDf['pan']
controlAmpPan = controlDf['amp']
controlPan = controlPan.multiply(np.pi/180)

lensDf = getLensPan()
lensPan = lensDf['pan']
lensAmpPan = lensDf['amp']
lensPan = lensPan.multiply(np.pi/180)

patches = []
patch = mpatches.Patch(color="red", label="w/ metalens")
patches.append(patch)
patch = mpatches.Patch(color="blue", label="w/o metalens")
patches.append(patch)

fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1, projection='polar')
ax2 = fig.add_subplot(1,2,2, projection='polar')
ax1.plot(lensPan, lensAmpPan, color='red')
ax1.plot(controlPan, controlAmpPan, color='blue')
ax2.plot(lensTilt, lensAmpTilt, color='red')
ax2.plot(controlTilt, controlAmpTilt, color='blue')

ax1.set_thetamin(-30)
ax1.set_thetamax(30)
ax1.set_theta_offset(math.pi/2)

ax2.set_thetamin(-30)
ax2.set_thetamax(30)
ax2.set_theta_offset(math.pi/2)

ax1.title.set_text("Pan Angle")
ax2.title.set_text("Tilt Angle")


ax1.tick_params(labelleft=False, labelright=True,
                labeltop=False, labelbottom=True)
ax2.tick_params(labelleft=True, labelright=False,
                labeltop=False, labelbottom=True)
# trans, _ , _ = ax1.get_xaxis_text1_transform(-30)
# ax1.text(np.deg2rad(30), 0.5, "Theta Label", transform=trans, 
#          rotation=30-90, ha="center", va="center")
fig.text(0.18, 0.47, 'dBm', rotation = -60,
         rotation_mode = 'anchor')

fig.text(0.95, 0.43, 'dBm', rotation = 60,
         rotation_mode = 'anchor')
ax1.text(-0.3, 1.3, "(a)", ha="left", va="top", transform=ax1.transAxes)
ax2.text(-0.3, 1.3, "(b)", ha="left", va="top", transform=ax2.transAxes)

leg = fig.legend(handles=patches,loc=(0.465, 0.3))
fig.tight_layout()

# ax.set_ylim([-70,-50])

# plt.show()
plt.savefig("7.5GHzPanTilt.svg")