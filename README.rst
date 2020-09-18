=============================
Django Email Builder
=============================

.. image:: https://badge.fury.io/py/django-email-builder.svg
    :target: https://badge.fury.io/py/django-email-builder

.. image:: https://travis-ci.org/frankhood/django-email-builder.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-email-builder

.. image:: https://codecov.io/gh/frankhood/django-email-builder/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-email-builder

Forget the boring customization of email templates! With our package,
you will disrupt the way how to tailor email through Django Admin!

Documentation
-------------

The full documentation is at https://django-email-builder.readthedocs.io.

Quickstart
----------

Install Django Email Builder:

::

    pip install django-email-builder

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'email_builder',
        ...
    )

Run migrations:
_______________

::

    python manage.py migrate email_builder


Add Django Email Builder's URL patterns:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^', include("email_builder.api.urls")),
        ...
    ]


Add template choices into yours  `settings.py`:

.. code-block:: python

    EMAIL_BUILDER_DEFAULT_LIBS_LOADED = [
        "i18n",
        "static",
    ]

    EMAIL_BUILDER_CODE_<YOUR_TEMPLATE_NAME> = "<your_template_name>_template"

    EMAIL_BUILDER_CODE_CHOICES = [
        (EMAIL_BUILDER_CODE_<YOUR_TEMPLATE_NAME>, "<Your Template Name> Template"),
    ]

    EMAIL_BUILDER_CONTEXT_HANDLER_PATH = (
        "<your.controller.path>.ExampleMailBuilderContextHandler"
    )


Create the project handler to add your own variables overriding `MailBuilderContextHandler` in `controllers.py` :

.. code-block:: python

    class ExampleMailBuilderContextHandler(MailBuilderContextHandler):
        @classmethod
        def get_available_variables(cls, email_code=None):
            # You can use factories to fill the fake value that will rendered in mail template preview
            factory = <YourModel>Factory.stub()

            variables = {
                settings.EMAIL_BUILDER_CODE_<YOUR_TEMPLATE_NAME>: {
                    "available_variables": {
                        "<your_model_field>": {"label": "Question Pub Date", "fake_value": factory.<your_model_field>},
                    }
                },
            }
            return variables


You can change base mail template adding into yours `settings.py`:

.. code-block:: python

    # for txt rendered mail
    BASE_MAIL_TXT_PATH = "email_templates/base_mail.txt"
    # for html rendered mail
    BASE_MAIL_HTML_PATH = "email_templates/base_mail.html"


Features
--------

* Use customized and ui based django variables into your mail template
* Add your own templatetags into mail template
* See simultaneously what will be displayed in the sent email


Running Tests
-------------

Does the code actually work? discover it with our docker!
It will run your tests with python3.6, python3.7, python3.8

::

    $ docker-compose up tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/frankhood/django-email-builder/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

• Add support for multilanguage with parler

• Add in the html and text editor the ability to select the base_mail

• Add in the html and text editor the ability to override a block content inherited by base_mail

• Add a js control to modify the loaded libraries if a templatetag or a filter is used in the templates

• Add Select2 to select multiple template_tags

• Increase configuration performance of available variables for every email template

• EmailTemplateBlock Inline multilanguage

Write Documentation
~~~~~~~~~~~~~~~~~~~

Django Email Builder could always use more documentation, whether as part of the
official Django Email Builder docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/frankhood/django-email-builder/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `django-email-builder` for local development.

1. Fork the `django-email-builder` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:frankhood/django-email-builder.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ cd django-email-builder/
    $ mkvirtualenv django-email-builder
    $ pip install -r requirements_dev.txt

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ docker-compose up tox

   To run all tests with Python:3.6, Python:3.7, Python:3.8.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, and 3.3, and for PyPy. Check
   https://travis-ci.org/frankhood/django-email-builder/pull_requests
   and make sure that the tests pass for all supported Python versions.


=======
Credits
=======

Development Lead
----------------

* Frankhood Business Solutions s.r.l <info@frankhood.it>
* https://frankhood.it/

Contributors
------------

* d.ria@frankhood.it
* g.donghia@frankhood.it


Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
