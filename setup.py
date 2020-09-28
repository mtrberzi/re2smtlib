import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="re2smtlib",
    version="0.0.1",
    author="Murphy Berzish",
    author_email="mtrberzi@uwaterloo.ca",
    description="Regular expression to SMT-LIB translator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtrberzi/re2smtlib",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3.6'
)
