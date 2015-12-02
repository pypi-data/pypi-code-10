"""
.. module:: fabfile
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: Petr Zikan <zikan.p@gmail.com>

This module contains many handful functions for dealing with remote simulations.

"""
import os
from fabric.api import run, cd, local, env, put, abort, get, settings, prefix, task, roles, execute
from fabric.decorators import hosts
from probe.cloud import Cloud
from probe.params import SimParams
from contextlib import contextmanager
import dataset
from terminaltables import AsciiTable
import time
import tempfile

env.warn_only = False

keys_to_db = [
    'phi_p',
    'T_i',
    'I',
    'ions',
    'r_p',
    'dr',
    'T_g',
    'T_e',
    'pressure',
    'geom',
    'phi_d',
    'NSP',
    'n_e',
    'dt',
    'r_d',
    'ntimes',
]
MPI_VERSION = '1.8.3'
HDF5_VERSION = '1.8.16'
WATCH_REMOTES = ['hercules.physics.muni.cz', 'xena.physics.muni.cz', 'umbriel.physics.muni.cz']

env.roledefs = {'argo': ['argo.physics.muni.cz'], }


@task
def sim_run(simsdir='~/.simulations', sourcedir='.', cloud=True,
            cloud_cfg='cloud.cfg', remote_venv='probe', dbfile='~/.simulations.sqlite',
            tmux_out_redirect='tmux.log', user=None, name=None, note=None, dry_run=False):
    """
    This is a function that can run a simulation on a remote host.

    It copies all files (not folders!) from ``sourcedir`` to ``simsdir`` and saves it under folder that is automatically
    generated (sim.<name>.<tempstr>) at remote host. You have to specify the host like:
    ``fab -H user@remote sim_run:kwarg=value...``

    Simulations are being ran in tmux using ``remote_venv``. Once simulation is successfully started, a record with
    all information is inserted into ``dbfile``.

    Output of tmux is redirected to ``tmux_out_redirect`` which is saved in simulation's folder at remote host.

    You can also specify a ``user``, ``name`` of simulation and add a ``note``.

    Args:
        simsdir (Optional[str]): folder on remote, where simulation will be stored (in a folder automatically generated)
        sourcedir (Optional[str]): path to folder with source files (default: .)
        cloud (Optional[bool]): if True, simulation will be suspended when other computation is running on a host,
                                set to False, to disable it
        cloud_cfg (Optional[str]): specifies path to a configuration file for running simulation with important
                            information (sim_start, sim_end, number of processors)
        remote_venv (Optional[str]): python env on remote host to use
        dbfile (Optional[str]): path to your local db file
        tmux_out_redirect (Optional[str]): file where all simulation's logging output will be stored
                            (on remote in simulation's dir)
        user (Optional[str]): simulation os remote can be also ran under different user that you are on local host
        name (Optional[str]): name of simulation (default: noname)
        note (Optional[str]): note
        dry_run (Optional[str]): if set to True, no files will be copied to remote and no simulation will be ran, but
                            all operations will be done on local (only for testing purposes)
    """

    with settings(warn_only=True):
        if local('git log', capture=True).failed:
            abort('source code has to be under version control!')

    git_sha = local('''git log | head -n 1 | awk '{print $2}' ''', capture=True).stdout.strip()
    git_branch = local('''git branch | head -n 1 | awk '{print $2}' ''', capture=True).stdout.strip()
    print git_branch, git_sha

    assert cloud_cfg in os.listdir(sourcedir), 'there is no cloud config in sourcedir!'

    user = env.user if user is None else user
    print '[sim-run] user: {}'.format(user)

    name = 'noname' if name is None else name
    print '[sim-run] name: {}'.format(name)

    sim_params = SimParams(os.path.join(sourcedir, 'input.params'))
    print sim_params.params

    # make sure that .simulations folder exists
    run('mkdir -p {}'.format(simsdir))
    with cd(simsdir):
        tempdir = run('mktemp -d -p {}'.format(simsdir))
        print '[sim-run] tempdir: {}'.format(tempdir)
        tempstr = tempdir.split('.')[-1]
        simdir = '.'.join(['sim', name, tempstr])
        simdir = os.path.join(os.path.expanduser(simsdir), simdir)
        run('mv {} {}'.format(tempdir, simdir))
        print '[sim-run] simdir: {}'.format(simdir)

        if not dry_run:

            # put(os.path.join(sourcedir, '*'), tempdir)
            files = local('''find {} -maxdepth 1 -name '*' -type f'''.format(sourcedir), capture=True).stdout.split()
            files = ' '.join(files)
            local('scp {} {}@{}:{}'.format(files, user, env.host, simdir))

            with cd(simdir):
                with rollbackwrap(simdir):
                    run('make')

                    execute(_create_tmux_session, tempstr, with_cd=simdir, host='{}@{}'.format(user, env.host))

                    if cloud:
                        cmd_run_simulation = 'probe_cloud.py -v cloud:run_simulation'
                    else:
                        cloud = Cloud(cloud_cfg)
                        # TODO: opackovac spousteni simulace
                        cmd_run_simulation = cloud.cfg['cmd']

                    if tmux_out_redirect:
                        cmd_run_simulation = cmd_run_simulation + ' 2>&1 | tee {}'.format(tmux_out_redirect)
                    cmd_template = 'tmux send-keys -t {}:0 "workon {} && {}" C-m'
                    cmd = cmd_template.format(tempstr, remote_venv, cmd_run_simulation)

                    run(cmd)
        else:
            print '[sim-run] this is only dry_run, no files were copied to remote host'

    # insert simulation into db
    db, simulations = get_db_and_simulations_table(dbfile)

    record = {key: sim_params.params[key] for key in keys_to_db}
    record.update(dict(host=env.host_string, simdir=simdir, tempstr=tempstr, user=user,
                       name=name, note=note, git_sha=git_sha, git_branch=git_branch))
    simulations.insert(record)

    print
    print tempstr


