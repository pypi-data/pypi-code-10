'''
Plot sensor maps.
'''
# author: Christian Brodbeck
from itertools import izip
from math import sin, cos, asin
import os

import numpy as np
import matplotlib as mpl
from matplotlib.lines import Line2D

from .._data_obj import SEQUENCE_TYPES, Datalist, as_sensor
from ._base import _EelFigure


SENSOR_AXES_FRAME = 0.0
SENSORMAP_FRAME = 0.1


# some useful kwarg dictionaries for different plot layouts
kwargs_mono = dict(mc='k',
                   lc='.5',
                   hllc='k',
                   hlmc='k',
                   hlms=7,
                   strlc='k')


def _head_outlines(radius, center=0):
    # generate outlines for center 0, radius 1
    nose_alpha = 0.2
    l = np.linspace(0, 2 * np.pi, 101)
    head_x = np.cos(l)
    head_y = np.sin(l)
    w = sin(nose_alpha)
    nose_x = np.array((-w, -w * 0.5, -w * 0.2, 0, w * 0.2, w * 0.5, w))
    ymin = cos(nose_alpha)
    nose_y = np.array((ymin, 1.02, 1.09, 1.1, 1.09, 1.02, ymin))
    ear_y = np.array((0.15, 0.145, 0.135, 0.125, 0.111, -0.011, -0.1864,
                      -0.2626, -0.2768, -0.2398))
    ear_x_right = np.array((cos(asin(ear_y[0])), 1., 1.02, 1.025, 1.03, 1.04,
                            1.07, 1.06, 1.02, cos(asin(ear_y[-1]))))
    ear_x_left = -ear_x_right

    # apply radius and center
    if isinstance(radius, SEQUENCE_TYPES):
        rx, ry = radius
    else:
        rx = ry = radius

    if isinstance(center, SEQUENCE_TYPES):
        cx, cy = center
        cx += 0.5
        cy += 0.5
    else:
        cx = 0.5
        cy = center + 0.5

    for item in (head_x, nose_x, ear_x_right, ear_x_left):
        item *= rx
        item += cx

    for item in (head_y, nose_y, ear_y):
        item *= ry
        item += cy

    return ((head_x, head_y), (nose_x, nose_y), (ear_x_left, ear_y),
            (ear_x_right, ear_y))


class _plt_connectivity:
    def __init__(self, ax, locs, connectivity, linestyle={}):
        self.ax = ax
        self.locs = locs
        self._h = []
        self.show(connectivity, linestyle)

    def show(self, connectivity, linestyle={}):
        while self._h:
            self._h.pop().remove()

        if connectivity is None:
            return

        for c, r in connectivity:
            x = self.locs[[c, r], 0]
            y = self.locs[[c, r], 1]
            line = Line2D(x, y, **linestyle)
            self.ax.add_line(line)
            self._h.append(line)


class _ax_map2d:

    def __init__(self, ax, sensors, proj, extent, size, color, marker,
                 mark=None, head_radius=None, head_pos=0., head_linewidth=None):
        self.ax = ax

        # ax.set_frame_on(False)
        ax.set_axis_off()

        self.sensors = _plt_map2d(ax, sensors, proj, extent, marker, size,
                                  color, mark, None, None, True, head_radius,
                                  head_pos, head_linewidth)

        locs = sensors.get_locs_2d(proj, extent)
        self.connectivity = _plt_connectivity(ax, locs, None)

        ax.set_aspect('equal')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    def mark_sensors(self, *args, **kwargs):
        self.sensors.mark_sensors(*args, **kwargs)

    def remove(self):
        "remove from axes"
        self.sensors.remove()


