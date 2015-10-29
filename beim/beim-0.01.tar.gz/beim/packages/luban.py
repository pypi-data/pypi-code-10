name = 'luban'
deps = 'pythia',
reponame = 'luban'
branch = "trunk"


from beim.package import repoutils
repo = repoutils.svn.getPackageRepository(reponame, branch, name=name)