def _create_tmux_session(tempstr, with_cd=None):
    if with_cd:
        with cd(with_cd):
            run('tmux new -d -s {}'.format(tempstr))
    else:
        run('tmux new -d -s {}'.format(tempstr))


@task
def sim_rollback(tempstr, dbfile='~/.simulations.sqlite', kill_tmux_session=True, delete_from_db=True):
    """
    Deletes simulation from remote computer and deletes also record about this simulation from database.
    This finds information (remote computer f.e.) about simulation from dbfile with tempstr.
    """
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    kill_tmux_session = False if kill_tmux_session == 'False' else True
    delete_from_db = False if delete_from_db == 'False' else True
    execute(_sim_rollback, sim, simulations, kill_tmux_session=kill_tmux_session, delete_from_db=delete_from_db,
            host='{}@{}'.format(sim['user'], sim['host']))


def _sim_rollback(sim, simulations_table, kill_tmux_session=True, delete_from_db=True):
    print '[sim_rollback] deleting dir {}'.format(sim['simdir'])
    with settings(warn_only=True):
        run('rm -r {}'.format(sim['simdir']))

    with settings(warn_only=True):
        if kill_tmux_session:
            run('tmux kill-session -t {}'.format(sim['tempstr']))

    with settings(warn_only=True):
        if delete_from_db:
            print '[sim_rollback] deleting record from db'
            simulations_table.delete(tempstr=sim['tempstr'])


@task
def sim_kill(tempstr, dbfile='~/.simulations.sqlite', kill_tmux_session=False):
    """
    Kills simulation with given tempstr.
    This can also kill tmux session if kill_tmux_session is set to True.
    """
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_sim_kill, sim, kill_tmux_session=kill_tmux_session, host='{}@{}'.format(sim['user'], sim['host']))


def _sim_kill(sim, kill_tmux_session=False):
    lines = run('cat {}'.format(os.path.join(sim['simdir'], 'pids.log'))).stdout.split()
    parent_pid, child_pid, sim_pid = lines[-1].split(',')
    print parent_pid, child_pid, sim_pid
    with settings(warn_only=True):
        run('kill {}'.format(parent_pid))

    time.sleep(1)

    if kill_tmux_session:
        with settings(warn_only=True):
            run('tmux kill-session -t {}'.format(sim['tempstr']))


