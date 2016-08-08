dia = '\\\\usdata011\MPRI-Public\DataAnalysis\Users'
ddata = 'Cristescu\MoffittAgg\Data'
fmat = 'moffitt_w_mut_14292_14_feb_2012_prim.mat'

mat = h5py.File(os.path.join(dia, ddata, fmat))
# mat.keys()
# #check if an object is a Group object
# mat['eg1'].get('signature_information', default=None, getclass=True) == h5py.Group

showMat(mat)
obj = mat['eg1']
mat2txt(obj)

# to see how the Matlab abuse the HDF5 format by putting the Cell Array into Reference objects
obj = mat['eg1']['signature_information']
key = 'signame'
objtmp = obj[key][()]
mat[objtmp[0,0]].value
map(chr, mat[objtmp[0,0].value)
