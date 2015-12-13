#!/usr/bin/env python
import os, json
from yaccli.lib.config import get_config_path

def create_stack():

	std_stack_path = os.path.join(get_config_path(),'yac-stack.json')

	file_found = os.path.exists(std_stack_path)

	print "loading stack def from %s. file exists? %s"%(std_stack_path,file_found)

	return "stack print complete"