@task
def sim_cuth5(tempstr, run_number, dbfile='~/.simulations.sqlite', move=False):
    """
    Removes much information from h5 file in order to reduce its size.
    run_number has to be set to (NumberOfOutputsYouWantToUse+1)
    """
    move = True if move == 'True' else False

    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)

    run_number = int(run_number)
    execute(_sim_cuth5, sim, run_number, host=sim['host'], move=move)


def _sim_cuth5(sim, run_number, move=False):

    input_params = run('cat {}'.format(os.path.join(sim['simdir'], 'input.params')), quiet=True).stdout

    with tempfile.TemporaryFile() as f:
        f.writelines(input_params)
        f.seek(0)
        sp = SimParams(f)

    print sp.params

    h5ls = _get_h5ls(sim)

    names = [name for name, _ in h5ls if name.startswith('ts_')]
    names.sort()

    index = names.index('ts_{:010d}'.format(int(sp.params['ntimes'] * (run_number - 1))))

    objects = set()
    for i in range(run_number - 1):
        # objects.add('init_{:04d}'.format(i))
        # objects.add('save_{:04d}'.format(i))
        objects.add('sweep_{:04d}'.format(i))
        objects.add('common_{:04d}'.format(i))
        objects.add('gstats_{:04d}'.format(i))

    objects.add('save_{:04d}'.format(run_number - 2))

    objects = objects.union(set(names[:index + 1]))
    objects = sorted(list(objects))
    objects = '\n'.join(objects)

    with settings(warn_only=True):
        local('rm -f tmp.objects')

    with open('tmp.objects', 'w') as f:
        f.write(objects)

    local('scp tmp.objects {}@{}:{}'.format(env.user, env.host, sim['simdir']))

    with cd(sim['simdir']):
        run('while read obj || [[ -n $obj ]]; do h5copy -v -i {} -o {} -s $obj -d $obj; done < tmp.objects'.format(
            os.path.join(sim['simdir'], 'sim.h5'),
            os.path.join(sim['simdir'], 'sim_new.h5')))
        if move:
           run('mv sim_new.h5 sim.h5')


@task
def sim_repairh5(tempstr, dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_sim_repairh5, sim, host=sim['host'])


def _sim_repairh5(sim):
    input_params = run('cat {}'.format(os.path.join(sim['simdir'], 'input.params')), quiet=True).stdout

    with tempfile.TemporaryFile() as f:
        f.writelines(input_params)
        f.seek(0)
        sp = SimParams(f)

    print sp.params

    h5ls = _get_h5ls(sim)

    common_no = 0
    save_no = 0
    init_no = 0

    for l in h5ls:
        name, typ = l
        if 'common' in name: common_no += 1
        if 'save' in name: save_no += 1
        if 'init' in name: init_no += 1

    #    assert common_no == init_no
    #    assert save_no == init_no - 1

    names = [name for name, _ in h5ls if name.startswith('ts_')]
    names.sort()

    index = names.index('ts_{:010d}'.format(int(sp.params['ntimes'] * (common_no - 1))))

    objects = set()
    for i in range(common_no - 1):
        # objects.add('init_{:04d}'.format(i))
        # objects.add('save_{:04d}'.format(i))
        objects.add('sweep_{:04d}'.format(i))
        objects.add('common_{:04d}'.format(i))
        objects.add('gstats_{:04d}'.format(i))

    objects.add('save_{:04d}'.format(common_no - 2))

    objects = objects.union(set(names[:index + 1]))
    objects = sorted(list(objects))
    objects = '\n'.join(objects)

    with cd(sim['simdir']):
        run('cat > objects <<EOL\n{}\nEOL'.format(objects))
        run('for obj in `cat objects`; do h5copy -v -i {} -o {} -s $obj -d $obj; done'.format(
            os.path.join(sim['simdir'], 'sim.h5'),
            os.path.join(sim['simdir'], 'sim_new.h5')))
        # run('mv sim_new.h5 sim.h5')


