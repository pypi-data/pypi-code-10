#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: David C. Morrill <dmorrill@enthought.com>
#
#-----------------------------------------------------------------------------
""" An action that saves the active perspective as a user perspective. """


# Local imports.
from .user_perspective_name import UserPerspectiveName
from .workbench_action import WorkbenchAction


class SaveAsUserPerspectiveAction(WorkbenchAction):
    """ An action that saves the active perspective as a user perspective. """

    #### 'Action' interface ###################################################

    # The action's unique identifier.
    id = 'pyface.workbench.action.save_as_user_perspective_action'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Save Perspective As...'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        window  = event.window
        manager = window.workbench.user_perspective_manager

        # Get the name of the new perspective.
        upn = UserPerspectiveName(name=window.active_perspective.name)
        if upn.edit_traits(view='save_as_view').result:
            # Make a clone of the active perspective, but give it the new name.
            perspective = manager.clone_perspective(
                 window, window.active_perspective, name=upn.name.strip()
            )

            # Add it to the window...
            window.perspectives.append(perspective)

            # ... and make it the active perspective.
            window.active_perspective = perspective

        return

#### EOF #####################################################################
