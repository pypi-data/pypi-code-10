import os.path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from funcsForSimulatedData import load, file_name, mask
from redshiftIterator import save_arrays, iterator


def flux_fluxDiff_arrays(my_dir, file_dir, filter1, filter2, z):

    mc_file_name = file_name(my_dir, file_dir, z)
    mc_dict = load(mc_file_name)
    type_Ia_flux_diff = (mc_dict['type_Ia']['flux'][filter2] -
                         mc_dict['type_Ia']['flux'][filter1])
    type_Ibc_flux_diff = (mc_dict['type_Ibc']['flux'][filter2] -
                          mc_dict['type_Ibc']['flux'][filter1])
    type_II_flux_diff = (mc_dict['type_II']['flux'][filter2] -
                         mc_dict['type_II']['flux'][filter1])
    flux = [mc_dict['type_Ia']['flux'][filter1],
            mc_dict['type_Ibc']['flux'][filter1],
            mc_dict['type_II']['flux'][filter1]]
    diff = [type_Ia_flux_diff, type_Ibc_flux_diff, type_II_flux_diff]
    for i, item in enumerate(diff):
        flux[i] = mask(flux[i], 98)
        diff[i] = mask(diff[i], 98)

    return flux, diff


def contour(my_dir, file_dir, filter1, filter2, flux_filter1,
            flux_filter1_err, flux_filter2, flux_filter2_err, z, outdir):
    """Generates a plot and transforms the figure into an HTML file from the
    montecarlo data. Adds a point to the data"""
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    flux, diff = flux_fluxDiff_arrays(my_dir, file_dir, filter1, filter2, z)
    diff_data = flux_filter2 - flux_filter1
    diff_data_err = flux_filter2_err + flux_filter1_err

    sns.set(style="white", palette="muted")
    sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})
    g = sns.JointGrid(filter2.upper() + " - " + filter1.upper() +
                      " flux difference", filter1.upper() + " flux", space=0)

    sns.kdeplot(diff[0], ax=g.ax_marg_x, legend=True, label='Type Ia')
    sns.kdeplot(flux[0], ax=g.ax_marg_y, vertical=True, legend=False)
    sns.kdeplot(diff[0], flux[0], cut=4, ax=g.ax_joint,
                alpha=0.8, cmap='Blues_d')

    sns.kdeplot(diff[1], ax=g.ax_marg_x, legend=True, label='Type Ib/c')
    sns.kdeplot(flux[1], ax=g.ax_marg_y, vertical=True, legend=False)
    sns.kdeplot(diff[1], flux[1], cut=4, ax=g.ax_joint,
                alpha=0.8, cmap='Greens_d')

    sns.kdeplot(diff[2], ax=g.ax_marg_x, legend=True, label='Type II')
    sns.kdeplot(flux[2], ax=g.ax_marg_y, vertical=True, legend=False)
    sns.kdeplot(diff[2], flux[2], cut=4, ax=g.ax_joint,
                alpha=0.8, cmap='Reds_d')

    g.ax_joint.errorbar(diff_data, flux_filter1,
                        xerr=diff_data_err, yerr=flux_filter1_err,
                        fmt='--o', c='k')
    g.set_axis_labels(xlabel=filter2.upper() + " - " + filter1.upper() +
                      " flux difference (counts/s)",
                      ylabel=filter1.upper() + " flux (counts/s)")
    g.ax_joint.annotate('z=%.2f' % z, xy=(0.75, 0.85),
                        xycoords='axes fraction', size=14)
    plt.tight_layout()
    file_z = 100*z
    file_z = int(file_z)
    # plt.show()
    plt.savefig(outdir + 'z%.0f_' % file_z + filter1 + '_' + filter2 + '_' +
                'contour.png')
    plt.close()


