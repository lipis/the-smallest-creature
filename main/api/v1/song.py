# coding: utf-8

from google.appengine.ext import ndb
from flask.ext import restful
import flask

from api import helpers
import auth
import model
import util

from main import api_v1


###############################################################################
# Admin
###############################################################################
@api_v1.resource('/admin/song/', endpoint='api.admin.song.list')
class AdminSongListAPI(restful.Resource):
  @auth.admin_required
  def get(self):
    song_keys = util.param('song_keys', list)
    if song_keys:
      song_db_keys = [ndb.Key(urlsafe=k) for k in song_keys]
      song_dbs = ndb.get_multi(song_db_keys)
      return helpers.make_response(song_dbs, model.song.FIELDS)

    song_dbs, song_cursor = model.Song.get_dbs()
    return helpers.make_response(song_dbs, model.Song.FIELDS, song_cursor)


@api_v1.resource('/admin/song/<string:song_key>/', endpoint='api.admin.song')
class AdminSongAPI(restful.Resource):
  @auth.admin_required
  def get(self, song_key):
    song_db = ndb.Key(urlsafe=song_key).get()
    if not song_db:
      helpers.make_not_found_exception('song %s not found' % song_key)
    return helpers.make_response(song_db, model.Song.FIELDS)
