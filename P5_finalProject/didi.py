# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:09:20 2016

@author: think
"""
import numpy as np
import pandas as pd
#from IPython.display import display
class Didi():
    
 @staticmethod
 def getFileList(FindPath,FlagStr=[]): 
  import os 
  FileList=[] 
  FileNames=os.listdir(FindPath) 
  if (len(FileNames)>0): 
   for fn in FileNames: 
    if (len(FlagStr)>0): 
     fullfilename=os.path.join(FindPath,fn) 
     FileList.append(fullfilename) 
 #对文件名排序 
  if (len(FileList)>0): 
   FileList.sort() 
  return FileList
 

  @staticmethod
  def processOrder():
   in_file_train='order_data_2016-01-01'
   inf_file_test='order_data_2016-01-23_test'
   order_data_train=pd.read_table(in_file_train, names=["order_id", "driver_id", "passenger_id", "start_district_hash","dest_district_hash","Price","Time"])
#order_data_test=pd.read_table(inf_file_test, names=["order_id", "driver_id", "passenger_id", "start_district_hash","dest_district_hash","Price","Time"])
   print order_data_train.head()
   print "======================================"
   
#print order_data_test.head()
#orderIsNotFulled=len(order_data['driver_id']=='dd65fa250fca2833a3a8c16d2cf0457c')
#print len(order_data_train[order_data_train['driver_id'].str.strip()=='NaN'])
def run():
     #processOrder('.',[])
    print processOrder()

if __name__ == '__main__':
    run()
