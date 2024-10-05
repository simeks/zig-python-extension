const std = @import("std");
const c = @cImport({
    @cInclude("Python.h");
});

const PyObject = [*c]c.PyObject;

var methods = [_]c.PyMethodDef{
    .{
        .ml_name = "hello",
        .ml_meth = hello,
        .ml_flags = c.METH_VARARGS,
        .ml_doc = hello_docs,
    },
    .{},
};

var module = c.PyModuleDef{
    .m_name = "zig_test",
    .m_methods = &methods,
};

export fn PyInit_zig_test() *c.PyObject {
    return c.PyModule_Create(&module);
}

const hello_docs =
    \\ Say hello!
    \\ Args:
    \\     name: Your name
;

fn hello(_: PyObject, args: PyObject) callconv(.C) PyObject {
    var name: [*:0]const u8 = undefined;
    if (c.PyArg_ParseTuple(args, "s", &name) == 0) {
        return null;
    }

    std.debug.print("Hello from zig, {s}\n", .{name});

    // This is basically what the Py_RETURN_NONE macro is doing in C,
    // Learned the hard way that for Python >=3.12 we can just write c.Py_None
    // thanks to immortal objects, but for older versions we need the ref count.
    return c.Py_NewRef(c.Py_None());
}
