from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from django.shortcuts import render

from config.mongo_conf import client, mongo_wrap


class LogPage(APIView):
    """ home page """

    view_name = 'logs'
    template_name = 'base.html'

    def get(self, request):
        context = dict()
        return render(request, self.template_name, context)


class WqLogs(APIView):
    """ wq page """

    view_name = 'wq'
    template_name = 'logs/wq.html'

    def get(self, request):
        action = request.query_params.get('action')
        print('action', action)
        if action == 'get_data':
            print('get_data', )

            db = client.test
            collection = db.wq_access
            res = collection.find({}).sort("create_date", -1).limit(50)
            data = mongo_wrap(res)
            return HttpResponse(data)

        context = dict()
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
