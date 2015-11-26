from setuptools import setup
from go_overlap.version import __version__

setup(
    name = "goverlap",
    scripts = ["bin/goverlap"],
    packages = ["go_overlap", "go_overlap/compute_set_overlaps",
                "go_overlap/create_term_subtree_gene_matrix",
                "go_overlap/gene_to_terms", "go_overlap/go",
                "go_overlap/go_hierarchy", "go_overlap/prepare_input_lists",
                "go_overlap/statistics", "go_overlap/utils"],
    version = __version__,
    description = "Powerful ontology term enrichment analyzer for the command line",
    author = "Endre Bakken Stovner",
    author_email = "endrebak@stud.ntnu.no",
    url = "http://github.com/endrebak/goverlap",
    keywords = ["Gene Ontology", "Term enrichment"],
    license = ["MIT"],
    install_requires = ["pandas", "docopt", "godb>=0.0.5", "biomartian>=0.0.19",
                        "kg>=0.0.8", "ebs>=0.0.9"],
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries :: Python Modules"],
    long_description = ("Powerful ontology term enrichment analyzer for the command line. See the url for more info.")
)
