import PyRSS2Gen as RSS2

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render

from .models import Feed

FEED_ELEMENT_LIST = ['title', 'link', 'description', 'language']
ITEM_ELEMENT_LIST = ['title', 'link', 'description', 'pubDate']

def __getRSSItemList(item_list):
    rss_item_list = []
    for item in item_list:
        rss_item_list.append(
            RSS2.RSSItem(
              **{element: getattr(item, element, '')
                 for element in ITEM_ELEMENT_LIST}
            )
        )
    return rss_item_list


def printFeed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    item_list = feed.item_set.order_by('pubDate')

    return HttpResponse(
      RSS2.RSS2(
        items=__getRSSItemList(item_list),
        **{element: getattr(feed, element, '')
           for element in FEED_ELEMENT_LIST}
      ).to_xml()
    )

@csrf_exempt
def createAccount(request):
    if 'username' not in request.POST \
    or 'password' not in request.POST:
        return HttpResponse(status=500)
    user = User.objects.create_user(request.POST['username'], password=request.POST['password'], is_active=False)
    user.save()
    feed = Feed.objects.create(
        title = "Computer status for %s" % request.POST['username'],
        link = "",
        description = "",
        language = "en",
        maximum_length = 50,
        user=user,
    )
    feed.save()
    return JsonResponse({'feed_id': feed.id})

@csrf_exempt
def postItem(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    item_attribute_dict = {}
    for item in ITEM_ELEMENT_LIST:
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

