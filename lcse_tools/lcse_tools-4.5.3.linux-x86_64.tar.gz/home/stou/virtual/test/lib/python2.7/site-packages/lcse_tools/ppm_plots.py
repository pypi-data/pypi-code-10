#!/usr/bin/env python

'''
This file contains plotting routines for RProfile data. It is for now
the repository of all plot functions... should be moved somewhere.

# TODO: Add an installable script we can just run
'''

__version__ = 3.0

import os
import lcse
import numpy as np

import logging
# from lockfile import AlreadyLocked, LockFile

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

log = logging.getLogger(__name__)
log.propagate = False
log.addHandler(ch)
log.setLevel(logging.INFO)
#log.setLevel(logging.ERROR)

colors = ['g', 'r', 'b', 'y', 'm']
styles = ['o-', 'v-', 'D-', '*-', 'H-','+-', 'x-', ]

def new_figure():
  ''' Better defaults '''

  log.info("Creating new figure")

  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=(12, 8), facecolor='w', edgecolor='k')
  fig.patch.set_facecolor('white')
  fig.patch.set_alpha(1.0)

  return fig

def update_axis(ax, rp=None, **kwargs):
  """ `xlim` and `ylim` """

  xlim = kwargs.get('xlim')
  ylim = kwargs.get('ylim')

  ax.legend(loc=0)
  ax.grid(True)

  if xlim:
    ax.set_xlim(xlim)
  elif rp:
    ax.set_xlim((rp.get('radinner'), rp.get('radouter')))

  if ylim:
    ax.set_ylim(ylim)

def get_filename(prefix, **kwargs):

  dump = kwargs.get('dump')
  bucket = kwargs.get('bucket', 0)
  filename = kwargs.get('filename')

  if bucket > 0:
    prefix += "-%03i" % bucket

  path = os.path.join(kwargs.get('path', ''), prefix)

  if not filename:
    if dump:
      filename = 'plot_%s-%04i.png' % (prefix, dump)
    else:
      filename = 'plot_%s.png' % (prefix,)

  return os.path.join(path, filename)

def check_exists(prefix, **kwargs):

  filename = get_filename(prefix, **kwargs)

  if os.path.exists(filename):
    log.warning("Skipping figure %s because it exists" % filename)
    return True
  else:
    return False

def save_fig(fig, prefix, **kwargs):
  """ 

  Keywords:

  `dump` 

  `dpi` the dpi for the figure, default is 200

  `path`

  `filename`

  `bucket`

  """

  dpi = kwargs.get('dpi', 200)

  filename = get_filename(prefix, **kwargs)
  path = os.path.dirname(filename)

  if not os.path.exists(path):
    os.makedirs(path)

  if os.path.exists(filename):
    log.info("Skipping figure %s because it exists" % filename)
    return

  fig.savefig(filename, dpi=dpi)
  log.info("Saved figure to %s" % filename)

def plot_var_one_bucket(rp, var, fig, **kwargs):
  ''' Plot the `var` with variable

  `xlim` and `ylim` are the axis limits
  '''

  bucket = kwargs.get('bucket', 0)
  dump = rp.get('dump')

  prefix = kwargs.get('prefix', '%s' % var)

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')

  data = rp.get_table(var)
  var_avg = data[0,:,bucket]
  var_min = data[1,:,bucket]
  var_max = data[2,:,bucket]
  var_sd = data[3,:,bucket]

  ax = fig.add_subplot(111)

  bucket_name = 'bucket %i' % bucket if bucket > 0 else 'global bucket'
  ax.set_title('%s for %s dump %04i' % (var, bucket_name, dump))
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, var_avg, 'k')
#  ax.plot(y, var_min,'b', label="min")
#  ax.plot(y, var_max,'r', label="max")
#  ax.errorbar(y, var_avg, yerr=var_sd,
#              label='average',
#              elinewidth=2, fmt='o', ecolor='g')

  update_axis(ax, rp=rp)

  save_fig(fig, prefix, dump=dump, **kwargs)

