from __future__ import absolute_import

from .channels import Channel
from .explorer import Explorer

from .meshgrid import MeshGrid
from .meshgrid import ExplorerMeshGrid

# Explorers
from .algorithms.m_rand     import RandomMotorExplorer
from .algorithms.s_rand     import RandomGoalExplorer
from .algorithms.s_mesh     import MeshgridGoalExplorer
from .algorithms.s_unreach  import UnreachGoalExplorer
from .algorithms.s_frontier import FrontierGoalExplorer
from .algorithms.reuse      import ReuseExplorer
from .algorithms.reuse      import ManualReuseExplorer
from .algorithms.reuse      import MultiReuseExplorer
from .algorithms.reuse      import GoalReuseExplorer
from .algorithms.reuse      import SubReuseExplorer
from .algorithms.s_set      import GoalSetExplorer
from .algorithms.meta       import MetaExplorer
from .algorithms.s_restrict import RestrictGoalExplorer
from .algorithms.m_disturb  import MotorDisturbExplorer
from .algorithms.adapt      import AdaptExplorer

# Interest Model
from .algorithms.im        import IMExplorer
from .algorithms.im        import LocalInterestModel
from .algorithms.im import PredictiveNoveltyMotivation
from .algorithms.im import IntermediateLevelOfNoveltyMotivation

from ._version import get_versions
__version__ = get_versions()["version"]
__commit__ = get_versions()["full-revisionid"]
__dirty__ = get_versions()["dirty"]
del get_versions
