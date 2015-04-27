import unittest
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path, '..', '..', 'lib'))

from l20n.format.parser import Parser, ParserError


class L20nParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    #def test_empty_entity(self):
    #    string = "<id>"
    #    ast = self.parser.parse(string)
    #    self.assertEqual(len(ast), 1)
    #    self.assertEqual(ast[0]['$i']['name'], "id")

    def test_string_value(self):
        string = "<id 'string'>"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast), 1)
        self.assertEqual(ast[0]['$i'], "id")
        self.assertEqual(ast[0]['$v'], 'string')

        string = '<id "string">'
        ast = self.parser.parse(string)
        self.assertEqual(len(ast), 1)
        self.assertEqual(ast[0]['$i'], "id")
        self.assertEqual(ast[0]['$v'], 'string')

#        string = "<id '''string'''>"
#        ast = self.parser.parse(string)
#        self.assertEqual(len(ast), 1)
#        self.assertEqual(ast[0]['$i'], "id")
#        self.assertEqual(ast[0]['$v'], 'string')

#        string = '<id """string""">'
#        ast = self.parser.parse(string)
#        self.assertEqual(len(ast), 1)
#        self.assertEqual(ast[0]['$i']['name'], "id")
#        self.assertEqual(ast[0]['$v'], 'string')

    def test_string_value_quotes(self):
        string = '<id "str\\"ing">'
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'], 'str"ing')

        string = "<id 'str\\'ing'>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'], "str'ing")

#        string = '<id """str"ing""">'
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['$v'], 'str"ing')

#        string = "<id '''str'ing'''>"
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['$v'], "str'ing")

#        string = '<id """"string\\"""">'
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['$v'], '"string"')

#        string = "<id ''''string\\''''>"
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['$v'], "'string'")

        string = "<id 'test \{{ more'>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'], "test {{ more")

        string = "<id 'test \\\\ more'>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'], "test \ more")

        string = "<id 'test \\a more'>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'], "test a more")

    def test_string_unicode(self):
        string = u"<id 'foo \\u00bd = \u00bd'>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'], u"foo \u00bd = \u00bd")

    def test_basic_errors(self):
        strings = [
            '< "str\\"ing">',
            "<>",
            "<id",
            "<id ",
            "id>",
            '<id "value>',
            '<id value">',
            "<id 'value>",
            "<id value'",
            "<id'value'>",
            '<id"value">',
            '<id """value"""">',
            '< id "value">',
            '<()>',
            '<+s>',
            '<id-id2>',
            '<-id>',
            '<id 2>',
            '<"id">',
            '<\'id\'>',
            '<2>',
            '<09>',
        ]
        for string in strings:
            try:
                self.assertRaises(ParserError, self.parser.parse, string)
            except AssertionError:
                raise AssertionError("Failed to raise parser error on: " +
                                     string)

    def test_complex_strings(self):
        string = "<id 'test {{ id }} test2'>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v'][0], 'test ')
        self.assertEqual(ast[0]['$v'][1]['t'], 'id')
        self.assertEqual(ast[0]['$v'][2], ' test2')

    def test_basic_attributes(self):
        string = "<id attr1: 'foo'>"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast[0]), 2)
        attr = ast[0]['attr1']
        self.assertEqual(attr, "foo")

        string = "<id attr1: 'foo' attr2: 'foo2'    >"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast[0]), 3)
        attr = ast[0]['attr1']
        self.assertEqual(attr, "foo")

        string = "<id 'value' attr1: 'foo' attr2: 'foo2' attr3: 'foo3' >"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast[0]), 5)
        attr = ast[0]['attr1']
        self.assertEqual(attr, "foo")
        attr = ast[0]['attr2']
        self.assertEqual(attr, "foo2")
        attr = ast[0]['attr3']
        self.assertEqual(attr, "foo3")

