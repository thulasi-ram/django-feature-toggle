=====
Feature Toggle
=====

Feature Toggle is a simple Django app based on the pattern proposed by Martin Fowler
Detailed documentation is in https://thulasi-ram.github.io/django-feature-toggle.

Quick start
-----------
1. Install the package `pip install django-feature-toggle`

2. Add "feature_toggle" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'feature_toggle',
    ]

3. Run `python manage.py migrate` to create the models required feature_toggle.

4. Start you app to use the feature_toggle