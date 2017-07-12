# 主要是基于dlib库实现人脸的人脸识别和关键点检测
#
# dlib的人脸识别是基于HOG特征的，效果要好于opencv自带的HAAR特征人脸检测，而且可以返回cofidence
#
# face_recognition主要提供两个文件，一个是人脸关键点比对，另一个是人脸特征描述的
#
# 人脸识别原理主要是在初次检测到人脸时，提取关键点，并保存描述子，当再次被检测到时，重复相同的过程，然后计算两个描述子的欧拉距离
#
#  依然是一种物理检测方法，类似于Eigen，Fish等特征实现的人脸检测。在小样本情况下可以得到好的效果，但当库增大时，识别速度会大大降低，也是传统方法的弊端
#
#

import cv2
import os
import face_recognition
import dlib

labels=[]
encode=[]

#save the descriptor of face as txt , if exists , loading
def init():
    global labels
    global  encode
    if not os.path.exists('./source'):
        os.makedirs('./source')
    else:        
        if not os.path.exists('./source/labels.txt'):
            os.chdir("./source")
            os.mknod("labels.txt")
            os.chdir("..")
            
        else:
            f_label=open('./source/labels.txt','r')
            temp1=f_label.read()
            f_label.close()
            labels=eval(temp1)

        if not os.path.exists('./source/encode.txt'):
            os.chdir("./source")
            os.mknod("encode.txt")
            os.chdir("..")
            
        else:
            f_encode=open('./source/encode.txt','r')
            temp2=f_encode.read()
            f_encode.close()
            encode=eval(temp2)

    return labels,encode

# add a new face to facesets
def add_face(img):

    location=face_recognition.face_locations(img)
    encoding=face_recognition.face_encodings(img,location)[0].tolist()
    
    label=raw_input("Enter your input: ")
    labels.append(label)
    encode.append(encoding)

    f_label=open('./source/labels.txt','w+')
    f_label.write(str(labels))
    f_label.close()

    f_encode=open('./source/encode.txt','w+')
    f_encode.write(str(encode))
    f_encode.close()

    print 'succeed to add_face : %s : %s' %(str(label),str(encoding))
    
#detect face 
def detect(frame):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        for i in xrange(len(encode)):
            match = face_recognition.compare_faces([encode[i]], face_encoding)

            name = "Unknown"

            if match[0]:
                name = labels[0]



            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            return frame

if __name__=='__main__':
    
    print 'initial unfinished. \n labels:\n %s \n %s encode : \n %s \n ' %(str(labels),'*'*30,str(encode))
    labels,encode=init()
    print 'initial finished. \n labels:\n %s \n %s encode : \n %s \n ' %(str(labels),'*'*30,str(encode))

    cv2.namedWindow('Video',1)

    cap=cv2.VideoCapture(0)

    while True:

        ret,frame=cap.read()
  

        detected_face=dlib.get_frontal_face_detector()
        dst=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        face=detected_face(dst,1)
        
        if face:
            if not (labels and encode):
                add_face(frame)
        
       image=detect(frame)
	try:
        	cv2.imshow('Video', image)
	except:
		cv2.imshow('Video',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('a'):
            add_face(frame)


cap.release()
cv2.destroyAllWindows()