#    def test_attributes_with_indexes(self):
#        string = "<id attr[2]: 'foo'>"
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['attr']['x'], 2)
#        string = "<id attr[2+3?'foo':'foo2']: 'foo'>"
#        ast = self.parser.parse(string)
#        self.assertEqual((ast[0]['attrs'][0]['index'][0]['test']
#                          ['left']['$v']), 2)
#        self.assertEqual((ast[0]['attrs'][0]['index'][0]['test']
#                          ['right']['$v']), 3)
#        string = "<id attr[2, 3]: 'foo'>"
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['attrs'][0]['index'][0]['$v'], 2)
#        self.assertEqual(ast[0]['attrs'][0]['index'][1]['$v'], 3)

    def test_attribute_errors(self):
        strings = [
            '<id : "foo">',
            "<id 2: >",
            "<id a: >",
            "<id: ''>",
            "<id a: b:>",
            "<id a: 'foo' 'heh'>",
            "<id a: 2>",
            "<id 'a': 'a'>",
            "<id \"a\": 'a'>",
            "<id 2: 'a'>",
            "<id a2:'a'a3:'v'>",
        ]
        for string in strings:
            try:
                self.assertRaises(ParserError, self.parser.parse, string)
            except AssertionError:
                raise AssertionError("Failed to raise parser error on: " +
                                     string)

    def test_hash_value(self):
        string = "<id {a: 'b', a2: 'c', d: 'd' }>"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast), 1)
        val = ast[0]['$v']
        self.assertEqual(len(val), 3)
        self.assertEqual(val['a'], 'b')

        string = "<id {a: '2', b: '3'} >"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast), 1)
        val = ast[0]['$v']
        self.assertEqual(len(val), 2)
        self.assertEqual(val['a'], "2")
        self.assertEqual(val['b'], "3")

    def test_hash_value_with_trailing_comma(self):
        string = "<id {a: '2', b: '3', } >"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast), 1)
        val = ast[0]['$v']
        self.assertEqual(len(val), 2)
        self.assertEqual(val['a'], "2")
        self.assertEqual(val['b'], "3")

    def test_nested_hash_value(self):
        string = "<id {a: 'foo', b: {a2: 'p'}}>"
        ast = self.parser.parse(string)
        self.assertEqual(len(ast), 1)
        val = ast[0]['$v']
        self.assertEqual(len(val), 2)
        self.assertEqual(val['a'], 'foo')
        self.assertEqual(val['b']['a2'], 'p')

    def test_hash_with_default(self):
        string = "<id {a: 'v', *b: 'c'}>"
        ast = self.parser.parse(string)
        self.assertEqual(ast[0]['$v']['__default'], 'b')

    def test_hash_errors(self):
        strings = [
            '<id {}>',
            '<id {a: 2}>',
            "<id {a: 'd'>",
            "<id a: 'd'}>",
            "<id {{a: 'd'}>",
            "<id {a: 'd'}}>",
            "<id {a:} 'd'}>",
            "<id {2}>",
            "<id {'a': 'foo'}>",
            "<id {\"a\": 'foo'}>",
            "<id {2: 'foo'}>",
            "<id {a:'foo'b:'foo'}>",
            "<id {a }>",
            '<id {a: 2, b , c: 3 } >',
            '<id {*a: "v", *b: "c"}>',
        ]
        for string in strings:
            try:
                self.assertRaises(ParserError, self.parser.parse, string)
            except AssertionError:
                raise AssertionError("Failed to raise parser error on: " +
                                     string)

