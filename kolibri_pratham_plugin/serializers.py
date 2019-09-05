from rest_framework import serializers

from kolibri.auth.models import Facility

from .models import DataStore
import random
import string
import os 
import json
import datetime
import sys

N=6

class DataStoreSerializer(serializers.ModelSerializer):

	def __init__(self, *args, **kwargs):
		many = kwargs.pop('many', True)
		super(DataStoreSerializer, self).__init__(many=many, *args, **kwargs)

	data = serializers.JSONField(default='\{\}')
	filter_name = serializers.CharField(default='enter filter')
	table_name = serializers.CharField(default='enter name')
	facility = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all())
	created_at = serializers.DateTimeField(read_only=True)

	class Meta:
		model = DataStore
		fields = (
			'id', 'data', 'filter_name', 'table_name', 'facility', 'created_at',
		)
