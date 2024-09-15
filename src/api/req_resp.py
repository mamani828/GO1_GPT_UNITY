#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Callable

@dataclass
class GenericRequest():
    function: Callable
    args    : dict

@dataclass
class Object():
    x : int
    y : int
    z : int

