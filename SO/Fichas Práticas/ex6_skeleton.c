#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>


#define MAX_COMMANDS 10

// parse the argument and execvp
// returns the result of exec
int exec_command(char* arg){

	//We are assuming a maximum number of arguments of 10.
	//This could be improved with realloc, for example.
	char *exec_args[10];
	int args_count = 0;
	int exec_ret = 0;

	char *token, *string, *tofree;

	tofree = string = strdup(arg);
	assert(string != NULL);

	while ((token = strsep(&string, " ")) != NULL) {
		exec_args[args_count]=token;
		args_count++;
	}
	exec_args[args_count]=NULL;

	exec_ret=execvp(exec_args[0],exec_args);

	perror("Exec error");

    free(tofree);

	return exec_ret;
}


int main(int argc, char** argv){

	int number_of_commands=4;
	char * commands[] = {
		"grep -v ^# /etc/passwd",
		"cut -f7 -d:",
		"uniq",
		"wc -l"
	};

	// TO DO ...

	return 0;
}
