import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'requests',
    'six'
    ]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

setup(name='pyramid_urireferencer',
      version='0.6.0',
      description='A pyramid plugin to handle referencing external URIs.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
        ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='https://github.com/OnroerendErfgoed/pyramid_urireferencer',
      keywords='web wsgi pyramid uri REST references',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramid_urireferencer',
      install_requires=requires,
      )
