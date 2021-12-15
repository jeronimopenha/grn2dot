import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grn2dot",
    version="0.1.0",
    author="Jeronimo Costa Penha",
    author_email="jeronimopenha@gmail.com",
    description="A small conversor for gnr format to networkx graphs and dot language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeronimopenha/grn2dot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
