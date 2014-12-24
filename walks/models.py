# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Walk(models.Model):
    """
    A Walk belongs to a user, it has a distance in meters,
    a duration (time) in seconds and a date.
    """
    user = models.ForeignKey(User)
    distance = models.FloatField()
    time = models.IntegerField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"Walk: (distance:{}) (time:{}) (date:{})".format(
            self.distance, self.time, self.date
        )
