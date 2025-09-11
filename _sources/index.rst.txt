Intro
#############

Welcome to the documentation of Outer RAIL SDK.

Contents of this landing page.

.. contents::
   :local:
   :depth: 2


What is RAIL
------------

RAIL stands for: **Research and Innovation AI Lab**

RAIL is a tool that allows AI practitioners to explore and use AI assets
directly in the AI on Demand platform (AIoD). RAIL is developed within the
`AI4Europe project <https://www.ai4europe.eu>`_ as one of the core services
of the `AI on Demand platform <https://aiod.eu>`_.

OuterRail organization
----------------------------

SDK provides two types of interfaces:

#. :ref:`Instances <instances>` - are classes that provide a way to work with individual instances of different
   parts of RAIL, e. g. individual templates, experiments, runs, datasets
#. :ref:`Managers <managers>` - contain operations that function on multiple instances, such as querying, counting,...
   Special case that is also handled by managers is creation of new Instances.

Links associated with the SDK
-----------------------------

* `AIoD platform <https://www.ai4europe.eu>`_
* `RAIL platform <https://rail.aiod.i3a.es/docs/about>`_
* `Github Repository <https://github.com/aiondemand/aiod-rail/tree/feature/outer-sdk/sdk-py>`_
* `Github Issues <https://github.com/aiondemand/aiod-rail/issues>`_ (**If you find any problems or bugs in the SDK please fill a github issue in the RAIL repository. For any reported issues we thank you in advance.**)

Installation
------------

Requirements
^^^^^^^^^^^^

`Python 3.9+`

PIP
^^^

The OuterRail package can simply be installed with pip via command:

.. code-block:: console

   pip install OuterRail

Manually with wheel
^^^^^^^^^^^^^^^^^^^
**To Be Determined**

In code setup
----------------------------------

Importing the package
^^^^^^^^^^^^^^^^^^^^^

You can import the entire SDK with:

.. code-block:: python

   import OuterRail

Alternatively you can import only needed parts with:

.. code-block:: python

   from OuterRail import what_you_need

Config and Logging in
^^^^^^^^^^^^^^^^^^

For the SDK to work with underlying RAIL backend, you need to
specify the URL of the RAIL service. Additionally, most of the functionality
requires authentication and therefore you need to be logged in to use this functionality.

The code for this would look something like:

.. code-block:: python
   :linenos:

   import os
   from OuterRail import Configuration

   config = Configuration(host="https://rail.aiod.eu/api/docs") # 1. Specify URL
   config.login(username="username", password="password") # 2. Log in
   ... your logic here ...
   config.logout() # 3. After your code, logout

Important considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
   It is at the moment only possible to register via google account or similar identity provider method.
   As such, you will need to get access to username and password from personal request to support of the authentication
   providers. Unfortunately, the proper channels for this are not yet in place.

.. note::
   Successfully created template will need to be approved by an administrator and afterward built as
   a docker container by the backend service. Only after these operations are done can it be used to
   make new experiments.

.. note::
   To create an experiment successfully, the template it is based on needs to be approved and built as a docker
   container.


Reference Table
----------------

.. toctree::
   :maxdepth: 2

   self
   configuration
   managers
   instances
