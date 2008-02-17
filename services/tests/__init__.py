# -*- coding: utf-8 -*-

import doctest
import unittest

from seishub.services.tests import test_xmlconformance


def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_xmlconformance.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')