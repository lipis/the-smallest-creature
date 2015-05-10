# coding: utf-8

from flask.ext import wtf
from google.appengine.ext import ndb
import flask
import wtforms

import auth
import model
import util

from main import app


###############################################################################
# List
###############################################################################
@app.route('/bio/')
def member_list():
  member_dbs, member_cursor = model.Member.get_dbs(order='name')
  return flask.render_template(
      'member/member_list.html',
      html_class='member-list',
      title='Bio',
      member_dbs=member_dbs,
      next_url=util.generate_next_url(member_cursor),
    )


###############################################################################
# View
###############################################################################
@app.route('/member/<int:member_id>/')
def member_view(member_id):
  member_db = model.Member.get_by_id(member_id)
  if not member_db:
    flask.abort(404)

  return flask.render_template(
      'member/member_view.html',
      html_class='member-view',
      title=member_db.name,
      member_db=member_db,
    )


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/member/')
@auth.admin_required
def admin_member_list():
  member_dbs, member_cursor = model.Member.get_dbs(
      order=util.param('order') or '-modified',
    )
  return flask.render_template(
      'member/admin_member_list.html',
      html_class='admin-member-list',
      title='Member List',
      member_dbs=member_dbs,
      next_url=util.generate_next_url(member_cursor),
      api_url=flask.url_for('api.admin.member.list'),
    )


###############################################################################
# Admin Update
###############################################################################
class MemberUpdateAdminForm(wtf.Form):
  name = wtforms.StringField(
      model.Member.name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  about = wtforms.TextAreaField(
      model.Member.about._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  joined_date = wtforms.DateField(
      model.Member.joined_date._verbose_name,
      [wtforms.validators.optional()],
    )


@app.route('/admin/member/create/', methods=['GET', 'POST'])
@app.route('/admin/member/<int:member_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_member_update(member_id=0):
  if member_id:
    member_db = model.Member.get_by_id(member_id)
  else:
    member_db = model.Member()
  if not member_db:
    flask.abort(404)

  form = MemberUpdateAdminForm(obj=member_db)

  if form.validate_on_submit():
    form.populate_obj(member_db)
    member_db.put()
    return flask.redirect(flask.url_for('admin_member_list', member_id=member_db.key.id()))

  return flask.render_template(
      'member/admin_member_update.html',
      title=member_db.name if member_id else 'New Member',
      html_class='admin-member-update',
      form=form,
      member_db=member_db,
      back_url_for='admin_member_list',
      api_url=flask.url_for('api.admin.member', member_key=member_db.key.urlsafe() if member_db.key else ''),
    )
