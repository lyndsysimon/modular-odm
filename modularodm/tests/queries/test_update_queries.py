from modularodm.tests import PickleStorageTestCase


class UpdateQueryBase(object):
    def test_update(self):
        """ Given a query, and an update clause, update all (and only) object
        returned by query.
        """
        pass

    def test_update_one(self):
        """ Given a primary key, update the referenced object according to the
        update clause
        """
        pass

    def test_remove(self):
        """ Given a query, remove all (and only) object returned by query. """
        pass

    def test_remove_one(self):
        """ Given a primary key, remove the referenced object. """
        pass


class UpdateQueryPickleTestCase(UpdateQueryBase, PickleStorageTestCase):
    pass


# TODO: MongoStorageTestCase not yet implemented
# class UpdateQueryMongoTestCase(UpdateQueryBase, MongoStorageTestCase):
#     pass