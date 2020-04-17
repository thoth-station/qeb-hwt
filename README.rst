# Qeb-Hwt

This is the implementation of https://github.com/apps/qeb-hwt.

![Thoth Health](https://img.shields.io/badge/Thoth:%20Health-3.5-brightgreen "Thoth Health")

Let Bots, powered with AI and continuously learning to increase its knowledge, manage your dependencies.


Installation
=============

Installing a Qeb-Hwt GitHub App in your organization.

1. Go to GitHub Marketplace

![GitHubMarketPlace](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/GitHubMarketplace.png)

2. Browse for `Qeb-Hwt` app or you can click on dependency management category and look for it.

![QebHwyGitHubApp](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/QebHwyGitHubApp.png)

![DependencyManagementCategory](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/DependencyManagementCategory.png)

![DependencyManagementQebHwt](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/DependencyManagementQebHwt.png)

3. Click on the set up plan (The App is Open Source and therefore Free) and you will be redirected to `install it for free` button.

![SetupPlan](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/SetupPlan.png)

![FreeApp](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/FreeApp.png)

4. Install and Authorize Qeb-Hwt for your organization/repositories (you can choose which repositores the app has access to).

![SelectRepos](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/SelectRepos.png)

![InstallApp](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/InstallApp.png)

Done!! You should see the following page if everything is successfull.

![SuccessfullyInstalledApp](https://raw.githubusercontent.com/thoth-station/Qeb-Hwt/master/docs/images/SuccessfullyInstalledApp.png)

Long Live Bots!


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
      python_version: '{python_version}'
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
| `python_version`       | Python version (major.minor)   |  3.6     |
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
