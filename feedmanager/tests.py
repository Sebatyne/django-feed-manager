from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Feed, Item

class PeriodTestCase(TestCase):

    def _createAccount(self, **kw):
        data = {
            'username': 'user',
            'password': 'pass',
        }
        data.update(kw)

        # Create an account
        res = self.client.post(
            '/feed/createAccount/',
            data,
        )

        self.assertEqual(res.status_code, 200)

        data['feed_id'] = res.json()['feed_id']

        # Validate user
        user_set = User.objects.filter(username=data['username'])
        self.assertEqual(len(user_set), 1)

        data['user'] = user_set.first()
        data['user'].is_active = True
        data['user'].save()

        return data


    def test_createAccountAndPostOneItem(self):
        data = self._createAccount()

        # Post a feed item
        res = self.client.post(
            '/feed/%d/postItem/' % data['feed_id'],
            {
                'username': data['username'],
                'password': data['password'],
                'title': 'Item Title',
                'link': 'Item Link',
                'description': 'Item Description',
                'pubDate': timezone.now().isoformat()[:10],
            }
        )

        self.assertEqual(res.status_code, 200)

        self.assertEqual(
            len(Item.objects.all()), 1)


    def test_feedNeverGrowMoreThanItsMaximumLength(self):
        max_length = 10
        data = self._createAccount(maximum_length=max_length)

        for i in range(max_length * 2):
            self.client.post(
                '/feed/%d/postItem/' % data['feed_id'],
                {
                    'username': data['username'],
                    'password': data['password'],
                    'title': 'Item Title %s' % i,
                    'link': 'Item Link',
                    'description': 'Item Description',
                    'pubDate': timezone.now().isoformat()[:10],
                }
            )

        self.assertEqual(
            len(Item.objects.all()), max_length)

        remaining_title_list = ['Item Title %s' % i for i in range(10, 20)]
        feed = Feed.objects.get(id=data['feed_id'])
        item_list = Item.objects.filter(feed=feed)

        for item in item_list:
            self.assertIn(item.title, remaining_title_list)
