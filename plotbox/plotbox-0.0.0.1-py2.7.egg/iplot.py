# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

def plotly_plot(
        x=None,
        y=None,
        df=None,
        style='scatter',
        title=None,
        filename='plotly_plot_test',
        xlabel=None,
        ylabel=None,
        vlines=None,
        hlines=None,
        xlim=(
            None,
            None),
    ylim=(
            None,
            None),
        dropna=True,
        dateextractX=False,
        dateextractY=False,
        figsize=(
            16,
            9),
        plotlyplot=True,
        saveAs=None,
        **kwargs):
    '''plotly_plot uses plotly to interactively plot a series or two
    Must set unique title or filename for plot to exist semi-permanently, else overwritten on the next use of function

    Parameters
    ----------
    x : array, series, or list OR column name in df
            numpy array, pandas series, or list of primary values to plot
    y : array, series, or list OR column name in df
            numpy array, pandas series, or list of secondary values to plot
    df : pandas DataFrame, optional
            if given, uses dataframe to create x and y arrays using x and y column names given
    style : string
            argument to choose style of plot. currently implemented dist, hist, line, and scatter
    title, xlabel, ylabel : string, optional
            labels of plot. if filename not given, filename = title
    vlines, hlines : int or list, optional
            list of x/y points to make vertical/horizontal lines in the plot
    xlim, ylim : tuple (min, max), optional
            horizontal/vertical boundries of the figure
    dropna : boolean, optional (default is True)
            drop nans from series
    dateextractX, dateextractY : boolean, optional (default is False)
            try to convert x and y to datetimes using utils.date.extract_date
    plotlyplot: boolean, optional (default is True)
            set to False for prototyping
    filename: string, optional
            file name on server for plotly plot. unique label ensures plot will not be overwritten
    saveAs : string (default is None)
            If given, save the figure using saveAs as the file name.
    kwargs : dict
            additional keyworded arguments passed to plotting functions

    To Do
    -----
    Fix autolabeling. broked it when fixing dates..
    Bug hunt'''

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)

    yisNone = False
    if y is None:
        yisNone = True

    # if dataframe provided, create x (and y) array(s)
    if df is not None:
        x = df[x]
        if not yisNone:
            y = df[y]

    # checking if x (and y) are pandas Series, if not convert to
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    else:
        if xlabel is None:
            xlabel = x.name
    if not yisNone:
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
        else:
            if ylabel is None:
                ylabel = y.name

    # if dropna, drop nan values from x (and accompanying values in y)
    if dropna:
        try:
            nan_indices = pd.isnull(x)
            if sum(nan_indices) > 0:
                print 'nan values in series to be dropped:', sum(nan_indices)
                x = x[~nan_indices].reset_index(drop=True)
                if not yisNone:
                    y = y[~nan_indices].reset_index(drop=True)
        except:
            pass

    # if y not provided: set y to x.index, swap x and y as we are interested
    # in plotting x on the 'y' against the index
    if yisNone:
        y = x.index
        x, y = y, x

    # try to extract_date x and y
    if dateextractX:
        try:
            x = utils.date.extract_date(x)
            print 'date extracted x'
        except:
            pass
    if dateextractY and not yisNone:
        try:
            y = utils.date.extract_date(y)
            print 'date extracted y'
        except:
            pass

    # dist or hist: distribution of x plot
    if style == 'dist':
        try:
            sns.distplot(y, **kwargs)
        except:
            print "failed producing seaborn distribution plot.. trying hist"
            plt.hist(y, **kwargs)
        if ylabel is None:
            ylabel = 'frequency'
    elif style == 'hist':
        plt.hist(y, **kwargs)
        if ylabel is None:
            ylabel = 'frequency'

    # line or scatter: x vs y plot
    elif style == 'line':
        plt.plot(x, y, **kwargs)
    elif style == 'scatter':
        plt.scatter(x, y, **kwargs)
    else:
        print 'style currently not available'
        return None

    if ylim[0] is None:
        y_min = plt.ylim()[0]
    else:
        y_min = ylim[0]
    if ylim[1] is None:
        y_max = plt.ylim()[1]
    else:
        y_max = ylim[1]
    plt.ylim(y_min, y_max)
    if xlim[0] is None:
        x_min = plt.xlim()[0]
    else:
        x_min = xlim[0]
    if xlim[1] is None:
        x_max = plt.xlim()[1]
    else:
        x_max = xlim[1]
    plt.xlim(x_min, x_max)

    # vlines, hlines. should maybe export this to their own function for other
    # uses
    if vlines is not None:
        if not isinstance(vlines, (list, pd.core.series.Series, np.ndarray)):
            vlines = [vlines]
        for vl in vlines:
            plt.plot([vl, vl], [y_min, y_max])
    if hlines is not None:
        if xlim is None:
            xlim = plt.xlim()
        if not isinstance(hlines, (list, pd.core.series.Series, np.ndarray)):
            hlines = [hlines]
        for hl in hlines:
            plt.plot([x_min, x_max], [hl, hl])

    # title, filename handling
    if (title is None) and (filename != 'plotly_plot_test'):
        title = filename
    if title is not None:
        plt.title(title, size=20)
        # if title is set and filename is default, set filename to title
        if filename == 'plotly_plot_test':
            filename = title

    # x and y label handling. auto labeling hashed out for now
    if xlabel is not None:
        plt.xlabel(xlabel, size=18)
    if ylabel is not None:
        plt.ylabel(ylabel, size=18)

    if saveAs is not None:
        plt.savefig(saveAs, bbox_inches='tight', dpi=270)

    # render in plotly or return nothing to output static chart
    if plotlyplot:
        iframe = py.iplot_mpl(fig, filename=filename, fileopt='overwrite')
        print iframe.embed_code.split('src="')[1].split('.emb')[0]
        py.iplot_mpl(fig, filename=filename, fileopt='overwrite')
        return iframe


