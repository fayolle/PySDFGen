#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <vector>

#include "makelevelset3.h"


pybind11::array_t<float>
compute_sdf(pybind11::array_t<float> V,
	    pybind11::array_t<unsigned int> F,
	    int res)
{
  std::vector<Vec3f> vert_list;
  std::vector<Vec3ui> face_list;
  
  for (int i = 0; i < V.shape(0); ++i) {
    float x = V.at(i, 0);
    float y = V.at(i, 1);
    float z = V.at(i, 2);
    vert_list.push_back(Vec3f(x,y,z));
  }

  for (int i = 0; i < F.shape(0); ++i) {
    unsigned int v0 = F.at(i, 0);
    unsigned int v1 = F.at(i, 1);
    unsigned int v2 = F.at(i, 2); 
    face_list.push_back(Vec3ui(v0,v1,v2));
  }

  
  // The mesh is already normalized
  Vec3f min_box(-1.f, -1.f, -1.f);
  float delta_x = 2.f / (float)res;

  Array3f phi_grid;
  make_level_set3(face_list, vert_list, min_box, delta_x,
		  res, res, res, phi_grid);

  
  pybind11::array_t<float> sdf({res, res, res});
  for (int i = 0; i < res; i++) {
    for (int j = 0; j < res; j++) {
      for (int k = 0; k < res; k++) {
        sdf.mutable_at(i, j, k) = phi_grid(i, j, k);
      }
    }
  }
  
  return sdf;
}

PYBIND11_MODULE(native, m) {
  m.def("compute_sdf", &compute_sdf, "Python wrapper to SDFGen");
}
