# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Album(model.Base):
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty()
  release_date = ndb.DateProperty(required=True)

  FIELDS = {
      'name': fields.String,
      'description': fields.String,
      'release_date': fields.DateTime,
    }

  FIELDS.update(model.Base.FIELDS)