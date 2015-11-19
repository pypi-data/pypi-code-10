from setuptools import setup
def readme(readme_name):
    with open(readme_name) as f:
        return f.read()
def main(readme_name):
    setup(name='neuro_athelets',
            version='0.11',
            description='python ml library for neuro eeg data',
            long_description=readme(readme_name),
            classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Scientific/Engineering :: Medical Science Apps.',
            'Topic :: Scientific/Engineering :: Visualization',
            ],
            url='http://github.com/leolincoln/neuro_athelets',
            author='Liu Liu',
            author_email='leoliu@u.northwestern.edu',
            license='MIT',
            packages=['neuro_athelets'],
            install_requires=[
            'funcsigs',
            'matplotlib',
            'mock',
            'nose',
            'numpy',
            'pandas',
            'pbr',
            'pyparsing',
            'python-dateutil',
            'pytz',
            'scikit-learn',
            'scipy',
            'six',
            'sklearn',
            'wheel',
            ],
            zip_safe=False)

if __name__ == '__main__':
    main('README.md')
