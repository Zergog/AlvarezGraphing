import os
import svgutils.transform as sg
freq = 7.5
pantilt = sg.fromfile(os.path.join("svggraphs", f"{freq}GHz", f"{freq}GHzPanTilt.svg"))
heatmap = sg.fromfile(os.path.join("svggraphs", f"{freq}GHz", f"{freq}GHzheatmap.svg"))
pantilt.append(heatmap)
pantilt.save('merged.svg')