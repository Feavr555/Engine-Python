#include <stdio.h>
#include <stdlib.h>
#include <glad/glad.h>

typedef unsigned int uint;

int sizeFile(FILE *file)
{
	fseek(file,0,SEEK_END);
	long position = ftell(file);
	fseek(file,0,SEEK_SET);
	return (int)position;
}


void GetError(uint shader)
{
	int result;
	int lengthinfo;
	char *infolog;
	glGetShaderiv(shader,GL_COMPILE_STATUS,&result);
	if(result == 0){
		glGetShaderiv(shader,GL_INFO_LOG_LENGTH,&lengthinfo);
		infolog = (char*)malloc(lengthinfo+20);
		glGetShaderInfoLog(shader,lengthinfo,NULL,&infolog[0]);
		printf("[ERROR]: %s\n",infolog);
	}
}

void GetErrorProgram(uint program)
{
	int result;
	int lengthinfo;
	char *infolog;
	glGetProgramiv(program,GL_LINK_STATUS,&result);
	if(result == 0){
		glGetProgramiv(program,GL_INFO_LOG_LENGTH,&lengthinfo);
		infolog = (char*)malloc(lengthinfo+20);
		glGetProgramInfoLog(program,lengthinfo,NULL,&infolog[0]);
		printf("[ERROR]: %s\n",infolog);
	}
}

uint LoadShaders(const char *vertex,const char *fragment)
{
	uint program = glCreateProgram();
	uint vertexid = glCreateShader(GL_VERTEX_SHADER);
	uint fragmentid = glCreateShader(GL_FRAGMENT_SHADER);
	FILE *fileVertex = fopen(vertex,"rb");
	FILE *fileFragment = fopen(fragment,"rb");
	int sizeVertex = sizeFile(fileVertex);
	int sizeFragment = sizeFile(fileFragment);
	char *codeVertex = (char*)malloc(sizeVertex+1);
	char *codeFragment = (char*)malloc(sizeFragment+1);
	fread(codeVertex,sizeVertex,1,fileVertex);
	codeVertex[sizeVertex] = '\0';
	fread(codeFragment,sizeFragment,1,fileFragment);
	codeFragment[sizeFragment] = '\0';

	glShaderSource(vertexid,1,(const char**)&codeVertex,NULL);
	glCompileShader(vertexid);
	GetError(vertexid);

	glShaderSource(fragmentid,1,(const char**)&codeFragment,NULL);
	glCompileShader(fragmentid);
	GetError(fragmentid);

	glAttachShader(program,vertexid);
	glAttachShader(program,fragmentid);
	glLinkProgram(program);
	GetErrorProgram(program);

	glDetachShader(program,vertexid);
	glDetachShader(program,fragmentid);

	glDeleteShader(vertexid);
	glDeleteShader(fragmentid);

	free(codeVertex);
	free(codeFragment);
	fclose(fileFragment);
	fclose(fileVertex);
	return program;
}

uint LoadShaders_t(const char *vertex,const char *fragment)
{
	uint program = glCreateProgram();
	uint vertexid = glCreateShader(GL_VERTEX_SHADER);
	uint fragmentid = glCreateShader(GL_FRAGMENT_SHADER);

	glShaderSource(vertexid,1,(const char**)&vertex,NULL);
	glCompileShader(vertexid);
	GetError(vertexid);

	glShaderSource(fragmentid,1,(const char**)&fragment,NULL);
	glCompileShader(fragmentid);
	GetError(fragmentid);

	glAttachShader(program,vertexid);
	glAttachShader(program,fragmentid);
	glLinkProgram(program);
	GetErrorProgram(program);

	glDetachShader(program,vertexid);
	glDetachShader(program,fragmentid);

	glDeleteShader(vertexid);
	glDeleteShader(fragmentid);

	return program;
}


uint LoadComp_t(const char *comp)
{
	uint program = glCreateProgram();
	uint shaderid = glCreateShader(GL_COMPUTE_SHADER);

	glShaderSource(shaderid,1,(const char**)&comp,nullptr);
	glCompileShader(shaderid);
	GetError(shaderid);

	glAttachShader(program,shaderid);
	glLinkProgram(program);
	GetErrorProgram(program);

	glDetachShader(program,shaderid);

	glDeleteShader(shaderid);

	return program;
}