class _plt_map2d:

    def __init__(self, ax, sensors, proj, extent, marker, size, color, mark,
                 mcolor, labels, invisible, head_radius, head_pos,
                 head_linewidth):
        """
        Parameters
        ----------
        ax : matplotlib Axes
            Axes.
        sensors : Sensor
            Sensor dimension.

        labels : None | 'index' | 'name' | 'fullname'
            Content of the labels. For 'name', any prefix common to all names
            is removed; with 'fullname', the full name is shown.
        """
        self.ax = ax
        self.sensors = sensors
        self.locs = sensors.get_locs_2d(proj, extent, SENSORMAP_FRAME)
        self._index = None if invisible else sensors._visible_sensors(proj)
        self._extent = extent

        # head outline
        if head_radius:
            if head_radius is True:
                head_radius = 0.5 * (1 - (SENSORMAP_FRAME * 0.9))

            if head_linewidth is None:
                head_linewidth = mpl.rcParams['lines.linewidth']

            for x, y in _head_outlines(head_radius, head_pos):
                ax.plot(x, y, color='k', linewidth=head_linewidth,
                        solid_capstyle='butt', clip_on=False)

        # sensors
        index = slice(None) if self._index is None else self._index
        self._sensor_h = ax.scatter(self.locs[index, 0], self.locs[index, 1],
                                    size, color, marker)

        self._label_h = []
        if labels:
            self.show_labels(labels)

        self._mark_handles = []
        if mark is not None:
            self.mark_sensors(mark, c=mcolor)

    def mark_sensors(self, sensors, s=20, c='yellow', *args, **kwargs):
        """Mark specific sensors

        Parameters
        ----------
        sensors : None | Sensor dimension index
            Sensors which should be marked (None to clear all markings).
        others :
            Matplotlib :func:`pyplot.scatter` parameters for the marking
            sensors.
        """
        if sensors is None:
            while self._mark_handles:
                self._mark_handles.pop().remove()
            return

        if c is None:
            c = 'yellow'

        idx = self.sensors.dimindex(sensors)
        h = self.ax.scatter(self.locs[idx, 0], self.locs[idx, 1], s, c, *args,
                            **kwargs)
        self._mark_handles.append(h)

    def remove(self):
        "remove from axes"
        self._sensor_h.remove()
        while self._mark_handles:
            self._mark_handles.pop().remove()

    def show_labels(self, text='name', xpos=0, ypos=0, ha='center', va='bottom',
                    **text_kwargs):
        """Plot labels for the sensors

        Parameters
        ----------
        text : None | 'index' | 'name' | 'fullname'
            Content of the labels. For 'name', any prefix common to all names
            is removed; with 'fullname', the full name is shown.
        xpos, ypos : scalar
            The position offset of the labels from the sensor markers.
        text_kwargs : **
            Matplotlib text parameters.
        """
        # remove existing labels
        while self._label_h:
            self._label_h.pop().remove()

        if not text or text == 'none':
            return

        if text == 'index':
            labels = map(str, xrange(len(self.sensors)))
        elif text == 'name':
            labels = self.sensors.names
            prefix = os.path.commonprefix(labels)
            pf_len = len(prefix)
            labels = [label[pf_len:] for label in labels]
        elif text == 'fullname':
            labels = self.sensors.names
        else:
            err = "text has to be 'index' or 'name', can't be %r" % text
            raise NotImplementedError(err)

        locs = self.locs
        if self._index is not None:
            labels = Datalist(labels)[self._index]
            locs = locs[self._index]

        locs = locs + [[xpos, ypos]]
        for (x, y), txt in izip(locs, labels):
            h = self.ax.text(x, y, txt, ha=ha, va=va, **text_kwargs)
            self._label_h.append(h)

    def separate_labels(self, pad):
        # separate overlapping labels
        locs = self.locs
        data_to_screen = self.ax.transData.transform_point
        screen_to_data = self.ax.transData.inverted().transform_point

        if self._extent:
            center = self._extent / 2.
            label_order = np.argsort((locs[:, 0] - center) ** 2)
        else:
            center = 0
            label_order = np.argsort(locs[:, 0] ** 2)

        n_labels = len(label_order)
        for i in xrange(1, n_labels):
            i_i = label_order[i]
            i_loc = locs[i_i, 0]
            if i_loc == center:
                continue
            h = self._label_h[i_i]
            i_bbox = h.get_window_extent()
            padded_bbox = i_bbox.expanded(pad, 0)
            side = -1 if i_loc < center else 1

            dx = 0
            for j in xrange(i):
                j_i = label_order[j]
                j_bbox = self._label_h[j_i].get_window_extent()
                if padded_bbox.overlaps(j_bbox):
                    if side == -1:
                        dx = min(dx, j_bbox.xmin - i_bbox.xmax - pad)
                    else:
                        dx = max(dx, j_bbox.xmax - i_bbox.xmin + pad)

            if dx:
                x, y = data_to_screen(h.get_position())
                h.set_position(screen_to_data((x + dx, y)))

    def set_label_color(self, color='k'):
        """Change the color of all sensor labels

        Parameters
        ----------
        color : matplotlib color
            New color for the sensor labels.
        """
        for h in self._label_h:
            h.set_color(color)


