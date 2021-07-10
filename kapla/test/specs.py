from __future__ import annotations
import typing

import pydantic


class YamlItemSpec(pydantic.BaseModel):
    """Base model representing a test item found in YAML file.

    Customize this class as you need.
    For example, if you want to build a test spec to perform HTTP tests, add the following fields:
        - method: To specify which HTTP method shoud be used when sending request
        - body: To specify the body of the request
        - headers: To specify header of the request
        - cookies: To specify cookies for the request
        - expect: To specify what to expect in return. This should also be a pydantic model. It could have the following fields: "status_code", "body", "headers", "validator".
          Where "validator" would be a valid import string (such as "kapla.my_module:my_function") pointing to a callable which accept a request and a context (context would be all input arguments used when building test case).
          It could also be a dictionary with a valid import string and some additional key word arguments. In any case, the function is expected to evaluate to True, else test is considered to be failed
    """

    name: str
    description: typing.Optional[str] = None
    groups: typing.List[str] = []
    variables: typing.Dict[str, typing.Any] = {}


class YamlFileSpec(pydantic.BaseModel):
    """Base model representing a test YAML file."""

    tests: typing.List[YamlItemSpec]
    description: typing.Optional[str] = None
    groups: typing.List[str] = []
    variables: typing.Dict[str, typing.Any] = {}
