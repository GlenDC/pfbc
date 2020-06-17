import os
from distutils.core import setup, Extension


with open("../README.md", "r") as fh:
    long_description = fh.read()


root = os.path.dirname(os.path.realpath(__file__))

setup(
    name="pfbc",
    version="0.1.0",
    author="Glen De Cauwsemaecker",
    author_email="contact@glendc.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glendc/pfbc",
    packages=[
        'pfbc',
        'pfbc.hardware',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    ext_modules=[Extension("pfbc.hardware.nirvana", [f"{root}/nirvana/primchips.c"])],
)
