from .swap import BaseClass

from .utils import is_base_model


def dependency_exists(dependency):
    """
    validates that the provided dependency is legitimate.
    """
    applied_migrations = get_applied_migrations()
    return bool(dependency in applied_migrations)


def get_model_dependency(cls):
    """
    Retrieves the South Migration dependency for a given Model
    """
    if is_base_model(cls):
        return None
    initial_migration = '0001_initial.py'
    dependency = (cls._meta.app_label, initial_migration)
    return dependency


def get_default_dependency():
    return get_model_dependency(BaseClass)
