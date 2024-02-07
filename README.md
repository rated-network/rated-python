# Rated Python
Python bindings for the Rated API

| |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD | [![CircleCI](https://dl.circleci.com/status-badge/img/circleci/Hqo3V5Mfcymy4YZBqYk79R/DefKjYr4Qh1krFnLci1Een/tree/main.svg?style=badge&circle-token=05448e79776505e8532c2a270d59bd9d23ebed72)](https://dl.circleci.com/status-badge/redirect/circleci/Hqo3V5Mfcymy4YZBqYk79R/DefKjYr4Qh1krFnLci1Een/tree/main)                                                                                                                                                                         |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/rated-python.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/rated-python/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/rated-python.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/rated-python/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rated-python.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/rated-python/) |
| Meta | [![Linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Types - Mypy](https://img.shields.io/badge/Types-MyPy-blue.svg)](https://github.com/python/mypy) [![License - CC-BY-SA-4.0](https://img.shields.io/badge/License-CC--BY--SA--4.0-9400d3.svg)](https://spdx.org/licenses/)                                                                                    |


## 🚀 Getting started
Install using `pip`:
```bash
pip install rated-python
```

## Requirements
* Python>=3.8
* A valid Rated API key [(Get your key)](https://www.rated.network/apis)

## Usage
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


