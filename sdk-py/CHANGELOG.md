# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] | DD-MM-YYYY
### Updated
* Configuration now automatically fetches API_KEY from environmental variable.

### Added
* Asset Manager
  * Manager for datasets, models, publications and platforms
  * Implements getting and counting of assets based on filters
  * Datasets can additionally be created
* Dataset Instance
  * New instance type for datasets
  * Contains a method for deletion of a specific dataset


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
