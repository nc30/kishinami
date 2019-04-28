from setuptools import setup

requires = ['naganami-mqtt', 'blinkt']

setup(
    name = "kishinami",
    version = '0.0.0',
    install_requires = requires,
    author = 'Himura Asahi',
    author_email = 'himura@nitolab.com',
    packages = ["kishinami"],
    description = "kishinami",
    url = "https://github.com/nc30/kishinami"
)
