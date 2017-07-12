# 
# 收集不同的人脸数据，通过设定thresh可以保证样本的多样性
#
#

import face_recognition_models
import cv2
import dlib
import os
import sys
import numpy as np

thresh=eval(sys.argv[1])

class get_data:
    def __init__(self,filepath):
        self.path=filepath
        self.detector=dlib.get_frontal_face_detector()
        self.win=dlib.image_window()
        self.predictor_model = face_recognition_models.pose_predictor_model_location()
        self.pose_predictor = dlib.shape_predictor(self.predictor_model)

        self.face_recognition_model = face_recognition_models.face_recognition_model_location()
        self.face_encoder = dlib.face_recognition_model_v1(self.face_recognition_model)


    def run(self):
        cap=cv2.VideoCapture(0)
        count=1
        first=True
        
        if cap.isOpened():
            while True:

                ret,frame=cap.read()
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=self.detector(frame,1)
                try:
                    x=faces[0].left()
                    y=faces[0].top()
                    width=faces[0].right()-x
                    height=faces[0].bottom()-y
                    #X,Y
                    img=frame[(y):(y+height),(x):(x+width)]
                    
                    cv2.imshow("show",img)
                    c=cv2.waitKey(10)
                    
                    #get face landmarks
                    face_landmark=self.pose_predictor(img,faces[0])
                    #get face discripter
                    describer=self.face_encoder.compute_face_descriptor(img,face_landmark, 1)
                    
                    #get face encoding
                    encoding=np.array(describer)
                    
                    if (first):
                        save_encoding=encoding 
                        first=False
                    print encoding[:10]
                    print '*'*30
                    print save_encoding[:10]
                    if (np.linalg.norm(encoding-save_encoding)>thresh):
                        save_encoding=encoding
                        dirname=self.path+str(count)+'.jpg'
                        print dirname
                        cv2.imwrite(dirname,img)
                        if not os.path.exists(dirname):
                            print 'save %s pictures' %('w'+str(count))
                        count=count+1
                    else:
                        print 'please change your feature!!!!'
                        print count
                        print np.linalg.norm(encoding-save_encoding)
                    
                        
                            
                    self.win.clear_overlay()    
                    self.win.add_overlay(faces)
                    self.win.set_image(frame)
                except:
                    print 'no human!!!'
            if count>20:
                sys.exit(0)
        else:
            print 'fail to open camera'

if __name__=='__main__':

    if len(sys.argv)<2:
        print 'use as :  python collectdata.py [thresh]'
    

    filepath='/home/yinnxinn/test/pic/'
    gdata=get_data(filepath)
    gdata.run()



