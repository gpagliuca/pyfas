import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfas",
    version="0.4.0",
    author="Giuseppe Pagliuca",
    author_email="giuseppe.pagliuca@gmail.com",
    description="Toolbox for Flow Assurance engineers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpagliuca/pyfas.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
