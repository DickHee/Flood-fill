import numpy as np

# -------- Test picture --------------
import cv2
import imageio as imio
import pylab
import matplotlib
from matplotlib import pyplot as plt

imgA = imio.imread("./blob3.png")
imgA = imgA[:,:,0]
full_image = (imgA>200)*1
full_image_dim = full_image.shape

print("image dim:",full_image_dim)
print("Full: ",full_image)



print("somestuff\n",(full_image==1)*1)


def floodFill(x,y,cluster_id):

    #print("floodfill", x,y,full_image[x,y])
    if full_image[x,y]==1:
        toFill = set()
        toFill.add((x,y))
        while len(toFill)!=0:
            (xi,yi) = toFill.pop()
            full_image[xi,yi] = cluster_id # Fill

            for xii in [-1,0,1]:
                for yii in [-1,0,1]:
                    if not (xii==0 and yii==0):
                        cx = xi + xii
                        cy = yi + yii

                        in_bound = cx>=0 and cx<=full_image_dim[0]-1 and\
                                    cy>=0 and cy<=full_image_dim[1]-1

                        if in_bound:
                            if full_image[cx,cy]==1:
                                toFill.add((cx,cy))
        return(1)
    else:
        return(0)

"""
xi=1
yi=1
while xi < sub_matrices_dim[0]:
    while yi < sub_matrices_dim[1]:
        cluster_id+=floodFill(xi,yi,cluster_id)
        if xi+3 < sub_matrices_dim[0]:
            xi = xi+3
        else:
            xi = sub_matrices_dim[0]-2
        if yi+3 < sub_matrices_dim[1]:
            yi = yi+3
        else:
            yi = sub_matrices_dim[1]-2
"""

cluster_id=2
for xi in range(1,full_image_dim[0],2):
    for yi in range(1,full_image_dim[1],2):
        cluster_id+=floodFill(xi,yi,cluster_id)

print("cluster: ",cluster_id, cluster_id-2)


cluster_areas=[]
cluster_x=[]
cluster_y=[]

cluster_coordinates = [[],[]]

nbr_clusters = cluster_id-2

# ---- Cluster areas and mass center ----
coordinates = np.mgrid[0:full_image_dim[0],0:full_image_dim[1]]
                                #(rows/cols,x,y)

if nbr_clusters>0:
    for cluster in range(0,nbr_clusters):
        current_cluster = full_image==2+cluster

        c_a=np.sum(current_cluster)
        cluster_areas.append(c_a)

        print(c_a)
        print("hmmm:\n",np.multiply(coordinates[0,:,:],current_cluster))
        print("hmmm:\n",np.multiply(coordinates[1,:,:],current_cluster))

        c_x = round(np.sum(np.multiply(coordinates[0,:,:],current_cluster))/c_a)
        c_y = round(np.sum(np.multiply(coordinates[1,:,:],current_cluster))/c_a)
        cluster_x.append(int(c_x))
        cluster_y.append(int(c_y))

        cluster_coordinates[0].append(int(c_x))
        cluster_coordinates[1].append(int(c_y))

print(cluster_areas)
print(cluster_x)
print(cluster_y)

print(cluster_coordinates)
