from django.shortcuts import render
from django.http import JsonResponse
import tweepy
import keys
import json
from trends import woeid_data
from tweepy import OAuthHandler
import urllib.parse


def home(request):
    trends = [None]
    length = 0
    content = {
        'trends': trends,
        'length': 0,
    }
    woeid_json = woeid_data.data
    woeid_worldwide = 1  # WOEID CODE FOR WORLDWIDE
    woeid_india = 2295377  # WOEID CODE FOR INDIA
    woeid_mumbai = 23424848  # WOEID CODE FOR MUMBAI
    location = request.POST.get('location')
    if 'location' in request.POST:
        print(location)
        auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
        auth.set_access_token(keys.access_token, keys.access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        woeid_id = woeid(woeid_json, location)
        if woeid_id is not None:
            print(woeid_id)
            trends_json = api.trends_place(id=woeid_id)
            trends_list = trends_json[0]['trends']
            trends = []
            url = []
            i = 0
            for trend in trends_list:
                trends.append(trend['name'])
                url.append(urllib.parse.quote_plus(trend['name']))
                i = i + 1
            length = len(trends)
            result = zip(trends, url)
        content.update({'length': length, 'location': location, 'result':result})

    return render(request, "trends.html", content)


def woeid(json_object, location):
    for dict in json_object:
        if dict['location'] == location:
            return dict['woeid']