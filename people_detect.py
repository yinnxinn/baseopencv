
#opencv自带的人形检测器，主要想测试一下HOG属性的分类器
#
#不过貌似3.0以后分类器不支持HOG特征了，只有HAAR和LBP了，个人感觉HOG特征蛮好用的
#


import cv2

hog=cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

print hog.getDescriptorSize()
print hog.getWinSigma()


src=cv2.imread('../test.jpg')

(rects, weights) = hog.detectMultiScale(src, winStride=(4, 4),padding=(8, 8), scale=1.05)

print weights
print rects

for (x,y,w,h) in rects:
	cv2.rectangle(src,(x,y),(x+w,y+h),(0,0,255),2)

cv2.imshow('src',src)
cv2.waitKey(0)
