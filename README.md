# Zig/C extension using Zig build

> Note: This is just a testing stuff, see related work if you want something that actually works.

Playground for using Zig to build both Zig and C extensions.

Related stuff:
* [Ziggy-Pydust](https://github.com/spiraldb/ziggy-pydust): Framework for packaging Python extensions written in Zig.
* [zaml: Python Extension in Zig](https://github.com/adamserafini/zaml) (https://www.youtube.com/watch?v=AKhqFOdjUfg)
* [The Python Package Index Should Get Rid Of Its Training Wheels](https://kristoff.it/blog/python-training-wheels/)

## Using

Prerequisites:
* Poetry (`pip install poetry`)

Build packages using:
```
> poetry build
```
Install packages into your environment:
```
> poetry install
```
Run test script:
```
> python say_hello.py
```

