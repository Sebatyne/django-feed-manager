from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Item

class PeriodTestCase(TestCase):

    def test_createAccountAndPostOneItem(self):
        data = {
            'username': 'user',
            'password': 'pass',
        }

        # Create an account
        res = self.client.post(
            '/feed/createAccount/',
            {
                'username': data['username'],
                'password': data['password']
            }
        )

        self.assertEqual(res.status_code, 200)

        feed_id = res.json()['feed_id']

        # Validate user
        user_set = User.objects.filter(username=data['username'])
        self.assertEqual(len(user_set), 1)

        user = user_set.first()
        user.is_active = True
        user.save()

        # Post a feed item
        res = self.client.post(
            '/feed/%d/postItem/' % feed_id,
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