class SensorMapMixin:
    # expects self._sensor_plots to be list of _plt_map2d
    __label_options = ['None', 'Index', 'Name', 'Full Name']
    __label_option_args = ['none', 'index', 'name', 'fullname']

    def __init__(self, sensor_plots, label=None):
        """Call after EelFigure init (toolbar fill)

        Parameters
        ----------
        sensor_plots : list of _plt_map2d
            Sensor-map objects.
        label : None | str
            Initial label argument (default None).
        """
        if not label:
            label = 'none'
        self.__label_color = 'k'
        self.__check_label_arg(label)
        self.__sensor_plots = sensor_plots
        self.__LabelChoice.SetSelection(self.__label_option_args.index(label))

    def _fill_toolbar(self, tb):
        import wx
        tb.AddSeparator()

        # sensor labels
        lbl = wx.StaticText(tb, -1, "Labels:")
        tb.AddControl(lbl)
        choice = wx.Choice(tb, -1, choices=self.__label_options)
        tb.AddControl(choice)
        self.__LabelChoice = choice
        choice.Bind(wx.EVT_CHOICE, self.__OnSensorLabelChoice)

        # sensor label color
        choices = ['black', 'white', 'blue', 'green', 'red', 'cyan', 'magenta',
                   'yellow']
        choice = wx.Choice(tb, -1, choices=choices)
        tb.AddControl(choice)
        self.__LabelColorChoice = choice
        choice.Bind(wx.EVT_CHOICE, self.__OnSensorLabelColorChoice)

        btn = wx.Button(tb, label="Mark")  # , style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, self.__OnMarkSensor)
        tb.AddControl(btn)

    def __check_label_arg(self, arg):
        if arg not in self.__label_option_args:
            raise ValueError("Invalid sensor label argument: %s" % repr(arg))

    def __OnMarkSensor(self, event):
        import wx
        msg = "Channels to mark, separated by comma"
        dlg = wx.TextEntryDialog(self._frame, msg, "Mark Sensor")
        if dlg.ShowModal() != wx.ID_OK:
            return

        chs = filter(None, map(unicode.strip, dlg.GetValue().split(',')))
        try:
            self.mark_sensors(chs)
        except Exception as exc:
            msg = '%s: %s' % (type(exc).__name__, exc)
            sty = wx.OK | wx.ICON_ERROR
            wx.MessageBox(msg, "Mark Sensors Failed for %r" % chs, style=sty)

    def __OnSensorLabelChoice(self, event):
        sel = event.GetSelection()
        sel_arg = self.__label_option_args[sel]
        self.set_label_text(sel_arg)

    def __OnSensorLabelColorChoice(self, event):
        sel = event.GetSelection()
        color = ['k', 'w', 'b', 'g', 'r', 'c', 'm', 'y'][sel]
        self.set_label_color(color)

    def mark_sensors(self, sensors, *args, **kwargs):
        """Mark given sensors on the plots

        Parameters
        ----------
        sensors : None | Sensor dimension index
            Sensors which should be marked (None to clear all markings).
        s : scalar | sequence of scalars
            Marker size(s) in points^2.
        c : color | sequence of colors
            Marker color(s).
        marker : str
            Marker style, default: ``'o'``.

        (Matplotlib :func:`pyplot.scatter` parameters)
        """
        for p in self.__sensor_plots:
            p.mark_sensors(sensors, *args, **kwargs)
        self.draw()

    def separate_labels(self, pad=10):
        """Move overlapping labels apart along the x axis

        Parameters
        ----------
        pad : scalar
            Minimum amount of padding between labels (in pixels; default 5).
        """
        for p in self.__sensor_plots:
            p.separate_labels(pad)
        self.draw()

    def set_label_color(self, color='w'):
        if hasattr(self, '_SensorLabelChoice'):
            sels = ['k', 'w', 'b', 'g', 'r', 'c', 'm', 'y']
            if color in sels:
                sel = sels.index(color)
                self.__LabelColorChoice.SetSelection(sel)

        self.__label_color = color
        for p in self.__sensor_plots:
            p.set_label_color(color)
        self.draw()

    def set_label_text(self, text='name'):
        """Add/remove sensor labels

        Parameters
        ----------
        labels : None | 'name' | 'index'
            Content of the labels. For 'name', any prefix common to all names
            is removed; with 'fullname', the full name is shown.
        """
        self.__check_label_arg(text)
        if hasattr(self, '_SensorLabelChoice'):
            sel = self.__label_option_args.index(text)
            self.__LabelChoice.SetSelection(sel)

        for p in self.__sensor_plots:
            p.show_labels(text, color=self.__label_color)
        self.draw()


