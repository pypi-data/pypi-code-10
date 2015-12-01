from .checkmod import CheckMod
import git as _git


def vcheck(mod, hexsha=None, version=None):
    try:
        cmod = CheckMod(mod)
    except _git.InvalidGitRepositoryError:
        raise NotImplemented('Only works for Git repositories.')

    if hexsha is not None and version is not None:
        raise ValueError('Only specify either hexsha ({}) or version({})'.format(hexsha, version))
    elif hexsha is None and version is None:
        raise ValueError('Neither hexsha nor version specified')
    elif hexsha is not None:
        if cmod.repo.head.object.hexsha == hexsha:
            return True
        else:
            return False
    elif version is not None:
        if cmod.repo.is_dirty():
            raise VersionError('Repo for module {} is dirty, version not well-defined.'.format(cmod.mainmod.__name__))

        for _tag in cmod.repo.tags:
            if cmod.hexsha == _tag.object.hexsha:
                if version == _tag.name:
                    return True

        raise VersionError('Repo for module {} does not match a released version.'.format(cmod.mainmod.__name__))


class VersionError(Exception):
    pass
