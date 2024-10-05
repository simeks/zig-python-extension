#include <stdio.h>

#include <Python.h>

PyObject* hello(PyObject*, PyObject* args) {
    const char* name = NULL;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    printf("Hello from C, %s\n", name);

    Py_RETURN_NONE;
}


PyMethodDef methods[] = {
    { "hello", hello, METH_VARARGS, NULL },
    { NULL, NULL, 0, NULL },
};

PyModuleDef module = {
    .m_name = "c_test",
    .m_methods = methods,
};

PyMODINIT_FUNC PyInit_c_test(void) {
    return PyModule_Create(&module);
}
