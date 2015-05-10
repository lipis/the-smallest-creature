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
@api_v1.resource('/admin/album/', endpoint='api.admin.album.list')
class AdminAlbumListAPI(restful.Resource):
  @auth.admin_required
  def get(self):
    album_keys = util.param('album_keys', list)
    if album_keys:
      album_db_keys = [ndb.Key(urlsafe=k) for k in album_keys]
      album_dbs = ndb.get_multi(album_db_keys)
      return helpers.make_response(album_dbs, model.album.FIELDS)

    album_dbs, album_cursor = model.Album.get_dbs()
    return helpers.make_response(album_dbs, model.Album.FIELDS, album_cursor)


@api_v1.resource('/admin/album/<string:album_key>/', endpoint='api.admin.album')
class AdminAlbumAPI(restful.Resource):
  @auth.admin_required
  def get(self, album_key):
    album_db = ndb.Key(urlsafe=album_key).get()
    if not album_db:
      helpers.make_not_found_exception('album %s not found' % album_key)
    return helpers.make_response(album_db, model.Album.FIELDS)