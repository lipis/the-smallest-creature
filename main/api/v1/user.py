# coding: utf-8

from __future__ import absolute_import

import logging

from flask.ext import restful
from google.appengine.ext import blobstore
from google.appengine.ext import deferred
from google.appengine.ext import ndb
import flask

from api import helpers
import auth
import model
import util

from main import api_v1


@api_v1.resource('/user/', endpoint='api.user.list')
class UserListAPI(restful.Resource):
  @auth.admin_required
  def get(self):
    user_keys = util.param('user_keys', list)
    if user_keys:
      user_db_keys = [ndb.Key(urlsafe=k) for k in user_keys]
      user_dbs = ndb.get_multi(user_db_keys)
      return helpers.make_response(user_dbs, model.User.FIELDS)

    user_dbs, user_cursor = model.User.get_dbs()
    return helpers.make_response(user_dbs, model.User.FIELDS, user_cursor)

  @auth.admin_required
  def delete(self):
    user_keys = util.param('user_keys', list)
    if not user_keys:
      helpers.make_not_found_exception('User(s) %s not found' % user_keys)
    user_db_keys = [ndb.Key(urlsafe=k) for k in user_keys]
    delete_user_dbs(user_db_keys)
    return flask.jsonify({
        'result': user_keys,
        'status': 'success',
      })


@api_v1.resource('/user/<string:user_key>/', endpoint='api.user')
class UserAPI(restful.Resource):
  @auth.admin_required
  def get(self, user_key):
    user_db = ndb.Key(urlsafe=user_key).get()
    if not user_db:
      helpers.make_not_found_exception('User %s not found' % user_key)
    return helpers.make_response(user_db, model.User.FIELDS)

  @auth.admin_required
  def delete(self, user_key):
    user_db = ndb.Key(urlsafe=user_key).get()
    if not user_db:
      helpers.make_not_found_exception('User %s not found' % user_key)
    delete_user_task(user_db.key)
    return helpers.make_response(user_db, model.User.FIELDS)


###############################################################################
# Helpers
###############################################################################
@ndb.transactional(xg=True)
def delete_user_dbs(user_db_keys):
  for user_key in user_db_keys:
    delete_user_task(user_key)


def delete_user_task(user_key, next_cursor=None):
  resource_dbs, next_cursor = util.get_dbs(
      model.Resource.query(),
      user_key=user_key,
      cursor=next_cursor,
    )
  if resource_dbs:
    for resource_db in resource_dbs:
      try:
        blobstore.BlobInfo.get(resource_db.blob_key).delete()
      except AttributeError:
        logging.error('Blob %s not found during delete (resource_key: %s)' % (
            resource_db.blob_key, resource_db.key().urlsafe(),
          ))

    ndb.delete_multi([resource_db.key for resource_db in resource_dbs])

  if next_cursor:
    deferred.defer(delete_user_task, user_key, next_cursor)
  else:
    user_key.delete()
