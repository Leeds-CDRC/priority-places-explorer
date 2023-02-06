import matplotlib
import numpy as np

# Used to pick colours for data visualisation 
cmap = matplotlib.cm.get_cmap('plasma')
colors = [matplotlib.colors.to_hex(cmap(i)) for i in np.arange(0,1,0.08)]

print(colors)