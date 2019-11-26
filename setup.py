from setuptools import setup, find_packages
from Cython.Build import cythonize


setup(
    name="release-the-gil",
    version="0.1",
    author="Bradlee Speice",
    author_email="bradlee@speice.io",
    description="Basic examples of parallelism in Python",
    url="https://github.com/speice-io/release-the-gil",
    packages=find_packages(),
    ext_modules=cythonize("src/*.pyx"),
    install_requires=[
        "Cython",
        "numba",
        "texttable"
    ],
)