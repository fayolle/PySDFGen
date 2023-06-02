import PySDFGen.native


def normalize(V, scale=0.8):
    """
    Normalize a mesh given its vertices.
    Return the normalized vertices in (-1,-1,-1)x(1,1,1)
    """
    min_box = V.min(0)
    max_box = V.max(0)
    c = (min_box + max_box) * 0.5
    s = 2.0 * scale / (max_box - min_box).max()
    Vn = (V - c) * s

    return Vn


def compute_sdf(V, F, res=64):
    """Convert a mesh to an SDF. Wrapper to SDFGen."""
    Vn = normalize(V)
    sdf = PySDFGen.native.compute_sdf(Vn, F, res)

    return sdf
