#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <map>
#include <string>

#include <random>
#include <unistd.h>

// output input args
int stdout_check(int argc, char **argv) {
    int n=1;
    std::cout << "Going to sleep for " << n << " seconds!" << std::endl;
    sleep(n);
    for (int i = 1; i < argc; ++i) {
        std::cout << argv[i] << std::endl;
    }
    return 0;
}

//split string by delimeter
std::vector<std::string> split (const std::string &s, char delim) {
    std::vector<std::string> result;
    std::stringstream ss (s);
    std::string item;

    while (getline (ss, item, delim)) {
        result.push_back(item);
    }

    return result;
}    

//generate random integer between min and max
int rand_num(int min, int max) {
    int rand_num_ = min + ( std::rand() % ( max - min + 1 ) );
    return rand_num_;
}

//generate data 
std::vector<std::pair<int,int>> rand_data(int bias, int variance) {
    std::vector<std::pair<int,int>> data;
    for (int i = 1; i<=100; i++) {
        int rand_n = rand_num(1, variance);
        data.push_back({ i, rand_n });
    }
    return data;
}

// //write data to csv
int writte_to_csv(std::vector<std::pair<int,int>> data, std::string file_name)
{
      std::ofstream myfile;
      std::stringstream ss;
      ss << "./Simulation/Simulation_data/" << file_name << ".csv";
      myfile.open (ss.str());
      for (auto point : data) {
          myfile << point.first << "," << point.second << "\n";
      }
      myfile.close();
      return 0;
}

std::map <std::string, std::string>  parse(int argc, char **argv) {
    std::map <std::string, std::string> inputparams;
    for (int i = 1; i < argc; ++i) {
        // std::cout << arg << std::endl;
        std::vector<std::string> a = split(argv[i], '=');
        // std::cout << a[0] << " " << a[1] << std::endl;
        inputparams[a[0]] = a[1];
    }
    return inputparams;
}

int main(int argc, char** argv){
    //command line arguments to the script
    std::map <std::string, std::string> inputparams = parse(argc, argv);
    stdout_check(argc, argv);
    // *char[] = {"--bias=3", "--variance=50", "--file_name=hallo"};
    // for (auto param : inputparams) {
    //     std::cout << param.first << " " <<  param.second << std::endl;
    // }

    int bias = std::stoi(inputparams["--bias"]);
    int variance = std::stoi(inputparams["--variance"]);
    std::string file_name = inputparams["--file_name"];

    // std::cout << "bias: " << bias << std::endl;
    // std::cout << "variance: " << variance << std::endl;
    // std::cout << "file_name: " << file_name << std::endl;

    std::vector<std::pair<int,int>> data = rand_data(bias, variance);
    // for (auto param : data) {
    //     std::cout << param.first << " " <<  param.second << std::endl;
    // }

    writte_to_csv(data, file_name);


}

