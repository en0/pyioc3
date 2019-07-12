# pyioc3

A fast and simple IOC Container for Python.

# About

pyioc3 is a fast and simple inversion of control (ioc) container
for python.  An IoC container uses class constructor (or in this case
__init__ method parameters) to build and inject dependencies. pyioc3 
takes advantage of python's type hint annotations to make injection
flexible and easy to use.

# Motivation

I Love python. I also love OOP.  I wanted better OOP in python. So i built
this to help enforce SOLID and make my programs better.

# Goals

Simple. Simple. Simple. Python is already flexible. An IOC container
is something that you could whip up to suite your needs in an
afternoon. Or you could install pyioc3 instead.

# Quick Start

Install the package

```bash
pip install --user pyioc3
```

Make an ioc.py

```python
from pyioc3 import StaticContainerBuilder
from .ducks import Duck, RubberDucky
from .quacks import QuackBehavior, Squeak

ioc_builder = StaticContainerBuilder()

ioc_builder.bind(
    annotation=QuackBehavior,
    implementation=Squeak)
ioc_builder.bind(
    annotation=Duck,
    implementation=RubberDucky)
    
ioc = ioc_builder.build()
__all__ = ["ioc"];
```

Use the container

```python
from ioc import ioc
from .ducks import Duck

duck: Duck = ioc.get(Duck)
duck.quack()
```

# What More
- Look at the examples.
- Feel free to contribute.
