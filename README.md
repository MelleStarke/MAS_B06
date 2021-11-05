# Sustainable Supplier Selection, Order Allocation, and Vehicle Routing using SPADE

This project serves as an implementation of the framework proposed by Maria Drakaki et al. (2019), in which a multi-agent system framework is proposed to optimize sustainability in supplier selection, order allocation, and vehicle routing in global supply chains.



## Versions

This project was written on Linux using Python 3.8. Which is probably the only operating system it runs on. 
The agents were implemented via the [SPADE](https://spade-mas.readthedocs.io/en/latest/readme.html) library, which uses [XMPP](https://xmpp.org/) to implement the [FIPA ACL](http://www.fipa.org/repository/aclspecs.html) Interaction Protocol. Note that older versions of Ubuntu (such as 16) may not be able to install SPADE.

SPADE can be installed by running

```
pip install spade
```

in the terminal.



## Simulation

A simulation file can be found in `/src/simulations` as `cost_sus_experiment.py`.

Due to relative imports, running the file can be a bit tricky. Opening the project in PyCharm and setting the configuration in the root folder (meaning the root folder of the GitHub project) should work.
Do be sure to check the "Run with Python console", "Add content roots to PYTHONPATH", and "Add source roots to PYTHONPATH" in the configuration just to be sure.
If the code doesn't work due to import errors, please contact me.

Otherwise you can try running

```
python -m src.simulations.cost_sus_experiment
```

in a terminal opened in the root folder. Assuming Python 3.8 is in the PATH.

