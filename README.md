# Rated API Python SDK
Python bindings for the Rated API

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![CircleCI](https://dl.circleci.com/status-badge/img/circleci/Hqo3V5Mfcymy4YZBqYk79R/DefKjYr4Qh1krFnLci1Een/tree/main.svg?style=badge&circle-token=05448e79776505e8532c2a270d59bd9d23ebed72)](https://dl.circleci.com/status-badge/redirect/circleci/Hqo3V5Mfcymy4YZBqYk79R/DefKjYr4Qh1krFnLci1Een/tree/main)                                                                                                                                                                         |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/rated-python.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/rated-python/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/rated-python.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/rated-python/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rated-python.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/rated-python/) |
| Meta    | [![Linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Types - Mypy](https://img.shields.io/badge/Types-MyPy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/License-MIT-9400d3.svg)](https://spdx.org/licenses/MIT.html)                                                                                                 |

## 👋 Introduction
The Rated SDK (Software Development Kit) for Python, which allows Python developers to write software that makes use of the Rated dataset. You can find the latest, most up to date, documentation at our docs site.

The Rated SDK is maintained and published by Rated Labs.

We’ve curated many examples which will help you kickstart your integration but to get a full list of all available endpoints, you are recommended to check out our API Reference and Swagger. 

## 🛟 Getting Help / Links
* [Documentation](https://docs.rated.network)
* [API Reference](https://api-docs.rated.network)
* [Feedback](https://feedback.rated.network)
* [Discord](https://discord.gg/hyCd8uDEXf)
* [Twitter](https://twitter.com/ratedw3b)

We use GitHub issues for tracking bugs and feature requests and have limited bandwidth to address them. 

Please use these community resources for getting help:
* Ask a question on our feedback board
* If it turns out that you may have found a bug, please open an issue



## 🚀 Getting started
### Requirements
* Python>=3.8
* A valid Rated API key [(Get your key)](https://www.rated.network/apis)

### Installation
Install using `pip`:
```bash
pip install rated-python
```

### Usage
**Example:** how to get a validator effectiveness rating by pubkey

```python
from rated import Rated
from rated.ethereum import MAINNET

RATED_KEY = "ey..."
r = Rated(RATED_KEY)
eth = r.ethereum(network=MAINNET)
for eff in eth.validator.effectiveness("0x123456789...", from_day=873, size=1): 
    print(f"Day: {eff.day}, Eff: {eff.validator_effectiveness}")

>>> Day: 873, Eff: 98.82005899705014
```

### Running tests
First install tox
```bash
pip install tox
```
Once tox has been installed you can run all tests:
```bash
tox
```

## 🤝 Contributing
We value feedback and contributions from our community. Whether it's a bug report, new feature, correction, or additional documentation, we welcome your issues and pull requests. 

Please read through this [CONTRIBUTING](CONTRIBUTING.md) document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your contribution.