def plot_log_var_one_bucket(rp, var, fig, **kwargs):
  ''' Plot the `var` multiplied by the volume of that shell
  `xlim` and `ylim` are the axis limits
  '''

  bucket = kwargs.get('bucket', 0)
  dump = rp.get('dump')

  prefix = kwargs.get('prefix', 'log_%s' % var)

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')
  d = rp.get_table(var)[0,:,bucket]

  ax = fig.add_subplot(111)

  bucket_name = 'bucket %i' % bucket if bucket > 0 else 'global bucket'

  ax.set_title('%s for %s dump %04i' % (var, bucket_name, dump))
  ax.set_xlabel('Radius ($10^3 km$)')
  ax.plot(y, np.log10(d),'k')

  update_axis(ax, rp=rp, **kwargs)

  save_fig(fig, prefix, dump=dump, **kwargs)

def plot_var_many_buckets(rp, var, fig, **kwargs):
  ''' Create a plot of several buckets against the global
  of a single variable. Only min/max/sd for the global are
  shown

  `buckets` if specified is a list of buckets to add to the plot
            otherwise we plot everything
  '''

#  fig = kwargs.get('fig', new_figure())
  buckets = kwargs.get('buckets', range(rp.bucket_count + 1))

#  if check_exists(prefix, dump=dump, **kwargs):
#    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')
  d = rp.get_table(var)

  ax = fig.add_subplot(111)

  ax.set_title('%s for many bucket' % (var))
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, d[0,:,0],'k')
  ax.plot(y, d[1,:,0],'b', label="min")
  ax.plot(y, d[2,:,0],'r', label="max")
  ax.errorbar(y, d[0,:,0], yerr=d[3,:,0],
                    elinewidth=2, fmt='o', ecolor='g')

  for bucket in buckets:
    ax.plot(y, d[0,:,bucket],'k')

  update_axis(ax, rp=rp, **kwargs)
  return ax

def plot_log_var_many_buckets(rp, var, fig, **kwargs):
  ''' Create a plot of several buckets against the global
  of a single variable. Only min/max/sd for the global are
  shown

  `buckets` if specified is a list of buckets to add to the plot
            otherwise we plot everything
  '''

#  fig = kwargs.get('fig', new_figure())
  buckets = kwargs.get('buckets', range(rp.bucket_count + 1))

#  if check_exists(prefix, dump=dump, **kwargs):
#    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')
  d = rp.get_table(var)

  ax = fig.add_subplot(111)

  ax.set_title('%s for many bucket' % (var))
  ax.set_xlabel('Radius ($10^3 km$)')
  ax.set_ylabel('$\log_{10}(%s)$' % var)

  ax.plot(y, np.log10(d[1,:,0]), 'b', label="min")
  ax.plot(y, np.log10(d[2,:,0]), 'r', label="max")
  ax.plot(y, np.log10(d[0,:,0]))

  for bucket in buckets:
    ax.plot(y, np.log10(d[0,:,bucket]),'k')

  update_axis(ax, rp=rp, **kwargs)
  return ax

def plot_ceul_mach_global(rp, fig, **kwargs):

  prefix = 'ceul_mach_global'

  dump = rp.get('dump')

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y')
  ceul = rp.get('ceul')
  mach = rp.get('mach')

  ax = fig.add_subplot(111)
  ax.set_title('$C_{eul}$ and Mach number for dump %4i' % dump)
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, ceul[0], 'b', label='$C_{eul}$')

  ax2 = ax.twinx()
  ax2.plot(y, mach[2], 'r', label='max(M)')
  ax2.plot(y, mach[0], '+k', label='M')
  ax2.plot(y, mach[1], 'g', label='min(M)')

  update_axis(ax, rp=rp)

  ax.legend(loc=2, prop={'size':6})
  ax2.legend(prop={'size':6})

  save_fig(fig, prefix, dump=dump, **kwargs)

