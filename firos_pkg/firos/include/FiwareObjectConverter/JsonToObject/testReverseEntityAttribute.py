#    Copyright 2018 Fraunhofer IML
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

import unittest
import sys

from JsonToObject.reverseEntityAttribute import ReverseEntityAttribute


class TestEntityAttribute(unittest.TestCase):

    def test_ReverseEntityAttributeBool(self):
        d = dict(type="boolean", value=True, metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual(True, rea.getValue())
        self.assertEqual(type(rea.getValue()), bool)

    def test_ReverseEntityAttributeInt(self):
        d = dict(type="number", value=1, metadata=dict(
            python=dict(type="dataType", value="int")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(1, rea.getValue())
        self.assertEqual(type(rea.getValue()), int)

    def test_ReverseEntityAttributeFloat(self):
        d = dict(type="number", value=2.132, metadata=dict(
            python=dict(type="dataType", value="float")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(2.132, rea.getValue())
        self.assertEqual(type(rea.getValue()), float)

    def test_ReverseEntityAttributeLong(self):
        if sys.version_info <= (3,0):
            d = dict(type="number", value=123456789123456789123, metadata=dict(
                python=dict(type="dataType", value="long")))
            rea = ReverseEntityAttribute(d)
            # self.assertEqual(123456789123456789123, rea.getValue()) # Python2 is not able to convert it back properly
            self.assertEqual(type(rea.getValue()), long)

    def test_ReverseEntityAttributeComplex(self):
        d = dict(type="array",
                 value=[dict(type="number",   value=0,   metadata=dict(python=dict(type="dataType", value="int"))),
                        dict(type="number", value=2.34, metadata=dict(python=dict(type="dataType", value="int")))],
                 metadata=dict(python=dict(type="dataType", value="complex")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(2.34j, rea.getValue())
        self.assertEqual(type(rea.getValue()), complex)

    def test_ReverseEntityAttributeString(self):
        d = dict(type="string", value="Hello world!", metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual("Hello world!", rea.getValue())
        self.assertEqual(type(rea.getValue()), str)

    def test_ReverseEntityAttributeUnicode(self):
        d = dict(type="string", value=u'Unicode',
                 metadata=dict(python=dict(type="dataType", value="unicode")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(u'Unicode', rea.getValue())
        if sys.version_info <= (3,0):
            self.assertEqual(type(rea.getValue()), unicode)
        else:
            self.assertEqual(type(rea.getValue()), str)

    def test_ReverseEntityAttributeTuple(self):
        d = dict(type="array", value=[dict(type="number", value=1, metadata=dict(python=dict(type="dataType", value="int"))), dict(
            type="number", value=2, metadata=dict(python=dict(type="dataType", value="int")))], metadata=dict(python=dict(type="dataType", value="tuple")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(tuple((1, 2)), rea.getValue())
        self.assertEqual(type(rea.getValue()), tuple)

    def test_ReverseEntityAttributeList(self):
        d = dict(
            type="array",
            value=[dict(type="number", value=1, metadata=dict(python=dict(type="dataType", value="int"))),
                   dict(type="number", value=2, metadata=dict(python=dict(type="dataType", value="int")))],
            metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual(list([1, 2]), rea.getValue())
        self.assertEqual(type(rea.getValue()), list)

    def test_ReverseEntityAttributeDict(self):
        d = dict(type="object", value=dict(
            a=dict(type="number", value=1, metadata=dict(
                python=dict(type="dataType", value="int"))),
            b=dict(type="number", value=2, metadata=dict(python=dict(type="dataType", value="int")))),
            metadata={})

        rea = ReverseEntityAttribute(d)
        self.assertEqual(dict(a=1, b=2), rea.getValue())
        self.assertEqual(type(rea.getValue()), dict)

    def test_ReverseEntityAttributeForeignClass(self):
        d = dict(type="ClassInt",
                 value=dict(int=dict(type="number", value=1, metadata=dict(
                     python=dict(type="dataType", value="int")))),
                 metadata=dict(python="class"))

        rea = ReverseEntityAttribute(d)
        self.assertEqual(dict(int=1), rea.getValue())
        self.assertEqual(type(rea.getValue()), dict)

    def test_ReverseEntityAttributeFloat_WithWrongValue(self):
        d = dict(type="number", value="2.132", metadata=dict(
            python=dict(type="dataType", value="float")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(2.132, rea.getValue())
        self.assertEqual(type(rea.getValue()), float)

    def test_ReverseEntityAttributeInt_WithWrongValue(self):
        d = dict(type="number", value="1", metadata=dict(
            python=dict(type="dataType", value="int")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(1, rea.getValue())
        self.assertEqual(type(rea.getValue()), int)

    def test_ReverseEntityAttributeBool_WithWrongValue(self):
        d = dict(type="boolean", value="False", metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual(False, rea.getValue())
        self.assertEqual(type(rea.getValue()), bool)
