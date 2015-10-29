# Scriptable KVM/QEMU guest agent in Python.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: December 30, 2014
# URL: https://negotiator.readthedocs.org

"""
``negotiator_host`` - Channel for communication with guests
===========================================================

This module implements the :py:class:`GuestChannel` class which provides the
host side of the channel between QEMU hosts and guests. Channel objects can be
used to query and command running guests.
"""

# Standard library modules.
import logging
import multiprocessing
import os
import socket
import stat
import time

# Modules included in our project.
from negotiator_common import NegotiatorInterface
from negotiator_common.config import CHANNELS_DIRECTORY, GUEST_TO_HOST_CHANNEL_NAME, HOST_TO_GUEST_CHANNEL_NAME
from negotiator_common.utils import GracefulShutdown

# External dependencies.
from executor import execute

# Semi-standard module versioning.
__version__ = '0.8.2'

# Initialize a logger for this module.
logger = logging.getLogger(__name__)


class HostDaemon(object):

    """The host daemon automatically manages a group of processes that handle "guest to host" calls."""

    def __init__(self, channel_directory=CHANNELS_DIRECTORY):
        """
        Initialize the host daemon.

        :param channel_directory: The pathname of the directory containing
                                  UNIX sockets connected to guests (a string).
        """
        self.active_channels = {}
        self.channel_directory = channel_directory
        self.enter_main_loop()

    def enter_main_loop(self):
        """Create and maintain active channels for all running guests."""
        with GracefulShutdown():
            try:
                while True:
                    self.update_active_channels()
                    time.sleep(10)
            finally:
                for channel in self.active_channels.values():
                    channel.terminate()

    def update_active_channels(self):
        """Automatically spawn subprocesses (workers) to maintain connections to all guests."""
        logger.debug("Checking for new/missing channels in %s ..", self.channel_directory)
        # Discover the available channels (by checking for UNIX socket files).
        available_channels = find_available_channels(self.channel_directory, GUEST_TO_HOST_CHANNEL_NAME).items()
        # Synchronize the set of active channels with the set of available channels.
        for key in set(self.active_channels) | set(available_channels):
            guest_name, unix_socket = key
            # Check if a previously spawned worker has died since the last update.
            if key in self.active_channels and not self.active_channels[key].is_alive():
                # Just remove the worker from the list of active channels, the
                # following code will start a new worker when it notices that
                # there is no worker associated with the channel anymore.
                logger.warning("Existing channel to guest %s has died, cleaning up ..", guest_name)
                self.active_channels.pop(key)
            # Create channels for available UNIX sockets that don't have a channel yet.
            if key in available_channels and key not in self.active_channels:
                logger.info("Initializing channel to guest %s (UNIX socket %s) ..", guest_name, unix_socket)
                channel = AutomaticGuestChannel(guest_name=guest_name, unix_socket=unix_socket)
                channel.start()
                self.active_channels[key] = channel
            # Destroy previously created channels whose UNIX socket has since disappeared.
            if key in self.active_channels and key not in available_channels:
                logger.info("Destroying channel to guest %s (UNIX socket %s) ..", guest_name, unix_socket)
                self.active_channels[key].terminate()
                self.active_channels.pop(key)


class AutomaticGuestChannel(multiprocessing.Process):

    """
    Thin wrapper for :py:class:`GuestChannel` that puts it in a separate process.

    Uses :py:class:`multiprocessing.Process` to isolate guest channels in
    separate processes.
    """

    def __init__(self, guest_name, unix_socket):
        """
        Initialize a :py:class:`GuestChannel` in a separate process.

        :param guest_name: The name of the guest to connect to (a string).
        :param unix_socket: The absolute pathname of the UNIX socket that we
                            should connect to (a string).
        """
        # Initialize the super class.
        super(AutomaticGuestChannel, self).__init__()
        # Store the arguments to the constructor.
        self.guest_name = guest_name
        self.unix_socket = unix_socket

    def run(self):
        """Start the main loop of the common negotiator interface."""
        try:
            # Initialize the guest to host channel.
            channel = GuestChannel(self.guest_name, self.unix_socket)
            # Wait for messages from the other side.
            channel.enter_main_loop()
        except GuestChannelInitializationError:
            # We know what the reason is here, so there's no need to log a noisy traceback.
            logger.error("Failed to initialize channel to guest %r! (worker will respawn in a bit)", self.guest_name)
        except Exception:
            # Unhandled exceptions get a traceback in the log output to make it easier to debug problems.
            logger.exception("Caught exception while connecting to guest %r! (worker will respawn in a bit)", self.guest_name)


