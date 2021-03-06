# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2020-04-02
### Changed
- upgraded twine to version 3.1.1 or later (due to a vulnerability on sub-dependency bleach)
- __version__ to 0.1.2

### Fixed
- typing error on state.py
- small errors in CHANGELOG.md
- some changelog issues

## [0.1.1] - 2019-11-16
### Changed
- changed setup.py, Makefile and __version__ to allow first PyPI release

## [0.1.0] - 2019-11-16
### Removed
- agent module - code migrated to a future BiscaAI library.

### Changed
- quite a bit internally, but the API didn't change much.

## [0.0.1] - 2019-11-14
### Added
- Everything. Modules card and state are reasonably stable. Module agent is not working.

[Unreleased]: https://github.com/NunoMCSilva/libbisca/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/NunoMCSilva/libbisca/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/NunoMCSilva/libbisca/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/NunoMCSilva/libbisca/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/NunoMCSilva/libbisca/releases/tag/v0.0.1
