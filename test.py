import pandas as pd

from importlib import import_module

from vantage6.algorithm.tools.mock_client import MockAlgorithmClient


ALGORITHM_MODULE = "v6-colnames-py"


def create_mock_client():
    datasets = [
        [{"database": pd.DataFrame({"patient_id": [1, 2], "age": [30, 41]})}],
        [
            {
                "database": pd.DataFrame(
                    {"patient_id": [3, 4], "age": [51, 62], "site": ["a", "b"]}
                )
            }
        ],
    ]
    return MockAlgorithmClient(
        datasets=datasets,
        module=ALGORITHM_MODULE,
        organization_ids=[101, 202],
        node_ids=[11, 22],
    )


def test_colnames_returns_local_columns():
    client = create_mock_client()
    algorithm = import_module(ALGORITHM_MODULE)

    result = algorithm.colnames(mock_client=client, mock_data=[client.datasets_per_org[101][0]])

    assert result == {
        "organization_id": 101,
        "node_id": 11,
        "columns": ["patient_id", "age"],
    }


def test_master_aggregates_columns_and_common_set():
    client = create_mock_client()
    algorithm = import_module(ALGORITHM_MODULE)

    result = algorithm.master(mock_client=client)

    assert result == {
        "organization_101": {
            "organization_id": 101,
            "node_id": 11,
            "columns": ["age", "patient_id"],
        },
        "organization_202": {
            "organization_id": 202,
            "node_id": 22,
            "columns": ["age", "patient_id", "site"],
        },
        "common": ["age", "patient_id"],
    }
