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

PyObject* hello_buffer(PyObject*, PyObject* args) {
    PyObject* arg1 = NULL;
    if (!PyArg_ParseTuple(args, "O", &arg1)) {
        return NULL;
    }

    Py_buffer buffer;
    if (PyObject_GetBuffer(arg1, &buffer, PyBUF_ND) != 0) {
        return NULL;
    }

    printf("Buffer shape:");
    for (int i = 0; i < buffer.ndim; ++i) {
        printf(" %d", buffer.shape[i]);
    }
    printf("\n");

    PyBuffer_Release(&buffer);

    Py_RETURN_NONE;
}

PyMethodDef methods[] = {
    { "hello", hello, METH_VARARGS, NULL },
    { "hello_buffer", hello_buffer, METH_VARARGS, NULL },
    { NULL, NULL, 0, NULL },
};

PyModuleDef module = {
    .m_name = "c_test",
    .m_methods = methods,
};

PyMODINIT_FUNC PyInit_c_test(void) {
    return PyModule_Create(&module);
}
