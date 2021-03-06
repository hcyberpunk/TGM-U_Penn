# -*- coding: utf-8 -*-
"""Prediction_Script_TGM.ipynb

"""
import keras_preprocessing
from keras.models import Sequential, Model
from keras.layers import Input
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
from keras.layers import UpSampling3D
from keras.layers.convolutional import MaxPooling3D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv3D, Conv2D
from keras.optimizers import RMSprop, Adam, Adadelta, Adagrad, SGD
from sklearn.metrics import mean_squared_error
from argparse import ArgumentParser
import numpy as np
import glob
from nilearn.image import math_img
import nibabel as nb
import os
import itertools
from keras.models import model_from_json
import sys

def bbox(img):

    r = np.any(img, axis=(1, 2))
    c = np.any(img, axis=(0, 2))
    z = np.any(img, axis=(0, 1))

    rmin, rmax = np.where(r)[0][[0, -1]]
    cmin, cmax = np.where(c)[0][[0, -1]]
    zmin, zmax = np.where(z)[0][[0, -1]]

    return rmin, rmax, cmin, cmax, zmin, zmax


def process():
    model_input = []
    t1 = []
    t1gd = []
    t2 = []
    flair = []
    gbm = []

    for ti in glob.glob(filepath+"/**/*_t1.nii.gz"):
      t1.append(ti)

    for tigd in glob.glob(filepath+"/**/*_t1Gd.nii.gz"):
      t1gd.append(tigd)

    for tii in glob.glob(filepath+"/**/*_t2.nii.gz"):
      t2.append(tii) 

    for flaiir in glob.glob(filepath+"/**/*_flair.nii.gz"):
      flair.append(flaiir)

    for gbmc in glob.glob(filepath+"/**/*_GlistrBoost_ManuallyCorrected.nii.gz"):
      gbm.append(gbmc) 

    n=0

    for (i,j,k,l,m) in zip(t1, t1gd, t2, flair, gbm):
      im5 = math_img('img > 1', img=m)
      im1 = nb.load(i)
      im2 = nb.load(j)
      im3 = nb.load(k)
      im4 = nb.load(l)
      #im5 = nb.load(img_path5)
      img1 = np.logical_and(im1, im5)
      img2 = np.logical_and(im2, im5)
      img3 = np.logical_and(im3, im5)
      img4 = np.logical_and(im4, im5)
      img5 = img1.get_data()
      img6 = img2.get_data()
      img7 = img3.get_data()
      img8 = img4.get_data()
      rmin1, rmax1, cmin1, cmax1, zmin1, zmax1 = bbox(img5)
      rmin2, rmax2, cmin2, cmax2, zmin2, zmax2 = bbox(img6)
      rmin3, rmax3, cmin3, cmax3, zmin3, zmax3 = bbox(img7)
      rmin4, rmax4, cmin4, cmax4, zmin4, zmax4 = bbox(img8)
      i1 = img5[rmin1:rmin1+94,cmin1:cmin1+85,zmin1:zmin1+72]
      i2 = img6[rmin2:rmin2+94,cmin2:cmin2+85,zmin2:zmin3+72]
      i3 = img7[rmin3:rmin3+94,cmin3:cmin3+85,zmin3:zmin3+72]
      i4 = img8[rmin4:rmin4+94,cmin4:cmin4+85,zmin4:zmin4+72]
      #img5 = nb.load(img_path5).get_data()
      #plot_anat(img5)
      #image = np.stack((i1,i2,i3,i4),axis=-1)
      image = np.dstack((i1,i2,i3,i4))
      #let1 = nilearn.image.new_img_like(im1,i1 )
      #plot_anat(let1)
      model_input.append(image)
      n+=1
      print("{} File(s) Loaded".format(n))
    return model_input

filepath = sys.argv[1]
modelpath = sys.argv[2]

model_input = process()
x = np.asarray(model_input)


json_file1 = open(modelpath+'/model_p1.json', 'r')
loaded_model_json1 = json_file1.read()
json_file1.close()
loaded_model1 = model_from_json(loaded_model_json1)

loaded_model1.load_weights(modelpath+"/model_p1.h5")
print("Model_p1 Loaded model from disk")

json_file2 = open(modelpath+'/model_dw.json', 'r')
loaded_model_json2 = json_file2.read()
json_file2.close()
loaded_model2 = model_from_json(loaded_model_json2)

loaded_model2.load_weights(modelpath+"/model_dw.h5")
print("Model_dw Loaded model from disk")

json_file3 = open(modelpath+'/model_t1.json', 'r')
loaded_model_json3 = json_file3.read()
json_file3.close()
loaded_model3 = model_from_json(loaded_model_json3)

loaded_model3.load_weights(modelpath+"/model_t1.h5")
print("Model_t1 Loaded model from disk")

pred_p1 = loaded_model1.predict(x)
pred_dw = (loaded_model2.predict(x))*1e-9
pred_t1 = loaded_model3.predict(x)

print("\n")
print("p1 prediction:")
print(pred_p1)
print("\n")
print("dw prediction:")
print(pred_dw)
print("\n")
print("t1 prediction:")
print(pred_t1)
