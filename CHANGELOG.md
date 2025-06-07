# Changelog

All notable changes to this project will be documented in this file.

## [0.2.9] - 2025-06-07
### Added
- Included only `.pickle` files in `SurvSet/resources/pickles` in the PyPI build (plus the one CSV table `resources/pickles/df_ds.csv`).
- Cleaned up packaging structure and added build/test instructions.
- Added one new dataset (it wasn't being properly processed before): [rhc](https://hbiostat.org/data/repo/rhc.html)
- Several items to `.gitignore`, testing can rely on a local `.env` if required. 

### Changed
- Removed reliance on `package_data`; now using `MANIFEST.in`.

### Fixed
- FRTCS processing now has dataset as a time-varying dataset structure
- Excluded unnecessary resource subfolders from packaging.
