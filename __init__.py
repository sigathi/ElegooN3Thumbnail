# Copyright (c) 2023 sigathi
# Copyright (c) 2020 LotmaxxSnapshot
# The ElegooN3Thumbnail plugin is released under the terms of the AGPLv3 or higher.

from . import ElegooN3Thumbnail


def getMetaData():
    return {}


def register(app):
    return {"extension": ElegooN3Thumbnail.ElegooN3Thumbnail()}