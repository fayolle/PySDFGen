import numpy as np
import os
import argparse
import PySDFGen
import sys


def readOFF(filename):
    f = open(filename)

    off = f.readline()
    off = off.strip()
    assert off.lower() == "off"

    # number of vertices, triangles, edges
    nums = f.readline()
    nums = nums.strip()
    nums = nums.split()
    assert len(nums) == 3
    num_verts = int(nums[0])
    num_faces = int(nums[1])
    num_edges = int(nums[2])

    # list of vertices
    verts = []
    for i in range(num_verts):
        line = f.readline()
        line = line.strip()
        line = line.split()

        # skip empty lines
        while len(line) == 0:
            line = f.readline()
            line = line.strip()
            line = line.split()

        verts.append((float(line[0]), float(line[1]), float(line[2])))

    # list of polygons
    tris = []
    for i in range(num_faces):
        line = f.readline()
        line = line.strip()
        line = line.split()
        num_vert = int(line[0])
        if num_vert != 3:
            raise Exception("Only triangle meshes are handled")

        tris.append((int(line[1]), int(line[2]), int(line[3])))

    f.close()
    return (np.array(verts), np.array(tris))


# Save field
def writeVTK(filename, res, field, spacing, origin):
    resx = res
    resy = res
    resz = res

    field_title = "VALUE"

    with open(filename, "w") as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("vtk output\n")
        f.write("ASCII\n")
        f.write("DATASET STRUCTURED_POINTS\n")
        f.write("DIMENSIONS " + str(resx) + " " + str(resy) + " " + str(resz) + "\n")
        f.write(
            "ORIGIN " + str(origin[0]) + " " + str(origin[1]) + " " + str(origin[2])
        )
        f.write(
            "SPACING " + str(spacing[0]) + " " + str(spacing[1]) + " " + str(spacing[2])
        )
        f.write("POINT_DATA " + str(resx * resy * resz) + "\n")
        f.write("SCALARS " + field_title + " double" + "\n")
        f.write("LOOKUP_TABLE default\n")

        np.savetxt(f, field)
        f.write("\n")


def main(argv):
    parser = argparse.ArgumentParser(description="Mesh to SDF")

    parser.add_argument("off_file_path", help="Path to the input mesh")
    parser.add_argument("vtk_file_path", help="Path to the output VTK file")
    parser.add_argument("--res", type=int, default=64, help="Regular grid resolution")
    parser.set_defaults()

    args = parser.parse_args(argv)

    assert os.path.isfile(args.off_file_path)
    res = args.res

    V, F = readOFF(args.off_file_path)
    (sdf, origin, spacing) = PySDFGen.compute_sdf(V, F, res)
    sdf_data = np.reshape(np.swapaxes(sdf, 0, 2), (res**3, 1))
    sdf_data = sdf_data.reshape(-1, 1)

    writeVTK(
        args.vtk_file_path,
        res,
        sdf_data,
        spacing=spacing,
        origin=origin
    )


if __name__ == "__main__":
    main(sys.argv[1:])
