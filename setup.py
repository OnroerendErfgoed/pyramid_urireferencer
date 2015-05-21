import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'requests'
    ]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

setup(name='pyramid_urireferencer',
      version='0.1.0',
      description='A pyramid plugin to handle referencing external URIs.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='http://pyramid_urireferencer.readthedocs.org',
      keywords='web wsgi pyramid uri REST references',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramid_urireferencer',
      install_requires=requires,
      )
