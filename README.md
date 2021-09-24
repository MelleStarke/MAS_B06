# Sustainable Supplier Selection, Order Allocation, and Vehicle Routing using SPADE

This project serves as an implementation of the framework proposed by Maria Drakaki et al. (2019), in which a multi-agent system framework is proposed to optimize sustainability in supplier selection, order allocation, and vehicle routing in global supply chains.



## Versions

This project was written on Linux using Python 3.8. Which is probably the only operating system it runs on.
The agents were implemented via the [SPADE](https://spade-mas.readthedocs.io/en/latest/readme.html) library, which uses [XMPP](https://xmpp.org/) to implement the [FIPA ACL](http://www.fipa.org/repository/aclspecs.html) Interaction Protocol.

SPADE can be installed by running

```
pip install spade
```

in the terminal.



## Preliminary Test

A preliminary test file can be found in `/src/simulations`. Despite there still being some run time errors related to concurrency, it serves as a minimal example of how the code runs.

Due to relative imports, running the file can be a bit tricky. Opening the project in PyCharm and setting the configuration in the root folder (meaning the root folder of the GitHub project) should work.

Otherwise you can simply run

```
python -m src.simulations.test
```

in a terminal opened in the root folder. Assuming Python 3.8 is in the PATH.

