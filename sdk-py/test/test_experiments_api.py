# coding: utf-8

"""
    AIoD - RAIL

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.20240209-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from aiod_rail_sdk.api.experiments_api import ExperimentsApi


class TestExperimentsApi(unittest.TestCase):
    """ExperimentsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ExperimentsApi()

    def tearDown(self) -> None:
        pass

    def test_create_experiment_v1_experiments_post(self) -> None:
        """Test case for create_experiment_v1_experiments_post

        Create Experiment
        """
        pass

    def test_execute_experiment_run_v1_experiments_id_execute_get(self) -> None:
        """Test case for execute_experiment_run_v1_experiments_id_execute_get

        Execute Experiment Run
        """
        pass

    def test_get_all_experiment_runs_v1_experiment_runs_get(self) -> None:
        """Test case for get_all_experiment_runs_v1_experiment_runs_get

        Get All Experiment Runs
        """
        pass

    def test_get_experiment_run_logs_v1_experiment_runs_id_logs_get(self) -> None:
        """Test case for get_experiment_run_logs_v1_experiment_runs_id_logs_get

        Get Experiment Run Logs
        """
        pass

    def test_get_experiment_run_v1_experiment_runs_id_get(self) -> None:
        """Test case for get_experiment_run_v1_experiment_runs_id_get

        Get Experiment Run
        """
        pass

    def test_get_experiment_runs_count_v1_count_experiments_id_runs_get(self) -> None:
        """Test case for get_experiment_runs_count_v1_count_experiments_id_runs_get

        Get Experiment Runs Count
        """
        pass

    def test_get_experiment_runs_v1_experiments_id_runs_get(self) -> None:
        """Test case for get_experiment_runs_v1_experiments_id_runs_get

        Get Experiment Runs
        """
        pass

    def test_get_experiment_v1_experiments_id_get(self) -> None:
        """Test case for get_experiment_v1_experiments_id_get

        Get Experiment
        """
        pass

    def test_get_experiments_count_v1_count_experiments_get(self) -> None:
        """Test case for get_experiments_count_v1_count_experiments_get

        Get Experiments Count
        """
        pass

    def test_get_experiments_v1_experiments_get(self) -> None:
        """Test case for get_experiments_v1_experiments_get

        Get Experiments
        """
        pass


if __name__ == "__main__":
    unittest.main()