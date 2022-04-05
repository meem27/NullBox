from django.shortcuts import render
from django.views import View
import requests
from requests_html import HTML, HTMLSession
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import wikipedia
# Create your views here.


class StackView(View):
    def get(self, request, *args, **kwargs):
        stack_title = []
        stack_link = []

        if 'stack' in request.GET:
            stack = request.GET.get('stack')
            resp = requests.get(
                f"https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle={str(stack)}&site=stackoverflow")
            print(resp)
            d = resp.json()
            for i in d['items']:
                stack_title.append(i["link"])
                stack_link.append(i["link"])

        data = {'title': stack_title, 'link': stack_link}

        return render(request, 'SiteTool/stack.html', {'data': data})


class UrbanView(View):
     def get(self, request, *args, **kwargs):
          meanings=[]
          link=None
          if 'urbansearch' in request.GET:
               urbansearch = request.GET.get('urbansearch')
               session = HTMLSession()
               l=f'https://www.urbandictionary.com/define.php?term={str(urbansearch)}'
               r = session.get(
                    f'https://www.urbandictionary.com/define.php?term={str(urbansearch)}')
               
               meaning = r.html.find('.meaning', first=False)
               for m in meaning:
                    meanings.append(m.text)
               link=l
          data = {
               'top_meaning': meanings[:1],
               'meaning': meanings[2:],
               'link':link
          }
          return render(request, 'SiteTool/urban.html', {'data': data})


class WikiView(View):
    def get(self, request, *args, **kwargs):
        Summary=None

        if 'wiki' in request.GET:
            wiki = request.GET.get('wiki')
            summary=wikipedia.summary(wiki,sentences=5,chars=2000,auto_suggest=True,redirect=True)
            Summary=summary
        return render(request, 'SiteTool/wiki.html', {'data': Summary})
