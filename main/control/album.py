# coding: utf-8

from flask.ext import wtf
from google.appengine.ext import ndb
import flask
import wtforms

import auth
import config
import model
import util

from main import app


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/album/')
@auth.admin_required
def admin_album_list():
  album_dbs, album_cursor = model.Album.get_dbs(
      order=util.param('order') or '-modified',
    )
  return flask.render_template(
      'album/admin_album_list.html',
      html_class='admin-album-list',
      title='Album List',
      album_dbs=album_dbs,
      next_url=util.generate_next_url(album_cursor),
      api_url=flask.url_for('api.admin.album.list'),
    )


###############################################################################
# Admin Update
###############################################################################
class AlbumUpdateAdminForm(wtf.Form):
  name = wtforms.StringField(
      model.Album.name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  description = wtforms.TextAreaField(
      model.Album.description._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  release_date = wtforms.DateField(
      model.Album.release_date._verbose_name,
      [wtforms.validators.required()],
    )
  tags = wtforms.StringField(
      model.Album.tags._verbose_name,
      [wtforms.validators.optional()],
    )


@app.route('/admin/album/create/', methods=['GET', 'POST'])
@app.route('/admin/album/<int:album_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_album_update(album_id=0):
  if album_id:
    album_db = model.Album.get_by_id(album_id)
  else:
    album_db = model.Album()
  if not album_db:
    flask.abort(404)

  form = AlbumUpdateAdminForm(obj=album_db)

  if flask.request.method == 'GET' and not form.errors:
    form.tags.data = config.TAG_SEPARATOR.join(form.tags.data)
  
  if form.validate_on_submit():
    form.tags.data = util.parse_tags(form.tags.data)
    form.populate_obj(album_db)
    album_db.put()
    return flask.redirect(flask.url_for('admin_album_list', order='-modified'))

  return flask.render_template(
      'album/admin_album_update.html',
      title=album_db.name if album_id else 'New Album',
      html_class='admin-album-update',
      form=form,
      album_db=album_db,
      back_url_for='admin_album_list',
      api_url=flask.url_for('api.admin.album', album_key=album_db.key.urlsafe() if album_db.key else ''),
    )
