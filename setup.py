import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


with open("README.md", "r") as fh:
    long_description = fh.read()


root = os.path.dirname(os.path.realpath(__file__))


class InstallLocalPackage(install):
    def run(self):
        install.run(self)
        subprocess.call(
            f"python {root}/pfbc/hardware/chips/nirvana/setup.py install", shell=True
        )


setup(
    name="pfbc",
    version="0.1.0",
    author="Glen De Cauwsemaecker",
    author_email="contact@glendc.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glendc/pfbc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': InstallLocalPackage,
    },
)
