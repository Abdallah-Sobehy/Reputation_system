# Reputation_system
A gossip based system which simulates opinion diffusion in a network between neighbors. 
Two forceful peers with static opinions connect to other peers in a network and their opposing opinions spread in the network based on the connections they made.
Forceful peers connect to other peers probabilistically with one of 4 strategies: D, 1/D, D^2 and U
Forceul peers pair face off in a simulation, and the winner is the one who has most followers.
Another type of forceful peer (smart peer) has prior knowledge of opponent's connections and with the formulation of a Mixed integer optimization problem,
it is able to beat the opposing peer with minimum number of conenctions.

Program execution : python main.py

To choose forceful peer strategies and type of graphs, variables in caps in  main.py needs to be changes (according to the documentation).

Needed libraries: networkx, numoy, scipy and matplotlib. 
pulp, Gurobi (for optimization with smart peer only)
