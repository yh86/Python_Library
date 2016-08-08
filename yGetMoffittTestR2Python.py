import os, shutil
#
# import in YS matlab library
#
execfile('YPyMatlab.py')

dia = '\\\\usdata011\MPRI-Public\DataAnalysis\Users'
ddata = 'Cristescu\MoffittAgg\Data'
fmat = 'moffitt_cnv_mut_os_nov12.mat'
fmatFullName = os.path.join(dia, ddata, fmat)

#
# copy file into local directory for faster process (reduce network slowing down)
#
#shutil.copy2( fmatFullName, './' )

#
# read in meta data of matlab data structure 
#mat = h5py.File(os.path.join(dia, ddata, fmat))
mat = h5py.File (fmatFullName)

# # mat.keys()
# # #check if an object is a Group object
# # mat['eg1'].get('signature_information', default=None, getclass=True) == h5py.Group

# showMat(mat)
# obj = mat['eg1']
# mat2txt(obj)


mat.keys()  # pay attention if the eg structure is called 'eg' or 'eg1' or something else

showMat(mat)
showMatLog(obj=mat,fname='ypymatlab_showMat.log', sourceName=fmatFullName) # create the log file of eg contents
#obj = mat['eg']
# export data into text file ".mat2txt"
#mat2txt(obj,mat)

#
# # to see how the Matlab abuse the HDF5 format by putting the Cell Array into Reference objects
# obj = mat['eg1']['signature_information']
# key = 'signame'
# objtmp = obj[key][()]
# mat[objtmp[0,0]].value
# map(chr, mat[objtmp[0,0].value)
#