def plot_ekr_ekt_entropy(rp, fig, **kwargs):
  ''' Do not use this method to loop over buckets and plot many of them
  since it will be quite inefficient.
  '''

  prefix = 'ekr_ekt_entropy_global'

  dump = rp.get('dump')

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y')
  ekr = rp.get('ekr')
  ekt = rp.get('ekt')
  p = rp.get('p')
  rho = rp.get('rho')

  entropy = p[0, :] / (rho[0, :]**(5./3.))

  ix_entropy = entropy > 0.0
  log_entropy = np.log10(entropy[ix_entropy])

  fig.clear()

  ax = fig.add_subplot(111)
  ax.set_title('ekr/ekt and entropy for dump %04i' % (dump))
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, ekr[0, :], 'r', label='ekr')
  ax.plot(y, ekt[0, :], 'g', label='ekt')

  ax2 = ax.twinx()
  ax2.plot(y[ix_entropy], log_entropy, 'b', label='log(A)')

  update_axis(ax, rp=rp)
  ax.legend(loc=2)
  ax2.legend(loc=1)

  save_fig(fig, prefix, dump=dump, **kwargs)

def plot_unwraped_quantity(rp, data, label, fig, **kwargs):
  """ Plot a scatter plot where the points represent bucket centers
  
  `rp` ray profile instance
  
  `data` data with dimension of the size of the buckets.

  `label` the text string to use for the plot quantities
  
  `fig` instances
  
  
  """

  path = kwargs.get('path', '.')
  save = kwargs.get('save', False)
  normalize = kwargs.get('normalize', True)
  scale = kwargs.get('scale', 3000.0)
  global_range = kwargs.get('global_range')
  
  dump = rp.get('dump')
  centers = rp.get_centers()

  phi_x = centers[0]
  theta_y = centers[1]
    
#     if not isinstance(scales, list):
#         scales = [scales for i in range(len(variables))]
    
#    colors = range(rp.get('nbuckets'))
#    cm = plt.cm.get_cmap('YlOrRd')
  cm = plt.cm.get_cmap('bwr')
  
  mm = (data.min(), data.max()) if global_range is None else global_range
  
  if normalize:
    data = (data - mm[0]) / (mm[1] - mm[0])
    mm = (0.0, 1.0)

  colors = data
      
  fig.clear()
  ax = fig.add_subplot(111)
  
  ax.set_title('%s dump %4i' % (label, dump))
  ax.set_xlabel(r'$\phi$')
  ax.set_ylabel(r'$\theta$')
  ax.set_ylim([0.0, np.pi])

#    sc = ax.scatter(phi_x, theta_y, s=scale * data, c=colors, 
#                    alpha=0.5, vmin=mm[0], vmax=mm[1], cmap=cm)

  sc = ax.scatter(phi_x, theta_y,  s= scale * data,
                  alpha=0.5, vmin=mm[0], vmax=mm[1], norm=True)
    
  ax.set_xticks(np.pi * np.arange(-1, 1.5, 0.5))
  ax.set_xticklabels(["-$\pi$", "-$\pi/2$","0", "$\pi/2$", "$\pi$"])
  
  ax.set_yticks(np.pi * np.arange(0, 1.25, 0.25))
  ax.set_yticklabels(["0", "$\pi/4$", "$\pi/2$", "$3 \pi/4$", "$\pi$"])
     
  if kwargs.get("annotate"):
    for i in range(rp.get('nbuckets')):
      ax.annotate(str(i + 1), (phi_x[i], theta_y[i]))

  x = range(phi_x)
  ax.xticks(x, labels)

#    plt.colorbar(sc)

  if save:
    ppm.save_fig(fig, label, dump=dump)

