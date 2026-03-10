#!/usr/bin/env python3
"""Tests for the user feed module."""

import unittest
from user_feed import add_post, get_feed, delete_post, clear_feed


class TestAddPost(unittest.TestCase):
    """Tests for the add_post function."""

    def setUp(self):
        clear_feed('user1')

    def tearDown(self):
        clear_feed('user1')

    def test_add_post_success(self):
        result = add_post('user1', 'Hello, world!')
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Post added successfully.')
        self.assertIn('post', result)

    def test_add_post_returns_post_with_fields(self):
        result = add_post('user1', 'My first post')
        post = result['post']
        self.assertIn('id', post)
        self.assertIn('user_id', post)
        self.assertIn('content', post)
        self.assertIn('timestamp', post)
        self.assertEqual(post['user_id'], 'user1')
        self.assertEqual(post['content'], 'My first post')

    def test_add_post_strips_whitespace(self):
        result = add_post('user1', '  trimmed  ')
        self.assertEqual(result['post']['content'], 'trimmed')

    def test_add_post_missing_user_id(self):
        result = add_post(None, 'Hello')
        self.assertFalse(result['success'])
        self.assertIn('user_id', result['message'])

    def test_add_post_empty_user_id_string(self):
        result = add_post('', 'Hello')
        self.assertFalse(result['success'])

    def test_add_post_empty_content(self):
        result = add_post('user1', '')
        self.assertFalse(result['success'])
        self.assertIn('empty', result['message'])

    def test_add_post_whitespace_only_content(self):
        result = add_post('user1', '   ')
        self.assertFalse(result['success'])

    def test_add_post_none_content(self):
        result = add_post('user1', None)
        self.assertFalse(result['success'])

    def test_add_post_numeric_user_id(self):
        clear_feed(42)
        result = add_post(42, 'Numeric user')
        self.assertTrue(result['success'])
        clear_feed(42)

    def test_add_post_zero_user_id(self):
        clear_feed(0)
        result = add_post(0, 'Zero ID user')
        self.assertTrue(result['success'])
        clear_feed(0)


class TestGetFeed(unittest.TestCase):
    """Tests for the get_feed function."""

    def setUp(self):
        clear_feed('user2')

    def tearDown(self):
        clear_feed('user2')

    def test_get_feed_empty(self):
        result = get_feed('user2')
        self.assertTrue(result['success'])
        self.assertEqual(result['posts'], [])

    def test_get_feed_returns_posts(self):
        add_post('user2', 'First')
        add_post('user2', 'Second')
        result = get_feed('user2')
        self.assertTrue(result['success'])
        self.assertEqual(len(result['posts']), 2)

    def test_get_feed_newest_first(self):
        add_post('user2', 'First')
        add_post('user2', 'Second')
        result = get_feed('user2')
        self.assertEqual(result['posts'][0]['content'], 'Second')
        self.assertEqual(result['posts'][1]['content'], 'First')

    def test_get_feed_missing_user_id(self):
        result = get_feed(None)
        self.assertFalse(result['success'])
        self.assertIn('user_id', result['message'])

    def test_get_feed_message_includes_count(self):
        add_post('user2', 'A post')
        result = get_feed('user2')
        self.assertIn('1', result['message'])


class TestDeletePost(unittest.TestCase):
    """Tests for the delete_post function."""

    def setUp(self):
        clear_feed('user3')

    def tearDown(self):
        clear_feed('user3')

    def test_delete_post_success(self):
        post_id = add_post('user3', 'Delete me')['post']['id']
        result = delete_post('user3', post_id)
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Post deleted successfully.')

    def test_delete_post_removes_from_feed(self):
        post_id = add_post('user3', 'Delete me')['post']['id']
        delete_post('user3', post_id)
        self.assertEqual(get_feed('user3')['posts'], [])

    def test_delete_post_not_found(self):
        result = delete_post('user3', 'nonexistent-id')
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'])

    def test_delete_post_missing_user_id(self):
        result = delete_post(None, 'some-id')
        self.assertFalse(result['success'])

    def test_delete_post_missing_post_id(self):
        result = delete_post('user3', None)
        self.assertFalse(result['success'])
        self.assertIn('post_id', result['message'])

    def test_delete_only_specified_post(self):
        id1 = add_post('user3', 'Keep me')['post']['id']
        id2 = add_post('user3', 'Delete me')['post']['id']
        delete_post('user3', id2)
        posts = get_feed('user3')['posts']
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['id'], id1)


class TestClearFeed(unittest.TestCase):
    """Tests for the clear_feed function."""

    def setUp(self):
        clear_feed('user4')

    def tearDown(self):
        clear_feed('user4')

    def test_clear_feed_success(self):
        add_post('user4', 'A post')
        result = clear_feed('user4')
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Feed cleared.')

    def test_clear_feed_removes_all_posts(self):
        add_post('user4', 'Post 1')
        add_post('user4', 'Post 2')
        clear_feed('user4')
        self.assertEqual(get_feed('user4')['posts'], [])

    def test_clear_feed_missing_user_id(self):
        result = clear_feed(None)
        self.assertFalse(result['success'])

    def test_clear_nonexistent_feed(self):
        result = clear_feed('no-such-user-xyz')
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()
