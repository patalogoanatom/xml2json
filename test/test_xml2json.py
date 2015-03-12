import unittest
import xml2json
import optparse
import json
import os

xmlstring = ""
options = None

class A:
    pretty = True


class SimplisticTest(unittest.TestCase):

    def setUp(self):
        global xmlstring, options
        filename = os.path.join(os.path.dirname(__file__), 'xml_ns2.xml')
        xmlstring = open(filename).read()
        options = optparse.Values({"pretty": False})

    def test_default_namespace_attribute(self):
        strip_ns = 0
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        # check string
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}tr") != -1)
        self.assertTrue(json_string.find("@class") != -1)

        # check the simple name is not exist
        json_data = json.loads(json_string)
        self.assertFalse("table" in json_data["root"])

    def test_strip_namespace(self):
        strip_ns = 1
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        json_data = json.loads(json_string)

        # namespace is stripped
        self.assertFalse(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)

        # TODO , attribute shall be kept
        #self.assertTrue(json_string.find("@class") != -1)

        #print json_data["root"]["table"]
        #print json_data["root"]["table"][0]["tr"]
        self.assertTrue("table" in json_data["root"])
        self.assertEqual(json_data["root"]["table"][0]["tr"]["td"] , ["Apples", "Bananas"])

    def test_json2xml(self):
    	test_case = '{"note": {"to": " Tove","from": "Jani","heading": "Reminder","body": "Dont forget me this weekend!"}}'
    	result = xml2json.json2xml(test_case)
    	self.assertEqual(result , '<note><body>Dont forget me this weekend!</body><to> Tove</to><from>Jani</from><heading>Reminder</heading></note>')

    def test_xml2json(self):
        test_case = "   <root><hi>Hello</hi><text>1</text><text>2</text><text>3</text><text>4</text><num>3</num><Sulya>1</Sulya><Sulya>2</Sulya><Sulya>3</Sulya><Sulya>4</Sulya><list><a>1</a><b>2</b><c>3</c></list></root>"
        result = xml2json.xml2json(test_case, A());
        self.assertEqual(result, '{\n    "root": {\n        "Sulya": [\n            "1",\n            "2",\n            "3",\n            "4"\n        ],\n        "hi": "Hello",\n        "list": {\n            "a": "1",\n            "b": "2",\n            "c": "3"\n        },\n        "num": "3",\n        "text": [\n            "1",\n            "2",\n            "3",\n            "4"\n        ]\n    }\n}')

    def test_json2elem(self):
        test_case = '''{
                        "root" : {
                            "@":"Hello",
                            "#text":[1,2,3,4], 
                            "#tail":3,
                            "Sulya":[1,2,3,4], 
                            "list":{
                                        "a":1, 
                                        "b":2, 
                                        "c":3
                                    }
                        }
                    }'''

        test_except = '''{
                "root" : {
                    "@":"Hello",
                    "#text":[1,2,3,4], 
                    "#tail":3,
                    "Sulya":[1,2,3,4], 
                    "list":{
                                "a":1, 
                                "b":2, 
                                "c":3
                            }
                },
                "aasdf" : "Fail"
            }'''
        try:
            result = xml2json.json2elem(test_except)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))    

        result = xml2json.json2elem(test_case)

if __name__ == '__main__':
    unittest.main()
