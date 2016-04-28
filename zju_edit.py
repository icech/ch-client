#!/usr/bin/env python
#encoding=utf-8

import urllib
import urllib2
import cookielib
import re
import time


def safari(url,postdata,headers,opener):
    request = urllib2.Request(url=url,data=postdata,headers=headers)
    result = opener.open(request)
    return result.read()


def LoginORLogout():
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)                    # add cookie
    opener = urllib2.build_opener(handler)
    login_url = 'https://net.zju.edu.cn/include/auth_action.php'         # Request URL
    logout_url = 'https://net.zju.edu.cn/cgi-bin/srun_portal'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'              # use det_url to quit logining.
    headers = { 'User-Agent' : user_agent }
    post_data = {
        'action' : 'login',
        'username' : None,
        'password' : None,
        'ac_id' : '3',
        'user_ip' : '',
        'nas_ip' : '',
        'user_mac' : '',
        'save_me' : '1',
        'ajax' : '1'}


    flag = 1
    print 'Choose Login(1) or Logout(0)'
    while flag:
        x = input('Please enter 1 or 0 : ')
        if x == 1 or x == 0:
            flag = 0
        else:
            print 'Wrong number, please reenter.'


    if x == 0:                                                           # logout
        try:
            postdata = urllib.urlencode({'action' : 'logout'})
            data = safari(logout_url, postdata, headers=headers,opener=opener)
            if re.search('logout_ok',data):
                print 'disconnect successful!'
            else:
                print data
        except:
            print 'Check your WLAN!'
    else:                                                       #login
        usrn = 'sitan'
        pwd = 'yc0630yc'
        post_data['username'] = usrn
        post_data['password'] = pwd
        postdata = urllib.urlencode(post_data)

        try:
            data = safari(login_url, postdata, headers=headers,opener=opener)
            if re.search('E2532',data) != None:                   # Case for your id has logined
                time.sleep(12)
                data = safari(login_url, postdata, headers=headers,opener=opener)
            if re.search('login_ok.*',data) != None:              #judge whether login successful
                print 'Connection successful!'
            else:
                print 'Connection failed!'
        except:
            print 'Check your WLAN!'
    return 0

#start program
if __name__ == '__main__':
    LoginORLogout()

