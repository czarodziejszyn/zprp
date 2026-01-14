# Logging Configuration

This module provides a unified logging configuration used across all project components.

## Implementation Details
Defined in logger.py, the configuration establishes a global message format and manages the verbosity of third-party libraries (silencing httpx logs).

Log Format: `LEVEL | MODULE_NAME | MESSAGE`

## Usage in Modules
To apply the global settings, the configuration must be imported at the beginning of the file, before initializing the local logger.


## Controlling Verbosity
The level of detail can be managed via the .env file using the LOG_LEVEL variable. This defines the minimum severity of logs to be displayed:  
* Development: `LOG_LEVEL=DEBUG`  
* Production: `LOG_LEVEL=INFO` (default)