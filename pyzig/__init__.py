import zig_test
import c_test


def hello(name):
    print("Hello zig!")
    zig_test.hello(name)
    print("Hello C!")
    c_test.hello(name)
