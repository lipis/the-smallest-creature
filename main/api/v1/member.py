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
@api_v1.resource('/admin/member/', endpoint='api.admin.member.list')
class AdminMemberListAPI(restful.Resource):
  @auth.admin_required
  def get(self):
    member_keys = util.param('member_keys', list)
    if member_keys:
      member_db_keys = [ndb.Key(urlsafe=k) for k in member_keys]
      member_dbs = ndb.get_multi(member_db_keys)
      return helpers.make_response(member_dbs, model.member.FIELDS)

    member_dbs, member_cursor = model.Member.get_dbs()
    return helpers.make_response(member_dbs, model.Member.FIELDS, member_cursor)


@api_v1.resource('/admin/member/<string:member_key>/', endpoint='api.admin.member')
class AdminMemberAPI(restful.Resource):
  @auth.admin_required
  def get(self, member_key):
    member_db = ndb.Key(urlsafe=member_key).get()
    if not member_db:
      helpers.make_not_found_exception('member %s not found' % member_key)
    return helpers.make_response(member_db, model.Member.FIELDS)