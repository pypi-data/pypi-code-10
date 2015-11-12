import os
from fabric.api import run, cd, local, env, put, abort, get, settings, prefix, task, execute
from fabric.decorators import hosts
from probe.cloud import Cloud
from probe.params import SimParams
from contextlib import contextmanager
import dataset
from terminaltables import AsciiTable
import time

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
MPI_VERSION='1.8.3'
HDF5_VERSION = '1.8.15-patch1'
WATCH_REMOTES = ['hercules.physics.muni.cz', 'xena.physics.muni.cz', 'umbriel.physics.muni.cz']

@task
def sim_run(simdir='~/.simulations', sourcedir='.', cloud=True,
            cloud_cfg='cloud.cfg', remote_venv='probe', dbfile='~/.simulations.sqlite',
            tmux_out_redirect='tmux.log', user=None, name=None, note=None, dry_run=False):

    with settings(warn_only=True):
        if local('git log', capture=True).failed:
            abort('source code has to be under version control!')

    git_sha = local('''git log | head -n 1 | awk '{print $2}' ''', capture=True).stdout.strip()
    git_branch = local('''git branch | head -n 1 | awk '{print $2}' ''', capture=True).stdout.strip()
    print git_branch, git_sha

    assert cloud_cfg in os.listdir(sourcedir), 'there is no cloud config in sourcedir!'

    user = os.environ['USER'] if user is None else user
    print '[sim-run] user: {}'.format(user)

    pwd = local('pwd', capture=True)
    print '[sim-run] pwd: {}'.format(pwd)

    sim_params = SimParams(os.path.join(sourcedir, 'input.params'))
    print sim_params.params

    # make sure that .simulations folder exists
    run('mkdir -p {}'.format(simdir))
    with cd(simdir):
        tempdir = run('mktemp -d -p {}'.format(simdir))
        tempstr = tempdir.split('.')[-1]
        print '[sim-run] tempdir: {}'.format(tempdir)

        if not dry_run:

            # put(os.path.join(sourcedir, '*'), tempdir)
            files = local('''find . -maxdepth 1 -name '*' -type f''', capture=True).stdout.split()
            files = ' '.join(files)
            local('scp {} {}@{}:{}'.format(files, user, env.host, tempdir))

            with cd(tempdir):
                with rollbackwrap(tempdir):
                    run('make')

                    run('tmux new -d -s {}'.format(tempstr))

                    if cloud:
                        cmd_run_simulation = 'probe_cloud.py -v cloud:run_simulation'
                    else:
                        cloud = Cloud(cloud_cfg)
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
    record.update(dict(host=env.host_string, tempdir=tempdir, tempstr=tempstr, user=user,
                       name=name, note=note, git_sha=git_sha, git_branch=git_branch))
    simulations.insert(record)

    print
    print tempstr


@task
def sim_rollback(tempstr, dbfile='~/.simulations.sqlite', kill_tmux_session=True):
    db, simulations = get_db_and_simulations_table(dbfile)
    tempdir = simulations.find_one(tempstr=tempstr)['tempdir']

    print '[sim_rollback] deleting dir {}'.format(tempdir)
    with settings(warn_only=True):
        run('rm -r {}'.format(tempdir))

    kill_tmux_session = False if kill_tmux_session == 'False' else True
    with settings(warn_only=True):
        if kill_tmux_session:
            run('tmux kill-session -t {}'.format(tempstr))

    print '[sim_rollback] deleting record from db'
    with settings(warn_only=True):
        simulations.delete(tempstr=tempstr)


@task
def sim_kill(tempstr, dbfile='~/.simulations.sqlite', kill_tmux_session=True):
    db, simulations = get_db_and_simulations_table(dbfile)
    tempdir = simulations.find_one(tempstr=tempstr)['tempdir']

    lines = run('cat {}'.format(os.path.join(tempdir, 'pids.log'))).stdout.split()
    parent_pid, child_pid, sim_pid = lines[-1].split(',')
    print parent_pid, child_pid, sim_pid
    with settings(warn_only=True):
        run('kill {}'.format(parent_pid))

    time.sleep(1)

    kill_tmux_session = False if kill_tmux_session == 'False' else True
    if kill_tmux_session:
        with settings(warn_only=True):
            run('tmux kill-session -t {}'.format(tempstr))


