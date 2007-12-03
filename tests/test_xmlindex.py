# -*- coding: utf-8 -*-

from zope.interface.exceptions import DoesNotImplement

from twisted.trial.unittest import TestCase

from seishub.core import SeishubError
from seishub.xmldb.xmlresource import XmlResource
from seishub.xmldb.xmlindex import XmlIndex, TEXT_INDEX

RAW_XML1="""<station rel_uri="bern">
    <station_code>BERN</station_code>
    <chan_code>1</chan_code>
    <stat_type>0</stat_type>
    <lon>12.51200</lon>
    <lat>50.23200</lat>
    <stat_elav>0.63500</stat_elav>
    <XY>
        <paramXY>20.5</paramXY>
        <paramXY>11.5</paramXY>
        <paramXY>blah</paramXY>
    </XY>
</station>"""

class XmlIndexTest(TestCase):
    def testAttributes(self):
        test_index=XmlIndex(key_path="xxx",
                            value_path="yyy",
                            type=TEXT_INDEX)
        
        test_index.setValue_path("node1/node2/node3")
        self.assertEquals("node1/node2/node3",
                          test_index.getValue_path())
        test_index.setKey_path("/resourceBLAH")
        self.assertEquals("/resourceBLAH",
                          test_index.getKey_path())
        self.assertEquals(TEXT_INDEX,
                          test_index.getType())
         
    def testEval(self):
        #index with single node key result:
        test_index=XmlIndex(#xpath_expr="/station[./chan_code]"
                            key_path="lon",
                            value_path="/station"
                            )
        #index with multiple nodes key result:
        xy_index=XmlIndex(key_path="XY/paramXY",
                          value_path="/station"
                          )
        
        empty_resource=XmlResource()
        test_resource=XmlResource(uri='/stations/bern',
                                  xml_data=RAW_XML1)
        
        class Foo(object):
            pass
        
        # pass a Foo: (which does not implement IXmlDoc)
        self.assertRaises(DoesNotImplement,
                          test_index.eval,
                          Foo())
        # pass an empty XmlDoc:
        self.assertRaises(SeishubError,
                          test_index.eval,
                          empty_resource)
        
        self.assertEquals({'value': '/stations/bern', 'key': '12.51200'},
                          test_index.eval(test_resource)[0])
        self.assertEquals([{'value': '/stations/bern', 'key': '20.5'}, 
                           {'value': '/stations/bern', 'key': '11.5'}, 
                           {'value': '/stations/bern', 'key': 'blah'}],
                          xy_index.eval(test_resource)
                          )
        