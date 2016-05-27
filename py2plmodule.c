#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>
#include "DDS_FTWs.h"
#define GPIO_BASE_ADDRESS 	0x41200000
#define BRAM_BASE_ADDRESS 	0x40000000

#define DATA_OFFSET 	4
#define DIRECTION_OFFSET 	4
 
#define MAP_SIZE 4096UL
#define MAP_MASK (MAP_SIZE - 1)

//define an exception
//static PyObject *exmodError;

static PyObject* XilOut32(PyObject* self, PyObject *args){
	int memfd;
	void *mapped_base, *mapped_dev_base; 
	off_t dev_base = GPIO_BASE_ADDRESS; //default GPIO address
	PyObject *hop_list;
	int value;
	double len=0;
	if(!PyArg_ParseTuple(args, "Ii", &dev_base, &value))
	{
		return NULL;
	}

	memfd = open("/dev/mem", O_RDWR | O_SYNC);
    	if (memfd == -1) {
		printf("Can't open /dev/mem.\n");
		exit(0);
	}
	//printf("/dev/mem opened.\n");
	//printf("XilOut at address %p.\n", dev_base);  
    
	mapped_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, memfd, dev_base & ~MAP_MASK);
    	if (mapped_base == (void *) -1) {
		printf("Can't map the memory to user space.\n");
		exit(0);
	}
 	//printf("Memory mapped at address %p.\n", mapped_base); 
 
	mapped_dev_base = mapped_base + (dev_base & MAP_MASK);
	//for() 
	{
		*((unsigned long *) (mapped_dev_base + DATA_OFFSET*0)) = value;
		//*((unsigned long *) (mapped_dev_base + DATA_OFFSET)) = 1;
	}
	if (munmap(mapped_base, MAP_SIZE) == -1) {
		printf("Can't unmap memory from user space.\n");
		exit(0);
	}
	
	close(memfd);
	return Py_BuildValue("i", value);
}

static PyObject* XilOut_list(PyObject* self, PyObject *args){
	int memfd;
	void *mapped_base, *mapped_dev_base; 
	off_t dev_base = BRAM_BASE_ADDRESS; //default GPIO address
	PyObject *hop_list=NULL,*pvalue=NULL,*list=NULL;
	int value;
	Py_ssize_t len=0,i;
	if(!PyArg_ParseTuple(args, "IO",&dev_base, &hop_list))
	{
		printf("py opject parsing error\n");
		return NULL;
	}

	memfd = open("/dev/mem", O_RDWR | O_SYNC);
    	if (memfd == -1) {
		printf("Can't open /dev/mem.\n");
		exit(0);
	}
	//printf("/dev/mem opened.\n"); 
    
	mapped_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, memfd, dev_base & ~MAP_MASK);
    	if (mapped_base == (void *) -1) {
		printf("Can't map the memory to user space.\n");
		exit(0);
	}
 	//printf("Memory mapped at address %p.\n", mapped_base); 
 
	mapped_dev_base = mapped_base + (dev_base & MAP_MASK);
	
    len = PyList_GET_SIZE(hop_list);
    printf("List Length is = %d\n", len);
	for(i=0;i<len;i++) 
	{
		list = PySequence_Fast(hop_list, "expected a sequence");
		value = (int)PyInt_AsLong(PyList_GET_ITEM(list, i));

		//printf("Mapping Hop Array index number = %d\n", value);
		*((unsigned long *) (mapped_dev_base + DATA_OFFSET*i)) = FTWlookup[value];
		//*((unsigned long *) (mapped_dev_base + DATA_OFFSET)) = 1;
	}
	if (munmap(mapped_base, MAP_SIZE) == -1) {
		printf("Can't unmap memory from user space.\n");
		exit(0);
	}
	
	close(memfd);
	return Py_BuildValue("i", value);
}

static PyObject* XilIn32(PyObject* self, PyObject *args){
	int memfd;
	void *mapped_base, *mapped_dev_base; 
	off_t dev_base = BRAM_BASE_ADDRESS; //default GPIO address
	PyObject *hop_list;
	int value,offset;
	double len=0;
	if(!PyArg_ParseTuple(args, "Ii",&dev_base, &offset))
	{
		return NULL;
	}

	memfd = open("/dev/mem", O_RDWR | O_SYNC);
    	if (memfd == -1) {
		printf("Can't open /dev/mem.\n");
		exit(0);
	}
	//printf("/dev/mem opened.\n"); 
    
	mapped_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, memfd, dev_base & ~MAP_MASK);
    	if (mapped_base == (void *) -1) {
		printf("Can't map the memory to user space.\n");
		exit(0);
	}
 	//printf("Memory mapped at address %p.\n", mapped_base); 
 
	mapped_dev_base = mapped_base + (dev_base & MAP_MASK);
	//for() 
	{
		/* Read value from the device register */
		value = *((unsigned *)(mapped_dev_base + offset));
		printf("BRAM Address: value: %08x\n",value);
		//*((unsigned long *) (mapped_dev_base + DATA_OFFSET)) = 1;
	}
	if (munmap(mapped_base, MAP_SIZE) == -1) {
		printf("Can't unmap memory from user space.\n");
		exit(0);
	}
	
	close(memfd);
	return Py_BuildValue("i", value);
}


static PyMethodDef py2pl_methods[] = {
	{"XilOut32",   XilOut32, METH_VARARGS,"push data to pl address"},
    {"XilOut_list",   XilOut_list, METH_VARARGS,"push list data to pl BRAM address"},
    {"XilIn32",   XilIn32, METH_VARARGS,"pop value of bram offset address"},
    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initpy2pl(void)
{
    (void) Py_InitModule("py2pl", py2pl_methods);
}