def plot_bucket_numbers(rp, fig):
  """Plot a map of bucket centers"""

  ax = fig.add_subplot(111)
  
  centers = rp.get_centers()
  phi_x = centers[0]
  theta_y = centers[1]    
  
  fig.clear()
  ax = fig.add_subplot(111)

  ax.set_title("Bucket Map")
  ax.set_xlabel(r'$\phi$')
  ax.set_ylabel(r'$\theta$')
  ax.set_ylim([0.0, np.pi])
      
  sc = ax.scatter(phi_x, theta_y)
     
  ax.set_xticks(np.pi * np.arange(-1, 1.5, 0.5))
  ax.set_xticklabels(["-$\pi$", "-$\pi/2$","0", "$\pi/2$", "$\pi$"])
  
  ax.set_yticks(np.pi * np.arange(0, 1.25, 0.25))
  ax.set_yticklabels(["0", "$\pi/4$", "$\pi/2$", "$3 \pi/4$", "$\pi$"])

  for i in range(rp.get('nbuckets')):
     ax.annotate(str(i + 1), (phi_x[i], theta_y[i]))

  return ax

def plot_energy(data_path, label, fig, stride=1, style="b-"):
  rp_set = lcse.rprofile_set(path=data_path, stride=stride)

  volumes = rp_set.get_dump().get_cell_volumes()

  t = []
  energy = []

  for rp in rp_set:
    dump = rp.get('dump')

    timerescaled = rp.get('timerescaled')
    t.append(timerescaled)

    enuc = rp.get_table('enuc')[0,:,1:]
    enuc *= volumes

    energy.append(enuc.sum())

  ax = fig.add_subplot(1,1,1)
  ax.ticklabel_format(useOffset=False)
  ax.grid(True)
  ax.set_ylabel("energy")
  ax.set_xlabel("time [min]")

  ax.plot(t, log(energy), style, label=label)

#  if save:
#    ppm.save_fig(fig, label)

def plot_diff_from_avg(r, rp_table, filter_fn=None):
  """`rp_table` is a table with the same format as returned by .get_table().
  
  pass array through `filter_fn`, example filter_fn=np.log10 will make the plot
  log
  """
  
#     if check_exists(prefix, dump=dump, **kwargs):
#         return
  
  diffs = rp_table[0,:,1:] - rp_table[0,:,0].reshape((-1, 1))
  diff_size = sqrt((diffs * diffs).sum(1))

  fig = ppm.new_figure()
  ax = fig.add_subplot(111)
      
  if filter_fn:
    ax.plot(r, filter_fn(diff_size))
  else:
    ax.plot(r, diff_size)
      
  ax.grid()
  return ax

# 
# Untested below? 
# 


def plot_spike(rp_set, fig, **kwargs):

  prefix = 'fuel'

  rp_main = rp_set.ray_profiles[0]

  limits = kwargs.get('limits', (rp_main.get('radinner'), rp_main.get('radouter')))

  y = rp_main.get('y')
  half_dx = 0.5 * (y[1] - y[0])

  spikes = kwargs.get('spikes', [])
  dumps = kwargs.get('dumps', [])
  times = kwargs.get('times', [])

  for i, rp in enumerate(rp_set):

    dump = rp.get('dump')
    time = rp.get('time')

    print dump,

    if dump in dumps or dump < 1:
      continue

    y = rp.get('y')
    y_limit = (y < limits[1]) & (y > limits[0])
    y = y[y_limit]

    fv = rp.get('fv')[0, y_limit]
    fv1 = 1.0 - fv

    rhobub = rp.get('rhobubble')[0, y_limit]
    rhospike = rp.get('rhospike')[0, y_limit]

    vols = (4. * np.pi / 3.) * ((y + half_dx)**3 - (y - half_dx)**3)
    bub_mass = vols * rhobub * fv1
    spike_mass = vols * rhospike * fv

    spikes.append(spike_mass.sum())
    dumps.append(dump)
    times.append(rp.get('time'))

  import matplotlib
  y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)

  ax = fig.add_subplot(111)
  ax.set_title('H-quantity')
  ax.plot(dumps, spikes, 'k')
