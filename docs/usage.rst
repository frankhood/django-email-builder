=====
Usage
=====

To use Django Email Builder in a project, add it to your `INSTALLED_APPS`:

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
