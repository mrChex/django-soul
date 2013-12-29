from distutils.core import setup

INSTALL_REQUIRES = [
    "django >= 1.6.1",
]

setup(
    name='django-soul',
    version='0.3dev',
    packages=['soul',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),

    install_requires = INSTALL_REQUIRES,
)