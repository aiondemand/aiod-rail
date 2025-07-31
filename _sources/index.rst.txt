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

#. Instances - Classes that provide a way to work with individual instances of different
   parts of RAIL, e. g. individual templates, experiments, runs, datasets
#. Managers - Contain operations that function on multiple instances, such as querying, counting,...
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

In code setup
----------------------------------

Importing the package
^^^^^^^^^^^^^^^^^^^^^

You can the entire SDK with:

.. code-block:: python

   import OuterRail

Alternatively you can import only needed parts with:

.. code-block:: python

   from OuterRail import what_you_need

Configuration
^^^^^^^^^^^^^^^^^^

For the SDK to work with underlying RAIL backend, you need to
specify the URL of the RAIL as well as your API key.
The code for this would look something like:

.. code-block:: python
   :linenos:

   import os
   from OuterRail import Configuration

   os.environ["AIOD_RAIL_API_KEY"] = "your_api_key"
   config = Configuration(host="http://localhost:8000")


Reference Table
----------------

.. toctree::
   :maxdepth: 2

   self
   configuration
   managers
   instances
