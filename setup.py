from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("D:/Users/vikto/Dropbox/Python/cython/zakras.pyx")
)
