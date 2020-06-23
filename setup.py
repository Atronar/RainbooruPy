from setuptools import setup
from setuptools import find_packages

setup(
  name = "RainbooruPy",
  description = "Python parser for Rainbooru",
  url = "https://github.com/Atronar/RainbooruPy",
  version = "0.0.1",
  author = "ATroN",
  author_email = "master.atron@gmail.com",
  platforms = ["any"],
  packages = find_packages(),
  python_requires='>=3.6',
  install_requires = ["requests","beautifulsoup4"],
  include_package_data = True,
  classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3"
  ]
)
