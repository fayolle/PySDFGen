#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <vector>
#include <limits>
#include <algorithm>
#include <cassert>

#include "makelevelset3.h"


pybind11::tuple
compute_sdf(pybind11::array_t<float> V,
	    pybind11::array_t<unsigned int> F,
	    int res)
{
  Vec3f min_box(std::numeric_limits<float>::max(),
		std::numeric_limits<float>::max(),
		std::numeric_limits<float>::max()), 
    max_box(-std::numeric_limits<float>::max(),
	    -std::numeric_limits<float>::max(),
	    -std::numeric_limits<float>::max());

  std::vector<Vec3f> vert_list;
  std::vector<Vec3ui> face_list;
  
  for (int i = 0; i < V.shape(0); ++i) {
    float x = V.at(i, 0);
    float y = V.at(i, 1);
    float z = V.at(i, 2);
    Vec3f point = Vec3f(x,y,z);
    vert_list.push_back(point);
    update_minmax(point, min_box, max_box);
  }

  for (int i = 0; i < F.shape(0); ++i) {
    unsigned int v0 = F.at(i, 0);
    unsigned int v1 = F.at(i, 1);
    unsigned int v2 = F.at(i, 2); 
    face_list.push_back(Vec3ui(v0,v1,v2));
  }

  Vec3f length = max_box - min_box;
  // Padding
  float max_length = std::max(length[0], std::max(length[1], length[2]));
  Vec3f unit(1,1,1);
  min_box -= 0.1f*max_length*unit;
  max_box += 0.1f*max_length*unit;
  length = max_box - min_box;
  // Cell size 
  max_length = std::max(length[0], std::max(length[1], length[2]));
  float delta = max_length/res;

  Array3f phi_grid;
  make_level_set3(face_list, vert_list, min_box, delta,
		  res, res, res, phi_grid);

  assert(phi_grid.ni == res);
  assert(phi_grid.nj == res);
  assert(phi_grid.nk == res);
  
  pybind11::array_t<float> sdf({res, res, res});
  for (int i = 0; i < res; i++) {
    for (int j = 0; j < res; j++) {
      for (int k = 0; k < res; k++) {
        sdf.mutable_at(i, j, k) = phi_grid(i, j, k);
      }
    }
  }

  pybind11::tuple origin = pybind11::make_tuple(min_box[0], min_box[1], min_box[2]);

  pybind11::tuple spacing = pybind11::make_tuple(delta, delta, delta); 

  pybind11::tuple sdf_grid = pybind11::make_tuple(sdf, origin, spacing);
  
  return sdf_grid;
}


PYBIND11_MODULE(native, m) {
  m.def("compute_sdf", &compute_sdf, "Python wrapper to SDFGen");
}
