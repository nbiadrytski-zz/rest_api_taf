## Rest API Test Automation framework
Test Automation framework to test Flask server.

Supports _Python 3.6+_.

#### Description
Uses:

1. ```pytest``` as test runner
2. Python ```requests``` module to perform HTTP requests


Is able to perform HTTP GET, POST, DELETE requests (can be extended) and validate responses.

Tests are in ```tests``` folder, codebase is in ```utils``` folder.

#### Usage
Run tests:

```python3 -m pytest -v --env=dev --junitxml=report.xml``` where

**--env=dev** - desired environment (see ```utils/data/env_config.ini``` for available environments)
**--junitxml** - path to xml report

You can also run certain tests by specifying their group from pytest.ini, e.g. case (tests for test cases), suite (test for test suites):

```python3 -m pytest -v -m case --env=dev --junitxml=report.xml```