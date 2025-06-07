"""
File that downloads custom datasets for the SurvSet package. This module downloads various datasets that are not part of the standard R packages.

# To run manually:
>>> python3 -m SurvSet._datagen.download_custom
"""

import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from urllib.request import urlretrieve
# Internal modules
from .utils.funs_support import makeifnot

class FileType(Enum):
    CSV = "csv"
    ZIP = "zip"
    XLS = "xls"
    DAT = "dat"


@dataclass
class DatasetConfig:
    """Configuration for a single dataset or group of datasets."""
    name: str
    base_url: str
    files: List[str]
    file_type: FileType
    subdirectory: Optional[str] = None
    url_pattern: Optional[str] = None  # For parameterized URLs like %s.dat


class DatasetDownloader:
    """Handles downloading and managing datasets."""
    
    def __init__(self, download_directory: str):
        assert os.path.exists(download_directory), f"Download directory {download_directory} does not exist."
        self.base_directory = download_directory
    
    def _get_download_path(self, config: DatasetConfig, filename: str) -> str:
        """Get the full path where a file should be downloaded."""
        if config.subdirectory:
            subdir = os.path.join(self.base_directory, config.subdirectory)
            makeifnot(subdir)
            return os.path.join(subdir, filename)
        return os.path.join(self.base_directory, filename)
    
    def _build_url(self, config: DatasetConfig, filename: str) -> str:
        """Build the complete URL for a file."""
        if config.url_pattern:
            # For parameterized URLs like the Hosmer datasets
            return config.base_url % filename.split('.')[0]  # Remove extension for parameter
        else:
            return os.path.join(config.base_url, filename).replace('\\', '/')
    
    def _download_single_file(self, url: str, filepath: str, file_type: FileType) -> bool:
        """Download a single file based on its type."""
        from .utils.funs_support import download_csv, download_zip
        
        try:
            if file_type == FileType.CSV:
                download_csv(url, os.path.dirname(filepath))
            elif file_type == FileType.ZIP:
                download_zip(url, os.path.dirname(filepath))
            else:  # XLS, DAT, or other direct downloads
                urlretrieve(url, filepath)
            return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
    
    def _get_expected_path(self, config: DatasetConfig, filename: str) -> str:
        """Get the expected path after download, accounting for file type conversions."""
        if config.file_type == FileType.ZIP:
            # For zip files, expect a folder with the same name (minus .zip)
            folder_name = filename.replace('.zip', '')
            return self._get_download_path(config, folder_name)
        elif config.file_type == FileType.DAT and filename.endswith('.dat') and config.name == "Hosmer & Lemeshow":
            # Convert .dat to .csv ONLY for Hosmer datasets (they get saved as CSV)
            csv_filename = filename.replace('.dat', '.csv')
            return self._get_download_path(config, csv_filename)
        else:
            # For all other files, expect the original filename
            return self._get_download_path(config, filename)
    
    def download_dataset(self, config: DatasetConfig) -> None:
        """Download all files for a given dataset configuration."""
        print(f"\n--- Downloading {config.name} datasets ---")
        
        for filename in config.files:
            expected_path = self._get_expected_path(config, filename)
            
            if os.path.exists(expected_path):
                print(f"File/folder {filename} already exists, skipping download.")
                continue
            
            print(f"Downloading {filename}...")
            url = self._build_url(config, filename)
            download_path = self._get_download_path(config, filename)
            
            success = self._download_single_file(url, download_path, config.file_type)
            if not success:
                print(f"Failed to download {filename}")
    
    def download_multiple_datasets(self, configs: List[DatasetConfig]) -> None:
        """Download multiple datasets."""
        for config in configs:
            self.download_dataset(config)
        print('\n~~~ Download completed ~~~')


def get_default_dataset_configs() -> List[DatasetConfig]:
    """Get the default dataset configurations."""
    return [
        DatasetConfig(
            name="Hosmer & Lemeshow",
            base_url="https://raw.githubusercontent.com/graemeleehickey/hosmer-lemeshow/master/edition2/%s.dat",
            files=["FRTCS.dat", "uis.dat"],
            file_type=FileType.DAT,
            subdirectory="hosmer",
            url_pattern="%s.dat"
        ),
        DatasetConfig(
            name="Lung Cancer",
            base_url="https://www.openml.org/data/get_csv/552598",
            files=["phpl04K8a"],
            file_type=FileType.CSV
        ),
        DatasetConfig(
            name="Reddy Gene Expression",
            base_url="https://dmkd.cs.vt.edu/projects/survival/data",
            files=["Gene_expression_data.zip"],
            file_type=FileType.ZIP
        ),
        DatasetConfig(
            name="Princeton GLM",
            base_url="https://grodri.github.io/datasets",
            files=["divorce.dat"],
            file_type=FileType.DAT
        ),
        DatasetConfig(
            name="HBiostat/Vanderbilt",
            base_url="https://hbiostat.org/data/repo",
            files=[
                "support2csv.zip", "prostate.xls", "2.20.Framingham.csv", 
                "rhc.csv", "acath.xls.zip", "vlbw.zip"
            ],
            file_type=FileType.CSV,  # Mixed types, handled specially
            subdirectory="vanderbilt"
        )
    ]


