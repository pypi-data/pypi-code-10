from setuptools import setup

setup(
    name="pygments-lexer-pseudocode",
    packages=["pygments_lexer_pseudocode"],
    version="2.0.1",
    description="Pygments Lexer for a french pseudocode",
    author="Simon Wachter",
    author_email="simon@wachter.me",
    url="https://github.com/svvac/pseudocode-pygments-lexer",
    license="MIT",
    entry_points="[pygments.lexers]\npseudocodelexer = pygments_lexer_pseudocode:PseudocodeLexer",
    install_requires=[ "pygments" ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ]
)
