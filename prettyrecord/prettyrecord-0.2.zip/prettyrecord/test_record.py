from unittest import TestCase

from prettyrecord import Record, Field, RecordField


class Point(Record, trait='plain'):
    x = Field(default_value=0)
    y = Field(default_value=0)
    name = Field(default_value='')


class Point3d(Point):
    z = Field(default_value=0)
    name = Field(default_value='3d')


class Connection(Record, trait='nested'):
    p1 = Point()
    p2 = Point()
    name = Field()


class TestRecord(TestCase):
    def setUp(self):
        self.p = Point(x=10, y=6, name='sth')
        self.p3 = Point3d(x=10, y=6, z=-1, name='p3')
        self.c = Connection(
            p1=Point(y=-2, name='p1'),
            p2=Point(x=1, y=1),
            name='connection'
        )

    def test_class_info(self):
        self.assertIsInstance(Point.x, Field)
        self.assertIsInstance(Connection.p1, RecordField)

        self.assertEqual(Point.__trait__, 'plain')
        self.assertTupleEqual(Point.__slots__, ('_Point__x', '_Point__y', '_Point__name'))

        self.assertEqual(Point3d.__trait__, 'plain')
        self.assertTupleEqual(Point3d.__slots__, ('_Point3d__z', '_Point3d__name'))

        self.assertEqual(Connection.__trait__, 'nested')
        self.assertTupleEqual(Connection.__slots__, ('_Connection__p1', '_Connection__p2', '_Connection__name'))

    def test_class_immutability(self):
        with self.assertRaises(AttributeError):
            Point.x = None

        with self.assertRaises(AttributeError):
            del Point.x

    def test_init(self):
        self.assertEqual(self.p.name, 'sth')
        self.assertEqual(self.p.x, 10)
        self.assertEqual(self.p.y, 6)

        self.assertEqual(self.c.name, 'connection')
        self.assertEqual(self.c.p1.x, 0)
        self.assertEqual(self.c.p1.y, -2)
        self.assertEqual(self.c.p1.name, 'p1')
        self.assertEqual(self.c.p2.x, 1)
        self.assertEqual(self.c.p2.y, 1)
        self.assertEqual(self.c.p2.name, '')

    def test_set(self):
        self.p.x = 123
        self.assertEqual(self.p.x, 123)

        self.p._Point__x = 456
        self.assertEqual(self.p.x, 456)

        with self.assertRaises(AttributeError):
            self.p.a = 10

    def test_repr(self):
        r = repr(self.p)
        self.assertTrue(r.startswith("Point("))
        self.assertTrue("x=10" in r)
        self.assertTrue("y=6" in r)
        self.assertTrue("name='sth'" in r)

        r = repr(self.c)
        self.assertTrue(r.startswith("Connection("))
        self.assertTrue("name='p1'" in r)
        self.assertTrue("p1=Point(" in r)
        self.assertTrue("name='connection'" in r)

    def test_eq(self):
        self.assertEqual(self.p, self.p)
        self.assertEqual(self.c, self.c)
        self.assertNotEqual(self.p, self.c)

        self.assertEqual(self.p, Point(x=10, y=6, name='sth'))
        self.assertNotEqual(self.p, Point(x=10, y=6, name=''))
        self.assertEqual(self.p3, Point3d(x=10, y=6, z=-1, name='p3'))

    def test_inheritance(self):
        self.assertTrue(hasattr(Point, 'x'))
        self.assertTrue(hasattr(Point3d, 'x'))

        self.assertEqual(Point.name.default_value, '')
        self.assertEqual(Point3d.name.default_value, '3d')

        g = Point3d()
        self.assertEqual(g.name, '3d')
        self.assertEqual(Point.name.__get__(g, type(g)), '')
        self.assertEqual(Point3d.name.__get__(g, type(g)), '3d')

    def test_iter_fields(self):
        self.assertListEqual(
            list(Point.iter_fields()),
            [(Point, Point.x), (Point, Point.y), (Point, Point.name)]
        )

        self.assertListEqual(
            list(Point3d.iter_fields()),
            [(Point, Point.x), (Point, Point.y), (Point, Point.name),
             (Point3d, Point3d.z), (Point3d, Point3d.name)]
        )

        self.assertListEqual(
            list(Connection.iter_fields()),
            [(Connection, Connection.p1), (Connection, Connection.p2), (Connection, Connection.name)]
        )
