################################################################################
# IZMSMetacmdProvider.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
################################################################################

# Imports.
from zope.interface import Interface
# Product Imports.
import IZMSActionListContributor

class IZMSMetacmdProvider(Interface,IZMSActionListContributor.IZMSActionListContributor):

  def getMetaCmdDescription(self, id=None, name=None):
    """
    Returns description of meta-command specified by ID.
    @rtype: C{str}
    """

  def getMetaCmd(self, id=None, name=None):
    """
    Returns action.
    @rtype: C{dict}
    """

  def getMetaCmdIds(self, sort=1):
    """
    Returns list of action-ids.
    @rtype: C{list}
    """

  def getMetaCmds(self, sort=True):
    """
    Returns list of actions.
    @rtype: C{list}
    """
