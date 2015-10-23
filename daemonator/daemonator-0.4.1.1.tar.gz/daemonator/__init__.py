from .daemonator import Daemon

__author__ = 'Flávio Cardoso Pontes'
__author_email__ = '<flaviopontes@acerp.org.br>'
__copyright__ = 'Copyright © 2015 Associação de Comunicação Educativa Roquette Pinto - ACERP'

__version_info__ = (0, 4, 1, 1)
__version__ = '.'.join(map(str, __version_info__))
__package__ = 'daemonator'

__all__ = ['Daemon']