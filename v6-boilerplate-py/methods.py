""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption.
"""
import time

from vantage6.tools.util import info, warn


def master(client, data, *args, **kwargs):
    """Master algoritm.

    The master algorithm is the chair of the Round Robin, which makes
    sure everyone waits for their turn to identify themselfs.
    """

    # get all organizations (ids) that are within the collaboration
    # FlaskIO knows the collaboration to which the container belongs
    # as this is encoded in the JWT (Bearer token)
    organizations = client.get_organizations_in_my_collaboration()
    ids = [organization.get("id") for organization in organizations]

    # The input fot the algorithm is the same for all organizations
    # in this case
    info("Defining input parameters")
    input_ = {
        "method": "columnnames",
    }

    # create a new task for all organizations in the collaboration.
    info("Dispatching node-tasks")
    task = client.create_new_task(
        input_=input_,
        organization_ids=ids
    )

    # wait for node to return results. Instead of polling it is also
    # possible to subscribe to a websocket channel to get status
    # updates
    info("Waiting for resuls")
    task_id = task.get("id")
    task = client.get_task(task_id)
    while not task.get("complete"):
        task = client.get_task(task_id)
        info("Waiting for results")
        time.sleep(1)

    info("Obtaining results")
    results = client.get_results(task_id=task.get("id"))

    # Turn this into a nice dictionary along with a set to check which names
    # the nodes have in common
    results_dict = {f'node{i}': results[i] for i in range(len(results))}
    results_dict['common'] = set([item for sublist in results for item in sublist])

    # return all the messages from the nodes
    return results_dict

def RPC_columnnames(data, *args, **kwargs):
    """RPC_columnames.

    Do computation on data local to this node and send it back to 
    central server for further processing.

    In this case simply create a list of columns
    """
    result = list(data.columns)

    return result