@task
def sim_extend(tempstr, sourcedir='.', cloud=True,
               cloud_cfg='cloud.cfg', remote_venv='probe', dbfile='~/.simulations.sqlite',
               tmux_out_redirect='tmux.log'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_sim_extend, sim, sourcedir=sourcedir, cloud=cloud, cloud_cfg=cloud_cfg,
            host=sim['host'], remote_venv=remote_venv, tmux_out_redirect=tmux_out_redirect)


def _sim_extend(sim, sourcedir='.', cloud=True,
                cloud_cfg='cloud.cfg', remote_venv='probe',
                tmux_out_redirect='tmux.log'):
    local('scp {} {}@{}:{}'.format(os.path.join(sourcedir, cloud_cfg), sim['user'], env.host, sim['simdir']))
    if cloud:
        cmd_run_simulation = 'probe_cloud.py -v cloud:run_simulation'
    else:
        cloud = Cloud(cloud_cfg)
        # TODO: opackovac spousteni simulace
        cmd_run_simulation = cloud.cfg['cmd']

    if tmux_out_redirect:
        cmd_run_simulation = cmd_run_simulation + ' 2>&1 | tee {}'.format(tmux_out_redirect)

    with settings(warn_only=True):
        _create_tmux_session(sim['tempstr'], with_cd=sim['simdir'])

    run('tmux send-keys -t {}:0 "workon {} && {}" C-m'.format(sim['tempstr'], remote_venv, cmd_run_simulation))


@task
def sim_move(tempstr, remote_to, user_to=None, dbfile='~/.simulations.sqlite'):
    """
    Moves simulation from remote computer where is now to remote_to.
    Default user, who moves simulation, is the one who started simulation, but you can specify it with user_to.
    """
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)

    if user_to is None:
        user_to = sim['user']

    simsdir = os.path.split(sim['simdir'])[0]
    print '[sim_move] creating simsdir on remote_to'
    execute(lambda: run('mkdir -p {}'.format(simsdir)), host='{}@{}'.format(user_to, remote_to))

    print '[sim_move] moving simulation'
    execute(_sim_move, sim, remote_to, user_to, host='{}@{}'.format(sim['user'], sim['host']))

    print '[sim_move] make'
    execute(lambda: run('cd {} && make'.format(sim['simdir'])), host='{}@{}'.format(user_to, remote_to))

    print '[sim_move] rolling back old simulation'
    execute(_sim_rollback, sim, simulations, kill_tmux_session=True, delete_from_db=False,
            host='{}@{}'.format(sim['user'], sim['host']))

    print '[sim_move] creating new tmux session'
    execute(_create_tmux_session, tempstr, with_cd=sim['simdir'], host='{}@{}'.format(user_to, remote_to))

    print '[sim_move] updating db'
    db_update(tempstr, 'host', remote_to, dbfile=dbfile)


def _sim_move(sim, remote_to, user_to):
    with cd(sim['simdir']):
        run('make clean')
    run('scp -r {} {}@{}:{}'.format(sim['simdir'], user_to, remote_to, sim['simdir']))


@task
def get_sim(tempstr, dbfile='~/.simulations.sqlite', destdir='.'):
    """
    Copies simulation with given tempstr to local destdir (default is ./)
    """
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_get_sim, sim, destdir=destdir, host='{}@{}'.format(sim['user'], sim['host']))


def _get_sim(sim, destdir='.'):
    local('rsync --progress {}@{}:{} {}'.format(sim['user'], sim['host'], os.path.join(sim['simdir'], 'sim.h5'),
                                                destdir))


def check_sim(simdir):
    output = run('cat {}'.format(os.path.join(simdir, 'pids.log')), quiet=True)
    if output.failed:
        return 'No pids.log, this should not happen!'

    lines = output.stdout.split()
    parent_pid, child_pid, sim_pid = lines[-1].split(',')

    if run('ps {}'.format(sim_pid), quiet=True).failed:
        return 'Finished'

    status = run('''ps cax | grep {} | awk '{{print $3}}' '''.format(sim_pid), quiet=True).stdout
    return status