#    def test_index(self):
#        #string = "<id[]>"
#        #ast = self.parser.parse(string)
#        #self.assertEqual(len(ast), 1)
#        #self.assertEqual(len(ast[0]['index']), 0)
#        #self.assertEqual(ast[0]['$v'], None)
#
#        #string = "<id[ ] >"
#        #ast = self.parser.parse(string)
#        #self.assertEqual(len(ast), 1)
#        #self.assertEqual(len(ast[0]['index']), 0)
#        #self.assertEqual(ast[0]['$v'], None)
#
#        string = "<id['foo'] 'foo2'>"
#        ast = self.parser.parse(string)
#        entity = ast[0]
#        self.assertEqual(entity['index'][0], "foo")
#        self.assertEqual(entity['$v'], "foo2")
#
#        string = "<id[2] 'foo2'>"
#        ast = self.parser.parse(string)
#        entity = ast[0]
#        self.assertEqual(entity['index'][0]['$v'], 2)
#        self.assertEqual(entity['$v'], "foo2")
#
#        string = "<id[2, 'foo', 3] 'foo2'>"
#        ast = self.parser.parse(string)
#        entity = ast[0]
#        self.assertEqual(entity['index'][0]['$v'], 2)
#        self.assertEqual(entity['index'][1], 'foo')
#        self.assertEqual(entity['index'][2]['$v'], 3)
#        self.assertEqual(entity['$v'], "foo2")
#
#    def test_index_errors(self):
#        strings = [
#            '<id[ "foo">',
#            '<id] "foo">',
#            '<id[ \'] "foo">',
#            '<id{ ] "foo">',
#            '<id[ } "foo">',
#            '<id[" ] "["a"]>',
#            '<id[a]["a"]>',
#            '<id["foo""foo"] "fo">',
#            '<id[a, b, ] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_macro(self):
#        string = "<id($n) {2}>"
#        ast = self.parser.parse(string)
#        self.assertEqual(len(ast), 1)
#        self.assertEqual(len(ast[0]['args']), 1)
#        self.assertEqual(ast[0]['expression']['$v'], 2)
#
#        string = "<id( $n, $m, $a ) {2}  >"
#        ast = self.parser.parse(string)
#        self.assertEqual(len(ast), 1)
#        self.assertEqual(len(ast[0]['args']), 3)
#        self.assertEqual(ast[0]['expression']['$v'], 2)
#
#    def test_macro_errors(self):
#        strings = [
#            '<id (n) {2}>',
#            '<id ($n) {2}>',
#            '<(n) {2}>',
#            '<id(() {2}>',
#            '<id()) {2}>',
#            '<id[) {2}>',
#            '<id(] {2}>',
#            '<id(-) {2}>',
#            '<id(2+2) {2}>',
#            '<id("a") {2}>',
#            '<id(\'a\') {2}>',
#            '<id(2) {2}>',
#            '<_id($n) {2}>',
#            '<id($n) 2}>',
#            '<id($n',
#            '<id($n ',
#            '<id($n)',
#            '<id($n) ',
#            '<id($n) {',
#            '<id($n) { ',
#            '<id($n) {2',
#            '<id($n) {2}',
#            '<id(nm nm) {2}>',
#            '<id($n) {}>',
#            '<id($n, $m ,) {2}>',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_expression(self):
#        string = "<id[0 == 1 || 1] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['left']['operator']['token'], '==')
#
#        string = "<id[a == b == c] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '==')
#        self.assertEqual(exp['left']['operator']['token'], '==')
#
#        string = "<id[ a == b || c == d || e == f ] 'foo'  >"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['left']['operator']['token'], '||')
#        self.assertEqual(exp['right']['operator']['token'], '==')
#
#        string = "<id[0 && 1 || 1] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['left']['operator']['token'], '&&')
#
#        string = "<id[0 && (1 || 1)] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '&&')
#        self.assertEqual(exp['right']['expression']['operator']['token'], '||')
#
#        string = "<id[1 || 1 && 0] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['right']['operator']['token'], '&&')
#
#        string = "<id[1 + 2] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '+')
#        self.assertEqual(exp['left']['$v'], 1)
#        self.assertEqual(exp['right']['$v'], 2)
#
#        string = "<id[1 + 2 - 3 > 4 < 5 <= a >= 'd' * 3 / q % 10] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '>=')
#
#        string = "<id[! +1] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '!')
#        self.assertEqual(exp['argument']['operator']['token'], '+')
#        self.assertEqual(exp['argument']['argument']['$v'], 1)
#
#        string = "<id[1+2] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '+')
#        self.assertEqual(exp['left']['$v'], 1)
#        self.assertEqual(exp['right']['$v'], 2)
#
#        string = "<id[(1+2)] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]['expression']
#        self.assertEqual(exp['operator']['token'], '+')
#        self.assertEqual(exp['left']['$v'], 1)
#        self.assertEqual(exp['right']['$v'], 2)
#
#        string = "<id[id2['foo']] 'foo2'>"
#        ast = self.parser.parse(string)
#        self.assertEqual(len(ast), 1)
#        exp = ast[0]['index'][0]
#        self.assertEqual(ast[0]['$v'], 'foo2')
#        self.assertEqual(exp['expression']['name'], 'id2')
#        self.assertEqual(exp['property'], 'foo')
#
#        #string = "<id[id['foo']]>"
#        #ast = self.parser.parse(string)
#        #self.assertEqual(len(ast), 1)
#        #exp = ast[0]['index'][0]
#        #self.assertEqual(ast[0]['$v'], None)
#        #self.assertEqual(exp['expression']['name'], 'id')
#        #self.assertEqual(exp['property'] , 'foo')
#
#    def test_expression_errors(self):
#        strings = [
#            '<id[1+()] "foo">',
#            '<id[1<>2] "foo">',
#            '<id[1+=2] "foo">',
#            '<id[>2] "foo">',
#            '<id[1==] "foo">',
#            '<id[1+ "foo">',
#            '<id[2==1+] "foo">',
#            '<id[2==3+4 "fpp">',
#            '<id[2==3+ "foo">',
#            '<id[2>>2] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_logical_expression(self):
#        string = "<id[0 || 1] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['left']['$v'], 0)
#        self.assertEqual(exp['right']['$v'], 1)
#
#        string = "<id[0 || 1 && 2 || 3] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['left']['operator']['token'], '||')
#        self.assertEqual(exp['right']['$v'], 3)
#        self.assertEqual(exp['left']['left']['$v'], 0)
#        self.assertEqual(exp['left']['right']['left']['$v'], 1)
#        self.assertEqual(exp['left']['right']['right']['$v'], 2)
#        self.assertEqual(exp['left']['right']['operator']['token'], '&&')
#
#    def test_logical_expression_errors(self):
#        strings = [
#            '<id[0 || && 1] "foo">',
#            '<id[0 | 1] "foo">',
#            '<id[0 & 1] "foo">',
#            '<id[|| 1] "foo">',
#            '<id[0 ||] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_binary_expression(self):
#        #from pudb import set_trace; set_trace()
#        string = "<id[a / b * c] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '*')
#        self.assertEqual(exp['left']['operator']['token'], '/')
#
#        string = "<id[8 * 9 % 11] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '%')
#        self.assertEqual(exp['left']['operator']['token'], '*')
#
#        string = "<id[6 + 7 - 8 * 9 / 10 % 11] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '-')
#        self.assertEqual(exp['left']['operator']['token'], '+')
#        self.assertEqual(exp['right']['operator']['token'], '%')
#
#        string = ("<id[0 == 1 != 2 > 3 < 4 >= 5 <= 6 + 7 - 8 * 9 / 10 % 11]"
#                  " 'foo'>")
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '!=')
#        self.assertEqual(exp['left']['operator']['token'], '==')
#        self.assertEqual(exp['right']['operator']['token'], '<=')
#        self.assertEqual(exp['right']['left']['operator']['token'], '>=')
#        self.assertEqual(exp['right']['right']['operator']['token'], '-')
#        self.assertEqual(exp['right']['left']['left']['operator']['token'],
#                         '<')
#        self.assertEqual(exp['right']['left']['right']['$v'], 5)
#        self.assertEqual((exp['right']['left']['left']['left']
#                          ['operator']['token']), '>')
#        self.assertEqual(exp['right']['right']['left']['operator']['token'],
#                         '+')
#        self.assertEqual(exp['right']['right']['right']['operator']['token'],
#                         '%')
#        self.assertEqual((exp['right']['right']['right']['left']
#                          ['operator']['token']), '*')
#        self.assertEqual((exp['right']['right']['right']['left']['right']
#                          ['operator']['token']), '/')
#
#    def test_binary_expression_errors(self):
#        strings = [
#            '<id[1 \ 2] "foo">',
#            '<id[1 ** 2] "foo">',
#            '<id[1 * / 2] "foo">',
#            '<id[1 !> 2] "foo">',
#            '<id[1 <* 2] "foo">',
#            '<id[1 += 2] "foo">',
#            '<id[1 %= 2] "foo">',
#            '<id[1 ^ 2] "foo">',
#            '<id 2 < 3 "foo">',
#            '<id 2 > 3 "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_unary_expression(self):
#        #from pudb import set_trace; set_trace()
#        string = "<id[! + - 1] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '!')
#        self.assertEqual(exp['argument']['operator']['token'], '+')
#        self.assertEqual(exp['argument']['argument']['operator']['token'], '-')
#
#    def test_unary_expression_errors(self):
#        strings = [
#            '<id[a ! v] "foo">',
#            '<id[!] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_call_expression(self):
#        string = "<id[foo()] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['callee']['name'], 'foo')
#        self.assertEqual(len(exp['arguments']), 0)
#
#        string = "<id[foo(d, e, f, g)] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['callee']['name'], 'foo')
#        self.assertEqual(len(exp['arguments']), 4)
#        self.assertEqual(exp['arguments'][0]['name'], 'd')
#        self.assertEqual(exp['arguments'][1]['name'], 'e')
#        self.assertEqual(exp['arguments'][2]['name'], 'f')
#        self.assertEqual(exp['arguments'][3]['name'], 'g')
#
#    def test_call_expression_errors(self):
#        strings = [
#            '<id[1+()] "foo">',
#            '<id[foo(fo fo)] "foo">',
#            '<id[foo(()] "foo">',
#            '<id[foo(())] "foo">',
#            '<id[foo())] "foo">',
#            '<id[foo("ff)] "foo">',
#            '<id[foo(ff")] "foo">',
#            '<id[foo(a, b, )] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_member_expression(self):
#        string = "<id[x['d']] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['expression']['name'], 'x')
#        self.assertEqual(exp['property'], 'd')
#
#        string = "<id[x.d] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['expression']['name'], 'x')
#        self.assertEqual(exp['property']['name'], 'd')
#
#        string = "<id[a||b.c] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '||')
#        self.assertEqual(exp['right']['expression']['name'], 'b')
#
#        string = "<id[ x.d ] 'foo' >"
#        ast = self.parser.parse(string)
#
#        string = "<id[ x[ 'd' ] ] 'foo' >"
#        ast = self.parser.parse(string)
#
#        string = "<id[ x['d'] ] 'foo' >"
#        ast = self.parser.parse(string)
#
#        string = "<id[x['d']['e']] 'foo' >"
#        ast = self.parser.parse(string)
#
#        string = "<id[! (a?b:c)['d']['e']] 'foo' >"
#        ast = self.parser.parse(string)
#
#    def test_member_expression_errors(self):
#        strings = [
#            '<id[x[[]] "foo">',
#            '<id[x[] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_attr_expression(self):
#        string = "<id[x::['d']] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['expression']['name'], 'x')
#        self.assertEqual(exp['attribute'], 'd')
#
#        string = "<id[x::d] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['expression']['name'], 'x')
#        self.assertEqual(exp['attribute']['name'], 'd')
#
#    def test_attr_expression_errors(self):
#        strings = [
#            '<id[x:::d] "foo">',
#            '<id[x[::"d"]] "foo">',
#            '<id[x[::::d]] "foo">',
#            '<id[x:::[d]] "foo">',
#            '<id[x.y::z] "foo">',
#            '<id[x::y::z] "foo">',
#            '<id[x.y::["z"]] "foo">',
#            '<id[x::y::["z"]] "foo">',
#            '<id[x::[1 "foo">',
#            '<id[x()::attr1] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_parenthesis_expression(self):
#        #from pudb import set_trace; set_trace()
#        string = "<id[(1 + 2) * 3] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '*')
#        self.assertEqual(exp['left']['expression']['operator']['token'], '+')
#
#        string = "<id[(1) + ((2))] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '+')
#        self.assertEqual(exp['left']['expression']['$v'], 1)
#        self.assertEqual(exp['right']['expression']['expression']['$v'], 2)
#
#        string = "<id[(a||b).c] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['expression']['expression']['operator']['token'],
#                         '||')
#        self.assertEqual(exp['property']['name'], 'c')
#
#        string = "<id[!(a||b).c] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['operator']['token'], '!')
#        self.assertEqual((exp['argument']['expression']['expression']
#                          ['operator']['token']), '||')
#        self.assertEqual(exp['argument']['property']['name'], 'c')
#
#        string = "<id[a().c] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['expression']['callee']['name'], 'a')
#        self.assertEqual(exp['property']['name'], 'c')
#
#    def test_parenthesis_expression_errors(self):
#        strings = [
#            '<id[1+()] "foo">',
#            '<id[(+)*(-)] "foo">',
#            '<id[(!)] "foo">',
#            '<id[(())] "foo">',
#            '<id[(] "foo">',
#            '<id[)] "foo">',
#            '<id[1+(2] "foo">',
#            '<id[a().c.[d]()] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_literal_expression(self):
#        string = "<id[012] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp['$v'], 12)
#
#    def test_literal_expression_errors(self):
#        strings = [
#            '<id[012x1] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_value_expression(self):
#        string = "<id['foo'] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp, 'foo')
#
#        string = "<id[{a: 'foo', b: 'foo2'}] 'foo'>"
#        ast = self.parser.parse(string)
#        exp = ast[0]['index'][0]
#        self.assertEqual(exp[0]['$v'], 'foo')
#        self.assertEqual(exp[1]['$v'], 'foo2')
#
#    def test_value_expression_errors(self):
#        strings = [
#            '<id[[0, 1]] "foo">',
#            '<id["foo] "foo">',
#            '<id[foo"] "foo">',
#            '<id[["foo]] "foo">',
#            '<id[{"a": "foo"}] "foo">',
#            '<id[{a: 0}] "foo">',
#            '<id[{a: "foo"] "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: %s" +
#                                     string)
#
#    def test_comment(self):
#        string = "/* test */"
#        ast = self.parser.parse(string)
#        comment = ast[0]
#        self.assertEqual(comment, ' test ')
#
#    def test_comment_errors(self):
#        strings = [
#            '/* foo ',
#            'foo */',
#            '<id /* test */ "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_identifier(self):
#        #string = "<id>"
#        #ast = self.parser.parse(string)
#        #self.assertEqual(len(ast), 1)
#        #self.assertEqual(ast[0]['$i']['name'], "id")
#
#        #string = "<ID>"
#        #ast = self.parser.parse(string)
#        #self.assertEqual(len(ast), 1)
#        #self.assertEqual(ast[0]['$i']['name'], "ID")
#        pass
#
#    def test_identifier_errors(self):
#        strings = [
#            '<i`d "foo">',
#            '<0d "foo">',
#            '<09 "foo">',
#            '<i!d "foo">',
#        ]
#        for string in strings:
#            try:
#                self.assertRaises(ParserError, self.parser.parse, string)
#            except AssertionError:
#                raise AssertionError("Failed to raise parser error on: " +
#                                     string)
#
#    def test_import(self):
#        string = "import('./foo.ast')"
#        ast = self.parser.parse(string)
#        self.assertEqual(ast[0]['type'], 'ImportStatement')
#        self.assertEqual(ast[0]['uri'], './foo.ast')

if __name__ == '__main__':
    unittest.main()