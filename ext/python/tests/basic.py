import syck
import unittest

class TestCase(unittest.TestCase):
    def parseOnly(self, obj, yaml):
        self.assertEqual(obj, syck.load(yaml))

class BasicTests(TestCase):
    def testBasicMap(self):
        self.parseOnly(
            { 'one': 'foo', 'three': 'baz', 'two': 'bar' }, """
one: foo
two: bar
three: baz
""" 
        )

    def testBasicStrings(self):
        self.parseOnly(
            { 1: 'simple string', 2: 42, 3: '1 Single Quoted String',
              4: 'YAML\'s Double "Quoted" String', 5: "A block\n  with several\n    lines.\n",
              6: 'A "chomped" block', 7: "A folded\n string\n" }, """
1: simple string
2: 42
3: '1 Single Quoted String'
4: "YAML's Double \\\"Quoted\\\" String"
5: |
  A block
    with several
      lines.
6: |-
  A "chomped" block
7: >
  A
  folded
   string
"""
        )

    def testSimpleSequence(self):
        self.parseOnly(
            [ 'Mark McGwire', 'Sammy Sosa', 'Ken Griffey' ], """
- Mark McGwire
- Sammy Sosa
- Ken Griffey
"""
        )

    def testSimpleMap(self):
        self.parseOnly(
            { 'hr': 65, 'avg': 0.278, 'rbi': 147 }, """
avg: 0.278
hr: 65
rbi: 147
"""
        )

    def testSimpleMapWithNestedSequences(self):
        self.parseOnly(
            { 'american':
                [ 'Boston Red Sox', 'Detroit Tigers', 'New York Yankees' ],
              'national':
                [ 'New York Mets', 'Chicago Cubs', 'Atlanta Braves' ] }, """
american:
  - Boston Red Sox
  - Detroit Tigers
  - New York Yankees
national:
  - New York Mets
  - Chicago Cubs
  - Atlanta Braves
"""
        )

    def testSimpleSequenceWithNestedMaps(self):
        self.parseOnly(
            [ { 'name': 'Mark McGwire', 'hr': 65, 'avg': 0.278 },
              { 'name': 'Sammy Sosa', 'hr': 63, 'avg': 0.288} ], """
-
  avg: 0.278
  hr: 65
  name: Mark McGwire
-
  avg: 0.288
  hr: 63
  name: Sammy Sosa
"""
        )

    def testSequenceOfSequences(self):
        self.parseOnly(
		  [ 
		  	[ 'name', 'hr', 'avg' ],
			[ 'Mark McGwire', 65, 0.278 ],
			[ 'Sammy Sosa', 63, 0.288 ]
		  ], """
- [ name         , hr , avg   ]
- [ Mark McGwire , 65 , 0.278 ]
- [ Sammy Sosa   , 63 , 0.288 ]
"""
        )

    def testMappingOfMappings(self):
        self.parseOnly(
		  { 'Mark McGwire':
		    { 'hr': 65, 'avg': 0.278 },
			'Sammy Sosa':
		    { 'hr': 63, 'avg': 0.288 }
		  }, """
Mark McGwire: {hr: 65, avg: 0.278}
Sammy Sosa:   {hr: 63,
               avg: 0.288}
"""
        )

    def testNestedComments(self):
        self.parseOnly(
		  { 'hr': [ 'mark mcgwire', 'sammy sosa' ],
		    'rbi': [ 'sammy sosa', 'ken griffey' ] }, """
hr: # 1998 hr ranking
  - mark mcgwire
  - sammy sosa
rbi:
  # 1998 rbi ranking
  - sammy sosa
  - ken griffey
"""
        )

class SyckTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self,map(BasicTests,     
            ("testBasicMap",
             "testBasicStrings",
             "testSimpleSequence",
             "testSimpleMap",
             "testSimpleMapWithNestedSequences",
             "testSimpleSequenceWithNestedMaps",
             "testSequenceOfSequences",
             "testMappingOfMappings")))

if __name__ == '__main__':
    unittest.main()
