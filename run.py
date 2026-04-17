from vantage6.client import Client

print("Attempt login to Vantage6 API")
client = Client("http://localhost", 5000, "/api")
client.authenticate("node1-user", "node1-password")

client.setup_encryption(None)

collaboration = client.collaboration.list()[0]
collaboration_id = collaboration["id"]
client.setup_collaboration(collaboration_id)
organization_ids = [organization["id"] for organization in client.organization.list()]

input_ = {
    "master": True,
    "method": "master",
    "args": [],
    "kwargs": {},
}

print("Requesting to execute colnames algorithm")
task = client.task.create(
    organizations=organization_ids,
    name="testing",
    image="jaspersnel/v6-colnames-py",
    description="Retrieve column names from all connected nodes",
    collaboration=collaboration_id,
    input_=input_,
)

print("Wait and fetch results")
results = client.wait_for_results(task["id"])
print(results)
