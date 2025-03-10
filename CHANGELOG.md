# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.3] - 2025-02-27
### Fixed
- segfault when incorrect output is provided to uci.get

## [0.10.2] - 2025-02-20
### Fixed
- building wheels and package installation

## [0.10.1] - 2025-02-13
### Fixed
- memory leak in pyuci.c
- commit_all should commit all packages

## [0.10.0] - 2023-08-07
### Added
- `Uci.add` function for adding anonymous section implemented
- `EUci.add` function to add both anonymous and named sections added

## [0.9.0] - 2022-03-04
### Added
- `convert` argument for `EUci.get`. It provides a way to convert values to any
  type with custom function.

### Changed
- `list` argument for `EUci.get` is now required to be set to `True` for lists
  otherwise only first value is returned. This is removal of auto-detection of
  lists. The get of list has to be now always explictly stated.
- `dtype` argument for `EUci.get` can now be any type that can be initialized
  with string as a single argument (such as `int("42")`.
- `default` argument for `EUci.get` now uses object instance `NoDefault` to
  detect that there is no default instead of presence of keyword argument.

### Removed
- obsolete "get" methods in `EUci`


## [0.8.1] - 2020-11-20
### Fixed
- missing include `collections.abc` in `euci` module


## [0.8] - 2020-08-26
### Added
- EUci support for IP address parsing

### Fixed
- Use of deprecated and in Python 3.9 removed library


## [0.7] - 2019-12-04
### Added
- EUci.boolean with boolean strings mapping


## [0.6.1] - 2019-11-26
### Fixed
- EUci.get() iterable non-iterable default


## [0.6] - 2019-05-06
### Added
- EUci method get() that overloads Uci one and provides automatic type conversion
- EUci method set() that overloads Uci one does conversion supplementary to what
  get() does
- Readme with API documentation


## [0.5] - 2019-04-22
### Added
- EUci default methods

### Removed
- Python 2 support


## [0.4.2] - 2019-04-01
### Changed
- Do not commit on context exit when no change was performed


## [0.4.1] - 2019-02-05
### Fixed
- Python 2 incompatibilities in EUci


## [0.4] - 2019-01-31
### Added
- EUci module (Extended UCI as Python extension to Uci module)


## [0.3] - 2018-03-15
### Added
- Support for Python context manager


## [0.2.1] - 2018-03-15
### Fixed
- UciExceptionNotFound name in uci module


## [0.2] - 2018-03-14
### Added
- Support for setting lists and tuples as values


## [0.1] - 2018-02-26
### Added
- Minimal functionality for getting and setting named sections implemented
