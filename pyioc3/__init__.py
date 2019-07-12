# -*- coding: utf-8 -*-
"""Python IOC Container"""
from .static_container_builder import StaticContainerBuilder
from .static_container import StaticContainer
from .scope_enum import ScopeEnum

name = "pyioc3"
__all__ = ["StaticContainerBuilder", "ScopeEnum", "StaticContainer"]