def scatter(my_dir, file_dir, filter1, filter2, z, outdir):

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    flux, diff = flux_fluxDiff_arrays(my_dir, file_dir, filter1, filter2, z)

    sns.set(style="white", palette="muted")
    sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})

    plt.scatter(diff[0], flux[0], c='b',
                label='Type Ia')
    plt.scatter(diff[1], flux[1], c='g',
                label='Type Ib/c')
    plt.scatter(diff[2], flux[2], c='r',
                label='Type II')
    plt.title('SNCosmo Simulated SNe: z=%.2f' % z)
    plt.xlabel(filter2.upper() + " - " + filter1.upper() +
               " flux difference (counts/s)")
    plt.ylabel(filter1.upper() + " flux (counts/s)")
    plt.legend()
    file_z = 100*z
    file_z = int(file_z)
    # plt.show()
    plt.savefig(outdir + 'z%.0f_' % file_z + filter1 + '_' + filter2 + '_' +
                'scatter.png')
    plt.close()


def plot(x, y, ylabel, title, outdir, outname=None):
    sns.set(style="darkgrid", palette="muted")
    sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})
    plot_name = title.replace(' ', '-')
    plot_name = plot_name.lower()
    if outname is not None:
        plot_name = outname

    plt.plot(x, y)
    plt.title(title)
    plt.xlabel('z')
    plt.ylabel(ylabel)
    plt.legend(['Type Ia', 'Type Ib/c', 'Type II'], loc='upper right')
    # plt.show()
    plt.savefig(outdir + plot_name + '.png')
    plt.close()


def subplot(x, y, title, outdir, title_photoz=None):
    ''' x, y and title are arrays
    '''
    new_title = [s for s in title if s]
    # Getting a title for the final PDF composed from the other names
    if sum(1 for x in title if x) == 3:
        final_title = title[0] + ' & ' + title[1] + ' & ' + title[2]
        plot_name = title[0] + '_' + title[1] + '_' + title[2]
    elif sum(1 for x in title if x) == 2:
        final_title = new_title[0] + ' & ' + new_title[1]
        plot_name = new_title[0] + '_' + new_title[1]
    else:
        final_title = new_title[0]
        plot_name = new_title[0]

    # Getting a plot name for the final PDF composed from the other names
    plot_name = plot_name.replace(' ', '-')
    plot_name = plot_name.lower()

    if title_photoz is not None:
        title[2] = title_photoz

    sns.set(style="darkgrid", palette="muted")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col',
                                               figsize=(12, 12))
    ax1.plot(x[0], y[0])
    ax1.set_title(title[0])
    ax1.legend(['Type Ia', 'Type Ib/c', 'Type II'], loc='upper right')
    ax1.set_ylabel('PDF')

    ax2.plot(x[1], y[1])
    ax2.set_title(title[1])
    ax2.legend(['Type Ia', 'Type Ib/c', 'Type II'], loc='upper right')

    ax3.plot(x[2], y[2])
    ax3.set_title(title[2])
    ax3.legend(['Type Ia', 'Type Ib/c', 'Type II'], loc='upper right')
    ax3.set_xlabel('z')
    ax3.set_ylabel('PDF')

    ax4.plot(x[3], y[3])
    ax4.set_title(final_title)
    ax4.legend(['Type Ia', 'Type Ib/c', 'Type II'], loc='upper right')
    ax4.set_xlabel('z')
    # Saving combined plot
    extent = ax4.get_window_extent().transformed(f.dpi_scale_trans.inverted())
    f.savefig(outdir + plot_name + '_single.png',
              bbox_inches=extent.expanded(1.3, 1.3))

    # plt.show()
    plt.savefig(outdir + plot_name + '.png')
    plt.close()