#  ax.plot(times, spikes, 'k')

  ax.set_xlabel("Time")
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)

  save_fig(fig, prefix, **kwargs)

  return dumps, times, spikes



#import matplotlib as mpl
#mpl.use("Agg")

#from matplotlib import rc
#rc('mathtext', default='regular')

#import matplotlib.pyplot as plt
#import numpy as np

def plot_file(dump, fig):

  rp = rprofile_reader('RProfile-01-%04i.bobaaa' % dump)

#  for bucket in range(rp.get('nbuckets')+1):
  for bucket in [0,]:

    ys = rp.get('y', bucket=bucket)
    ekr = np.sqrt(rp.get('ekr', bucket=bucket))
    ekt = np.sqrt(rp.get('ekt', bucket=bucket))
    p = rp.get('p', bucket=bucket)
    rho = rp.get('rho', bucket=bucket)

    entropy = p / (rho**(5./3.))

    fig.clear()

    ax = fig.add_subplot(111)

    if bucket == 0:
      plt.title('Global profile for fluid speed and entropy (dump %04i)' % (dump))
    else:
      plt.title('Profile %i for fluid speed and entropy (dump %04i)' % (bucket, dump))

    ax.plot(ys, ekt, 'g', label='transverse speed')
    ax.plot(ys, ekr, 'r', label='radial speed')
    ax.set_ylabel("Speed ($10^3km/s$)")
    ax.legend(loc=2)
    ax.grid(True)
#    plt.ylim((0,0.06))
    plt.ylim((0,0.45))

    ax2 = ax.twinx()
    ax2.plot(ys, np.log10(entropy), 'b', label='entropy')
    ax2.set_ylabel("log(entropy)")
    ax2.legend()

    plt.xlim((8,22))

    fig_file = 'plots/speed/plot_%s_%03i_%04i.png' % ("logS-speed", bucket, dump)
    fig.savefig(fig_file, dpi=200)

    fig.clear()

    ysh = rp.get('y_hi', bucket=bucket)
    fv = rp.get('fv_hi', bucket=bucket)
    fvsd = rp.get('fvsd_hi', bucket=bucket)
    fvmn = np.log10(rp.get('fvmn_hi', bucket=bucket))
    fvmx = np.log10(rp.get('fvmx_hi', bucket=bucket))

    fv_log = np.log10(fv)

    if bucket == 0:
      plt.title('Global radial profile for fractional volume of H (dump %4i)' % (dump))
    else:
      plt.title('Profile %i for fractional volume of H (dump %4i)' % (bucket, dump))

    plt.xlim((14,20))
    plt.ylim((-7,0))
    plt.grid(True)
    plt.xlabel('Radius ($10^6 m$)')
    plt.ylabel('log(fv)')

    label = 'fv'

#    plt.errorbar(ysh, fv_log, yerr=fv_sdlog, label='%s avg' % (label))
    plt.plot(ysh, fv_log, 'b', label='avg')
    plt.plot(ysh, fvmn, 'g', label='min')
    plt.plot(ysh, fvmx, 'r', label='max')
    plt.legend(loc=2)

    fig_file = 'plots/fv/plot_log-%s_%03i_%04i.png' % ("fv", bucket, dump)
    fig.savefig(fig_file, dpi=200)

def get_interface_location(rp, levels):

  nbuckets = rp.get('nbuckets')
  level_ct = len(levels)

  j_hi = rp.get_table('j_hi')
  y_hi = rp.get_table('y_hi')
  fv_hi = rp.get_table('fv_hi')[0,:,:]

  data = np.zeros((level_ct, nbuckets+1))

  #TODO: Don't loop
  for bucket in range(nbuckets+1):

    one_thing = fv_hi[:, bucket]

    first = np.argmax(one_thing > 0.0)
    last = np.argmin(one_thing < 1.0)

    j_restricted = j_hi[first-1:last-1]
    y_restricted = y_hi[first-1:last-1]

    fv_restricted = fv_hi[first-1:last-1, bucket]

    if fv_restricted.size == 0:
      continue

    for l, val in enumerate(levels):
      data[l, bucket] = np.interp(val, fv_restricted, y_restricted)

  return data

