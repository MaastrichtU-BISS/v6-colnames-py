from vantage6.client import Client
from pathlib import Path
import time

print("Attempt login to Vantage6 API")
client = Client("http://localhost", 5000, "/api")
client.authenticate("johan", "1234")

client.setup_encryption(None)

input_ = {
    "master": "true",
    "method":"master", 
    "args": [], 
    "kwargs": {}
}

print("Requesting to execute colnames algorithm")

task = client.post_task(
    name="testing",
    image="ghcr.io/MaastrichtU-BISS/v6-colnames-py",
    collaboration_id=1,
    input_= input_,
    organization_ids=[1]
)

print("Wait and fetch results")
res = client.result.get(id_=task.get("results")[0]['id'])
attempts=1
while((res["result"] == None) and attempts < 7):
    print("waiting...")
    time.sleep(5)
    res = client.result.get(id_=task.get("results")[0]['id'])
    attempts += 1

print(res)
