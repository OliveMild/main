#!/usr/bin/env python3
"""User feed module for managing per-user activity feeds."""

import time
import uuid


# In-memory store: {user_id: [post_dict, ...]}
_feeds = {}


def add_post(user_id, content):
    """Add a post to a user's feed.

    Args:
        user_id: The identifier for the user (str or int).
        content: The text content of the post (str).

    Returns:
        A dict with 'success' (bool), 'message' (str), and on success
        'post' (dict) containing the created post.
    """
    if not user_id and user_id != 0:
        return {'success': False, 'message': 'user_id is required.'}
    if not isinstance(content, str) or not content.strip():
        return {'success': False, 'message': 'Post content cannot be empty.'}

    post = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'content': content.strip(),
        'timestamp': time.time(),
    }
    _feeds.setdefault(user_id, []).append(post)
    return {'success': True, 'message': 'Post added successfully.', 'post': post}


def get_feed(user_id):
    """Retrieve all posts in a user's feed, newest first.

    Args:
        user_id: The identifier for the user.

    Returns:
        A dict with 'success' (bool), 'message' (str), and on success
        'posts' (list of post dicts ordered newest-first).
    """
    if not user_id and user_id != 0:
        return {'success': False, 'message': 'user_id is required.'}

    posts = _feeds.get(user_id, [])[::-1]
    return {'success': True, 'message': f'{len(posts)} post(s) found.', 'posts': posts}


def delete_post(user_id, post_id):
    """Delete a post from a user's feed.

    Args:
        user_id: The identifier for the user.
        post_id: The unique ID of the post to remove.

    Returns:
        A dict with 'success' (bool) and 'message' (str).
    """
    if not user_id and user_id != 0:
        return {'success': False, 'message': 'user_id is required.'}
    if not post_id:
        return {'success': False, 'message': 'post_id is required.'}

    user_posts = _feeds.get(user_id, [])
    new_posts = [p for p in user_posts if p['id'] != post_id]
    if len(new_posts) == len(user_posts):
        return {'success': False, 'message': 'Post not found.'}
    _feeds[user_id] = new_posts
    return {'success': True, 'message': 'Post deleted successfully.'}


def clear_feed(user_id):
    """Remove all posts from a user's feed.

    Args:
        user_id: The identifier for the user.

    Returns:
        A dict with 'success' (bool) and 'message' (str).
    """
    if not user_id and user_id != 0:
        return {'success': False, 'message': 'user_id is required.'}

    _feeds.pop(user_id, None)
    return {'success': True, 'message': 'Feed cleared.'}


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print('Usage: user_feed.py <user_id> <content>')
        sys.exit(1)

    result = add_post(sys.argv[1], sys.argv[2])
    print(result['message'])
    sys.exit(0 if result['success'] else 1)
