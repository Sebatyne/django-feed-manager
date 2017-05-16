from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed as SyndicationFeed
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render

from .models import Feed, Item


class FeedView(SyndicationFeed):

    def get_object(self, request, feed_id):
        if request.method == 'POST':
            return postItem(request, feed_id)
        return Feed.objects.get(pk=feed_id)

    def description(self, feed):
        return feed.description

    def link(self, feed):
        return feed.link

    def title(self, feed):
        return feed.title


    def items(self, feed):
        return feed.item_set.order_by('pubDate')


    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pubDate

    def item_title(self, item):
        return item.title


@csrf_exempt
def createAccount(request):
    if 'username' not in request.POST \
            and 'password' not in request.POST:
        return HttpResponse(status=500)

    user = User.objects.create_user(request.POST['username'], password=request.POST['password'], is_active=False)
    user.save()

    feed = Feed.objects.create(
        title = "Computer status for %s" % request.POST['username'],
        link = "",
        description = "",
        language = "en",
        maximum_length = int(request.POST.get('maximum_length', 50)),
        user=user,
    )
    feed.save()

    return JsonResponse({'feed_id': feed.id})


@csrf_exempt
def postItem(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    item_attribute_dict = {}
    for item in Item.PROPERTY_LIST:
        try:
          item_attribute_dict[item] = request.POST[item]
        except KeyError:
            pass
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return HttpResponse(status=401)
    except KeyError:
        return HttpResponse(status=500)
    feed.addItem(**item_attribute_dict)
    return HttpResponse(status=200)