class SensorMaps(_EelFigure):
    """Multiple views on a sensor layout.

    Allows selecting sensor groups and retrieving corresponding indices.

    Parameters
    ----------
    sensors : Sensor | NDVar
        The sensors to use, or an NDVar with a sensor dimension.
    select : list of int
        Initial selection.
    proj : str
        Sensor projection for the fourth plot.
    size : scalar
        Size for the sensor markers.
    color : matplotlib color
        Color for the sensor markers.
    marker : str
        Marker for the sensor positions.
    frame : scalar
        Size of the empty space around sensors in axes.
    title : None | string
        Figure title.

    Notes
    -----
    **Selecting Sensor Groups:**

     - Dragging with the left mouse button adds sensors to the selection.
     - Dragging with the right mouse button removes sensors from the current
       selection.
     - The 'Clear' button (or :meth:`clear`) clears the selection.

    """
    def __init__(self, sensors, select=[], proj='default', size=1,
                 color='k', marker='.', frame=0.05, *args, **kwargs):
        sensors = as_sensor(sensors)

        # layout figure
        ftitle = 'SensorMaps'
        sens_name = getattr(sensors, 'sysname', None)
        if sens_name:
            ftitle = '%s: %s' % (ftitle, sens_name)

        self._drag_ax = None
        self._drag_x = None
        self._drag_y = None
        _EelFigure.__init__(self, ftitle, 4, 3, 1, False, ncol=2, nrow=2, *args,
                            **kwargs)
        self.figure.subplots_adjust(left=0, bottom=0, right=1, top=1,
                                    wspace=.1, hspace=.1)

        # store args
        self._sensors = sensors

        ext = np.vstack((sensors.locs.min(0), sensors.locs.max(0)))
        aframe = np.array([-frame, frame])
        xlim = ext[:, 0] + aframe
        ylim = ext[:, 1] + aframe
        zlim = ext[:, 2] + aframe

        # back
        ax = self.ax0 = self.figure.add_subplot(2, 2, 1)
        ax.proj = 'y-'
        ax.extent = False
        self._h0 = _ax_map2d(ax, sensors, ax.proj, ax.extent, size, color, marker)

        # left
        ax = self.ax1 = self.figure.add_subplot(2, 2, 2, sharey=self.ax0)
        ax.proj = 'x-'
        ax.extent = False
        self._h1 = _ax_map2d(ax, sensors, ax.proj, ax.extent, size, color, marker)

        # top
        ax = self.ax2 = self.figure.add_subplot(2, 2, 3, sharex=self.ax0)
        ax.proj = 'z+'
        ax.extent = False
        self._h2 = _ax_map2d(ax, sensors, ax.proj, ax.extent, size, color, marker)

        self.ax0.set_xlim(*xlim)
        self.ax0.set_ylim(*zlim)
        self.ax1.set_xlim(*zlim)
        self.ax2.set_ylim(*ylim)

        # proj
        ax = self.ax3 = self.figure.add_subplot(2, 2, 4)
        ax.proj = proj
        ax.extent = 1
        self._h3 = _ax_map2d(ax, sensors, ax.proj, ax.extent, size, color, marker)
        self.ax3.set_xlim(-frame, 1 + frame)
        self.ax3.set_ylim(-frame, 1 + frame)

        self._sensor_maps = (self._h0, self._h1, self._h2, self._h3)
        self._show()

        # selection
        self.sel_kwargs = dict(marker='o', s=5, c='r', linewidths=.9)
        self._sel_h = []
        if select is not None:
            self.set_selection(select)
        else:
            self.select = None

        # setup mpl event handling
        self.canvas.mpl_connect("button_press_event", self._on_button_press)
        self.canvas.mpl_connect("button_release_event", self._on_button_release)

    def _fill_toolbar(self, tb):
        import wx

        tb.AddSeparator()

        # plot labels
        btn = wx.Button(tb, wx.ID_CLEAR, "Clear")
        tb.AddControl(btn)
        btn.Bind(wx.EVT_BUTTON, self._OnClear)

    def clear(self):
        "Clear the current sensor selection."
        self.select = None
        self.update_mark_plot()

    def get_selection(self):
        """
        Returns
        -------
        selection : list
            Returns the current selection as a list of indices.
        """
        if self.select is None:
            return []
        else:
            return np.where(self.select)[0]

    def _on_button_press(self, event):
        ax = event.inaxes
        if ax:
            self._is_dragging = True
            self._drag_ax = event.inaxes
            self._drag_x = event.xdata
            self._drag_y = event.ydata

            self.canvas.store_canvas()
            x = np.ones(5) * event.xdata
            y = np.ones(5) * event.ydata
            self._drag_rect = ax.plot(x, y, '-k')[0]

    def _on_button_release(self, event):
        if not hasattr(self, '_drag_rect'):
            return

        x = self._drag_rect.get_xdata()
        y = self._drag_rect.get_ydata()
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)

        ax = self._drag_ax
        locs = self._sensors.get_locs_2d(ax.proj, ax.extent)
        x = locs[:, 0]
        y = locs[:, 1]
        sel = (x > xmin) & (x < xmax) & (y > ymin) & (y < ymax)

        if self.select is None:
            self.select = sel
        elif event.button == 1:
            self.select[sel] = True
        else:
            self.select[sel] = False

        # clear dragging-related attributes
        self._drag_rect.remove()
        del self._drag_rect
        self._drag_ax = None
        self._drag_x = None
        self._drag_y = None

        self.update_mark_plot()

    def _on_motion(self, event):
        super(self.__class__, self)._on_motion(event)
        ax = event.inaxes
        if ax and ax is self._drag_ax:
            x0 = self._drag_x
            x1 = event.xdata
            y0 = self._drag_y
            y1 = event.ydata
            x = [x0, x1, x1, x0, x0]
            y = [y0, y0, y1, y1, y0]
            self._drag_rect.set_data(x, y)
            self.canvas.redraw(artists=[self._drag_rect])

    def _OnClear(self, event):
        self.clear()

    def set_selection(self, select):
        """
        Set the current selection with a list of indices.

        Parameters
        ----------
        select : sensor index
            Index for sensor dimension, for example array_like of int, or list
            of sensor names.
        """
        idx = self._sensors.dimindex(select)
        self.select = np.zeros(len(self._sensors), dtype=bool)
        self.select[idx] = True
        self.update_mark_plot()

    def update_mark_plot(self):
        for h in self._sensor_maps:
            h.sensors.mark_sensors(self.select, **self.sel_kwargs)
        self.canvas.draw()


