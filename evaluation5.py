import numpy as np

import sys
sys.setrecursionlimit(500000)
# -------- Test picture --------------
import cv2
import imageio as imio
import pylab
import matplotlib
from matplotlib import pyplot as plt

#img = imio.imread("./blob2.png")
#plt.imshow(img)
#pylab.show()
imgA = imio.imread("./blob5.png")
imgA = imgA[:,:,0]
test = (imgA>200)*1

print(test.shape)
#print(test)

# ---- Extract submatrices
strd = np.lib.stride_tricks.as_strided
stride=1
sub_shape = (stride*2+1,stride*2+1)
strides = 2*test.strides
view_shape = tuple(np.subtract(test.shape, sub_shape) + 1) + sub_shape
#print(sub_shape),print(view_shape),print(strides)
sub_matrices = strd(test,view_shape,strides,writeable=False)
#print(sub_matrices)




full_image = test
full_image_dim = full_image.shape
filled = np.zeros((full_image_dim[0],full_image_dim[1]), dtype=int)
center_shift=np.asarray([-1,0,1])
#print(center_shift)


def floodfill(sub_matrix,center_row,center_col,cluster_id):
    # Center is part of cluster? No -> do nothin
    # Already filled? Yes -> do nothin
    # Fill center, floodfill surounding 8 pix
    global full_image
    if (sub_matrix[1,1] == 1) and filled[center_row,center_col]==0:# Part of cluster and not filled
        full_image[center_row,center_col] = cluster_id
        filled[center_row,center_col]=1

        xi = center_row + center_shift
        yi = center_col + center_shift


        for xii in range(0,3):
            for yii in range(0,3):
                not_edge = xi[xii]>0 and xi[xii]<full_image_dim[0]-1 and\
                            yi[yii]>0 and yi[yii]<full_image_dim[1]-1
                print("xi,yi:",xi[xii],yi[yii])
                print("xii,yii:",xii,yii)
                print("not edge ", not_edge)
                if not_edge:
                    dimshit=full_image[ xi[xii]-1:xi[xii]+2, yi[yii]-1:yi[yii]+2].shape
                    if dimshit[0]!=3 or dimshit[1]!=3:
                        print("xi,yi:",xi[xii],yi[yii])
                        print("xii,yii:",xii,yii)
                        print("not edge ", not_edge)
                        print("range x:", xi[xii]-1,xi[xii]+2)
                        print("range y:", yi[yii]-1,yi[yii]+2)
                        print("full:\n",full_image[ xi[xii]-1:xi[xii]+2, yi[yii]-1:yi[yii]+2])
                    floodfill(full_image[ xi[xii]-1:xi[xii]+2, yi[yii]-1:yi[yii]+2]
                                        ,xi[xii],yi[yii],cluster_id)
                else:
                    #print("sub mat:\n",sub_matrix)
                    #print(sub_matrix[xii,yii] == 1)
                    #print(filled[xi[xii],yi[yii]]==0)
                    if (sub_matrix[xii,yii] == 1) and filled[xi[xii],yi[yii]]==0:
                        full_image[xi[xii],yi[yii]] = cluster_id
                        filled[xi[xii],yi[yii]]=1
        return(1)
    else:
        return(0)

#print("hello")
#print("filled :\n",filled[0:full_image_dim[0],0:full_image_dim[1]])
#print("full : \n",full_image[0:full_image_dim[0],0:full_image_dim[1]])


clusters=[]
cluster_id=2
sub_matrices_dim = sub_matrices.shape
"""
print("sub mat dim: ",sub_matrices_dim)
for xi in range(0,sub_matrices_dim[0]):
    for yi in range(0,sub_matrices_dim[1]):
        cluster_id+=floodfill(sub_matrices[xi,yi,:,:],xi+1,yi+1,cluster_id) #????
"""


floodfill(sub_matrices[91,64,:,:],91+1,64+1,cluster_id)
#print("cluster: ",cluster_id, cluster_id-2)


"""
print("---------range stuff")
fork= np.zeros((5,5))
for i in range(0,5):
    for j in range(0,5):
        fork[i,j]=i-j

print(fork)
a=1
b=1
print(fork[a-1:a+2,b-1:b+2])
a=3
print(fork[a-1:a+2,b-1:b+2])
print("---------range stuff")
print("hello")
print("filled :\n",filled[0:10,0:10])
print("full : \n",full_image[0:10,0:10])
print("flood 1")
cluster_id+=floodfill(sub_matrices[0,0,:,:],0+1,0+1,cluster_id)
print("Cluster id",cluster_id)
print("filled :\n",filled[0:10,0:10])
print("full : \n",full_image[0:10,0:10])

print(sub_matrices[1,1,:,:])
print("flood 2")
cluster_id+=floodfill(sub_matrices[1,1,:,:],1+1,1+1,cluster_id)
print("filled :\n",filled[0:10,0:10])
print("full : \n",full_image[0:10,0:10])

print(cluster_id)
print(cluster_id-2)


#print(filled)
#print(full_image)
"""
