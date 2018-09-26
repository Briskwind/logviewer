import json

from extensions.mongo_conf import ACCESS, DRUGLISTRPC_OUT, WANGQIANCELERY_ERR, XSL_ACCESS, XSL_API_ACCESS, XSL_EYAOS_ERR
from rest_framework.views import APIView
from django.shortcuts import render

from extensions.common import get_data_by_conditions, mongo_wrap

from logviewer.settings import PAGE_COUNT


class WqLogs(APIView):
    """ wq page """

    view_name = 'wq'
    template_name = 'logs/wq.html'

    def get(self, request):
        start_time = request.GET.get('start', None)
        end_time = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        res = get_data_by_conditions(start_time, end_time, key_words, ACCESS)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT
        data = mongo_wrap(res)
        context = dict(

            data=data[::-1],
            items=data[start:end][::-1],
        )

        return render(request, self.template_name, context)


class CeleryLogs(APIView):
    """ celery page """

    view_name = 'celery'
    template_name = 'logs/celery.html'

    def get(self, request):
        start_time = request.GET.get('start', None)
        end_time = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        res = get_data_by_conditions(start_time, end_time, key_words, WANGQIANCELERY_ERR)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT
        data = mongo_wrap(res)

        context = dict(
            data=data,
            items=data[start:end][::-1],
        )
        return render(request, self.template_name, context)


class DruglistLogs(APIView):
    """ druglist page """

    view_name = 'wq'
    template_name = 'logs/druglist.html'

    def get(self, request):
        start_time = request.GET.get('start', None)
        end_time = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        res = get_data_by_conditions(start_time, end_time, key_words, DRUGLISTRPC_OUT)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT
        data = mongo_wrap(res)

        context = dict(
            data=data,
            items=data[start:end][::-1],
        )
        return render(request, self.template_name, context)



class XslAccess(APIView):
    """ 新势力日志"""
    view_name = 'xsl_access'
    template_name = 'logs/xsl_access.html'

    def get(self, request):
        start_time = request.GET.get('start', None)
        end_time = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        res = get_data_by_conditions(start_time, end_time, key_words, XSL_ACCESS)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT
        data = mongo_wrap(res)

        context = dict(
            data=data,
            items=data[start:end][::-1],
        )
        return render(request, self.template_name, context)



class XslApiAccess(APIView):
    """ 新势力日志"""
    view_name = 'xsl_api_access'
    template_name = 'logs/xsl_api_access.html'

    def get(self, request):
        start_time = request.GET.get('start', None)
        end_time = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        res = get_data_by_conditions(start_time, end_time, key_words, XSL_API_ACCESS)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT
        data = mongo_wrap(res)

        context = dict(
            data=data,
            items=data[start:end][::-1],
        )
        return render(request, self.template_name, context)


class XslEyaosError(APIView):
    """ 新势力日志"""
    view_name = 'xsl_eyaos_error'
    template_name = 'logs/xsl_eyaos_error.html'

    def get(self, request):
        start_time = request.GET.get('start', None)
        end_time = request.GET.get('end', None)
        key_words = request.GET.get('key_words', None)
        page = int(request.GET.get('page', 1))

        res = get_data_by_conditions(start_time, end_time, key_words, XSL_EYAOS_ERR)

        start = PAGE_COUNT * (page - 1)
        end = start + PAGE_COUNT
        data = mongo_wrap(res)

        context = dict(
            data=data,
            items=data[start:end][::-1],
        )
        return render(request, self.template_name, context)