def plotly_date_frequency_plot(
        df=None,
        array=None,
        series=None,
        title=None,
        filename='plotly_date_frequency_plot_test',
        weekend_bool=True,
        weekend_height=20,
        xlabel=None,
        ylabel=None,
        vlines=None,
        hlines=None,
        xlim=None,
        ylim=None,
        **kwargs):
    '''plotly_date_frequency_plot uses plotly to interactively plot a bar chart showing a date series or df[array] frequency
    Requires df, array str or series
    To write a permanent, linkable plot, change filename
    Optional weekend indicators with adjustable height

    .. todo:

            Add hue parameter for stacked bar plot (see Jason's implementation)
            Add resample argument for weekly, monthly views

    '''

    if series is None:
        series = df[array]
    else:
        series = pd.Series(series)

    day_vcs = series.value_counts().sort_index()
    day_tuples = zip(day_vcs.keys(), day_vcs.values)

    if weekend_bool:
        # create list of weekend tuples to indicate weekends
        start, end = utils.date.extract_date(
            min(series)), utils.date.extract_date(
            max(series))
        running_day = start
        weekend_days = []
        while running_day <= end:
            if running_day.weekday() in set([5, 6]):
                weekend_days.append(running_day)
            running_day += dt.timedelta(days=1)
        if len(weekend_days) % 2 == 1:
            weekend_days = weekend_days[:-1]
        weekend_tuples = []
        for i in range(len(weekend_days) / 2):
            weekend_tuples.append(
                (weekend_days[i * 2], weekend_days[i * 2 + 1]))

    # plotly plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(utils.date.extract_date([day[0] for day in day_tuples]), [
            count[1] for count in day_tuples], **kwargs)
    if weekend_bool:
        for i in weekend_tuples:
            plt.plot([i[0], i[1], i[0], i[1]], [.1, weekend_height,
                                                weekend_height, .1], alpha=.6, color='grey')

    if vlines is not None:
        if ylim is None:
            ylim = plt.ylim()
        if not isinstance(vlines, (list, pd.core.series.Series, np.ndarray)):
            vlines = [vlines]
        for vl in vlines:
            plt.plot([vl, vl], [ylim[0], ylim[1]])

    if hlines is not None:
        if xlim is None:
            xlim = plt.xlim()
        if not isinstance(hlines, (list, pd.core.series.Series, np.ndarray)):
            hlines = [hlines]
        for hl in hlines:
            plt.plot([xlim[0], xlim[1]], [hl, hl], )

    if title is not None:
        plt.title(title, size=20)
    if xlabel is not None:
        plt.xlabel(xlabel, size=20)
    if ylabel is not None:
        plt.ylabel(ylabel, size=20)
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    return py.iplot_mpl(fig, filename=filename, fileopt='overwrite')

def histogram(df, title, xlabel='', ylabel='', colorscale = 'Portland'):
    data = Data([Heatmap(z = list(np.array(df)),
                        colorscale = colorscale, x = df.index, y = df.columns)])
    layout = Layout(title=title,
                    xaxis=XAxis(title=xlabel,
                                # titlefont=Font(family='Courier New, monospace',
                                #             size=18,
                                #             color='#7f7f7f')
                                ),
                    yaxis=YAxis(title=ylabel,
                                # titlefont=Font(family='Courier New, monospace',
                                #             size=18,
                                #             color='#7f7f7f')
                                )
                    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename=title)
    return plot_url

