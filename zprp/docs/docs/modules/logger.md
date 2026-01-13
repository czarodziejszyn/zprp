# Logger reference
This module is responsible for unifing logging configuration for all modules.


The configuration is defined in logger.py. It sets a global message format and adjusts the verbosity of third-party libraries (httpx)
Python


Every log entry includes the severity level, the name of the module where the log originated, and the message.



## Usage in Modules

To use this configuration in any part of the project, it needs to be imported before initializing local logger. This ensures the global settings are applied first.

## Controling level of details
You can control the detail of the logs via the .env file by LOG_LEVEL variable, which defines the minimum severity of logs to display.
        Example for development: LOG_LEVEL=DEBUG
        Example for production: LOG_LEVEL=INFO (default)


====
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