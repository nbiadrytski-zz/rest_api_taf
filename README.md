## REST API TAF
Test Automation framework based on unittest module to test Flask server app.

Supports _Python 3.6+_.

#### Description
Uses:

1. ```unittest``` as test runner
2. Python ```requests``` module to perform HTTP requests


Is able to perform HTTP GET, POST, DELETE requests (can be extended) and validate responses.

Tests are in ```tests``` folder, codebase is in ```utils``` folder.

#### Usage
Run tests:

``` python -m unittest -v```


If you want to generate test report, then run tests as:

``` python tests/__init__.py```

This will generate HTML test report into reports/ directory.