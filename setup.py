from setuptools import setup
from setuptools import find_packages
import kishinami

requires = ['naganami-mqtt==0.0.4', 'blinkt']

setup(
    name = "kishinami",
    version = kishinami.__version__,
    install_requires = requires,
    author = 'Himura Asahi',
    author_email = 'himura@nitolab.com',
    packages = find_packages(),
    description = "kishinami",
    url = "https://github.com/nc30/kishinami"
)
