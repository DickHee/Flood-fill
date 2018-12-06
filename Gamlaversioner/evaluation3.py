import numpy as np

import sys
sys.setrecursionlimit(500000)
# -------- Test picture --------------
import cv2
import imageio as imio
import pylab
import matplotlib
from matplotlib import pyplot as plt

img = imio.imread("./blob3.png")
#plt.imshow(img)
#pylab.show()
imgA = imio.imread("./blob3.png")
imgA = imgA[:,:,0]
test = (imgA>200)*1

#print(test[1023,0])
#print(test.shape)
#print(test)

# ----------.....
#from PIL import Image
#aImg = Image.fromarray(tesh,'L')
#aImg.save("my.png")

# ------------------------------------
"""
test = np.zeros((10,10))
for xi in range(0,10):
    for yi in range(0,10):
        test[xi,yi]=xi-yi

print(test)
"""
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
filled = np.zeros((full_image_dim[0],full_image_dim[1]))
center_shift=np.asarray([-1,0,1])
#print(center_shift)

def floodfill(sub_matrix,center_row,center_col,cluster_id):
    # Center is part of cluster? No -> do nothin
    # Already filled? Yes -> do nothin
    # Fill center, floodfill surounding 8 pix, clusterId=clusterId+1
    global full_image
    if (sub_matrix[1,1] == 1) and filled[center_row,center_col]==0:# Part of cluster and not filled
        full_image[center_row,center_col] = cluster_id
        filled[center_row,center_col]=1

        xi = center_row + center_shift
        yi = center_col + center_shift

        not_edge = (xi[0]>0 and yi[0]>0) and \
                    (xi[2]<full_image_dim[0] and yi[0]>0) and \
                    (xi[0]>0 and yi[2]<full_image_dim[1]) and \
                    (xi[2]<full_image_dim[0] and yi[2]<full_image_dim[1])
        if not_edge:
            for xii in range(0,3):
                for yii in range(0,3):
                    floodfill(full_image[ xi[xii]-1:xi[xii]+1
                                         ,yi[yii]-1:yi[yii]+1]
                                         ,xi[xii],yi[yii],cluster_id)

        return(1) # Filled a cluster is filled
    else:
        return(0)


sub_matrices_dim = sub_matrices.shape

print("hello")

clusters=[]
cluster_id=2

for xi in range(0,sub_matrices_dim[0],2):
    for yi in range(0,sub_matrices_dim[1],2):
        print(cluster_id)
        cluster_id+=floodfill(sub_matrices[xi,yi,:,:],xi+1,yi+1,cluster_id) #????

print(cluster_id-2)
#print(filled)


"""
def apply_frame_function(frame, stride):
    #n, m = frame.shape
    #row_amount = n*m
    #feat_amount = (stride*2+1)*(stride*2+1)
    #out = zeros(row_amount,feat_amount)
    sub_shape = (stride*2+1,stride*2+1)
    strd = np.lib.stride_tricks.as_strided
    view_shape = tuple(np.subtract(frame.shape, sub_shape) + 1) + sub_shape
    strides = 2*frame.strides
    sub_matrices = strd(frame, view_shape, strides, writeable = False)
    a,b,c,d = sub_matrices.shape
    out = np.zeros((a*b,c*d))
    sub2 = sub_matrices.reshape(a*b,c*d)
    for rows in np.arange(c*d):
        out[:,rows] = sub2[:,rows]
    return(out)

k=apply_frame_function(test,1)

print(k.shape)
"""
