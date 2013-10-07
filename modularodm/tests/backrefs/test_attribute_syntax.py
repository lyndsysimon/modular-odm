import unittest

# from modularodm import StoredObject
from modularodm.fields import ForeignField, StringField, ForeignList
from modularodm.storedobject import ContextLogger
from modularodm.tests import (
    ModularOdmTestCase
)
from modularodm import StoredObject


class OneToManyFieldTestCase(ModularOdmTestCase):

    def define_objects(self):

        class Foo(StoredObject):
            _meta = {
                'optimistic': True
            }
            _id = StringField()
            my_bar = ForeignField('Bar', backref='my_foos')
            my_other_bar = ForeignField('Bar', backref='my_foos')

        class Bar(StoredObject):
            _meta = {'optimistic': True}
            _id = StringField()

        return Foo, Bar

    def set_up_objects(self):

        self.bar = self.Bar()
        self.bar.save()

        self.foos = []
        for i in xrange(5):
            foo = self.Foo()
            if i > 0:
                foo.my_bar = self.bar
            else:
                foo.my_other_bar = self.bar
            foo.save()
            self.foos.append(foo)

    def test_dunder_br_returns_foreignlist(self):
        self.assertIs(
            type(self.bar.foo__my_foos),
            ForeignList
        )

    def test_dunder_br_returns_correct(self):
        self.assertEqual(
            len(self.bar.foo__my_foos),
            5
        )

    @unittest.skip('Behavior not defined.')
    def test_dunder_br_unknown_field(self):
        with self.assertRaises(KeyError):
            self.bar.foo__not_a_real_key

    def test_dunder_br_unknown_node(self):
        with self.assertRaises(KeyError):
            self.bar.not_a_real_node__foo

    def test_dunder_br_parent_field_correct(self):
        self.assertEqual(
            len(self.bar.foo__my_foos__my_other_bar),
            1
        )

    def test_dunder_br_laziness(self):
        StoredObject._clear_caches()

        with ContextLogger() as c:
            # get the Bar object
            bar = self.Bar.find_one()
            # access the ForeignList
            bar.foo__my_foos

            # Two calls so far - .find_one() and .find()
            self.assertNotIn(
                'foo',
                [k[0] for k, v in c.report().iteritems()],
            )

            # access a member of the ForeignList, forcing that member to load
            bar.foo__my_foos[0]

            # now there should be a call to Foo.get()
            self.assertEqual(
                c.report()[('foo', 'get')][0],
                1
            )