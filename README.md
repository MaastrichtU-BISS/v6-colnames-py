<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align=center> A privacy preserving federated learning solution</h3>

--------------------

# v6-colnames-py
This algoithm is part of the [vantage6](https://vantage6.ai) solution. Vantage6 allowes to execute computations on federated datasets. This contains the code for the v6-colnames-py algorithm, which returns the column names of all the nodes in a collaboration.



### Running the train
This will mainly depend on how the infrastructure has been set up - the correct URLs have to be entered and login details need to be correct. As an example, the `run.py` file has been provided. This has been taken from [this repository](https://gitlab.com/UM-CDS/pht/vantage6-docker-demo/-/blob/master/researcher/python/run.py), which also contains an example infrastructure that can be used to simulate a real-world scenario (it also works with the example `method.py` file provided). The details in the `run.py` file are in place to use this sample infrastructure and have to be changed for a production environment. As can be see in this local `run.py`, no `(kw)args` are needed to run this algorithm. Then simply run the file using:

```bash
python run.py
```

The output of this algorithm is a dictionary, with one key for each of the nodes (e.g. `node1`, `node2`), and one key for a set with the intersection of all column names present in the nodes. This set is useful to make sure that the algorithm you're running will have the appropriate data available on each of the nodes.

## Read more
See the [documentation](https://docs.vantage6.ai/) for detailed instructions on how to install and use the server and nodes.

------------------------------------
> [vantage6](https://vantage6.ai)