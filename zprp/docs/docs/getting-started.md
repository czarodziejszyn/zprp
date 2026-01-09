Getting started
===============

This is where you describe how to get set up on a clean install, including the
commands necessary to get the raw data (using the `sync_data_from_s3` command,
for example), and then how to make the cleaned, final data sets.


## Testing Structure
### Unit tests
The project follows a co-located testing strategy. Each module contains its own `tests/` directory.

#### Execution
You can execute the entire test suite at once or target specific modules using the provided Makefile commands.
* Run all tests:
```
make tests
```

* Run module-specific tests:
```
make backend_tests
make scraper_tests
make geocoding_tests
```