#
#
# 这是试用face++效果的。 face++的官方demo是基于最基本的python代码写出来的，模拟POST消息发送。用requests简单很多
#
#

import requests
import cv2
import os

#developer info
key=
secret=

#api
detect_api='https://api-cn.faceplusplus.com/facepp/v3/detect'
compare_api='https://api-cn.faceplusplus.com/facepp/v3/compare'
search_api='https://api-cn.faceplusplus.com/facepp/v3/search'
createfaceset_api='https://api-cn.faceplusplus.com/facepp/v3/faceset/create'   #5 facetoken at time and 1000 total
facean_api='https://api-cn.faceplusplus.com/facepp/v3/face/analyze'
setuserid_api='https://api-cn.faceplusplus.com/facepp/v3/face/setuserid'

#transform data
data={'api_key':key,'api_secret':secret}
facetokens=[]

user_id=['ldh','gfc','gtl','cxc','dyj']

#set face_token
for i in xrange(5):
	try:
		print 'detect picture . .' + str(i+1)
		fpath='/home/yinnxinn/test/pic/'+str(i+1)+'.jpg'
		files={'image_file':('image_file',open(fpath,'rb'),'application/octet-stream')}
		rep=requests.post(detect_api,data=data,files=files)
		result=rep.text
		req=eval(result)
		faces=req["faces"]
		face_token=faces.pop()
		facetokens.append(face_token["face_token"])
	except:
		print 'fail to detect'
	#set the face info
	try:
		infodata={'api_key':key,'api_secret':secret,'face_token':face_token["face_token"],'user_id':user_id[i]}
		rep_info=requests.post(setuserid_api,data=infodata)
		resule_info=rep_info.text
		req_info=eval(resule_info)
		print req_info['user_id']
		if (req_info.keys=='error_message'):
			print 'failed to set userID'

		
	except:
		print 'fail to set info '
	

#createfaceset
try:
	print 'detection finished..creating faceset'
	face_set_data={'api_key':key,'api_secret':secret,'display_name	':'male stars','face_tokens':facetokens}
	faceset_rep=requests.post(createfaceset_api,data=face_set_data)
	result_faceset=faceset_rep.text
	req_faceset=eval(result_faceset)
	print 'succeed to create faceset :'+req_faceset["faceset_token"]+'\n'
	if (not req_faceset["faceset_token"]):
		print 'fail to create faceset : male stars'
except:
	print 'fail to set faceset '

#test the search_api
try:
	print 'test the search api'
	search_path='/home/yinnxinn/test/pic/test.jpg'
	search_data= {'api_key':key,'api_secret':secret,'faceset_token':req_faceset["faceset_token"]}
	print search_data
	search_files={'image_file':('image_file',open(search_path,'rb'),'application/octet-stream')}
	search_rep=requests.post(search_api,data=search_data,files=search_files)
	result_search=search_rep.text
	result_req=eval(result_search)
	facebox=result_req('faces').pop["face_rectangle"]
	width=facebox("width")
	top=facebox("top")
	left=facebox("left")
	height=facebox("height")
	test_face=cv2.imread("search_path",1)
	cv2.rectangle(test_face,(left,top),(left+width,top+height),Scalar(255,0,0),2)
	cv2.namedWindow("show",1)
	cv2.imshow("show",test_face)
	cv2.waitKey(0)
	cv2.destroyWindow("show")
	
except:
	print 'fail'