@task
def check_sims(dbfile='~/.simulations.sqlite'):
    """
    Checks if simulations with records in dbfile are running or finished.
    """
    db, simulations = get_db_and_simulations_table(dbfile)
    sims = simulations.all()
    for sim in sims:
        status = execute(check_sim, sim['simdir'], host='{}@{}'.format(sim['user'], sim['host']))
        print '{}: {}'.format(sim['tempstr'], status['{}@{}'.format(sim['user'], sim['host'])])


@task
def get_h5ls(tempstr, dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    h5ls = execute(_get_h5ls, sim, host='{}@{}'.format(sim['user'], sim['host']))['{}@{}'.format(env.user, sim['host'])]
    for l in h5ls:
        print l[0], l[1]


def _get_h5ls(sim):
    h5ls = run('h5ls {}'.format(os.path.join(sim['simdir'], 'sim.h5')), quiet=True).stdout.split(os.linesep)
    h5ls = [l.strip() for l in h5ls]
    h5ls = [tuple(l.split()) for l in h5ls]
    return h5ls


@task
def get_params(tempstr, dbfile='~/.simulations.sqlite'):
    """
    Prints parameters of simulation with given tempstr.
    """
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_get_params, sim, host='{}@{}'.format(sim['user'], sim['host']))


def _get_params(sim):
    run('cat {}'.format(os.path.join(sim['simdir'], 'input.params')))


@task
def get_remote_info():
    cpu_number = run('cat /proc/cpuinfo | grep processor | wc -l', quiet=True).stdout
    df = run('df -h .', quiet=True).stdout
    df_info = df.split('\n')[-1].split()
    print '{}: cpu: {}, disk_total: {}, disk_avail: {}'.format(env.host, cpu_number, df_info[1], df_info[3])


@task
@hosts('argo.physics.muni.cz')
def install_ssh_key(remote, public_key=None, user=None):
    if not public_key:
        public_key = local('cat ~/.ssh/id_rsa.pub', capture=True).stdout

    login_to_install = public_key.strip().split(' ')[2]
    print '[install_ssh_key]: key_to_install: {}'.format(login_to_install)

    if not user:
        user = env.user

    output = run('''ssh {}@{} 'cat .ssh/authorized_keys' '''.format(user, remote, public_key))
    if not output.failed:
        logins_on_remote = [key.split(' ')[2].strip() for key in output.stdout.split('\n')]
        print '[install_ssh_key]: logins_on_remote: {}'.format(logins_on_remote)
        if login_to_install in logins_on_remote:
            abort('not installing {}, it is already on {}'.format(login_to_install, remote))

    run('''ssh {}@{} 'echo {} >> .ssh/authorized_keys' '''.format(user, remote, public_key))


@task
@hosts('argo.physics.muni.cz')
def install_ssh_key_from_remote_to_remote(remote_from, remote_to, user_from=None, user_to=None):
    if not user_from:
        user_from = env.user
    if not user_to:
        user_to = env.user

    output = run('''ssh {}@{} 'ls ~/.ssh' '''.format(user_from, remote_from))
    print '[install_ssh_key_from_remote_to_remote] output: {}'.format(output.stdout)
    files = output.stdout.split()
    if 'id_rsa.pub' not in files:
        abort('no id_rsa.pub on {}, run ssh-keygen there'.format(remote_from))

    public_key = run('''ssh {}@{} 'cat ~/.ssh/id_rsa.pub' '''.format(user_from, remote_from)).stdout

    install_ssh_key(remote_to, public_key=public_key, user=user_to)


@task
def install_ssh_keygen():
    output = run('ls ~/.ssh')
    files = output.stdout.split()
    if 'id_rsa.pub' in files:
        print 'id_rsa.pub already generated'
        return

    run('ssh-keygen')


@task
def install_paths():
    run('''echo 'export PATH=/home/'"${USER}"'/.local/bin:$PATH' >> ~/.bashrc''')
    run('''echo 'export LD_LIBRARY_PATH=/home/'"${USER}"'/.local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc''')


