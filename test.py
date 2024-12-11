import yaml

# from custom_provenance import provenance as p
import provenance as p
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Dict

import logging


import provenance as p
from functools import wraps


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load the YAML configuration file
with open("basic_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Ensure the default_repo is set in the configuration
if "default_repo" not in config:
    raise ValueError("The 'default_repo' key is missing in the configuration")

# Pass the configuration dictionary to load_config
p.load_config(config)


# class TestObject:
#     prop1: int
#     prop2: str
#     prop3: bool


# def __init__():
#     testObj = TestObject(prop1=1, prop2="Test", prop3=True)
#     aux = testFun(testObj)
#     print(testObj)
#     print(aux)


# @p.provenance()
# def testFun(obj: TestObject):
#     obj.prop2 = "Changed"
#     return obj


class TestObject:
    prop1: int
    prop2: str
    prop3: bool

    def __init__(self, prop1, prop2, prop3):
        self.prop1 = prop1
        self.prop2 = prop2
        self.prop3 = prop3


@p.provenance()
def testFun(obj: TestObject):
    new_obj = TestObject(obj.prop1, "Changed", obj.prop3)
    return new_obj


def main():
    testObj = TestObject(prop1=1, prop2="Test", prop3=True)
    aux = testFun(testObj)
    print(f"Original: {testObj.prop1}, {testObj.prop2}, {testObj.prop3}")
    print(f"Modified: {aux.prop1}, {aux.prop2}, {aux.prop3}")


if __name__ == "__main__":
    main()
