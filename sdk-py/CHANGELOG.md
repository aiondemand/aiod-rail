# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] | DD-MM-YYYY

## [1.2.3] | 08.10-2025

### Updated
* Added an enhanced search option for dataset searching.
* Authentication
  * Saving token information to a file now includes auth settings (auth_host, auth_realm, client_id).
  * Persistent auth is invalidated if auth settings do not match those in the file.
  * Handling of trailing / in auth_host URL.
  * Improved logic for the handling of persistent login sessions.
* Fixes for file download from experiment runs.
* Models updated to mirror those on the RAIL backend.

## [1.2.2] | 23.09-2025

### Updated
* Changed the default client ID for SSO to "aiod-sdk".

## [1.2.1] | 23.09-2025

### Updated
* The minimum required python version is now 3.11.

## [1.2.0] | 16-09-2025

### Updated
* Authentication method via a device code flow.
  * Now supports persistent login sessions via a local file storing the refresh token.
  * Login method now has a timeout parameter (default 300 seconds).
  * Logout method to clear the current session and delete the local file if persistent login was used.

### Added
* Asset Manager
  * Manager for datasets, models, publications and platforms
  * Implements getting and counting of assets based on filters
  * Datasets can additionally be created
* Dataset Instance
  * New instance type for datasets
  * Contains a method for deletion of a specific dataset
* Run Instance
  * New method to stop a specific run

### Removed
* API_KEY authentication method.

## [1.1.0] | 16-07-2025

### Updated
* Existing managers and instances docstrings to contain usage examples

### Added
* Experiment Run Manager
  * New manager for runs
  * Contains one method enabling getting of specific runs by their ID.

## [1.0.1] | 09-07-2025

### Updated
* README for PyPi

## [1.0.0] | 09-07-2025

### Updated
*

### Added
* First version of the SDK

### Deprecated
*

### Removed
*
