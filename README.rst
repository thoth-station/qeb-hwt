# Qeb-Hwt

This is the implementation of https://github.com/apps/qeb-hwt.

Let Bots, powered with AI and continuously learning to increase its knowledge, manage your dependencies.

Installation
============

To install Qeb-HWt App, please refer to the following `link <https://github.com/thoth-station/Qeb-Hwt/blob/master/docs/INSTALLATION.md>`__. 

Usage
======

Qeb-Hwt is one of the integration of `Thamos CLI <https://github.com/thoth-station/adviser/blob/master/docs/source/integration.rst>`__. 
Internally, it relies on `Thamos CLI <https://github.com/thoth-station/thamos/>`__
and on actual `Thoth Adviser <https://github.com/thoth-station/adviser/>`__, core component that provides reccomendations.

You need to provide your own custom configuration file as a template called `.thoth.yaml`. 

An example of configuration file template can be:

.. code-block:: console

    host: {THOTH_SERVICE_HOST}
    tls_verify: true
    requirements_format: pipenv

    runtime_environments:
    - name: '{os_name}:{os_version}'
      operating_system:
        name: {os_name}
        version: '{os_version}'
      hardware:
        cpu_family: {cpu_family}
        cpu_model: {cpu_model}
      python_version: '{python_version}'
      cuda_version: {cuda_version}
      recommendation_type: stable

Listing of automatically expanded configuration options which are supplied the
config sub-command (these options are optional and will be expanded based on HW
or SW discovery):

+------------------------+--------------------------------+----------+
| Configuration option   | Explanation                    | Example  |
+========================+================================+==========+
| `os_name`              | name of operating system       | fedora   |
+------------------------+--------------------------------+----------+
| `os_version`           | version of operating system    |  30      |
+------------------------+--------------------------------+----------+
| `cpu_family`           | CPU family identifier          |  6       |
+------------------------+--------------------------------+----------+
| `cpu_model`            | CPU model identifier           |  94      |
+------------------------+--------------------------------+----------+
| `python_version`       | Python version (major.minor)   |  3.6     |
+------------------------+--------------------------------+----------+
| `cuda_version`         | CUDA version (major.minor)     |  9.0     |
+------------------------+--------------------------------+----------+

These configuration options are optional and can be mixed with adjustment based
on environment variables (see ``THOTH_SERVICE_HOST`` example above). Note the
environment variables are not expanded on `thamos config` call but rather on
other sub-commands issued (e.g. ``thamos advise`` or others).

The output format coming out of recommendations can be compatible with
`Pipenv <https://pipenv.kennethreitz.org/en/latest/>`__,
`raw pip <https://pip.pypa.io/en/stable/user_guide/>`__  or similar to the one
provided by `pip-tools <https://pypi.org/project/pip-tools/>`__ (actually same as for
``pip`` as these formats are interchangeable). The format is configured using
``requirements_format`` configuration option, available options are:

* ``requirements_format: pipenv`` for `Pipenv <https://pipenv.kennethreitz.org/en/latest/>`__ compatible output.
Remember you need to have ``Pipfile`` in your directory in this case.
* ``requirements_format: pip`` or ``requirements_format: pip-tools`` for `pip <https://pip.pypa.io/en/stable/user_guide/>`__ or `pip-tools <https://pypi.org/project/pip-tools/>`__ compatible output.
Remember you need to have ``requirements.txt`` or ``requirements.in`` in your directory in this case.

An example of configuration:

.. code-block:: console

    host: khemenu.thoth-station.ninja
    tls_verify: false
    requirements_format: pipenv

    runtime_environments:
    - name: rhel:8
      operating_system:
        name: rhel
        version: "8"
      python_version: "3.6"
      recommendation_type: latest
