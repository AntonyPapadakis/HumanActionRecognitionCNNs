import os,sys,io,shutil,csv
from decimal import Decimal
import numpy as np

def unit_vector(vector):
  """ Returns the unit vector of the vector."""

  return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
  """Finds angle between two vectors"""

  v1_u = unit_vector(v1)
  v2_u = unit_vector(v2)
  return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def x_rotation(vector,theta):
  """Rotates 3-D vector around x-axis"""

  R = np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
  return np.dot(R,vector)

def y_rotation(vector,theta):
  """Rotates 3-D vector around y-axis"""

  R = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta), 0, np.cos(theta)]])
  return np.dot(R,vector)

def z_rotation(vector,theta):
  """Rotates 3-D vector around z-axis"""

  R = np.array([[np.cos(theta), -np.sin(theta),0],[np.sin(theta), np.cos(theta),0],[0,0,1]])
  return np.dot(R,vector)

def create_directories(workdir,counter,action,angle_id,label,theta_set):
  """creates the action directories required for our rotations"""

  counter+=1
  #making csv file in action directory for Right
  pathset=[]
  for theta in theta_set:
    path_by_theta =workdir + '/actions'+angle_id+"by"+str(theta)+'/' +str(label[0:4])+"_"+str(counter)+"_"+"action"+"_"+action+".csv"
    pathset.append(path_by_theta)


  #checking existence
  for path in pathset:
    if os.path.exists(path)==False:
      action_file = open(path,"w")
      action_file.close()
   
    else:
      #create
      action_file = open(path,"a")
      action_file.close()
      



  return counter, pathset


def rotation_by_angle(array_for_rotations,theta):
  """performs a single angle rotation"""

  w_string=""
  for coordinates in range(3,153,3):

      if(coordinates<=75 or (coordinates>75 and 0.0 not in array_for_rotations[0,76:150])):
          joint_array = np.array([array_for_rotations[0,coordinates-3],array_for_rotations[0,coordinates-2],array_for_rotations[0,coordinates-1]])

   
          new_vect = y_rotation(joint_array, theta)
          joint_array = new_vect
          
          w_string += str(joint_array[0])+','+str(joint_array[1])+','+str(joint_array[2])+','
      elif():
          joint_array = arr[0,i-3:i]
          w_string += str(joint_array[0])+','+str(joint_array[1])+','+str(joint_array[2])+','   

  return w_string

def rotate(datadir,labeldir,workdir):
  """main function performing the rotation"""

  pathS = datadir
  pathL = labeldir

  if workdir in os.getcwd():
    workdir = "."

  #skeleton directory
  dirSkeleton = os.listdir( pathS )

  #label directory
  dirLabel = os.listdir( pathL )

  theta_set=[]

  for theta in range(1,16):
    theta_set.append(theta)
    theta_set.append(theta+0.5)

  print(theta_set)  


  for angle_id in {"Left","Middle","Right"}:
    if os.path.exists(workdir + '/actions'+angle_id)==False: os.mkdir(workdir + '/actions'+angle_id)

    for theta in theta_set:
      if os.path.exists(workdir + '/actions'+angle_id+"by"+str(theta))==False: os.mkdir(workdir + '/actions'+angle_id+"by"+str(theta))



  #right middle and left action counters
  count_actionsR=0
  count_actionsM=0
  count_actionsL=0

  #initialization of action file variables
  action_file_original=""


  for data,label in zip(dirSkeleton,dirLabel):

    #ppp string to check the camera angle of each action 
    if "L" in label:
        angle_id ="Left"
    if "M" in label:
        angle_id ="Middle"
    if "R" in label:
        angle_id ="Right"        

    #single label path
    path_single_label = pathL + '/' + label

    #label file
    single_label_file = open(path_single_label)

    #line read
    line = single_label_file.readline()

    while line!="":

      #line values
      values = line.split(',')
      if len(values)<2:
          break

      #get values
      action = values[0]
      starting_action_frame = values[1]
      ending_action_frame = values[2]

      if "Right" in angle_id:
        count_actionsR, pathset = create_directories(workdir,count_actionsR,action,angle_id,label,theta_set)
        counter = count_actionsR
          
      if "Middle" in angle_id:
        count_actionsM, pathset = create_directories(workdir,count_actionsM,action,angle_id,label,theta_set)
        counter = count_actionsM
     
      if "Left" in angle_id:
        count_actionsL, pathset = create_directories(workdir,count_actionsL,action,angle_id,label,theta_set)
        counter = count_actionsL
          
      #data
      pathdat = pathS + '/' + label
      single_data_file = open(pathdat,"r")

      #write data
      for num_of_frame,dataLine in enumerate(single_data_file):
        #getting data according to frame instructions
        if num_of_frame >= int(starting_action_frame)-1 and num_of_frame<=int(ending_action_frame)-1:

            values = dataLine.split(' ')

            #writes data to the original file
            w_string_original=""

            w_string_theta=""


            
            array_for_rotations = np.zeros([1,150])

            for y in range(0,len(values)):
              array_for_rotations[0,y] = Decimal(values[y])

            #ORIGINAL FILE  

            path_original = workdir + '/actions'+angle_id+'/' +str(label[0:4])+"_"+str(counter)+"_"+"action"+"_"+action+".csv"
            action_file_original = open(path_original,"a")

            for coordinates in range(0,150):
              w_string_original += str(array_for_rotations[0,coordinates]) + ','


            #write string in the action file
            if(w_string_original!=""): 
                action_file_original.write(w_string_original)
                action_file_original.write("\n")              

            #ROTATION BY theta DEGREES ABOUT THE Y AXIS

            for theta,path in zip(theta_set,pathset):
              w_string_theta=rotation_by_angle(array_for_rotations,theta * np.pi/180)
                    
              action_file = open(path,"a")
              if(w_string_theta!=""): 
                  action_file.write(w_string_theta)
                  action_file.write("\n")


        elif num_of_frame>int(ending_action_frame):
            break


      #read new line
      line = single_label_file.readline()