@task
def get_sim(tempstr, dbfile='~/.simulations.sqlite', simdir='~/.simulations', destdir='.'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    print '[sim_get] {}:{}'.format(sim['host'], sim['tempdir'])
    # env.hosts = [sim['host']]
    user = sim.get('user', os.environ['USER'])
    print '[sim_get] user: {}'.format(user)
    local('rsync --progress {}@{}:{} {}'.format(user, sim['host'], os.path.join(sim['tempdir'], 'sim.h5'), destdir))


def check_sim(tempdir):
    output = run('cat {}'.format(os.path.join(tempdir, 'pids.log')), quiet=True)
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
    db, simulations = get_db_and_simulations_table(dbfile)
    sims = simulations.all()
    for sim in sims:
        status = execute(check_sim, sim['tempdir'], host='{}@{}'.format(sim['user'], sim['host']))
        print '{}: {}'.format(sim['tempstr'], status['{}@{}'.format(sim['user'], sim['host'])])


@task
def get_h5ls(tempstr, dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_get_h5ls, sim, host='{}@{}'.format(sim['user'], sim['host']))


def _get_h5ls(sim):
    run('h5ls {}'.format(os.path.join(sim['tempdir'], 'sim.h5')))


@task
def get_params(tempstr, dbfile='~/.simulations.sqlite'):
    db, simulations = get_db_and_simulations_table(dbfile)
    sim = simulations.find_one(tempstr=tempstr)
    execute(_get_params, sim, host='{}@{}'.format(sim['user'], sim['host']))


def _get_params(sim):
    run('cat {}'.format(os.path.join(sim['tempdir'], 'input.params')))


@task
def get_cpu():
    run('cat /proc/cpuinfo | grep processor | wc -l')


@task
@hosts('argo.physics.muni.cz')
def install_ssh_key(remote, public_key=None, user=None):
    if not public_key:
        public_key = local('cat ~/.ssh/id_rsa.pub', capture=True).stdout

    if not user:
        user = env.user

    run('''ssh {}@{} 'echo {} >> .ssh/authorized_keys' '''.format(user, remote, public_key))


@task
@hosts('argo.physics.muni.cz')
def install_ssh_keys_from_remote_to_watch_remotes(remote_from, user=None):

    if not user:
        user = env.user

    output = local('''ssh {}@{} 'ls ~/.ssh' '''.format(user, remote_from), capture=True)
    files = output.stdout.split()
    if 'id_rsa.pub' not in files:
        abort('no id_rsa.pub on {}, run ssh-keygen there'.format(remote_from))

    public_key = local('''ssh {}@{} 'cat ~/.ssh/id_rsa.pub' '''.format(user, remote_from), capture=True).stdout

    for remote in WATCH_REMOTES:
        install_ssh_key(remote, public_key=public_key, user=user)


@task
def install_ssh_keygen():
    output = run('ls ~/.ssh')
    files = output.stdout.split()
    if 'id_rsa.pub' in files:
        abort('id_rsa.pub already generated')

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
        print '{}: NO virtualenvwrapper {}, {}'.format(env.host, output.stdout)
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
def install_python_package(package, virtualev='probe'):
    with settings(warn_only=True):
        if run('workon {}'.format(virtualev)).failed:
            if run('mkvirtualenv {}'.format(virtualev)).failed:
                abort('cant create virtualenv probe')

    with prefix('workon {}'.format(virtualev)):
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
def show_db(dbfile='~/.simulations.sqlite', show_all='False'):
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
def show_log(tempstr, dbfile='~/.simulations.sqlite', logfile='tmux.log'):
    db, simulations = get_db_and_simulations_table(dbfile)
    tempdir = simulations.find_one(tempstr=tempstr)['tempdir']
    run('cat {}'.format(os.path.join(tempdir, logfile)))


def get_db_and_simulations_table(dbfile):
    db = dataset.connect('sqlite:///{}'.format(os.path.expanduser(dbfile)))
    simulations = db['simulations']
    return db, simulations


@contextmanager
def rollbackwrap(tempdir):
    try:
        yield
    except SystemExit:
        rollback(tempdir)
        abort("Fail!")


def rollback(tempdir):
    print '[ROLLBACK]: deleting tempdir: {}'.format(tempdir)
    run('rm -rf {}'.format(tempdir))


def which_file(filename):
    output = run('which {}'.format(filename), quiet=True)
    if output.failed:
        print '{}: NO {}'.format(env.host, filename)
        return False
    else:
        print '{}: {}'.format(env.host, output.stdout)
        return True

