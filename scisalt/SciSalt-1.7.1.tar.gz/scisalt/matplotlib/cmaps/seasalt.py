import matplotlib as _mpl
import matplotlib.pyplot as _plt
_plt.rc('axes', color_cycle='577C98, 66BD66, EC8080, ECBE80, BE6698, BBDD77, 585858')
colors = ['#577C98', '#66BD66', '#EC8080', '#BE6698', '#BBDD77', '#585858']
names = ['b', 'g', 'r', 'm', 'y', 'gray']

for code, color in zip(names, colors):
    rgb = _mpl.colors.colorConverter.to_rgb(color)
    _mpl.colors.colorConverter.colors[code] = rgb
    _mpl.colors.colorConverter.cache[code] = rgb
