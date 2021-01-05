# noinspection PyUnresolvedReferences
from safrs import ValidationError

import db
import models
import util
# noinspection PyUnresolvedReferences
import logic
import unittest

from app import create_app_for_test


class TestModel(unittest.TestCase):
    create_app_for_test()

    def test_add_store_and_delete_again(self):
        orig = count_stores()
        expected = orig + 1
        store = models.StoreModel(name="StoreToAdd", email="StoreToAdd@mail.com", store_type="pos")
        store.save_to_db()
        util.log(store.json())
        result = count_stores()
        print("added store: {}".format(store.json()))
        self.assertEqual(result, expected)
        store.delete_from_db()
        result = count_stores()
        expected = orig
        self.assertEqual(result, expected)
        print("store  deleted")
        count_stores()

    def test_add_store_and_item_and_delete_again(self):
        store = models.StoreModel(name="StoreToAdd", email="StoreToAdd@mail.com", store_type="pos")
        store.save_to_db()
        item1 = models.ItemModel('item1', 9.99, store.id)
        item2 = models.ItemModel('item2', 8.99, store.id)
        item1.save_to_db()
        item2.save_to_db()
        result = count_items_for_store(store.id)
        expected = 2
        self.assertEqual(result, expected)
        self.assertEqual(store.item_count, expected)
        print("Item_Count from LogicRule: {}".format(store.item_count))
        item1.delete_from_db()
        item2.delete_from_db()
        result = count_items_for_store(store.id)
        expected = 0
        self.assertEqual(result, expected)
        self.assertEqual(store.item_count, expected)
        print("Item_Count from LogicRule: {}".format(store.item_count))
        store.delete_from_db()

    @unittest.skip("throws IntegrityError('(sqlite3.IntegrityError) NOT NULL constraint failed: items.store_id")
    def test_add_store_and_item_and_delete_again_store_first(self):
        #  currently fails parent check regression
        store = models.StoreModel("StoreToAddFkUnitTest")
        store.save_to_db()
        item1 = models.ItemModel('item1FkUnitTest', 9.98, store.id)
        item2 = models.ItemModel('item2FkUnitTest', 8.98, store.id)
        item1.save_to_db()
        item2.save_to_db()
        result = count_items_for_store(store.id)
        expected = 2
        self.assertEqual(result, expected)
        self.assertEqual(store.item_count, expected)
        print("ItemCount from LogicRule: {}".format(store.item_count))
        result: (Exception, None) = None
        try:
            store.delete_from_db()
        except ValidationError as e:
            print("expected exception: {} ".format(e))
            db.session.rollback()
            result = e
        except Exception as e:
            print("unexpected exception: {} ".format(e))
            db.session.rollback()
            result = e
        else:
            print("Missing Constraint exception: 'Delete rejected - items has rows'")
        finally:
            count_items_for_store(store.id)
            item1.delete_from_db()
            item2.delete_from_db()
            count_items_for_store(store.id)
            store.delete_from_db()
            print("Finally Delete Store and Items in correct order")

        self.assertIsInstance(result, ValidationError)

    def test_add_store_with_x_trigger_constraint(self):
        store = models.StoreModel("StoreXYZ")
        result: (Exception, None) = None
        try:
            store.save_to_db()
        except ValidationError as e:
            print("expected exception: {} ".format(e))
            db.session.rollback()
            result = e
        except Exception as e:
            print("unexpected exception: {} ".format(e))
            db.session.rollback()
            result = e
        else:
            print("Missing Constraint exception: 'NO x in Store Name'")

        self.assertIsInstance(result, ValidationError)  # ConstraintException


def count_stores() -> int:
    result: int = models.StoreModel.query.count()
    print("Number of Stores: {} ".format(result))
    return result


def count_items_for_store(store_id: int) -> int:
    result: int = models.ItemModel.query.filter_by(store_id=store_id).count()
    print("Number of Items: {}  for Store {}".format(result, store_id))
    return result


if "__main__" == __name__:
    unittest.main()
