babelmap
========

![An example graph generated](graph.png)

Generates a global map of nodes and their routes based on data provided by the babel daemon, it is important to recognize this generates a map based off of router ID's which are originator ID's, therefore this map is not a topology map but rather somethign similiar to babelweb. It simply shows who learnt what route from what **original** router - hence it will always appear as a mesh despite that not being the network's actual topology.

## Usage

Fill the file `peers.list` with the babel nods you want to contact with `<ip> <port>` pairings. An example is in the `peers.list` file in this repository.

## Dependancies

* `ncat`
* `python3`
