# encoding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import absolute_import, division, unicode_literals

import json
from unittest import TestCase
from mo_dots import Null
from moz_sql_parser import parse

try:
    from tests.util import assertRaises
except ImportError:
    from .util import assertRaises  # RELATIVE IMPORT SO WE CAN RUN IN pyLibrary


class TestSimple(TestCase):

    maxDiff = 50000

    def test_null_literal(self):
        sql = "select 'null'"
        result = parse(sql)
        expected = {"select": {"value": {"literal": "null"}}}
        self.assertEqual(result, expected)
        
    def test_null_value(self):
        sql = "select null"
        result = parse(sql)
        expected = {"select": {"value": Null}}
        self.assertEqual(result, expected)
        
        
    def test_null_value2(self):
        sql = "select 'a',null"
        result = parse(sql)
        expected = {"select": [{"value": {"literal": "a"}}, {"value": Null}]}
        self.assertEqual(result, expected)

    def test_value2(self):
        sql = "select 'a'"
        result = parse(sql)
        expected = {'select': {'value': {'literal': 'a'}}}
        self.assertEqual(result, expected)

    def test_null_value3(self):
        sql = "select null,b from x"
        result = parse(sql)
        expected = {'from': 'x', 'select': [{'value': Null}, {'value': 'b'}]}
        self.assertEqual(result, expected)

    def test_null_parameter(self):
        sql = "select DECODE()"
        result = parse(sql)
        #  see to_json_call. when param is null, set {}.
        expected = {"select": {"value": {"decode": {}}}}
        # expected = {"select": {"value": {"decode": Null}}}
        self.assertEqual(result, expected)

    def test_null_parameter2(self):
        sql = "select DECODE(NULL)"
        result = parse(sql)
        expected = {"select": {"value": {"decode": None}}}
        # expected = {"select": {"value": {"decode": Null}}}
        self.assertEqual(result, expected)

    def test_null_parameter3(self):
        sql = "select DECODE(NULL,a)"
        result = parse(sql)
        #  see to_json_call. when param is null, set {}.
        expected = {"select": {"value": {"decode": [None,"a"]}}}
        # expected = {"select": {"value": {"decode": Null}}}
        self.assertEqual(result, expected)

    def test_null_parameter4(self):
        sql = "select DECODE(a,NULL)"
        result = parse(sql)
        #  see to_json_call. when param is null, set {}.
        expected = {"select": {"value": {"decode": ["a", None]}}}
        # expected = {"select": {"value": {"decode": Null}}}
        self.assertEqual(result, expected)

    def test_issue18(self):
        sql = "SELECT a, CASE WHEN some_columns = 'Bob' THEN NULL ELSE 'helloworld' END AS some_columns FROM mytable"
        result = parse(sql)
        expected = {
            "from": "mytable",
            "select": [
                {"value":'a'},
                {
                    "name":'some_columns', 
                    'value':{
                        'case': [
                            {'when': {'eq': [ 'some_columns', {'literal':'Bob'}] }, 'then': None},
                            {'literal':'helloworld'},
                       ]
                    }
                }
            ]
        }

        self.assertEqual(result, expected)

        
 