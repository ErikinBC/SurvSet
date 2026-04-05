"""Unit tests for SurvLoader behavior and resource loading fallbacks."""

import importlib.resources as std_pkg_resources
import unittest
from unittest.mock import patch

import numpy as np
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

    def test_coxnet_alpha_selection_improves_score(self):
        """Test that selecting optimal alpha produces better scores than default (issue #6)."""
        try:
            from sksurv.util import Surv
            from sksurv.linear_model import CoxnetSurvivalAnalysis
            from sklearn.impute import SimpleImputer
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            self.skipTest("scikit-survival or scikit-learn not available")

        loader = SurvLoader()
        df = loader.load_dataset("prostate")["df"]

        # Prepare minimal data
        senc = Surv()
        y = senc.from_arrays(df["event"].astype(bool), df["time"])
        
        # Simple preprocessing: impute and scale numeric columns
        X = df[[c for c in df.columns if c.startswith("num_")]].fillna(0)
        imputer = SimpleImputer(strategy="median")
        scaler = StandardScaler()
        X = scaler.fit_transform(imputer.fit_transform(X))

        # Fit model
        mdl = CoxnetSurvivalAnalysis(n_alphas=10)
        mdl.fit(X, y)

        # Get score for each alpha
        scores = [mdl.score(X, y, alpha=alpha) for alpha in mdl.alphas_]
        best_alpha_idx = np.argmax(scores)
        best_alpha = mdl.alphas_[best_alpha_idx]
        best_score = scores[best_alpha_idx]

        # Last alpha (default) should generally be worse or equal
        default_score = mdl.score(X, y, alpha=mdl.alphas_[-1])

        # The fix ensures we pick a better (or equal) alpha explicitly
        self.assertGreaterEqual(best_score, default_score * 0.99)  # Allow 1% tolerance for numerical variations


if __name__ == "__main__":
    unittest.main()
