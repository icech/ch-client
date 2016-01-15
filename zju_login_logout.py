#!/usr/bin/env python
#encoding=utf-8

import urllib
import urllib2
import cookielib
import re
import getpass


def safari(url,postdata,headers,opener):
    request = urllib2.Request(url=url,data=postdata,headers=headers)
    result = opener.open(request)
    return result.read()


def LoginORLogout():
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)                    # add cookie
    opener = urllib2.build_opener(handler)
    login_url = 'https://net.zju.edu.cn/cgi-bin/srun_portal'         # Request URL
    det_url = 'https://net.zju.edu.cn/rad_online.php'                # if your id have logined in other terminal,
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'              # use det_url to quit logining.
    headers = { 'User-Agent' : user_agent }
    post_data = {
        'action' : 'login',
        'username' : None,
        'password' : None,
        'ac_id' : '3',
        'type' : '1',
        'wbaredirect' : 'http://www.isee.zju.edu.cn/notice/',
        'is_ldap' : '1',
        'local_auth' : '1'}

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
            data = safari(login_url, postdata, headers=headers,opener=opener)
            if re.search('成功',data):
                print 'disconnect successful!'
        except:
            print 'Check your WLAN!'
    else:                                                       #login
        usrn = raw_input('Please enter your ID: ')
        #pwd = raw_input('Please enter your password: ')
        pwd = getpass.getpass('Please enter your password: ')

        post_data['username'] = usrn
        post_data['password'] = pwd

        postdata1 = urllib.urlencode(post_data)

        postdata2 = urllib.urlencode({
            'action' : 'auto_dm',
            'username' : usrn,
            'password' : pwd
        })

        post_data['action'] = 'login_ok'
        postdata3 = urllib.urlencode(post_data)

        try:
            data = safari(login_url, postdata1, headers=headers,opener=opener)
            if re.search('错误',data) != None:                             #Test your id and password
                print 'Connection failed!'
                print 'The reason :your ID or password is wrong!'
                return -1
            if re.search('已在',data) != None:                          # Case for your id has logined in other terminal
                data = safari(det_url, postdata2, headers=headers,opener=opener)
            if re.search('ok',data):
                data = safari(login_url, postdata3, headers=headers,opener=opener)
            if re.search('.*sum_seconds.*',data) != None:              #judge whether login successful
                print 'Connection successful!'
            else:
                print 'Connection failed!'
        except:
            print 'Check your WLAN!'
    return 0


LoginORLogout()

