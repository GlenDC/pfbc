from distutils.core import setup, Extension
import os

root = os.path.dirname(os.path.realpath(__file__))


def main():
    setup(name="nirvana",
          version="1.0.0",
          description="Python interface for primitive chips written in C, handed by God.",
          author="glendc",
          author_email="contact@glendc.com",
          ext_modules=[Extension("pfbc.hardware.nirvana", [f"{root}/src/primchips.c"])])


if __name__ == "__main__":
    main()
