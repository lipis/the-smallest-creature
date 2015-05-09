# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Song(model.Base):
  name = ndb.StringProperty(required=True)
  url_name = ndb.StringProperty(required=True)
  index = ndb.IntegerProperty(default=0)
  year = ndb.IntegerProperty(default=0)
  sound_cloud_id = ndb.StringProperty(verbose_name='SoundCloud ID')
  youtube_id = ndb.StringProperty(verbose_name='YouTube ID')
  imgur_id = ndb.StringProperty(verbose_name='Imgur ID')
  tags = ndb.StringProperty(repeated=True)
  artist = ndb.StringProperty()
  lyrics = ndb.TextProperty(indexed=False)

  FIELDS = {
      'name': fields.String,
      'url_name': fields.String,
      'index': fields.Integer,
      'year': fields.Integer,
      'sound_cloud_id': fields.String,
      'youtube_id': fields.String,
      'imgur_id': fields.String,
      'tags': fields.List(fields.String),
      'artist': fields.String,
      'lyrics': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)