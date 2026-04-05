"""Unit tests for SurvLoader behavior and resource loading fallbacks."""

import importlib.resources as std_pkg_resources
import unittest
from unittest.mock import patch

import pandas as pd

from SurvSet.data import SurvLoader


class TestSurvLoader(unittest.TestCase):
    def test_load_dataset_returns_expected_structure(self):
        loader = SurvLoader()
        result = loader.load_dataset("ova")

        self.assertIsInstance(result, dict)
        self.assertIn("df", result)
        self.assertIn("ref", result)
        self.assertIsInstance(result["df"], pd.DataFrame)
        self.assertIsInstance(result["ref"], str)
        self.assertFalse(result["df"].empty)

    def test_load_dataset_invalid_name_raises_assertion(self):
        loader = SurvLoader()
        with self.assertRaises(AssertionError):
            loader.load_dataset("madeup_dataset")

    def test_resource_root_fallback_when_namespace_lookup_fails(self):
        real_files = std_pkg_resources.files

        def files_with_namespace_failure(package):
            if package == "SurvSet.resources.pickles":
                raise TypeError("expected namespace-package lookup failure")
            return real_files(package)

        with patch("SurvSet.data.pkg_resources.files", side_effect=files_with_namespace_failure):
            loader = SurvLoader()
            df_ds = loader.load_csv("df_ds.csv")

        self.assertIsInstance(df_ds, pd.DataFrame)
        self.assertIn("ds", df_ds.columns)
        self.assertGreater(len(df_ds), 0)

    def test_resource_root_fallback_when_namespace_package_missing(self):
        real_files = std_pkg_resources.files

        def files_with_missing_namespace(package):
            if package == "SurvSet.resources.pickles":
                raise ModuleNotFoundError("No module named 'SurvSet.resources'")
            return real_files(package)

        with patch("SurvSet.data.pkg_resources.files", side_effect=files_with_missing_namespace):
            loader = SurvLoader()
            df_ds = loader.load_csv("df_ds.csv")

        self.assertIsInstance(df_ds, pd.DataFrame)
        self.assertIn("ds", df_ds.columns)
        self.assertGreater(len(df_ds), 0)


if __name__ == "__main__":
    unittest.main()
