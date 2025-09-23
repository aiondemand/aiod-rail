# OuterRail

An SDK for AI on Demand RAIL platform.

[![PyPI version](https://badge.fury.io/py/OuterRail.svg)](https://badge.fury.io/py/OuterRail)
[![Python Version](https://img.shields.io/pypi/pyversions/OuterRail.svg)](https://pypi.org/project/OuterRail/)
[![Downloads](https://pepy.tech/badge/OuterRail)](https://pepy.tech/project/OuterRail)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is RAIL

RAIL stands for: __Research and Innovation AI Lab__

RAIL is a tool that allows AI practitioners to explore and use AI assets
directly in the AI on Demand platform (AIoD). RAIL is developed within the
[AI4Europe project](https://www.ai4europe.eu) as one of the core services
of the [AI on Demand platform](https://aiod.eu).

## OuterRail organization

SDK provides two types of interfaces:

- __Instances__ - are classes that provide a way to work with individual instances of different parts of RAIL, e. g. individual templates, experiments, runs, datasets
- __Managers__ - contain operations that function on multiple instances, such as querying, counting,...
Special case that is also handled by managers is creation of new Instances.

## Installation

### Requirements
Python 3.11+

### pip install
The OuterRail package can simply be installed with pip via command:
```sh
pip install OuterRail
```
### Manual installation with wheel

## Usage

### Importing the package

You can import the SDK with:
```python
import OuterRail
```

## In code setup

### Importing the package
You can the entire SDK with:

```python
import OuterRail
```

Alternatively, you can import only needed parts with:

```python
from OuterRail import what_you_need
```

### Config and Logging in

For the SDK to work with underlying RAIL backend, you need to
specify the URL of the RAIL service. Additionally, most of the functionality
requires authentication, and therefore you need to be logged in to use this functionality. <br>
Logging in will require entering a device code on the provided URL, where afterwards you will be log in to the service
and give consent to resources needed by the SDK.

The code for this would look something like:

```python
import os
from OuterRail import Configuration

config = Configuration(host="https://rail.aiod.eu/api") # 1. Specify URL
config.login() # 2. Blocking function until log in or timeout
# ... your logic here ...
config.logout() # 3. After your code, logout
```

### Examples
For more examples, you can check out the following sources:
- [RAIL](https://rail.aiod.eu) - with example code for using the SDK
- [Official documentation](https://aiondemand.github.io/aiod-rail/)
- Docstrings in the SDK itself

## Author

This SDK was created at [KInIT](https://kinit.sk) by Jozef Barut.
