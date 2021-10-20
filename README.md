# simulation-GUI
A PyQt example GUI for running simulation scripts and analyzing simulation generated data.

GUI is composed of two components:
1) the "RUN" tab where the user can choose the values of input parameters and run external simulation scripts (code in Run folder).
2) the "ANALYZE" tab where the user can visualize the simulation-generated data corresponding to the GUI-selected input parameters for the simulations (code in Analyze folder).

Both components have a Model-View-Controll architecture. User input is registered by the View, which delegates this information to the Controller which orchestrates the desired response. When needed, Controller sends a request to the Model, which is communicating with the databases (positioned in the Databases folder), whose rows correspond to individual simulation runs and columns to input parameters, while the last column holds the file_name of the simulation generated data file. Upon a user request for the simulation data with some combination of imput parameter values, the model filters the database table and uses the corresponding file_names to find the data files. 

In this example code the simulation is represented by a simple python script which generates a list of 2D data points (x,y). The simulation script simulation.py is positioned in the Simulation folder, together with the folder Simulation_data which holds the generated data files. 