@task
def install_mpi():
    run('mkdir -p .local')
    with cd('~/.local'):
        run('wget http://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-{}.tar.gz'.format(MPI_VERSION))
        run('gunzip -c openmpi-{}.tar.gz | tar xf -'.format(MPI_VERSION))
        with cd('openmpi-{}'.format(MPI_VERSION)):
            run('./configure --prefix=/home/${USER}/.local')
            run('make all install')


@task
def install_mpi_paths():
    mpirun_dir = find_file('mpirun')
    print '{}: {}'.format(env.host, mpirun_dir)
    run('''echo 'export PATH={}:$PATH' >> ~/.bashrc'''.format(mpirun_dir))
    libmpi_dir = find_file('libmpi.so')
    print '{}: {}'.format(env.host, libmpi_dir)
    run('''echo 'export LD_LIBRARY_PATH={}:$LD_LIBRARY_PATH' >> ~/.bashrc'''.format(libmpi_dir))


def find_file(filename):
    output = run('find / -name {} 2> /dev/null'.format(filename), quiet=True)
    if output.stdout == '':
        abort('{}: FILE {} NOT FOUND!'.format(env.host, filename))

    filedir = os.path.join(*[os.path.sep] + output.stdout.split()[0].split('/')[:-1])
    return filedir


@task
def check_mpi():
    run('which mpirun')


@task
def install_hdf5():
    if not which_file('h5pfc'):
        run('mkdir -p ~/.local')
        with cd('~/.local'):
            run('wget ftp://ftp.hdfgroup.org/HDF5/current/src/hdf5-{}.tar.gz'.format(HDF5_VERSION))
            run('tar -xvzf hdf5-{}.tar.gz'.format(HDF5_VERSION))
            with cd('hdf5-{}'.format(HDF5_VERSION)):
                run('./configure --enable-fortran --enable-parallel --prefix=/home/${USER}/.local --enable-shared')
                run('make')
                run('make install')


@task
def check_hdf5():
    which_file('h5pfc')


@task
def install_pip():
    if run('wget https://bootstrap.pypa.io/get-pip.py').failed:
        if run('wget --no-check-certificate http://bootstrap.pypa.io/get-pip.py').failed:
            abort('[install_pip] cant wget pip')

    run('python get-pip.py --user')


@task
def check_pip():
    which_file('pip')


@task
def install_virtualenvwrapper():
    run('pip install --user virtualenvwrapper')
    run('mkdir -p ~/.virtualenvs')
    run('''echo 'export WORKON_HOME=/home/'"${USER}"'/.virtualenvs' >> .bashrc''')
    run('''echo 'source /home/'"${USER}"'/.local/bin/virtualenvwrapper.sh' >> .bashrc''')


@task
def check_virtualenvwrapper():
    output = run('pip list | grep virtualenvwrapper', quiet=True)
    if output.failed:
        print 'NO virtualenvwrapper {}, {}'.format(env.host, output.stdout)
        return False
    else:
        print '{}: {}'.format(env.host, output.stdout)
        return True


@task
def check_probe():
    output = run('workon probe', quiet=True)
    if output.failed:
        print '{}: no probe!'.format(env.host)
    else:
        print '{}: OK'.format(env.host)


@task
def install_python_package(package, virtualenv='probe'):
    with settings(warn_only=True):
        if run('workon {}'.format(virtualenv)).failed:
            if run('mkvirtualenv {}'.format(virtualenv)).failed:
                abort('cant create virtualenv probe')

    with prefix('workon {}'.format(virtualenv)):
        run('pip install -U {}'.format(package))
        # run('pip install Cython')
        # run('pip install mpi4py')
        # run('pip install numpy')
        # run('pip install --global-option=build_ext --global-option="-I/home/$USER/.local/include" --global-option="-L/home/$USER/.local/lib" h5py')
        # run('pip install matplotlib')
        # run('pip install scipy')
        # run('pip install pandas')
        # run('pip install boltons')
        # run('pip install sphinx')
        # run('pip install probe-data-process')
        # run('pip install bokeh')
        # run('pip install statsmodels')
        # run('pip install ipython')


