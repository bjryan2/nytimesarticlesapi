from distutils.core import setup

setup(
    name='nytimesarticleapi',
    version='0.1.0',
    author='Brendan Ryan',
    author_email='ryan.brendanjohn@gmail.com',
    py_modules=['nytimesarticleapi'],
    url='http://github.com/bjryan2/nytimesarticleapi',
    description='A python wrapper for the NYTimes articles api',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.1.0",
    ],
)
