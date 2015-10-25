#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run kamer with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='kamer',
    version='4',
    url='https://pikacode.com/bart/kamer',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" KAMER - mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijk stoffen """,
    license='MIT',
    zip_safe=False,
    scripts=["bin/kamer",],
    install_requires=["meds"],
    packages=['kamer',
             ],
    long_description = """ 

############
TWEEDE KAMER
############

::


 Tweede Kamer der Staten-Generaal
 Postbus 20018
 2500 EA Den Haag



TWEEDE KAMER

Behandeling met antipsychotica is opzettelijke benadeling van de gezondheid gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen, om met die benadeling van de gezondheid te proberen de psychotische symptomen te verminderen.

kortom:

Antipsychotica brengen schade toe aan de hersenen in de hoop de psychotische symptomen te verminderen. De schade die men toebrengt is opzettelijk en daarmee is het mishandeling.

Een wet die daartoe verplicht en op die manier de mishandeling niet strafbaar maakt, maakt de behandeling nog niet een niet strafbaar feit. Er word nog steeds een strafbaar feit gepleegd, waar men schuldig aan is en wat men direct dient te stoppen. Men kan hoogstens niet strafbaar pleiten, niet het gedogen van het plegen van een strafbaar feit.

Het is de plicht van het Openbaar Ministerie om op te treden als er strafbare feiten worden gepleegd, ook als vervolging tot niet strafbaar leid, met als argument dat het plegen van strafbare feiten gestopt moet worden.

Met het aannemen van de Wet verplichte Geestelijke Gezondheidzorg maakt de Tweede Kamer de behandeling met antipsychotica verplicht en daarmee mishandeling gepleegd door het toedienen van voor het leven en de gezondheid schadelijke stoffen niet strafbaar.

De Tweede Kamer maakt zich hiermee schuldig aan het op grote schaal mogelijk maken van mishandeling.

Mishandeling van medicijnen is strafbaar in het Wetboek van Strafrecht:

* Artikel 300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

* Artikel 304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

Niet vervolgen van mishandeling met medicijnen is niet een optie. Niet vervolgen betekent dat men geen einde maakt aan de mishandeling.

U dient terstond het Openbaar Ministerie ontvankelijk te maken voor elke patient die zijn mishandeling door de strafrechter gestopt wil zien worden.

Mishandeling met medicijnen niet strafbaar maken is wat de WvGGZ doet. Niet strafbaar betekent dat het misdrijf wel gedaan word maar niet gestopt word.

Men is schuldig aan het misdrijf maar niet strafbaar. Het aannemen van de WvGGZ maakt dat u zich schuldig maakt aan het mogelijk maken van mishandeling door het niet strafbaar te maken.

                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
