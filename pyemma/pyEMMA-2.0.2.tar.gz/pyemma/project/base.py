from pyemma.coordinates.pipelines import Pipeline
from pyemma.coordinates.transform import PCA, TICA, Transformer
from pyemma.msm import EstimatedMSM, BayesianMSM
import jsonpickle


__author__ = 'marscher'
from pyemma.coordinates import source as _source


class Project(object):
    """
    a project stores the discretization and models living on this disc.

    Parameters
    ----------

    Examples
    --------

    """

    def __init__(self, timeunit='nanoseconds'):
        self.model_estimators = []
        self.pipeline = Pipeline([])
        self.timeunit = timeunit
        self._dirty = True

    ########### discretization

    def add_md_data(self, trajfiles, topfile):
        try:
            self._reader = _source(trajfiles, top=topfile)
        except IOError:
            raise

        self.pipeline.set_element(0, self._reader)

        return self._reader

    def add_trajectory_file(self, filename):
        if not hasattr(self, '_reader'):
            raise RuntimeError('create reader first!')

        import os
        os.stat(filename)

        self._reader.trajfiles.append(filename)
        self._reader.__set_dimensions_and_lengths()

        return self._reader

    @property
    def featurizer(self):
        try:
            return self._reader.featurizer
        except AttributeError:
            raise

    def add_transformation(self, T, *args, **kw):
        if isinstance(T, basestring):
            from pyemma.coordinates.api import __all__ as valid_names
            from pyemma import coordinates
            func = getattr(coordinates, T)
            inst = func(*args, **kw)
        else:
            assert isinstance(T, Transformer)
            inst = T

        self.pipeline.add_element(inst)
        return inst

    ########### model estimation

    def add_model_estimator(self, estimator, *args, **kw):

        if isinstance(estimator, basestring):
            if estimator == 'msm':
                estimator = EstimatedMSM
            elif estimator == 'bmsm':
                estimator = BayesianMSM

        self.model_estimators.append(estimator)

    def estimate(self):
        if not hasattr(self.pipeline._chain[-1], 'dtrajs'):
            raise RuntimeError('last elemement of discretization pipeline should be a clustering object')

        self.pipeline.parametrize()
        dtrajs = self.pipeline._chain[-1].dtrajs

    @property
    def timeunit(self):
        return self._timeunit

    @timeunit.setter
    def timeunit(self, unit):
        self._timeunit = unit

    def info(self):
        """
    something like:

    INPUT
    -------
    [top] topology:    protein.pdb, 1788 atoms
    [trajs] trajectories:    2 trajectories, 200 ns, 2000 frames
        traj1.xtc    100 ns, 1000 frames
        traj2.xtc    100 ns, 1000 frames

    FEATURES
    --------------
    [featurizer]: number of features:   3520
    - 3520 ca-distances

    TRANSFORMS
    -------------------
    1. [tica]: TICA, lag = 10, dim = 2
    2. [kmeans]: k-means, 1000 clusters

    MODELS
    ------------
    1. [bmsm]: Bayesian Markov model, lag = 100,
    2. [hmsm]: Hidden Markov model, lag = 100, 3 states
        """
        return "i'm a stupid project"

    def save(self, filename):
        out = jsonpickle.encode(self.pipeline)
        with open(filename, 'w') as fh:
            fh.write(out)
        return out

    @staticmethod
    def load(filename):
        with open(filename) as fh:
            input = fh.read()
            return jsonpickle.decode(input)

    @staticmethod
    def load2(string):
        return jsonpickle.decode(string)

    def copy(self):
        import copy
        return copy.deepcopy(self)


def create_proj(fn):
    p = Project()
    # disc
    #p.add_md_data('/home/marscher/md_dummy/traj_rnd.xtc', '/home/marscher/md_dummy/4QYZ.pdb.gz')
    p.add_md_data( '/home/marscher/md_dummy/traj_1frame.xtc','/home/marscher/md_dummy/4QYZ.pdb.gz')

    feat = p.featurizer
    feat.add_backbone_torsions()

    print feat.dimension()

    #p.add_transformation('tica', lag=1)
    #p.add_transformation('pca', dim=3)
    p.add_transformation('cluster_kmeans', k=2)

    # models
    p.add_model_estimator('msm')
    p.add_model_estimator('bmsm')

    p.estimate()
    return p.save(fn)

def load_proj(fn):
    return Project.load(fn)

if __name__ == '__main__':
    string = create_proj('/tmp/first_proj')
    #p = load_proj('/tmp/first_proj')
    p = Project.load2(string)
    print p