#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *nand(PyObject *self, PyObject *args) {
    int a, b;
    if(!PyArg_ParseTuple(args, "pp", &a, &b))
        return NULL;
    int out = !(a&b);
    return PyBool_FromLong(out);
}

static PyMethodDef PrimChipsMethods[] = {
    {
        "nand",
        nand,
        METH_VARARGS,
        "Python interface for NAND chip written in C",
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef primChipsModule = {
    PyModuleDef_HEAD_INIT,
    "nirvana",
    "Python interface for primitive chips written in C, handed by God.",
    -1,
    PrimChipsMethods,
};

PyMODINIT_FUNC PyInit_nirvana(void) {
    return PyModule_Create(&primChipsModule);
}
