import urllib.request
for i in range(61,100):
	if(i>9):
		name='17121A15'+str(i)+'.jpg'
	else:
		name='17121A150'+str(i)+'.jpg'
	url='http://examsportal.vidyanikethan.edu/verify/photos/bt17/15/'+name
	urllib.request.urlretrieve(url,name)
