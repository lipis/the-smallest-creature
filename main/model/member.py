# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Member(model.Base):
  name = ndb.StringProperty(required=True)
  image_url = ndb.StringProperty(default='', verbose_name='Image URL')
  joined_date = ndb.DateProperty()
  about = ndb.TextProperty(required=True, verbose_name='About (Markdown)')

  FIELDS = {
      'name': fields.String,
      'image_url': fields.String,
      'joined_date': fields.DateTime,
      'about': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)