def combined(final_pdf, my_dir, file_dir, filter1, filter2,
             filter3, flux_filter1, flux_filter2, flux_filter3,
             flux_filter1_err, flux_filter2_err, flux_filter3_err, outdir,
             file_with_RF_and_SF_arrays, photo_z_type=None, photo_z_file=None,
             photo_z_redshift_file=None, mu=None, sigma=None):

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if not os.path.isfile(file_with_RF_and_SF_arrays):
        file_name = save_arrays(
            my_dir, file_dir, filter1, filter2, filter3, flux_filter1,
            flux_filter2, flux_filter3, flux_filter1_err, flux_filter2_err,
            flux_filter3_err, outdir)
        my_dict = load(file_name)

    else:
        my_dict = load(file_with_RF_and_SF_arrays)
    rf = my_dict['rf']
    sf = my_dict['sf']
    z = my_dict['rf_z']

    rf = np.asarray(rf)
    sf = np.asarray(sf)

    if photo_z_type is not False:
        photo_z, my_z = iterator('photo_z', my_dir, file_dir, filter1,
                                 filter2, filter3, flux_filter1, flux_filter2,
                                 flux_filter3, flux_filter1_err,
                                 flux_filter2_err, flux_filter3_err,
                                 photo_z_type=photo_z_type,
                                 photo_z_file=photo_z_file,
                                 photo_z_redshift_file=photo_z_redshift_file,
                                 mu=mu, sigma=sigma)
        if photo_z_type == 'file':
            title_photoz = 'Galaxy Photo-z from file'
        else:
            title_photoz = ("Galaxy Photo-z: Gaussian( mu=%.2f, sigma=%.2f)"
                            % (mu, sigma))

    if final_pdf == 'RF+SF+photoz':
        plt.clf()
        title = ['Random Forest', 'Survival Function', 'Photo-z']
        plot(z, rf, 'PDF', 'Random Forest', outdir)
        plot(z, sf, '1 - CDF', 'Survival Function', outdir)
        plot(z, photo_z, 'PDF', title_photoz, outdir, outname='photoz')

        first_product = np.multiply(sf, rf)
        product = (np.multiply(first_product.T, photo_z)).T

        x = [z, z, z, z]
        y = [rf, sf, photo_z, product]
        subplot(x, y, title, outdir, title_photoz)
        # norm_product = product/product.sum()

    elif final_pdf == 'RF+SF':
        plt.clf()
        title = ['Random Forest', 'Survival Function', '']
        plot(z, rf, 'PDF', 'Random Forest', outdir)
        plot(z, sf, '1 - CDF', 'Survival Function', outdir)
        product = np.multiply(rf, sf)

        x = [z, z, [], z]
        y = [rf, sf, [], product]
        subplot(x, y, title, outdir)

        # norm_product = product/product.sum()

    elif final_pdf == 'RF+photoz':
        plt.clf()
        title = ['Random Forest', '', 'Photo-z']
        plot(z, rf, 'PDF', 'Random Forest', outdir)
        plot(z, photo_z, 'PDF', title_photoz, outdir, outname='photoz')

        product = np.multiply(rf.T, photo_z)
        product = product.T
        # norm_product = product/product.sum()

        x = [z, [], z, z]
        y = [rf, [], photo_z, product]
        subplot(x, y, title, outdir, title_photoz)

    elif final_pdf == 'SF+photoz':
        plt.clf()
        title = ['', 'Survival Function', 'Photo-z']
        plot(z, sf, '1 - CDF', 'Survival Function', outdir)
        plot(z, photo_z, 'PDF', title_photoz, outdir, outname='photoz')

        product = np.multiply(sf.T, photo_z)
        product = product.T
        # norm_product = product/product.sum()

        x = [[], z, z, z]
        y = [[], sf, photo_z, product]
        subplot(x, y, title, outdir, title_photoz)

    elif final_pdf == 'RF':
        plt.clf()
        plot(z, rf, 'PDF', 'Random Forest', outdir)

    elif final_pdf == 'SF':
        plt.clf()
        plot(z, sf, '1 - CDF', 'Survival Function', outdir)

    elif final_pdf == 'photoz':
        plt.clf()
        plot(z, photo_z, 'PDF', title_photoz, outdir, outname='photoz')
