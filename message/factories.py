# -*- coding: utf-8 -*-

import random

import factory
from factory import django, fuzzy
from test.factories import UserFactory
from test.utils import lorem_ipsum

from geozones.factories import LocationFactory
from .models import Message


def point_gen(num):
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    return "POINT(%f %f)" % (longitude, latitude)


class MessageFactory(django.DjangoModelFactory):
    """ Factory for messages. """
    FACTORY_FOR = Message

    message = lorem_ipsum()
    user = factory.SubFactory(UserFactory)
    messageType = fuzzy.FuzzyChoice(
        (Message.REQUEST, Message.OFFER, Message.INFO))
    is_virtual = fuzzy.FuzzyChoice((True, False))

    @factory.lazy_attribute
    def linked_location(self):
        if self.is_virtual:
            ret = None
        else:
            ret = LocationFactory()
        return ret
