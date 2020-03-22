import cv2
import numpy as np
import tweepy
from credentials import *
import time
import os
import requests
# Bug lover tbh jajaja
lst_url = ["nothing haha"]
while True:
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth,wait_on_rate_limit=True)
	twt = api.search("#JBotSketchIt",result_type="recent",count=1)
	for tweet in twt:
		try:
		 	user = tweet.id
		 	img_url = tweet.entities['media'][0]['media_url']
		 	index = dict((y,x) for x,y in enumerate(lst_url))
		 	try:
		 		a_index = index[img_url]
		 	except:
		 		request = requests.get(img_url, stream=True)
		 		if request.status_code == 200:
		 			imgName = str(user)+'.png'
		 			with open(imgName, 'wb') as image:
		 				for chunk in request:
		 					image.write(chunk)
				 	img = cv2.imread(imgName)
				 	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				 	grey = cv2.medianBlur(grey,5)
				 	edges = cv2.adaptiveThreshold(grey,200,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,3)
				 	colors = cv2.bilateralFilter(img,9,300,300)
				 	cartoon = cv2.bitwise_and(colors,colors,mask=edges)
				 	img_name = str(user)+"1.png"
				 	cv2.imwrite(img_name,cartoon)
				 	api.update_with_media(img_name, status="Yo!! Rate my 🖌 Drawing out of 10 😪",in_reply_to_status_id = user,auto_populate_reply_metadata=True)
				 	os.remove(imgName)
				 	os.remove(img_name)
				 	print("Done")
				 	time.sleep(25)
				 	lst_url.append(img_url)
				 	print(lst_url)
		except Exception as e:
			print(e)