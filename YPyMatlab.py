
"""@package YPyMatlab

Python module for loading and exporting Matlab data structure

Supports both version 7.3 and version 7.1 (or earlier) of Matlab

"""

import h5py, io, os, scipy, numpy, re

def showMat(obj,level=None):
	""" Show all elements in a Mat(lab) (version >7.1) data structure """
	step = 3
	if level is None:
		level = 3
		print obj
	else:
		print '.'*(level-step), obj
	for key in obj.keys(): 
		#print 'name=', key, ' >>>>>> ', obj.get(key, default=None, getclass=True), ' >>>>>> size=', len(obj[key])		
		if isinstance(obj[key], h5py.Dataset):	
			print '.'*level, 'name=', key, ' >>>>>> ', obj.get(key, default=None, getclass=True), ' >>>>>> size=', obj[key].shape
		if isinstance(obj[key], h5py.Group):
			#print '.'*level, 'Here'
			#print '.'*level,obj[key]			
			if len(obj[key])>100:
				print '.'*(level), obj[key]
				#print '.'*level, 'name=', key, ' >>>>>> ', obj.get(key, default=None, getclass=True), ' >>>>>> size=', len(obj[key])
				print ' '*8, 'Length=', len(obj[key]), '... Too many group members...skip'
			else:
				showMat(obj[key], level+step)
	return

def getMatCell (obj, mat):
	if type(obj) == h5py.Reference: 
		getMatCell(mat[obj],mat)
	elif type(obj)==h5py.Dataset and obj.dtype==h5py.Reference:
		objsize = obj.shape
		if len(objsize)==2:
			if objsize[0]==1 and objsize[1]==1:				
				print ''.join(map(chr, mat[obj[0,0]].value))
				return ''.join(map(chr, mat[obj[0,0]].value))			
			elif objsize[0]>2 or objsize[1]>2:
				return map(lambda o: getMatCell(mat[o[0]], mat), obj)
		else:
			print 'Error'
	else:
		print 'getMatCell(): Not Matlab Cell data type'
	return

	
def mat2txt (obj):
	"""
	Export elements in a Mat(lab) data structure into text files
	
	Need better understanding of h5py.Reference type, which seems to be pointers. Eg.,
	x = mat[mat['eg1']['signature_information']['signame'][0,825]].value
	print ''.join(map(chr,x))
	As of now, assuming all numeric variables are in NxP matrix (float), all string 
	variables are in a 1xN or Nx1 vector form
	"""	
	#key = 'batch'
	#obj = mat['eg1']
	for key in obj.keys():
	
		print obj[key].name, '.'*6
	
		# Group object (not Dataset), recursively traverse one level down
		if type(obj[key]) == h5py.Group:
			mat2txt(obj[key])
		elif type(obj[key]) == h5py.Dataset and obj[key].dtype==h5py.Reference:
			ret = getMatCell(obj[key], mat)
			ret = map(lambda s: s or "", ret)
			open(obj[key].name.replace('/','_')+'.txt','w').write('\n'.join(ret))
		# Dataset is a Reference type, need to get the strings stored in Reference
		# Need to watch out the dimension of the Dataset
		elif obj[key].dtype == h5py.Reference:
			objsize = obj[key].shape
			""" need to be 2-d Reference vector"""
			if len(objsize) <> 2:
				continue
			if objsize[0]<>1 and objsize[1]<>1:
				continue
			
			""" get the value """
			objtmp = obj[key][()]
			
			if objsize[0]==1:
				""" 1xN row vector """
				#x = mat[mat['eg1']['batch'][0,14290]].value	
				#print ''.join(map(chr,x))
				ret = map(lambda o: ''.join(map(chr, obj[o].value)), objtmp[0,])
			
			if objsize[1]==1:
				""" Nx1 column vector """
				#x = mat[mat['eg1']['covsymbol'][1,0]].value
				#print ''.join(map(chr,x))
				ret = map(lambda o: ''.join(map(chr, obj[o].value)), objtmp[:,0])
			
			""" clean up empty strings '\x00' """
			ret = map(lambda s: s.replace('\x00', ''), ret)
			
			open(obj[key].name.replace('/','_')+'.txt','w').write('\n'.join(ret))		
		
		
		elif type(obj[key])==h5py.Dataset and obj[key].dtype in ['float32','float64']:
			""" Dataset is primitive float type, export directly """		
			numpy.savetxt(obj[key].name.replace('/','_')+'.txt', obj[key], fmt='%0.6f', delimiter=',')
		# if type(obj[key])==h5py.Dataset and obj[key].dtype == 'float32':
			# numpy.savetxt(obj[key].name.replace('/','_')+'.txt', obj[key], fmt='%0i', delimiter=',')
		# if type(obj[key])==h5py.Dataset and obj[key].dtype == 'float64':	
			# numpy.savetxt(obj[key].name.replace('/','_')+'.txt', obj[key], fmt='%0.6f', delimiter=',')
		
		else:
			print 'Object type is not supported', type(obj[key])
	return



def showMat7(obj,level=None,prefix=None):
	""" 
	Show all elements in a Mat(lab) (version <7.1) data structure
	
	PARAMETERS
		obj 	an nump.ndarry object
	
	USAGE:
		dia = '\\\\usdata011\MPRI-Public\DataAnalysis\Users'
		ddata = 'nebozhyn\CBD\CBD-2011'
		fmat = 'eg_CBD-2011_613x57060_04-10-2012.mat'
		test = scipy.io.loadmat(os.path.join(dia, ddata, fmat), squeeze_me=True, chars_as_strings=True,mat_dtype=True, struct_as_record=True)
		obj=test['eg']
		showMat7(obj)	
	"""
	step = 3
	if level is None:
		level = 3
		print obj.dtype.names
	else:
		print '.'*(level-step), prefix, ': ', obj.dtype.names
	for e in obj[()].dtype.names:
		if obj[e][()].dtype.names != None:
			showMat7(obj[()][e], level+step, prefix=e)
		else:
			print '.'*level, 'name =', e, ">>>",  obj[e][()].dtype
	return




def mat2txt7 (obj, outprefix='', outsuffix='.mat2txt'):
	"""
	Export elements in a Mat(lab) data structure into text files
	
	Only works with Matlab version 7.1 or earlier

	PARAMETERS
		obj 	an nump.ndarry object
		
	USAGE
		mat2txt(test['eg'])

	"""
	for e in obj[()].dtype.names:
		if obj[e][()].dtype.names != None:
			mat2txt7(obj[()][e], outprefix, outsuffix)
		elif obj[e][()].dtype in ['float32','float64']:
			""" Dataset is primitive float type, export directly """
			""" numpy.savetxt( e+'.txt', obj[e][()], fmt='%0.6f', delimiter=',') """
			numpy.savetxt( outprefix + e + outsuffix, obj[e][()], fmt='%0.6f', delimiter=',')		
		else:
			""" f = open( e+'.txt','w') """
			f = open( outprefix + e + outsuffix,'w')
			if obj[e][()].size == 1:
				f.write("%s\n" % obj[e][()][()])
			else:
				for item in obj[e][()]:
					f.write("%s\n" % item[()])
			f.close()
	return

	
	
