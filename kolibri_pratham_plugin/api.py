from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from pip._vendor.html5lib import filters
from rest_framework import pagination, permissions, viewsets, status
from rest_framework.decorators import action

from kolibri.auth.api import KolibriAuthPermissionsFilter
from kolibri.plugins.coach.api import OptionalPageNumberPagination

from .models import DataStore
from .serializers import DataStoreSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from pprint import pprint
import random
import string
import os
import json
import datetime
import sys
import time

N=6


class DataStoreViewset(viewsets.ModelViewSet):
    model = DataStore
    filter_backends = (KolibriAuthPermissionsFilter, DjangoFilterBackend, SearchFilter,)
    queryset = DataStore.objects.all()
    serializer_class = DataStoreSerializer
    filter_fields = ('filter_name', 'table_name')
    # permission_classes = (KolibriReportPermissions,)
    pagination_class = OptionalPageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

        def save_in_folder():
            if serializer.data['table_name'] == 'USAGEDATA':
                randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
                with open(os.path.join(r"D:\Kolibri_data_bkp\AutoDataBackup",
                                       randstr+'.json'), "w+") as outfile:
                    json.dump(self.request.data, outfile, indent=4, sort_keys=True)
            else:
                pass

        save_in_folder()

        def show_data():
            if serializer.data['table_name'] == 'USAGEDATA':
                device_id = serializer.data['data']['metadata']['DeviceId']
                serial_id = serializer.data['data']['metadata']['SerialID']
                app_name = serializer.data['data']['metadata']['appName']
                apk_version = serializer.data['data']['metadata']['apkVersion']
                score_count = serializer.data['data']['metadata']['ScoreCount']
                pratham_code = serializer.data['data']['metadata']['prathamCode']
                device_name = serializer.data['data']['metadata']['DeviceName']

                now = datetime.datetime.now()

                view_to_crl = {
                                "device_id": str(device_id).encode("ascii", "replace").decode(),
                                "serial_id": serial_id.encode("ascii", "replace").decode(),
                                "app_name": app_name.encode("ascii", "replace").decode(),
                                "apk_version": apk_version.encode("ascii", "replace").decode(),
                                "score_count": score_count,
                                "pratham_code": pratham_code.encode("ascii", "replace").decode(),
                                "device_name": device_name.encode("ascii", "replace").decode(),
                                "date": now.strftime("%Y-%m-%d %H:%M:%S")
                            }

                view_to_crl = str(view_to_crl).encode("ascii", "replace").decode()

                try:
                    with open(os.path.join(r"D:\Kolibri_data_bkp\AutoSummaryBackup",
                                           'score_data.json'), "a") as newfile:
                        newfile.writelines(view_to_crl.encode().decode()+",")
                        newfile.write("\n")
                except Exception as e:
                    print(e)

        show_data()

# def get_queryset(self):
    #     self.queryset = DataStore.objects.all()
    #     self.filter_name = self.request.query_params.get('filter_name', None)
    #     self.table_name = self.request.query_params.get('table_name', None)

    #     if self.filter_name is not None:
    #         self.queryset = self.queryset.filter(filter_name__iexact=self.filter_name)
    #     if self.table_name is not None:
    #         self.queryset = self.queryset.filter(table_name__iexact=self.table_name)
    #     elif self.filter_name and self.table_name:
    #         self.queryset = self.queryset.filter(filter_name__iexact=self.filter_name,
    #         table_name__iexact=self.table_name)

    #     print(self.table_name)

    #     return self.