def download_custom(fold_custom: str, dataset_configs: Optional[List[DatasetConfig]] = None) -> None:
    """
    Download custom datasets with improved modularity.
    
    Args:
        fold_custom: Name of the folder to download datasets into
        dataset_configs: Optional list of dataset configurations. If None, uses defaults.
    """
    if dataset_configs is None:
        dataset_configs = get_default_dataset_configs()
    
    downloader = DatasetDownloader(fold_custom)
    
    # Separate HBiostat datasets for special handling
    regular_configs = []
    hbiostat_configs = []
    
    for config in dataset_configs:
        if config.name == "HBiostat/Vanderbilt":
            hbiostat_configs.append(config)
        else:
            regular_configs.append(config)
    
    # Download regular datasets using the batch method
    if regular_configs:
        downloader.download_multiple_datasets(regular_configs)
    
    # Handle HBiostat datasets specially due to mixed file types
    for config in hbiostat_configs:
        _download_hbiostat_datasets(downloader, config)
    
    print('\n~~~ End of download_custom.py ~~~')


def _download_hbiostat_datasets(downloader: DatasetDownloader, config: DatasetConfig) -> None:
    """Special handler for HBiostat datasets with mixed file types."""
    print(f"\n--- Downloading {config.name} datasets ---")
    
    for filename in config.files:
        file_ext = filename.split('.')[-1]
        
        # Determine file type from extension
        if file_ext == 'zip' or filename.endswith('.xls.zip'):
            file_type = FileType.ZIP
            expected_name = filename.replace('.zip', '')
            if filename.endswith('.xls.zip'):
                expected_name = filename.replace('.xls.zip', '')
        elif file_ext == 'xls':
            file_type = FileType.XLS
            expected_name = filename
        elif file_ext == 'csv':
            file_type = FileType.CSV
            expected_name = filename
        else:
            print(f"Unsupported file type for {filename}")
            continue
        
        expected_path = downloader._get_download_path(config, expected_name)
        
        if os.path.exists(expected_path):
            print(f"File/folder {expected_name} already exists, skipping download.")
            continue
        
        print(f"Downloading {filename}...")
        url = os.path.join(config.base_url, filename).replace('\\', '/')
        download_path = downloader._get_download_path(config, filename)
        
        success = downloader._download_single_file(url, download_path, file_type)
        if not success:
            print(f"Failed to download {filename}")


# Utility functions for external use
def create_dataset_config(name: str, base_url: str, files: List[str], 
                         file_type: str, subdirectory: Optional[str] = None,
                         url_pattern: Optional[str] = None) -> DatasetConfig:
    """Helper function to create a DatasetConfig."""
    return DatasetConfig(
        name=name,
        base_url=base_url,
        files=files,
        file_type=FileType(file_type.lower()),
        subdirectory=subdirectory,
        url_pattern=url_pattern
    )


def add_custom_dataset(name: str, base_url: str, files: List[str], 
                      file_type: str, subdirectory: Optional[str] = None) -> DatasetConfig:
    """Add a custom dataset configuration."""
    return create_dataset_config(name, base_url, files, file_type, subdirectory)


if __name__ == '__main__':
    # Load the default arguments
    from . import di_argpase_defaults
    import argparse
    
    parser = argparse.ArgumentParser(description="Download custom datasets")
    parser.add_argument(
        '--fold_custom', 
        help=di_argpase_defaults['fold_custom']['help'], 
        default=di_argpase_defaults['fold_custom']['val']
    )
    parser.add_argument(
        '--datasets',
        nargs='*',
        help="Specific datasets to download (by name). If not specified, downloads all.",
        default=None
    )
    
    args = parser.parse_args()
    
    # Filter datasets if specific ones were requested
    configs = get_default_dataset_configs()
    if args.datasets:
        configs = [c for c in configs if c.name in args.datasets]
        if not configs:
            print(f"No matching datasets found. Available: {[c.name for c in get_default_dataset_configs()]}")
            exit(1)
    
    # Call the download function
    download_custom(fold_custom=args.fold_custom, dataset_configs=configs)