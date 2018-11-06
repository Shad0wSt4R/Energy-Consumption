#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>

//I have always been told never to use namespace std. They say
//take only what you need.

//using namespace std;

std::string GetStdoutFromCommand(std::string cmd) {

	std::string data;
FILE * stream;
const int max_buffer = 256;
char buffer[max_buffer];
cmd.append(" 2>&1");

stream = popen(cmd.c_str(), "r");
if (stream) {
while (!feof(stream))
if (fgets(buffer, max_buffer, stream) != NULL) data.append(buffer);
pclose(stream);
}
return data;
}

int main (){
	std::ofstream ofile;

	std::string ls = GetStdoutFromCommand("cat /proc/cpuinfo");

	ofile.open("CPU_info.txt");
	if(ofile.is_open()){
		ofile << "Here's cpu info: " << std::endl << ls << std::endl;;
	}
	else{
		std::cout << "Unable to openfile" << std::endl;
	}
	ofile.close();

	//std::cout << "Here's cpu info: " << std::endl << ls << std::endl;

return 0;
}