def get_interface_statistics(dump_data, dumps=None, results=None):
  log.info("get_interface_statistics")

  data_len = len(dump_data)

  if data_len == 0:
    return

  dumps = np.zeros(data_len, dtype=np.int32) if not dumps else dumps
  results = np.zeros((2, dump_data[0][1].shape[0], data_len)) if not results else results

  for i, d in enumerate(dump_data):

    dumps[i] = d[0]
    r = d[1][:,1:]

    print d[0],

    for l in range(r.shape[0]):
      results[0, l, i] = r[l].mean()
      results[1, l, i] = np.std(r[l])

  return dumps, results

def plot_interface(dumps, time_data, results, levels, **kwargs):

  styles_len = len(styles)
  colors_len = len(colors)

  fig = kwargs.get('fig', new_figure())
  quiet = kwargs.get('quiet', False)

  x_limits = kwargs.get('xlimits')
  y_limits = kwargs.get('ylimits')
  sd_only = kwargs.get('sd_only', False)

  ax = fig.add_subplot(1,1,1)
  ax.ticklabel_format(useOffset=False)
  ax.grid(True)
  ax.set_xlabel("dump #")
  ax.set_ylabel("r [1000 km]")

  if not sd_only:
    ax.set_title("Location of FV interface", y=1.08)
    for i, v in enumerate(levels):
      avg = results[0,i,:]
      sd = results[1,i,:]
      color = colors[ i % colors_len]

      ax.errorbar(dumps, avg, yerr=sd, label='fv=%f' % v,
                  fmt='k.-', ecolor=color)
  else:
    ax.set_title("Standard-Deviation of FV interface", y=1.08)
    for i, v in enumerate(levels):
      sd = results[1,i,:]
      style = styles[ i % styles_len]
      ax.plot(dumps, sd, style, label='fv=%f' % v)

  if x_limits:
    print "X LIMITS", x_limits
    ax.set_xlim(x_limits)
    #ax2.set_xlim(x_limits)

  if y_limits:
    ax.set_ylim(y_limits)
    #ax2.set_ylim(y_limits)

  ax.legend(loc=2)
  ax2 = ax.twiny()
  ax2.set_xlabel("time [min]")
  ax2.set_xticks(ax.get_xticks())
  ax2.set_xticklabels(time_data)
  ax2.set_xbound(ax.get_xbound())
  ax2.set_ybound(ax.get_ybound())


  save_fig(fig, 'interface', **kwargs)

  if quiet:
    matplotlib.pyplot.close(fig)

def plot_interface_analysis(rps, **kwargs):

  dumps = kwargs.get('dumps')
  time_data = kwargs.get('timing', [])
  prefix = kwargs.get('prefix')
  xlimits = kwargs.get('xlimits')
  levels = kwargs.get("levels", (0.5, 0.1, 0.01, 0.001, 1e-5))

  dump_data = []

  for rp in rps:
    dump = rp.get('dump')

    if dumps and dump not in dumps:
      continue

    print dump,

    d = get_interface_location(rp, levels)
    dump_data.append((dump, d))
    time_data.append('%0.f' % rp.get('timerescaled'))

  dumps, results = get_interface_statistics(dump_data)

  plot_interface(dumps, time_data, results, levels, filename='%s.png' % prefix,
                 xlimits=xlimits)

  plot_interface(dumps, time_data, results, levels, filename='%s_sd_only.png' % prefix,
                 xlimits=xlimits, sd_only=True)

  # Return dump_data so we can cache it
  return dump_data

