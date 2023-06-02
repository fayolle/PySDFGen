from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "PySDFGen.native",["src/pywrapper.cpp","src/makelevelset3.cpp"],
        include_dirs=["src"],
    ),
]

setup(
    name="PySDFGen",
    description="Python wrapper to SDFGen",
    packages=["PySDFGen"],
    package_dir={"PySDFGen": "PySDFGen"},
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    python_requires=">=3.6",
    install_requires=["numpy"],
)
