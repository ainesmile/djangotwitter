from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.test import Client

from twitter.views import handler
from twitter.models import Tweet, Followship

class HandleTest(TestCase):
    fixtures = [
        'twitter/fixtures/test_user_data.json',
        'twitter/fixtures/test_tweet_data.json',
        'twitter/fixtures/test_replyship_data.json',
        'twitter/fixtures/test_followship_data.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

        self.tweet_from_admin = Tweet.objects.get(pk=1)
        self.tweet_from_user1 = Tweet.objects.get(pk=2)
        self.tweet_from_user2 = Tweet.objects.get(pk=3)

        self.reply_from_admin_to_admin = Tweet.objects.get(pk=5)
        self.reply_from_admin_to_user1 = Tweet.objects.get(pk=6)
        self.reply_from_admin_to_user2 = Tweet.objects.get(pk=7)
        self.reply_from_admin_to_user3 = Tweet.objects.get(pk=8)
        

    def test_get_receivers_should_be_adminuser12_stream_type_tweet(self):
        users = set([self.admin, self.user1, self.user2])
        receivers = handler.get_receivers(self.tweet_from_admin, 'T')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_user12_stream_type_tweet(self):
        users = set([self.user1, self.user2])
        receivers = handler.get_receivers(self.tweet_from_user1, 'T')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_user2_stream_type_tweet(self):
        users = set([self.user2])
        receivers = handler.get_receivers(self.tweet_from_user2, 'T')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_admin_stream_type_reply(self):
        users = set([self.admin])
        receivers = handler.get_receivers(self.reply_from_admin_to_admin, 'Y')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_adminuser12_stream_type_reply(self):
        users = set([self.admin, self.user1, self.user2])
        receivers = handler.get_receivers(self.reply_from_admin_to_user1, 'Y')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_adminuser2_stream_type_reply(self):
        users = set([self.admin, self.user2])
        receivers = handler.get_receivers(self.reply_from_admin_to_user2, 'Y')
        self.assertEqual(receivers, users)

    def test_get_receivers_should_be_admin_stream_type_reply(self):
        users = set([self.admin])
        receivers = handler.get_receivers(self.reply_from_admin_to_user3, 'Y')
        self.assertEqual(receivers, users)