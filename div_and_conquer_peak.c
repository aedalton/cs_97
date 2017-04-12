#include <stdio.h>
#include <stdlib.h>

// SIMPLE PORT
// WORK IN PROGRESS, IMPROVEMENTS LATER

// A binary search based function that returns index of a peak element
int read_file_for_line() { 
  int lineNumber = 7;

  static const char filename[] = "file.txt"; /* retrieve from argv */
  FILE *file = fopen(filename, "r");
  int count = 0;
  if ( file != NULL ) {
    char line[256]; /* or other suitable maximum line size */
    while (fgets(line, sizeof line, file) != NULL) {
      if (count == lineNumber) {
	//use line or in a function return it
	//in case of a return first close the file with "fclose(file);"
      }
      else {
	count++;
      }
    }
    fclose(file);
  }
  else {
    //file doesn't exist
    return 1;
  }
}
int read_file() {
  FILE * fp;
  char * line = NULL;
  size_t len = 0;
  ssize_t read;
  
  fp = fopen("/etc/motd", "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);
  
  while ((read = getline(&line, &len, fp)) != -1) {
    printf("Retrieved line of length %zu :\n", read);
    printf("%s", line);
  }
  
  fclose(fp);
}

const char *readLine(FILE *file)
{
  char *lineBuffer=calloc(1,1), line[128];

  if ( !file || !lineBuffer )
  {
    fprintf(stderr,"an ErrorNo 1: ...");
    exit(1);
  }

  for(; fgets(line,sizeof line,file) ; strcat(lineBuffer,line) )
  {
    if( strchr(line,'\n') ) *strchr(line,'\n')=0;
    lineBuffer=realloc(lineBuffer,strlen(lineBuffer)+strlen(line)+1);
    if( !lineBuffer )
    {
      fprintf(stderr,"an ErrorNo 2: ...");
      exit(2);
    }
  }
  return lineBuffer;
}

/* Driver program to check above functions */
int main()
{
  return 0;
}
