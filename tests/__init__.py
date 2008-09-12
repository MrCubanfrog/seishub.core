# -*- coding: utf-8 -*-

import doctest
import unittest

from seishub.tests import test_config, test_core, test_xmlconformance, \
                          test_core_zope_compatibility


def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_core.suite())
    suite.addTest(test_core_zope_compatibility.suite())
    suite.addTest(test_config.suite())
    suite.addTest(doctest.DocFileSuite('test_config.txt'))
    # XXX: add later
    #suite.addTest(test_xmlconformance.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')