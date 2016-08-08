dia = '\\\\usdata011\MPRI-Public\DataAnalysis\Users'
ddata = 'Huang\proj_Vax_HIVtat\Data'
fmat = 'mHIV_PID20379Aug2012_EG.mat'

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


#test = scipy.io.loadmat(os.path.join(dia, ddata, fmat), squeeze_me=True, chars_as_strings=True,mat_dtype=True, struct_as_record=True)