## kapla-test

An example implementation of a pytest test collector that can parse YAML files.


### Installing the project

This project is packaged using [`poetry`](https://python-poetry.org/). You can clone it and install it using the following command:

```bash
git clone https://github.com/charbonnierg/kapla-test.git
cd kapla-test
poetry install
```

### Running the tests

Tests are located in `tests` directory. A single file is present, it's a non realistic test that exists only for demonstration purpose. Let pytest discover and parse the tests by running the following command at the root of the repository:

```bash
pytest
```

### Understanding test discovery

When the `pytest` command is executed, one of the first actions performed is to check for the presence of a file named `conftest.py`. This file is then read, and if a function named `pytest_collect_file` is defined within this file (either imported or defined locally), `pytest` will still load python tests as it does by default, and will also tries to collect tests items from each file using the `pytest_collect_file` function.

### Updating the expected YAML syntax

Expected YAML syntax is defined in the `kapla.test.specs`. This module defines too classes:

- `YamlItemSpec`: A `pydantic.BaseModel` representing a single test item schema.

- `YamlFileSpec`: A `pydantic.BaseModel` representing a whole YAML test file.

You can update those two classes to fit your needs, however, `YamlItemSpec` **must always have a name**.

### Implementing complex test cases

In order to implement complex test cases, it is first needed to update the expected YAML syntax as described above. Once this is done, you can update `kapla.test.collector.YamlItem.runtest()` function to perform complex actions based on the test spec.

### Going further

Let's try to come up with a test spec to perform HTTP tests.

The following fields could be required or optional test item configuration that impact how test action is performed:

- *method*: To specify which HTTP method shoud be used when sending request

- *body*: To specify the body of the request

- *headers*: To specify header of the request

- *cookies*: To specify cookies for the request

The following field could be required or optional test item configuration that impact how test validation should be performed:

- *expect*: To specify what to expect in return. This should also be a pydantic model. It could have the following fields: "*status_code*", "*body*", "*headers*", "*validator*".

Where "*validator*" would be a valid import string (such as `kapla.my_module:my_function`) pointing to a callable which accept a request and a context (context would be all input arguments used when building test case).
It could also be a dictionary with a valid import string and some additional key word arguments. In any case, the function is expected to evaluate to `True`, else test is considered to be failed.

### VSCode settings for the project:

The following settings are used to contribute to the project:

```json
{
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
}
```
