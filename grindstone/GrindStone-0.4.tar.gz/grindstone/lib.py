#!/usr/bin/env python
"""
File: lib.py
Package: grindstone
Author: Elijah Caine
Description:
    Utility functionality and classes for the grindstone package.
"""
import json
import os

def key_of(d):
    """
    Returns the key of a single element dict.
    """
    if len(d) > 1 and not type(d) == dict():
        raise ValueError('key_of(d) may only except single element dict')
    else:
        return keys_of(d)[0]


def keys_of(d):
    """
    Returns the keys of a dict.
    """
    try:
        return list(d.keys())
    except:
        raise ValueError('keys_of(d) must be passed a dict')


class GrindStone(object):
    """
    The GrindStone object.
    """
    def __init__(self, path=None):
        # Establish variables
        self.grindstone_filename = '.grindstone'
        if path is not None:
            self.path = os.path.abspath(path)+'/'
        else:
            raise ValueError('Path must not be None')

        self.grindstone_path = self.path + self.grindstone_filename
        # open the grindstone
        self.grindstone = self.open_grindstone()


    def open_grindstone(self):
        """
        Opens a grindstone file and populates the grindstone with it's
        contents.
        Returns an empty grindstone json object if a file does not exist.
        """
        try:
            with open(self.grindstone_path, 'r') as f:
                # Try opening the file
                return json.loads(f.read())
        # If the file is empty
        except json.decoder.JSONDecodeError:
            # Default return empty object with empty tasks list
            return {'tasks': []}
        # The file does not yet exist
        except FileNotFoundError:
            # Default return empty object with empty tasks list
            return {'tasks': []}


    def add_task(self, name=None, desc=None):
        """
        Adds object to list of grindstone['tasks'].
        """
        # A name is required to create a task
        for k in self.get_tasks():
            if name in keys_of(k):
                raise ValueError('Task already exists')

        if name is not None:
            # desc can be None, so we can just append whatever we have
            self.grindstone['tasks'].append( {name: desc} )
        else:
            # Raising errors is good, and makes tests easy.
            raise ValueError('Tasks `name` cannot be None')


    def delete_task(self, task=None):
        """
        Deletes a given task by name.
        """
        # Iterate over the list of tasks
        for t in self.grindstone['tasks']:
            # If they key of the task matches the task given
            if key_of(t) == task:
                # Remove that task
                self.grindstone['tasks'].remove(t)
                # Return True because something did happen
                return True
        # Return false because nothing happened
        return False


    def write_grindstone(self):
        """
        Writes self.gs to self.grindstone_path.
        """
        with open(self.grindstone_path, 'w') as f:
            # Write the JSON dump of the file
            f.write(json.dumps(self.grindstone))


    def get_task(self, task=None):
        """
        Returns a (task, description) tuple for a given task
        """
        # Iterate over the grindstone tasks
        for t in self.grindstone['tasks']:
            # if they key matches the task
            if key_of(t) == task:
                # Return this task
                return t
        # Otherwise return nothing
        return None


    def get_tasks(self, task=None):
        """
        Returns all tasks in the grinstone
        """
        return self.grindstone['tasks']