@task
def check_python_package(package, virtualenv='probe'):
    with prefix('workon {}'.format(virtualenv)):
        output = run('pip list | grep {}'.format(package), quiet=True)
        if output.failed:
            print '{}: NO PACKAGE {}, {}'.format(env.host, package, output.stdout)
            return False
        else:
            print '{}: {}'.format(env.host, output.stdout)
            return True


@task
def db_show(dbfile='~/.simulations.sqlite', show_all='False'):
    """
    Shows database located in dbfile.
    You can specify, if you want to see all information with show_all.
    """
    db, simulations = get_db_and_simulations_table(dbfile)

    show_all = True if show_all == 'True' else False

    if len(simulations) > 0:
        sims = [sim for sim in simulations.all()]

        if show_all:
            print '[show_db] printing all columns of db'
            sims_list = [sims[0].keys()]
            for sim in sims:
                sims_list.append([str(s) for s in sim.values()])
        else:
            print '[show_db] printing only selected columns of db'
            cols = ['name', 'tempstr', 'host', 'geom', 'r_p', 'r_d', 'n_e', 'phi_p', 'I', 'T_i', 'T_g', 'T_e',
                    'pressure', 'NSP', 'note']
            sims_list = [cols]
            for sim in sims:
                row = list()
                for col in cols:
                    row.append(str(sim[col]))
                sims_list.append(row)

        table = AsciiTable(sims_list)
        print
        print 'Simulations'
        print table.table
    else:
        print 'There are no simulations in db.'


@task
def db_update(tempstr, column, value, dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)

    value_type = type(sim[column])
    value = value_type(value)

    sim[column] = value
    print '[db_update] updating {} to new value {}'.format(column, value)
    simulations.update(sim, ['id'])


@task
def show_log(tempstr, dbfile='~/.simulations.sqlite', logfile='tmux.log'):
    db, simulations = get_db_and_simulations_table(dbfile)
    simdir = simulations.find_one(tempstr=tempstr)['simdir']
    run('cat {}'.format(os.path.join(simdir, logfile)))


def get_db_and_simulations_table(dbfile):
    db = dataset.connect('sqlite:///{}'.format(os.path.expanduser(dbfile)))
    simulations = db['simulations']
    return db, simulations


@contextmanager
def rollbackwrap(simdir):
    try:
        yield
    except SystemExit:
        rollback(simdir)
        abort("Fail!")


def rollback(simdir):
    print '[ROLLBACK]: deleting simdir: {}'.format(simdir)
    run('rm -rf {}'.format(simdir))


def which_file(filename):
    output = run('which {}'.format(filename), quiet=True)
    if output.failed:
        print '{}: NO {}'.format(env.host, filename)
        return False
    else:
        print '{}: {}'.format(env.host, output.stdout)
        return True


@task
def archive(tempstr, run_number, dbfile='~/.simulations.sqlite', name=None, destination="/home/probe/data/cloud/", fit_last=1e6,
            compress=True, clean=False):
    """
    This function archives simulation with given tempstr at probe@argo.physics.muni.cz:destination.
    Automatically ipynotebook is created and record of simulation is inserted into database at probe.  
    run_number has to be set to (NumberOfOutputs+1).
    If name of simulation was't specified at start, you can specify it now with argument name.
    In order to prevent archiving huge h5 files, you can compress h5 file. This is done by default.
    You can set clean to True to delete simulation from remote computer, but it is better to check simulation and rollback it manually.
    """
    destination = os.path.join(destination)
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    if not name:
        name = sim['name']
    if name == "noname":
        print "[archive] This simulation has no name"
    # Todo?: Posledni sance, jak nastavit jmeno
    if compress == "False":
        compress = False
    if compress:
        print "[archive] EXECUTING: _sim_cuth5"
        run_number = int(run_number)
        execute(_sim_cuth5, sim, run_number, host=sim['host'])
    print "[archive] EXECUTING: _archive"
    execute(_archive, tempstr, name, destination, compress, host=sim['host'])
    if clean:
        print "[archive] EXECUTING: rollback"
        execute(rollback, "./simulations/sim.{}.{}".format(name, tempstr), host=sim['host'])
    print "[archive] EXECUTING: _ipynotebook"
    execute(_ipynotebook, name, tempstr, destination, fit_last,
            host='probe@argo.physics.muni.cz')
    print "[archive] ]EXECUTING: _insert_to_central_db"
    execute(_insert_to_central_db, tempstr, sim, destination, host='argo.physics.muni.cz')


