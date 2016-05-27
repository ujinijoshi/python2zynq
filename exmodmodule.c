#include <Python.h>

//define an exception
static PyObject *exmodError;

static PyObject* exmod_say_hello(PyObject* self, PyObject *args){
	const char* msg;
	int sts=0;
	
	//we expect at least 1 argument
	if(!PyArg_ParseTuple(args, "s", &msg)){
		return NULL;
	}

	if(strcmp(msg,"thid_is_an_error")==0){
		PyErr_SetString(exmodError, "System test exception");
		return NULL;	
	}else{
		printf("This is C \n message is :%s\n",msg);
		sts=21;
	}
	return Py_BuildValue("i", sts);
}

static PyObject* exmod_add(PyObject* self, PyObject *args)
{
	double a,b;
	double sts=0;
	if(!PyArg_ParseTuple(args, "dd", &a,&b))
	{
		return NULL;
	}

	sts = a + b;
	printf("This is C \n Addition 0f %f + %f = %f",a,b,sts);
	return Py_BuildValue("d",sts);
	
}

static PyMethodDef exmod_methods[] = {
	{"say_hello",   exmod_say_hello, METH_VARARGS,"Say Hello"},
    {"add",		exmod_add,       METH_VARARGS,"Add numbers"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initexmod(void)
{
    (void) Py_InitModule("exmod", exmod_methods);
}

