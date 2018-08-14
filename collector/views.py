import json

import datetime
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from django.shortcuts import render

from config.mongo_conf import client, mongo_wrap

# class LogPage(APIView):
#     """ home page """
#
#     view_name = 'logs'
#     template_name = 'base.html'
#
#     def get(self, request):
#         context = dict()
#         return render(request, self.template_name, context)
from logviewer.settings import PAGE_COUNT


class WqLogs(APIView):
    """ wq page """

    view_name = 'wq'
    template_name = 'logs/wq.html'

    def get(self, request):
        db = client.test
        collection = db.wq_access

        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        conditions = {}
        create_date_dict = {}
        if start:
            start_time = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            create_date_dict["$gt"] = start_time

        if end:
            end_time = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
            create_date_dict["$lt"] = end_time

        if key_words:
            conditions['log'] = {"$regex": key_words}

        if start or end:
            conditions['create_date'] = create_date_dict

        res = collection.find(conditions).sort("create_date", -1).limit(500)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT

        data = mongo_wrap(res)
        context = dict(
            data=data,
            items=data[start:end],
        )

        return render(request, self.template_name, context)


class CeleryLogs(APIView):
    """ celery page """

    view_name = 'celery'
    template_name = 'logs/celery.html'

    def get(self, request):
        context = dict()
        return render(request, self.template_name, context)


class DruglistLogs(APIView):
    """ druglist page """

    view_name = 'wq'
    template_name = 'logs/druglist.html'

    def get(self, request):
        context = dict()
        return render(request, self.template_name, context)