class GuestChannel(NegotiatorInterface):

    """
    The host side of the channel connecting KVM/QEMU hosts and guests.

    See also :py:class:`AutomaticGuestChannel` which wraps
    :py:class:`GuestChannel` and puts it in its own process.
    """

    def __init__(self, guest_name, unix_socket=None):
        """
        Initialize a negotiator host agent.

        :param guest_name: The name of the guest to connect to (a string).
        :param unix_socket: The absolute pathname of the UNIX socket that we
                            should connect to (a string, optional).
        """
        self.guest_name = guest_name
        # Figure out the absolute pathname of the UNIX socket?
        if not unix_socket:
            unix_socket = os.path.join(CHANNELS_DIRECTORY, '%s.%s' % (self.guest_name, HOST_TO_GUEST_CHANNEL_NAME))
        # Connect to the UNIX socket.
        logger.debug("Opening UNIX socket: %s", unix_socket)
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            logger.debug("Connecting to UNIX socket: %s", unix_socket)
            self.socket.connect(unix_socket)
        except Exception:
            raise GuestChannelInitializationError("Guest refused connection attempt!")
        logger.debug("Successfully connected to UNIX socket!")
        # Initialize the super class, passing it a file like object connected
        # to the character device in read/write mode.
        super(GuestChannel, self).__init__(handle=self.socket.makefile(),
                                           label="UNIX socket %s" % unix_socket)

    def prepare_environment(self):
        """
        Prepare environment variables for command execution on KVM/QEMU hosts.

        The following environment variables are currently exposed to commands:

        ``$NEGOTIATOR_GUEST``
          The name of the KVM/QEMU guest that invoked the command.
        """
        os.environ['NEGOTIATOR_GUEST'] = self.guest_name


class GuestChannelInitializationError(Exception):

    """Exception raised by :py:class:`GuestChannel` when socket initialization fails."""


def find_available_channels(directory, name):
    """
    Find available channels by checking for available UNIX sockets.

    This uses :py:func:`find_running_guests()` to ignore UNIX sockets that are
    not connected to a running guest (since these sockets are useless until
    they become connected to a running guest).

    :param directory: The pathname of the directory to search (a string).
    :param name: The name of the channel to search for (a string).
    :returns: A dictionary with KVM/QEMU guest names (strings) as keys and
              pathnames of UNIX sockets as values.
    """
    channels = {}
    suffix = '.%s' % name
    running_guests = set(find_running_guests())
    for entry in os.listdir(directory):
        # Validate the filename suffix.
        if entry.endswith(suffix):
            pathname = os.path.join(directory, entry)
            # Make sure we're dealing with a UNIX socket.
            if stat.S_ISSOCK(os.stat(pathname).st_mode):
                guest_name = entry[:-len(suffix)]
                # Make sure the guest is available and running.
                if guest_name in running_guests:
                    channels[guest_name] = pathname
                else:
                    logger.debug("Ignoring UNIX socket %s (guest %r isn't running) ..", pathname, guest_name)
    return channels


def find_running_guests():
    """
    Find the names of the guests running on the current host.

    This function parses the output of the ``virsh list`` command instead of
    using the libvirt API because of two reasons:

    1. I'm under the impression that the libvirt API is still very much in flux
       and large changes are still being made, so it's not the most stable
       foundation for Negotiator to find running guests.

    2. The Python libvirt API needs to match the version of the libvirt API on
       the host system and there is AFAIK no obvious way to express this in the
       ``setup.py`` script of Negotiator.

    :returns: A generator of strings with guest names.
    """
    logger.debug("Discovering running guests using 'virsh list' command ..")
    output = execute('virsh --quiet list --all', capture=True, logger=logger)
    for line in output.splitlines():
        logger.debug("Parsing 'virsh list' output: %r", line)
        try:
            vm_id, vm_name, vm_status = line.split(None, 2)
            if vm_status == 'running':
                yield vm_name
        except Exception:
            logger.warning("Failed to parse 'virsh list' output! (%r)", line)
