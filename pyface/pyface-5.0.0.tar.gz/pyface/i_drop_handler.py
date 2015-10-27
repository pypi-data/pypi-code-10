from traits.api import Interface


class IDropHandler(Interface):
    """ Interface for a drop event handler, which provides API to check if the
    drop can be handled or not, and then handle it if possible.
    """

    def can_handle_drop(self, event, target):
        """ Whether or not a drag event can be handled

        This is used to give feedback to the user about whether a drop is
        possible via the shape of the cursor or similar indicators.

        Parameters
        ----------
        event : drag event
            A drag event with information about the object being dragged.
        target : toolkit widget
            The widget that would be dropped on.

        Returns
        -------
        can_drop : bool
            True if the current drop handler can handle the given drag
            event occurring on the given target widget.
        """

    def handle_drop(self, event, target):
        """ Performs drop action when drop event occurs on target widget.

        Parameters
        ----------
        event : drop event
            A drop event with information about the object being dropped.
        target : toolkit widget
            The widget that would be dropped on
        """
