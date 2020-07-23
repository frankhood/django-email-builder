=============================
Django Email Builder
=============================

.. image:: https://badge.fury.io/py/django-email-builder.svg
    :target: https://badge.fury.io/py/django-email-builder

.. image:: https://travis-ci.org/frankhood/django-email-builder.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-email-builder

.. image:: https://codecov.io/gh/frankhood/django-email-builder/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-email-builder

Useful 

Documentation
-------------

The full documentation is at https://django-email-builder.readthedocs.io.

Quickstart
----------

Install Django Email Builder::

    pip install django-email-builder

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'email_builder.apps.EmailBuilderConfig',
        ...
    )

Add Django Email Builder's URL patterns:

.. code-block:: python

    from email_builder import urls as email_builder_urls


    urlpatterns = [
        ...
        url(r'^', include(email_builder_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
