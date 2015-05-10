# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class Song(model.Base):
  rank = ndb.IntegerProperty(default=0)
  name = ndb.StringProperty(required=True)
  album_key = ndb.KeyProperty(kind=model.Album, verbose_name='Album')
  writer_key = ndb.KeyProperty(kind=model.Member, verbose_name='Written By')
  release_date = ndb.DateProperty()
  sound_cloud_id = ndb.StringProperty(verbose_name='SoundCloud ID')
  youtube_id = ndb.StringProperty(verbose_name='YouTube ID')
  tags = ndb.StringProperty(repeated=True)
  artist = ndb.StringProperty()
  lyrics = ndb.TextProperty(indexed=False)

  FIELDS = {
      'rank': fields.Integer,
      'name': fields.String,
      'album_key': fields.Key,
      'writer_key': fields.Key,
      'release_date': fields.DateTime,
      'sound_cloud_id': fields.String,
      'youtube_id': fields.String,
      'tags': fields.List(fields.String),
      'artist': fields.String,
      'lyrics': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)