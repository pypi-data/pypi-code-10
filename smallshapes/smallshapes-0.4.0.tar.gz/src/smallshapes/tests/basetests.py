from smallshapes import *
import unittest
import numbers

class TestCase(unittest.TestCase):
    def assertAlmostEquals(self, a, b, msg=None):
        if isinstance(a, numbers.Number):
            super().assertAlmostEquals(a, b, msg)
        if not a.almost_equal(b):
            raise AssertionError('%r != %r' % (a, b))

class BaseTests(TestCase):
    def can_find_anytype(self):
        c = Circle(5, (0, 0))
        self.assertEqual(c.__anytype__, CircleAny) 

class Base(TestCase):
    mutable_cls = None
    immutable_cls = None
    args = None

    def setUp(self):
        self.mutable = self.mutable_cls(*self.args)
        self.immutable = self.immutable_cls(*self.args)
        super().setUp()
            
    def test_construct_mutable(self):
        self.mutable_cls(*self.args)
        
    def test_construct_immutable(self):
        self.immutable_cls(*self.args)
        
    def test_mutable_equality(self):
        self.assertEqual(self.mutable, self.mutable_cls(*self.args))
    
    def test_immutable_equality(self):
        self.assertEqual(self.immutable, self.immutable_cls(*self.args))
        
    def test_mutable_equals_to_immutable(self):
        self.assertEqual(self.mutable, self.immutable)
        self.assertEqual(self.immutable, self.mutable)
    
    def test_is_immutable(self):
        self.assertIsInstance(self.immutable, Immutable)
        
    def test_is_mutable(self):
        assert isinstance(self.mutable, Mutable), self.mutable


class SerializableBase(Base):
    def test_mutable_serialize_to_args(self):
        self.assertEqual(tuple(self.mutable), self.args)
    
    def test_immutable_serialize_to_args(self):
        self.assertEqual(tuple(self.immutable), self.args)
        
    
class LocatableBase(SerializableBase):
    def test_zero_displacement_does_not_change_type_mutable(self):
        new = self.mutable.displaced(0, 0)
        self.assertEqual(type(self.mutable), type(new))
        
    def test_zero_displacement_does_not_change_type_immutable(self):
        new = self.immutable.displaced(0, 0)
        self.assertEqual(type(self.immutable), type(new))
            
    def test_zero_displacement_does_not_change_object_mutable(self):
        new = self.mutable.displaced(0, 0)
        self.assertEqual(new, self.mutable)

    def test_zero_displacement_does_not_change_object_immutable(self):
        new = self.immutable.displaced(0, 0)
        self.assertEqual(new, self.immutable)

    def test_inplace_displacement_using_pos(self):
        obj = self.mutable_cls(*self.args)
        oldpos = obj.pos
        newpos = oldpos + (10, 10) 
        obj.pos = newpos
        self.assertAlmostEqual(obj.pos, newpos)
    
class HasAABBBase(unittest.TestCase):
    aabb_args = None
    
    def setUp(self):
        self.aabb_example = self.immutable_cls(*self.aabb_args)
        self.aabb_mexample = self.mutable_cls(*self.aabb_args)
        self.aabb_displaced= self.aabb_example.displaced(1, 1)
        self.aabb_mdisplaced = self.aabb_mexample.displaced(1, 1)
        super().setUp()
     
    def test_aabb_test(self):
        self.assertAlmostEqual(self.aabb_example.aabb, AABB(0, 1, 1, 2)) 
        self.assertAlmostEqual(self.aabb_mexample.aabb, AABB(0, 1, 1, 2))
    
    def test_displace_bounds(self):
        self.assertAlmostEqual(self.aabb_displaced.xmin, 1)
        self.assertAlmostEqual(self.aabb_displaced.xmax, 2)
        self.assertAlmostEqual(self.aabb_displaced.ymin, 2)
        self.assertAlmostEqual(self.aabb_displaced.ymax, 3)
        
    def test_mdisplace_bounds(self):
        self.assertAlmostEqual(self.aabb_mdisplaced.xmin, 1)
        self.assertAlmostEqual(self.aabb_mdisplaced.xmax, 2)
        self.assertAlmostEqual(self.aabb_mdisplaced.ymin, 2)
        self.assertAlmostEqual(self.aabb_mdisplaced.ymax, 3)
    
    def test_displace_shape(self):
        self.assertAlmostEqual(self.aabb_displaced.shape, (1, 1))
        self.assertAlmostEqual(self.aabb_displaced.width, 1)
        self.assertAlmostEqual(self.aabb_displaced.height, 1)
        
    def test_mdisplace_shape(self):
        self.assertAlmostEqual(self.aabb_mdisplaced.shape, (1, 1))
        self.assertAlmostEqual(self.aabb_mdisplaced.width, 1)
        self.assertAlmostEqual(self.aabb_mdisplaced.height, 1)
    
    def test_displace_points(self):
        self.assertAlmostEqual(self.aabb_displaced.pos, (1.5, 2.5))
        self.assertAlmostEqual(self.aabb_displaced.pos_sw, (1, 2))
        self.assertAlmostEqual(self.aabb_displaced.pos_se, (2, 2))
        self.assertAlmostEqual(self.aabb_displaced.pos_nw, (1, 3))
        self.assertAlmostEqual(self.aabb_displaced.pos_ne, (2, 3))
        
    def test_mdisplace_points(self):
        self.assertAlmostEqual(self.aabb_mdisplaced.pos, (1.5, 2.5))
        self.assertAlmostEqual(self.aabb_mdisplaced.pos_sw, (1, 2))
        self.assertAlmostEqual(self.aabb_mdisplaced.pos_se, (2, 2))
        self.assertAlmostEqual(self.aabb_mdisplaced.pos_nw, (1, 3))
        self.assertAlmostEqual(self.aabb_mdisplaced.pos_ne, (2, 3))
        
class CircleTest(LocatableBase, HasAABBBase):
    mutable_cls = mCircle
    immutable_cls = Circle
    args = (2.5, (0, 1))
    aabb_args = (0.5, (0.5, 1.5))

class SegmentTest(LocatableBase, HasAABBBase):
    mutable_cls = mSegment
    immutable_cls = Segment
    args = ((0, 1), (1, 2))
    aabb_args = ((0, 1), (1, 2))

class AABBTest(LocatableBase, HasAABBBase):
    mutable_cls = mAABB
    immutable_cls = AABB
    args = (0, 1, 0, 2)
    aabb_args = (0, 1, 1, 2)

class PolyTest(LocatableBase, HasAABBBase):
    mutable_cls = mPoly
    immutable_cls = Poly
    args = aabb_args = ((0, 1), (1, 1), (0, 2))
     
del Base, SerializableBase, LocatableBase, HasAABBBase
            
if __name__ == '__main__':
    unittest.main()
    