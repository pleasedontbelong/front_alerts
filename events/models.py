# -*- coding: utf-8 -*-
from django.db import models

from jsonfield import JSONField
from .constants import EVENT_STATUS


class Event(models.Model):
    event_data = JSONField(blank=True, null=True)
    received_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    parsed_date = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=EVENT_STATUS,
                                              default=EVENT_STATUS.RECEIVED)
    event_name = models.CharField(max_length=150, blank=True, null=True)
    event_id = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.status, self.received_date)
