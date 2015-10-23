from distutils.core import setup

if __name__ == '__main__':
	import sys

	exec(compile(open("groupdocs/version.py").read(), "groupdocs/version.py", 'exec'))
	
	setup(
		name = __pkgname__,
		version = __version__,
		author = "GroupDocs Team",
		author_email = "support@groupdocs.com",
		description = "GroupDocs Cloud SDK for Python3",
		keywords = "groupdocs, viewer, html viewer, document viewer, annotation, document annotation, image annotation, pdf annotation, document assembly, e-signature, electronic signature, comparison, document comparison, conversion, document conversion, pdf, word, excel, powerpoint, html, cad, tiff",
		license = "Apache License (2.0)",
		long_description = open('README.rst').read(),
		platforms = 'any',
		packages = ['groupdocs', 'groupdocs.models'],
		url = "http://groupdocs.com/",
		download_url = "https://github.com/groupdocs/groupdocs-python3",
		classifiers = [
			"Development Status :: 4 - Beta",
			"Intended Audience :: Developers",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"License :: OSI Approved :: Apache Software License"
		],
		data_files=[('', ['README.rst'])]
	)