def hkr(all_hist_data, hist_labels, rug_text, bin_size=.2, curve_type = 'kde', show_hist = True, show_curve = True, show_rug = True, **kwargs):
    """
    Plots multiple
    """
    blnk_length=len(all_hist_data)
    hist_x=[None]*blnk_length
    start=[None]*blnk_length
    end=[None]*blnk_length
    colors=["rgb(31, 119, 180)", "rgb(255, 127, 14)", "rgb(44, 160, 44)", "rgb(214, 39, 40)", 
            "rgb(148, 103, 189)", "rgb(140, 86, 75)", "rgb(227, 119, 194)", 
            "rgb(127, 127, 127)", "rgb(188, 189, 34)", "rgb(23, 190, 207)"]

    for index in range(blnk_length):
        hist_x[index] = all_hist_data[index]
        start[index] = min(all_hist_data[index])*1.
        end[index] = max(all_hist_data[index])*1.
    
    def make_hists(all_hist_data, bin_size, start, end, hist_labels, colors):
        hist = [None]*blnk_length
        for index in range(blnk_length):
            hist[index] = Histogram(x=hist_x[index],
                                    histnorm='probability',
                                    name=hist_labels[index],
                                    marker=Marker(color=colors[index]),
                                    autobinx=False, # this is important, otherwise xbin_size won't apply
                                    xbins=XBins(start=start[index],  # first bin start
                                                end=end[index],      # last bin end
                                                size=bin_size),
                                    opacity=.7)
        return hist

    def make_kde(hist_x, start, end, hist_labels, colors, bin_size):
        curve_x = [None]*blnk_length
        curve_y = [None]*blnk_length
        curve = [None]*blnk_length
                    
        for index in range(blnk_length):
            curve_x[index] = np.linspace(start[index], end[index], 500)
            curve_y[index] = gaussian_kde(hist_x[index])(curve_x[index])
            curve_y[index] = curve_y[index]*bin_size
    
        for index in range(blnk_length):
            curve[index] = Scatter(x=curve_x[index],
                                   y=curve_y[index],
                                   mode='lines',
                                   name=hist_labels[index],
                                   marker=Marker(color=colors[index]))
        return curve

    def make_normal(hist_x, start, end, hist_labels, colors, bin_size):
        mean = [None]*blnk_length
        sd = [None]*blnk_length
        curve_x = [None]*blnk_length
        curve_y = [None]*blnk_length
        curve = [None]*blnk_length
        hist_c = hist_x
        
        
        for index in range(blnk_length):
            mean[index], sd[index] = norm.fit(hist_c[index])
            curve_x[index] = np.linspace(start[index], end[index], 500)
            curve_y[index] = norm.pdf(curve_x[index],loc=mean[index],scale=sd[index])
            curve_y[index] = curve_y[index]*bin_size

        for index in range(blnk_length):
            curve[index] = Scatter(x=curve_x[index],
                                   y=curve_y[index],
                                   mode='lines',
                                   name=hist_labels[index],
                                   marker=Marker(color=colors[index]))
        return curve
    
    def make_rug(hist_x, rug_text, colors):
        rug = [None]*blnk_length

        for index in range(blnk_length):
            rug[index] = Scatter(x=hist_x[index],
                                 y=[hist_labels[index]]*len(hist_x[0]),
                                 text=rug_text,
                                 mode='markers',
                                 name=hist_labels[index],
                                 marker=Marker(color=colors[index],
                                               symbol='line-ns-open'))
        return rug
        
    hist = make_hists(all_hist_data, bin_size, start, end, hist_labels, colors)
    if curve_type == 'Normal':
        curve = make_normal(hist_x, start, end, hist_labels, colors, bin_size)
    else:
        curve = make_kde(hist_x, start, end, hist_labels, colors, bin_size)
    rug = make_rug(hist_x, rug_text, colors)
        
    if show_rug == True:
        fig = tools.make_subplots(rows=2, shared_xaxes=True)
        for index in range(len(rug)):
            fig.append_trace((rug[index]), 2,1)
        fig['layout']['xaxis1']['zeroline'] = False
        fig['layout']['yaxis2']['dtick'] = 1 # sets tick interval
        fig['layout']['yaxis1']['domain'] = [.35, 1]
        fig['layout']['yaxis2']['domain'] = [0, .25]
    else:
        fig = tools.make_subplots(rows = 1)

    if show_hist == True:
        for index in range(len(hist)):
            fig.append_trace((hist[index]), 1,1)
    if show_curve == True:        
        for index in range(len(curve)):
            fig.append_trace((curve[index]), 1,1)
    
    fig['layout']['barmode'] = 'overlay'
    fig['layout']['hovermode'] = 'closest'
    
    return fig
