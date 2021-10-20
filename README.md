# simulation-GUI
A PyQt example GUI for running simulation scripts and analyzing simulation generated data.

GUI is composed of two components:
1) The "RUN" tab where the user can run external simulation scripts and choose values of the script arguments. The simulation script stores generated data in a file and saves the file name together with the input arguments as a reference in a database. The implementation of the "RUN" component can be found in the Run folder.
2) The "ANALYZE" tab where the user can visualize the simulation-generated data corresponding to the GUI-selected input arguments for the simulations. The implementation of the "ANALYZE" component can be found in the Analyze folder.

Both components have a Model-View-Controll architecture. View registers the user input and delegates this information to the Controller which orchestrates the desired response. When needed, Controller sends a request to the Model, which has access to the databases, whose rows correspond to individual simulation runs and columns to input parameters, while the last column holds the file name of the simulation generated data file. Upon a user request for the simulation data with some combination of imput parameter values, the model filters the database table and uses the corresponding file names to find the data files. 

In this example code the simulation is represented by a simple python script which generates a list of 2D data points (x,y). The simulation script simulation.py is positioned in the Simulation folder, together with the folder Simulation_data which holds the generated data files. The databases are positioned in the Databases folder.


