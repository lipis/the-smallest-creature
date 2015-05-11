# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Member(model.Base):
  name = ndb.StringProperty(required=True)
  about = ndb.TextProperty(required=True, verbose_name='About (Markdown)')
  joined_date = ndb.DateProperty()

  FIELDS = {
      'name': fields.String,
      'about': fields.String,
      'joined_date': fields.DateTime,
    }

  FIELDS.update(model.Base.FIELDS)
