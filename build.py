import platform
import subprocess
import sys
import sysconfig

from pathlib import Path

from setuptools import Extension
from setuptools.command.build_ext import build_ext

try:
    import numpy
except ImportError:
    pass


def build(setup_kwargs):
    setup_kwargs.update(
        {
            "ext_modules": [
                ZigExtension("zig_test", ["src/zig_test.zig"]),
                ZigExtension("c_test", ["src/c_test.c"]),
            ],
            "cmdclass": {"build_ext": ZigBuildExt},
        }
    )


class ZigExtension(Extension):
    def __init__(self, name, sources):
        super().__init__(name, sources)


class ZigBuildExt(build_ext):
    def initialize_options(self) -> None:
        return super().initialize_options()

    def finalize_options(self) -> None:
        return super().finalize_options()

    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        if not isinstance(ext, ZigExtension):
            raise RuntimeError("Not a ZigExtension")

        python_include_dir = Path(sysconfig.get_path("include"))

        # If path is not in LIBDIR (windows), make a guess
        python_lib_dir = python_include_dir.parent / "libs"
        if lib_dir := sysconfig.get_config_var("LIBDIR"):
            python_lib_dir = lib_dir

        python_lib = "python3"
        if lib_version := sysconfig.get_config_var("LDVERSION"):
            python_lib = f"python{lib_version}"

        target_path = Path(self.get_ext_fullpath(ext.name))

        args = [
            sys.executable,
            "-m",
            "ziglang",
            "build-lib",
            "-OReleaseFast",
            "-dynamic",
            f"-I{python_include_dir}",
            f"-L{python_lib_dir}",
            "-lc",
            f"-l{python_lib}",
            f"-femit-bin={target_path}",
            "-fno-emit-implib",
        ]

        # TODO: Using non-MSVC builds for extensions is likely a recipe for
        # disaster, but I really don't want to depend on MSVC :(
        # # For compatibility with CPython we want to use MSVC on Windows
        # if platform.system() == "Windows":
        #     args.extend(["-target", "x86_64-windows-msvc"])

        subprocess.run(args + ext.sources)

        # Clean-up of files we don't want to distribute
        pdb_path = target_path.with_suffix(".pdb")
        pdb_path.unlink(True)
        obj_path = Path(f"{target_path}.obj")
        obj_path.unlink(True)
