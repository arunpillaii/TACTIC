#!/usr/bin/python 
###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#
import tacticenv

from pyasm.common import Container, jsonloads, Environment, Xml
from pyasm.security import Batch
from pyasm.search import Search, SearchType

from pyasm.unittest import UnittestEnvironment

import unittest


import urllib2

class RestTest(unittest.TestCase):

    def test_all(self):

        test_env = UnittestEnvironment()
        test_env.create()


        self.server = "http://localhost"
        self.server = "http://192.168.56.105"

        try:
            self._setup()
            print("")
            print("")
            print("")
            self._test_accept()
            self._test_method()
            self._test_custom_handler()
            print("")
            print("")
            print("")

        finally:
            #test_env.delete()
            pass


    def send_request(self, url, headers, data={} ):

        ticket = Environment.get_ticket()

        method = headers.get("Method")
        if method == 'POST':
            data['login_ticket'] = ticket
            import urllib
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
        else:
            url = "%s?login_ticket=%s" % (url, ticket)
            print("url: ", url)
            request = urllib2.Request(url)

        for key,value in headers.items():
            request.add_header(key,value)

        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            # try again
            print("WARNING: ", e)
            response = urllib2.urlopen(request)

        #print(response.info().headers)

        value = response.read()

        accept = headers.get("Accept")
        if accept == "application/json":
            value = jsonloads(value)

        return value



    def _setup(self):

        url = SearchType.create("config/url")
        url.set_value("url", "/rest0/{code}")
        url.set_value('widget', '''
        <element widget="true">
          <display class='tactic.protocol.PythonRestHandler'>
            <script_path>rest/test</script_path>
          </display>
        </element>
        ''')
        url.commit()


        url = SearchType.create("config/url")
        url.set_value("url", "/rest2")
        url.set_value('widget', '''
        <element widget="true">
          <display class='tactic.protocol.TestCustomRestHandler'>
          </display>
        </element>
        ''')
        url.commit()



        url = SearchType.create("config/url")
        url.set_value("url", "/rest3/{method}/{data}")
        url.set_value('widget', '''
        <element widget="true">
          <display class='tactic.protocol.SObjectRestHandler'>
          </display>
        </element>
        ''')
        url.commit()





        script = SearchType.create("config/custom_script")
        script.set_value("folder", "rest")
        script.set_value("title", "test")
        script.set_value("script", """

from pyasm.common import Xml

accept = kwargs.get("Accept")
method = kwargs.get("Method")

print("kwargs: ", kwargs)

code = kwargs.get("code")
if code == "CODE0123":
    return "OK"

if method == "POST":
    return "Method is POST"



if accept == "application/json":
    return [3,2,1]
    
else:
    return Xml('''
    <arr>
      <int>1</int>
      <int>2</int>
      <int>3</int>
    </arr>
    ''')
        """)
        script.commit()






    def _test_accept(self):


        # try json
        url = "%s/tactic/default/unittest/rest0" % self.server
        headers = {
            "Accept": "application/json"
        }
        ret_val = self.send_request(url, headers)
        self.assertEquals( [3,2,1], ret_val)


        # try xml
        url = "%s/tactic/default/unittest/rest0" % self.server
        headers = {
            "Accept": "application/xml"
        }
        ret_val = self.send_request(url, headers)
        xml = Xml(ret_val)
        values = xml.get_values("arr/int")
        self.assertEquals( ['1','2','3'], values)


        # try json
        url = "%s/tactic/default/unittest/rest0/CODE0123" % self.server
        headers = {
            "Accept": "application/json"
        }
        ret_val = self.send_request(url, headers)
        self.assertEquals( "OK", ret_val)




    def _test_method(self):

        # try json
        url = "%s/tactic/default/unittest/rest0" % self.server
        headers = {
            "Accept": "application/json",
            "Method": "POST"
        }
        ret_val = self.send_request(url, headers)
        self.assertEquals( "Method is POST", ret_val)



    def _test_custom_handler(self):

        # try json
        url = "%s/tactic/default/unittest/rest2" % self.server
        headers = {
            "Accept": "application/json",
            "Method": "POST"
        }
        ret_val = self.send_request(url, headers)
        self.assertEquals( "Test Custom POST", ret_val)


        # try json
        url = "%s/tactic/default/unittest/rest3/expression" % self.server
        headers = {
            "Accept": "application/json",
            "Method": "POST"
        }
        data = {
            'expression': '@SOBJECT(unittest/person)'
        }
        ret_val = self.send_request(url, headers, data)
        print(ret_val)


    def _test_update(self):
        # try json
        url = "%s/tactic/default/unittest/rest3/person/CODE0123" % self.server
        headers = {
            "Accept": "application/json",
            "Method": "PUT"
        }
        data = {
            'description': 'abcdefg'
        }
        ret_val = self.send_request(url, headears, data)




if __name__ == "__main__":
    Batch()
    unittest.main()

