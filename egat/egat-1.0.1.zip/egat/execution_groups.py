def execution_group(id):
    """A decorator designed to be used with both classes and functions. Pass the 
    decorator some object that represents the Execution Group the decorated object 
    should be added to. If one test function in an Execution Group fails then no
    more tests from that Execution Group will run."""
    def add_execution_group(class_or_func):
        execution_groups = getattr(class_or_func, 'execution_groups', [])
        execution_groups.append(id)
        class_or_func.execution_groups = execution_groups
        return class_or_func
    return add_execution_group

