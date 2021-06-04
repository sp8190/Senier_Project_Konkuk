#!/usr/bin/env python
# coding: utf-8

# In[9]:


import urllib.request
import bs4

url="http://192.168.200.172:8091/stream.html"
html=urllib.request.urlopen(url)

bs_obj=bs4.BeautifulSoup(html,"html.parser")
#top_right=bs_obj.find("div",{"class":"eg-flick-camera"})
top_right=bs_obj.find("img",{"id":"streamimage"})
print(top_right)


# In[3]:





# In[ ]:




