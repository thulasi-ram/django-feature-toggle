======
Usage:
======

Toggle is the class that should be used in the code.
for ex: 
  

.. sourcecode:: python

    
    
    from feature_toggle.toggle import Toggle
    tgl = Toggle(environment=environment, name='test', code='test1')


Now you can use this ``tgl`` any where even as dependency injection.

``name`` can be descriptive.

``code`` is only capital A-Z and underscore is allowed.

``name`` and ``code`` are optional but any one of them is mandatory. Getting a toggle by ``code`` is encouraged.
for ex:

.. sourcecode:: python

    Toggle(environment=environment, code='test1')

By defaulting initializing a non exisiting will raise custom Exception: FeatureToggleDoesNotExist. To suppress it you can send ``raise_does_not_exist`` while initialization

.. sourcecode:: python

    tgl = Toggle(environment=environment, code='test1', raise_does_not_exist=False)

This will create a toggle run time and will let you do your work. But if you want to persist your toggle you can use ``tgl.create()``.


Models:
========

``FeatureToggle`` - The actual class where the toggles are stored.

``FeatureToggleAttribute`` - All the attributes for a particular feature toggle can be put here. For ex: ``start_date`` and ``end_date.``

These can be set through the admin panel under the FeatureToggle section

Basic methods:
==============
``tgl.is_active()``: Checks the active status of a toggle

``tgl.is_enabled()``: Checks the active status and validation if any of start_date and end_date are present in the attributes.

All the other attributes set in the FeatureToggleAttribute model can be accessed directly via ``tgl.<attribute name>``

for ex: if start_date is set in FeatureToggleAttribute. it can be accessed as ``tgl.start_date.``

Custom Toggles:
===============

You can always extend the ``Toggle`` class to suit your business logic. And you can use the services provided in ``FeatureToggleService`` (in ``feature_toggle.services``) for flexibility.

The contract is bound to an interface ``BaseToggle`` (in ``feature_toggle.toggle_base``). If you need to implement a barebone toggle, that should be a subclass of this toggle.


Custom Environments:
====================

If you feel the default environments are not suitable to you. Please set a choice tuple for ``FEATURE_TOGGLE_CUSTOM_ENV_CHOICES`` in settings.

Note that this custom choices will be appended to the default choices. If incase you want to have only your custom choices, set ``FEATURE_TOGGLE_DEFAULT_ENV_CHOICES=()`` in your settings.

Services will make an assertion for valid environments.


Custom Attributes:
====================

Same as Environments if you need more attributes you should set ``FEATURE_TOGGLE_CUSTOM_ATTR_CHOICES`` in settings.

Note that this custom choices will be appended to the default choices. If incase you want to have only your custom choices, set ``FEATURE_TOGGLE_DEFAULT_ATTR_CHOICES=()`` in your settings.

There is no assertion for now in attributes since the only way to add them is through admin. Overriding the default will affect the admin and new choices will be shown.