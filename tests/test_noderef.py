# -*- coding: utf-8 -*-
import sys
sys.path[0:0] = [""]
import unittest

from bson import DBRef, ObjectId

from mongoengine import *
from mongoengine.connection import get_db
from mongoengine.context_managers import query_counter, no_dereference


class NoDerefTests(unittest.TestCase):

    def setUp(self):
        connect(db='mongoenginetest')
        self.db = get_db()

    def test_no_dereference(self):
        class TestUser(Document):
            name = StringField()

        class TestPost(Document):
            author = ReferenceField('TestUser', dbref=False)

        TestUser.drop_collection()
        TestPost.drop_collection()

        bob = TestUser(name='Bob')
        bob.save()
        TestPost(author=bob).save()

        # check normal usage
        post = TestPost.objects.first()
        self.assertTrue(isinstance(post.author, TestUser))

        # test no_dereference
        post = TestPost.objects.no_dereference().first()
        self.assertTrue(isinstance(post.author, DBRef))

        # test no_dereference with iteration ------ It will FAIL
        for post in TestPost.objects.no_dereference():
            self.assertTrue(isinstance(post.author, DBRef))

        with no_dereference(TestPost) as NDTestPost:
            # This case still fails!
            post = TestPost.objects.first()
            self.assertTrue(isinstance(post.author, ObjectId))

if __name__ == '__main__':
    unittest.main()