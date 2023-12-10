# AlvarezGraphing

6 GHz Data and 7.5 GHz Data: Contains the tilt and pan data in tiltpandata, each filename (ex -0.4.xlsx) representing the tilt of that sweep and each Angle (deg) in the file representing the pan. Also contains gain measurements at different frequencies for the optimal spacing and lens separation at 6 and 7.5 GHz. Some unused tilt sweep data as well, we chose to interpolate over the pan data (taking the pan 0 deg datapoints at various tilts) since the gimbal had trouble with tilt sweeps.

Control Data: Contains gain and pan/tilt data when the lenses were not mounted, ie transmitting directly across the chamber. We were able to get tilt sweep measurements without the lens mounted, as the gimbal was affected by its weight.

Variable Lens Distance Data: Data collected with lenses at various separations (folder names). File names are the distance of the lens from the emitting horn.