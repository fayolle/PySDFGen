import PySDFGen.native


def normalize(V, scale=0.9):
    """
    Normalize a mesh given its vertices.
    Return the normalized vertices in the unit box centered at the origin
    """
    min_box = V.min(0)
    max_box = V.max(0)
    c = (min_box + max_box) * 0.5
    s = 1.0 * scale / (max_box - min_box).max()
    Vn = (V - c) * s

    return Vn


def compute_sdf_normalized(V, F, res=64):
    """Normalize a mesh and convert a mesh to an SDF. Wrapper to SDFGen."""
    Vn = normalize(V)
    sdf = PySDFGen.native.compute_sdf_normalized(Vn, F, res)

    return sdf


def compute_sdf(V, F, res=64):
    """Convert a mesh to an SDF. Wrapper to SDFGen."""
    (sdf, origin, spacing) = PySDFGen.native.compute_sdf(V, F, res)

    return (sdf, origin, spacing)