class SensorMap(SensorMapMixin, _EelFigure):
    """Plot sensor positions in 2 dimensions

    Parameters
    ----------
    sensors : NDVar | Sensor
        sensor-net object or object containing sensor-net
    labels : None | 'index' | 'name' | 'fullname'
        Content of the labels. For 'name', any prefix common to all names
        is removed; with 'fullname', the full name is shown.
    proj:
        Transform to apply to 3 dimensional sensor coordinates for plotting
        locations in a plane
    size : scalar
        Size for the sensor markers.
    color : matplotlib color
        Color for the sensor markers.
    marker : str
        Marker for the sensor positions.
    mark : None | list of int
        List of sensor indices to mark.
    head_radius : scalar | tuple | True
        Radius of the head outline drawn over sensors (on sensor plots with
        normalized positions, 0.45 is the outline of the topomap); 0 to plot no
        outline; tuple for separate (right, anterior) radius. True to be equal
        to :class:`plot.Topomap` with ``method="mne"``.
        The default is determined automatically.
    head_pos : scalar
        Head outline position along the anterior axis (0 is the center, 0.5 is
        the top end of the plot).
    connectivity : bool
        Show sensor connectivity (default False).
    title : None | string
        Figure title.
    """
    _make_axes = False

    def __init__(self, sensors, labels='name', proj='default', size=1,
                 color='k', marker='.', mark=None, head_radius=None,
                 head_pos=0., connectivity=False, *args, **kwargs):
        sensors = as_sensor(sensors)

        if sensors.sysname:
            ftitle = 'SensorMap: %s' % sensors.sysname
        else:
            ftitle = 'SensorMap'
        _EelFigure.__init__(self, ftitle, 1, 5, 1, False, *args, **kwargs)

        # axes with same scaling as plot.Topomap
        w = 1. - 2 * SENSOR_AXES_FRAME
        ax = self.figure.add_axes((SENSOR_AXES_FRAME, SENSOR_AXES_FRAME, w, w))

        # store args
        self._axes.append(ax)
        self._sensors = sensors
        self._proj = proj
        self._marker_handles = []
        self._connectivity = None

        self._markers = _ax_map2d(ax, sensors, proj, 1, size, color, marker,
                                  mark, head_radius, head_pos)
        SensorMapMixin.__init__(self, [self._markers.sensors])

        if labels:
            self.set_label_text(labels)

        if connectivity:
            self.show_connectivity()

        self._show()

    def remove_markers(self):
        "Remove all sensor markers."
        while len(self._marker_handles) > 0:
            h = self._marker_handles.pop(0)
            h.remove()
        self.canvas.draw()

    def show_connectivity(self, show=True):
        """Show the sensor connectivity as lines connecting sensors.

        Parameters
        ----------
        show : None | True | scalar
            True to show the default connectivity.
            None to remove the connectivity lines.
            Scalar to plot connectivity for a different connect_dist parameter
            (see Sensor.connectivity()).
        """
        if not show:
            self._markers.connectivity.show(None)
        else:
            if show is True:
                conn = self._sensors.connectivity()
            else:
                conn = self._sensors.connectivity(show)
            self._markers.connectivity.show(conn)
        self.draw()


def map3d(sensors, marker='c*', labels=False, head=0):
    """3d plot of a Sensors instance"""
    import matplotlib.pyplot as plt

    sensors = as_sensor(sensors)

    locs = sensors.locs
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(locs[:, 0], locs[:, 1], locs[:, 2])
    # plot head ball
    if head:
        u = np.linspace(0, 1 * np.pi, 10)
        v = np.linspace(0, np.pi, 10)

        x = 5 * head * np.outer(np.cos(u), np.sin(v))
        z = 10 * (head * np.outer(np.sin(u), np.sin(v)) - .5)  # vertical
        y = 5 * head * np.outer(np.ones(np.size(u)), np.cos(v))  # axis of the sphere
        ax.plot_surface(x, y, z, rstride=1, cstride=1, color='w')
    # n = 100
    # for c, zl, zh in [('r', -50, -25), ('b', -30, -5)]:
    # xs, ys, zs = zip(*
    #               [(random.randrange(23, 32),
    #                 random.randrange(100),
    #                 random.randrange(zl, zh)
    #                 ) for i in range(n)])
    # ax.scatter(xs, ys, zs, c=c)
