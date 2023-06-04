# PySDFGen

Python wrapper to [SDFGen](https://github.com/christopherbatty/SDFGen)

## Installation
Install from source 
``` bash
pip install .
```

## Dependencies 
Pybind11 for compiling the C++ source and NumPy.

## Example of use
A script and an example test mesh can be found in ```examples/```.
``` bash
cd examples
python PySDFGen_example.py ./data/cuboids.off ./data/cuboids.vtk
```
It will compute the SDF for the triangle mesh ```cuboids.off``` and save it in the file ```cuboids.vtk```. The legacy VTK file format is used. The resulting SDF can be visualized with [paraview](https://www.paraview.org/).
