from django.db import models
from jsonfield import JSONField
from django.db.models import ForeignKey

from kolibri.auth.models import AbstractFacilityDataModel
from kolibri.auth.models import Facility


class DataStore(AbstractFacilityDataModel):
    morango_model_name = "datastore"

    data = JSONField(default={}, blank=True)
    filter_name = models.CharField(max_length=100, default='enter filter name')
    table_name = models.CharField(max_length=100, default='enter table name')
    facility = ForeignKey(Facility)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def infer_dataset(self, *args, **kwargs):
        return self.facility.dataset

    def calculate_partition(self):
        return self.dataset_id
