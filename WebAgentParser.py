import urllib2 
import time
import sys
import ssl
import os

from HTMLParser import HTMLParser  
from FillAgentData import insert_inscription_to_db
from FillAgentData import  insert_main_info_to_db


class MyHTMLParser(HTMLParser):

   def __init__(self):
      print "enter init"
      HTMLParser.__init__(self)
      self.recording = 0 
      self.flagItemPrice = 0
      self.address = 0
      self.city = 0
      self.property_picture = 0
      self.count = 0
      self.data = ""
      self.img_user = ""
      self.myarray = []
      self.array_cnt = 0
      self.phone = 0
      self.strphone = ""
      self.img_phone = ""
      self.agent_name = ""
      self.agent_lastname = ""
      self.urlprefix = "https://propriodirect.com"
      self.housepic = ""
      self.SiteToAnalyze = 0

   def handle_starttag(self, tag, attrs):

        if tag == 'img':
            # self.address = 0
            # self.flagItemPrice = 0
            for name, value in attrs:
                if name == 'src':
                    if value.find("properties") > 0 and self.property_picture == 0 and self.SiteToAnalyze == 1:
                        # print "Finding property picture: -> " + self.urlprefix + value
                        self.count += 1
                        self.data += (self.urlprefix + value)
                        self.property_picture = 1
                    elif value.find("account") > 0 and (value.lower().find(self.agent_name) > 0 or value.lower().find(self.agent_lastname) > 0):  # where we find for Agent picture
                        self.img_user = self.urlprefix + value
                        # print "user picture "    
                        print "user picture : " + self.urlprefix + value    
                    elif value.find("phone") > 0:
                        self.img_phone = self.urlprefix + value
                
        elif (tag == 'p' or tag == 'div' or tag == 'h4' or tag == 'a'):
            for name, value in attrs:
                # print "***********>" + name + " " + value
                if name == 'class' and value.find("phone_container") >= 0:
                    if self.phone == 0:
                         self.phone = 1
                if name == "href" and self.phone == 1:
                    self.phone = 2
                    
                if name == 'class' and value.find("_desktop") > 0: #check only desktop verison of the site
                    self.SiteToAnalyze = 1
                if name == 'class' and value.find("_mobile") > 0 : 
                    self.SiteToAnalyze = 0
                    
                if self.SiteToAnalyze == 1:
                    if name == 'class' and value.find("_price") > 0: 
                        # print "finding price ------> " + value
                        self.flagItemPrice = 1
                    elif name == 'class' and value.find("_address") > 0:
                        # print "address ------>" + value
                        if self.address == 0:
                            self.address = 1
                    elif name == 'class' and value.find("_city") > 0:
                        # print "City -------->" + value
                        if self.city == 0:
                            self.city = 1
        
             
   def handle_endtag(self, tag):

        # print "end tag ----->" + tag
        if tag == 'img':
            self.recording -= 1 
        elif tag == 'p' or tag == 'div' or tag == 'h4':
            if self.address == 1: 
                self.address = 0
                self.data += "|"  # delimiter between info....
            if self.city == 1:
                self.city = 0
                self.data += "|"
            if self.flagItemPrice == 1:
                self.flagItemPrice = 0
                self.data += "|"
            if self.phone == 2:
                self.phone = 0
                self.strphone += "|"  # delimiter between info....

   def handle_charref(self, ch):
       if self.address == 1:

            mychr = ""
            mychr += chr(int(ch))
            self.data += mychr

   def handle_data(self, indata):

        # print indata.decode('utf8')
        if self.property_picture == 1:
            
            # print "-----------------agent Data=", self.data
            # self.data += self.housepic
            strdata = self.data.split('|')
            if len(strdata) == 4:
                print "-----------------agent Data=", self.data
                print self.housepic
                self.myarray.append([])
                self.myarray[self.array_cnt].append((strdata[3]).decode('utf8'))
                self.myarray[self.array_cnt].append((strdata[0]).decode('utf8'))
                self.myarray[self.array_cnt].append((strdata[2]).decode('utf8'))
                self.myarray[self.array_cnt].append((strdata[1].replace("\xc2\xa0", " ")).decode('utf8'))
                self.array_cnt += 1
            
            self.flagItemPrice = 0
            self.address = 0
            self.property_picture = 0
            self.city = 0;
            self.data = ""            
        else:
            
            if self.address == 1:
                #print indata.strip()
                self.data += (indata.strip())
            if self.city == 1:
                #print indata.strip()
                self.data += (indata.strip())
            if self.flagItemPrice == 1:
                #print indata.strip()
                self.data += (indata.strip())
            if self.phone == 2:
                #print indata.strip()
                self.strphone += indata.strip()                

if __name__ == '__main__':         

    if len(sys.argv) < 3:
        print "Missing Instance Parameters"
        print "Example : script.py url name lastname" 
        exit()

    else:
        print 'Number of arguments:', len(sys.argv), 'arguments.'
        print 'Argument List:', str(sys.argv)
        reload(sys)
        sys.setdefaultencoding('utf8')
    
    url = sys.argv[1]  # URL
    name = sys.argv[2]  # Agent-name
    lastname = sys.argv[3]  # Agent-name
    
    URLtoOpen = url + "/" + name + "-" + lastname + "/"
    print URLtoOpen
    p = MyHTMLParser()
    p.agent_name = name
    p.agent_lastname = lastname
    if os.name == 'nt': #in windows
        context = ssl._create_unverified_context() #do not check ssk certificate please :-)
        f = urllib2.urlopen(URLtoOpen,context=context)
    else:
        f = urllib2.urlopen(URLtoOpen)
    html = f.read()
    p.feed(html)
    for i in range(len(p.myarray)) :
        p.myarray[i][1] = unicode(p.myarray[i][1])
        print "---------------------------------------------"
        print p.myarray[i][0]  # url photo
        print p.myarray[i][1]  # address
        print p.myarray[i][2]  # Lieu
        print p.myarray[i][3]  # prix
        print "---------------------------------------------"
    print p.img_phone
    print p.strphone
    
    insert_inscription_to_db(name.replace("-", "_") + "_" + lastname, p.myarray)
    insert_main_info_to_db(p.img_user, name.replace("-", "_") + "_" + lastname, p.img_phone, p.strphone.decode('utf8'), "", "0", str(p.count))
    p.close()
            
