"""
Algorithm entrypoints for the Vantage6 column-name discovery workflow.
"""

from vantage6.algorithm.tools.decorators import algorithm_client, data
from vantage6.algorithm.tools.util import info


@algorithm_client
def master(client, *args, **kwargs):
    """
    Dispatch a child task to every organization in the collaboration and
    aggregate their column names.
    """
    organizations = client.organization.list()
    organization_ids = [organization["id"] for organization in organizations]

    info("Defining input parameters")
    input_ = {
        "method": "colnames",
        "args": [],
        "kwargs": {},
    }

    info("Dispatching node-tasks")
    task = client.task.create(
        input_=input_,
        organizations=organization_ids,
        name="Collect column names",
        description="Retrieve local column names for all organizations",
    )

    info("Waiting for results")
    results = client.wait_for_results(task["id"])
    info("Obtaining results")

    if not results:
        return {"common": [], "organizations": {}}

    organizations_result = {}
    common = set(results[0]["columns"])
    for result in sorted(results, key=lambda entry: entry["organization_id"]):
        key = f"organization_{result['organization_id']}"
        columns = sorted(result["columns"])
        organizations_result[key] = {
            "organization_id": result["organization_id"],
            "node_id": result["node_id"],
            "columns": columns,
        }
        common &= set(columns)

    organizations_result["common"] = sorted(common)
    return organizations_result


@data()
@algorithm_client
def colnames(client, data, *args, **kwargs):
    """
    Return the local dataframe column names together with organization metadata.
    """
    return {
        "organization_id": client.organization_id,
        "node_id": client.node_id,
        "columns": list(data.columns),
    }
