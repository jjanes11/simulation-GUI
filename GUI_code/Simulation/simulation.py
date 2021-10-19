import sys
from time import sleep
import csv
import random
import os


SIM_DIR = os.path.dirname(os.path.abspath(__file__))

def stdout_check(args):
    n=5
    sys.stdout.write(f"Going to sleep for {n} seconds!")
    sys.stdout.flush()
    sleep(1)
    sys.stdout.write(str(args[1:]))

def writte_to_file(data, file_name):
    with open(f'{SIM_DIR}/Simulation_data/{file_name}.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

def rand_data(bias, variance):
    list = []
    randomlist = []
    for i in range(0,100):
        n = bias + random.randint(1,variance)
        randomlist.append(n)
    for i in range(0,100):
        list.append(i)
    return zip(list,randomlist)


if __name__ == "__main__":
    args = sys.argv
    stdout_check(args)
    inputparams = {}
    for arg in args[1:]:
        a=arg.split("=")
        inputparams[a[0]] = a[1] 

    bias = int(inputparams["--bias"])
    variance = int(inputparams["--variance"])
    file_name = inputparams["--file_name"]
    data = rand_data(bias, variance)
    writte_to_file(data, file_name)

