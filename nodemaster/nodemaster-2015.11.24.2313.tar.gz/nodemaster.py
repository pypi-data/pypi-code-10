#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# nodemaster                                                                   #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides node control utilities.                                #
#                                                                              #
# 2014 Will Breaden Madden, w.bm@cern.ch                                       #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

name    = "nodemaster"
version = "2015-11-24T2313Z"

import os

def launch_tmux(
    commands = None
    ):
    configuration =\
    """
    set -g set-remain-on-exit on
    new -s "nodemaster"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 5000
    ## mouse mode
    set -g mode-mouse on
    set -g mouse-select-pane on
    set -g mouse-select-window on
    set -g mouse-resize-pane on # resize panes with mouse (drag borders)
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    """
    for command in range(1, len(commands)):
        configuration += "\nsplit-window -v\nselect-layout even-vertical"
    for index, command in enumerate(commands):
        configuration += "\nselect-pane -t {index}".format(
            index = index
        )
        configuration += "\nsend-keys '{command}' Enter".format(
            command = command
        )
    configuration += "\nset -g set-remain-on-exit off"
    command = \
        "configurationtmux=\"$(mktemp)\" && { echo \"" +\
        configuration                                  +\
        "\" > \"${configurationtmux}\"; "              +\
        "tmux"                                         +\
        " -f \"${configurationtmux}\" attach; "        +\
        "unlink \"${configurationtmux}\"; }"
    os.system(command)