def _archive(tempstr, name, destination, compress):
    """
    Archives simulation with given tempstr and name at probe@argo.physics.muni.cz:destination.
    """
    print "[_archive] Simulation will be archived in:", destination
    with cd('.simulations/sim.{}.{}/'.format(name, tempstr)):
        if compress:
            run('mv ./sim.h5 ../{}_old.h5'.format(name))
            run('mv ./sim_new.h5 ./{}.h5'.format(name))
            run('mv ./input.params ./{}.params'.format(name))
            run('scp -r ../sim.{}.{} probe@argo.physics.muni.cz:{}'.format(name, tempstr, destination))
            run('mv ../{}_old.h5 ./sim.h5'.format(name))
            run('rm ./{}.h5 '.format(name))
            run('mv ./{}.params ./input.params'.format(name))
        else:
            run('mv ./sim.h5 ./{}.h5'.format(name))
            run('mv ./input.params ./{}.params'.format(name))
            run('scp -r ../sim.{}.{} probe@argo.physics.muni.cz:{}'.format(name, tempstr, destination))
            run('mv ./{}.h5 ./sim.h5'.format(name))
            run('mv ./{}.params ./input.params'.format(name))


def _ipynotebook(name, tempstr, destination, fit_last):
    """
    Creates notebook at probe@argo.physics.muni.cz:/home/probe/notebooks/cloud/ that is named name.tempstr.ipynb
    """
    with cd('/home/probe/notebooks/cloud/'):
        run('cp GreatTemplate.ipynb ./{}.{}.ipynb'.format(name, tempstr))
        run('sed -i \'s|ThisShallBeYourName|{}|g\' {}.{}.ipynb'.format(name, name, tempstr))
        run('sed -i \'s|PathToH5|{}sim.{}.{}/|g\' {}.{}.ipynb'.format(destination, name, tempstr, name, tempstr))
        run('sed -i \'s|PathToParams|{}sim.{}.{}/|g\' {}.{}.ipynb'.format(destination, name, tempstr, name,
                                                                          tempstr))
        run('sed -i \'s|FitThisNumberOfTimesteps|{}|g\' {}.{}.ipynb'.format(fit_last, name, tempstr))


def _insert_to_central_db(tempstr, sim, destination):
    """
    Inserts record of simulation with given tempstr to database at probe@argo.physics.muni.cz:/home/probe/.simulations.sqlite
    """
    with settings(warn_only=True):
        local('rm -r ~/.sim.tmp')
    local('mkdir -p ~/.sim.tmp')
    local('scp probe@argo.physics.muni.cz:{}sim.{}.{}/{}.params ~/.sim.tmp/'.format(destination, sim['name'], tempstr, sim['name']))
    local('scp probe@argo.physics.muni.cz:/home/probe/.simulations.sqlite ~/.sim.tmp/')
    db, simulations = get_db_and_simulations_table('~/.sim.tmp/.simulations.sqlite')
    sim_params = SimParams(os.path.expanduser('~/.sim.tmp/{}.params'.format(sim['name'])))
    record = {key: sim_params.params[key] for key in keys_to_db}
    record.update(dict(host=sim['host'], simdir=sim['simdir'], tempstr=tempstr, user=sim['user'],
					   name=sim['name'], note=sim['note'], git_sha=sim['git_sha'], git_branch=sim['git_branch']))
    simulations.insert(record)
    local('scp ~/.sim.tmp/.simulations.sqlite probe@argo.physics.muni.cz:/home/probe/.simulations.sqlite')
    local('rm -r ~/.sim.tmp')


