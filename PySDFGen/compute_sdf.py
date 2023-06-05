import PySDFGen.native


def normalize_mesh(V, scale=1.0):
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


def compute_sdf(V, F, res=64, normalize=False):
    """Convert a mesh to an SDF. Wrapper to SDFGen."""
    if normalize:
        V = normalize_mesh(V)
    (sdf, origin, spacing) = PySDFGen.native.compute_sdf(V, F, res)

    return (sdf, origin, spacing)
