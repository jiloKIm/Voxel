def read_header(fp):
    line = fp.readline().strip()
    if not line.startswith(b'#binvox'):
        raise IOError('Not a binvox file')
    dims = list(map(int, fp.readline().strip().split(b' ')[1:]))
    translate = list(map(float, fp.readline().strip().split(b' ')[1:]))
    scale = list(map(float, fp.readline().strip().split(b' ')[1:]))[0]
    line = fp.readline()
    return dims, translate, scale

with open('base_3.binvox', 'rb') as f:
    model = read_header(f)

print(model)
import binvox_rw
import numpy as np

with open('base_3.binvox', 'rb') as f:
    model = binvox_rw.read_as_3d_array(f)

print(model.dims, model.translate, model.scale, model.axis_order, model.data)
with open('base_3.binvox', 'rb') as f:
    model = binvox_rw.read_as_coord_array(f)

print(model.data)
with open('base_3.binvox', 'rb') as f:
    model = binvox_rw.read_as_3d_array(f)
    model = binvox_rw.dense_to_sparse(model.data)

print(model)
