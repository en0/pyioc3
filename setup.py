from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pyioc3",
    version="1.0",
    description="Python IOC Container",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Laird",
    author_email="irlaird@gmail.com",
    url="https://github.com/en0/pyioc",
    packages=["pyioc3"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
