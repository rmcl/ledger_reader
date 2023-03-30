import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ledger_reader",
    version="0.4",
    author="Russell McLoughlin",
    author_email="russ.mcl@gmail.com",
    description="A simple parser for hledger journal files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmcl/ledger_reader",
    packages=setuptools.find_packages(),
    entry_points={},
    install_requires=[
        'rply',
    ],
    extras_require={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
