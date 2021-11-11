==============
Feature Toggle
==============

Feature Toggle is a simple Django app based on the behavioural pattern `Feature Toggle <https://martinfowler.com/articles/feature-toggles.html>`_ proposed by Martin Fowler.

Quick links
===========
    PyPi: `https://pypi.org/project/django-feature-toggle/ <https://pypi.org/project/django-feature-toggle/>`_


    Source: `https://github.com/thulasi-ram/django-feature-toggle <https://github.com/thulasi-ram/django-feature-toggle>`_


    Docs: `https://django-feature-toggle.readthedocs.io/en/latest/ <https://django-feature-toggle.readthedocs.io/en/latest/>`_



Quick start
===========
1. Install the package ``pip install django-feature-toggle``

2. Add "feature_toggle" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'feature_toggle',
    ]

3. Run ``python manage.py migrate`` to create the models required feature_toggle.

4. Start your app to use the feature_toggle.


Quick Setup
===========

For people intrested in contributing:

1. Make a virtual environment
2. run ``python setup.py install`` or ``python3 setup.py install``
3. run ``pip install -r requirements.txt`` or ``pip3 install -r requirements.txt``
4. Make your changes and run tests by doing steps ``5`` and ``6``
5. ``git checkout py2_django_app`` and run ``python manage.py test`` make sure you have python 2 in your environment
6. ``git checkout py3_django_app`` and run ``python3 manage.py test`` make sure you have python 3 in your environment
7. ``5`` and ``6`` will be mitigated in the near future by tox or by using travis.


Generating Docs
===============
Handled by: https://readthedocs.org/projects/django-feature-toggle


Legacy
1. cd to ``docs\``
2. run ``make custom-gh-pages``
3. The current state of docs is a mix of ``gh-pages`` and ``wiki``
4. Docs are generated using sphinx. Generates files read from ``index.rst`` to ``_build`` directory.
5. ``make custom-gh-pages`` custom command copies ``_build`` to ``gh-pages`` directory and commits it which is used by github docs.
