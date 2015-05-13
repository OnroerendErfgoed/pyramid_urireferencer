pyramid_urireferencer
=====================

This plugin for pyramid helps in handling references to resources in other
applications by allowing querying on references to certain URI's.


.. image:: https://travis-ci.org/OnroerendErfgoed/pyramid_urireferencer.png?branch=master
        :target: https://travis-ci.org/OnroerendErfgoed/pyramid_urireferencer
.. image:: https://coveralls.io/repos/OnroerendErfgoed/pyramid_urireferencer/badge.png?branch=master
        :target: https://coveralls.io/r/OnroerendErfgoed/pyramid_urireferencer

.. image:: https://readthedocs.org/projects/pyramid_urireferencer/badge/?version=latest
        :target: https://readthedocs.org/projects/pyramid_urireferencer/?badge=latest
.. image:: https://badge.fury.io/py/pyramid_urireferencer.png
        :target: http://badge.fury.io/py/pyramid_urireferencer

Building the docs
-----------------

More information about this library can be found in `docs`. The docs can be
built using `Sphinx <http://sphinx-doc.org>`_.

Please make sure you have installed Sphinx in the same environment where
pyramid_urireferencer is present.

.. code-block:: bash

    # activate your virtual env
    $ pip install -r requirements-dev.txt
    $ python setup.py develop
    $ cd docs
    $ make html
