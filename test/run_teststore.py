#  from logic_bank.util import ConstraintException
#  just run as main
from safrs import ValidationError

import models
from db import session, remove_session
from app import create_app_for_test

create_app_for_test()


def read_all_stores():
    result = {'items': list(map(lambda s: s.json(), models.StoreModel.query.all()))}
    print(result)


def count_stores():
    result = models.StoreModel.query.count()
    print("Number of Stores: {} ".format(result))


def count_items_for_store(store_id: int):
    result = models.ItemModel.query.filter_by(store_id=store_id).count()
    print("Number of Items: {}  for Store {}".format(result, store_id))


def add_store_and_delete_again():
    store = models.StoreModel("StoreToAdd")
    store.save_to_db()
    print("added store: {}".format(store.json()))
    count_stores()
    store.delete_from_db()
    print("store  deleted")
    count_stores()


def add_store_with_x():
    store = models.StoreModel("StoreXYZ")
    try:
        store.save_to_db()
    except ValidationError :
        session.rollback()  
    else:
        print("Missing Constraint exception: 'NO x in Store Name'")


def add_store_and_item_and_delete_again():
    store = models.StoreModel("StoreToAdd")
    store.save_to_db()
    item1 = models.ItemModel('item1', 9.99, store.id)
    item2 = models.ItemModel('item2', 8.99, store.id)
    item1.save_to_db()
    item2.save_to_db()
    count_items_for_store(store.id)
    print("Item_Count from LogicRule: {}".format(store.item_count))
    item1.delete_from_db()
    item2.delete_from_db()
    count_items_for_store(store.id)
    print("Item_Count from LogicRule: {}".format(store.item_count))
    store.delete_from_db()


'''
def add_store_and_item_and_delete_again_store_first():
    store = models.StoreModel("StoreToAddFkTest")
    store.save_to_db()
    item1 = models.ItemModel('item1FkTest', 9.98, store.id)
    item2 = models.ItemModel('item2FkTest', 8.98, store.id)
    item1.save_to_db()
    item2.save_to_db()
    count_items_for_store(store.id)
    print("Item_Count from LogicRule: {}".format(store.item_count))
    try:
        store.delete_from_db()
    except ConstraintException as e:
        print("expected exception: {} ".format(e))
        session = db.Session()
        session.rollback()
    else:
        session = db.Session()
        session.rollback()
        print("Missing Constraint exception: 'Delete rejected - items has rows'")
    finally:
        count_items_for_store(store.id)
        item1.delete_from_db()
        item2.delete_from_db()
        count_items_for_store(store.id)
        store.delete_from_db()
        print("Finally Delete Store and Items in correct order")
'''


def add_item_no_parent():
    item1 = models.ItemModel('itemNoParent', 9.99, None)
    item1.save_to_db()


def add_item_non_existing_parent():
    try:
        item1 = models.ItemModel('itemNoParent', 9.99, 4711)
        item1.save_to_db()
    except Exception as e:
        print("expected exception: {} ".format(e))
        session.rollback()
    else:
        print("Missing Constraint exception: 'no parent for item'")


if __name__ == "__main__":
    #   add_item_no_parent()  # currently throws exceptions
    #   add_store_and_item_and_delete_again_store_first()

    add_item_non_existing_parent()

    read_all_stores()
    count_stores()
    add_store_and_delete_again()
    add_store_with_x()

    add_store_and_item_and_delete_again()
    remove_session()
