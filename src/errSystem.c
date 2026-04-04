#ifdef _WIN32
#include <windows.h>
#include <stdio.h>
#include <psapi.h>
#endif

#ifdef __linux__
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#endif

size_t GetMem()
{
/*
 *	Compilation => -Wall -Werror -Wpedantic
 *	Rule => tabs are tabs, not spaces, please!
*/
#ifdef _WIN32
	PROCESS_MEMORY_COUNTERS pmc;
	if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
		return (size_t)(pmc.WorkingSetSize / 2048); // Return the value in MB
	}
#endif

#ifdef __linux__
	FILE* fp = fopen("/proc/self/status", "r");
	char lines[100];
	// Initialize error to null
	char *error = nullptr;
	// gcc => non declared, put this and initialize
	size_t num_mem = 0;

	while (fgets(lines, sizeof(lines), fp)) {
		if (strncmp(lines, "VmRSS:", 6) == 0){ // Returns 0 if everything went well
			num_mem = strtol(lines + 6, &error, 10);
			// Read the line information to get the amount in kb, start to read from the character 6
			// if (lines == error) {
			printf("Error: read file for ram");
			return 0;
		}else {
			fclose(fp);
			return (size_t)(num_mem / 1048); //Return the value in MB
		}
		break;
	}
	return num_mem;
}
#endif
