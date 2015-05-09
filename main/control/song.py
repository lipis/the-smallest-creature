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
# Admin List
###############################################################################
@app.route('/admin/song/')
@auth.admin_required
def admin_song_list():
  song_dbs, song_cursor = model.Song.get_dbs(
      order=util.param('order') or '-modified',
    )
  return flask.render_template(
      'song/admin_song_list.html',
      html_class='admin-song-list',
      title='Song List',
      song_dbs=song_dbs,
      next_url=util.generate_next_url(song_cursor),
      api_url=flask.url_for('api.admin.song.list'),
    )


###############################################################################
# Admin Update
###############################################################################
class SongUpdateAdminForm(wtf.Form):
  name = wtforms.StringField(
      model.Song.name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  url_name = wtforms.StringField(
      model.Song.url_name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  index = wtforms.IntegerField(
      model.Song.index._verbose_name,
      [wtforms.validators.optional()],
    )
  year = wtforms.IntegerField(
      model.Song.year._verbose_name,
      [wtforms.validators.optional()],
    )
  sound_cloud_id = wtforms.StringField(
      model.Song.sound_cloud_id._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  youtube_id = wtforms.StringField(
      model.Song.youtube_id._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  imgur_id = wtforms.StringField(
      model.Song.imgur_id._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  tags = wtforms.StringField(
      model.Song.tags._verbose_name,
      [wtforms.validators.optional()],
    )
  artist = wtforms.StringField(
      model.Song.artist._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  lyrics = wtforms.TextAreaField(
      model.Song.lyrics._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )


@app.route('/admin/song/create/', methods=['GET', 'POST'])
@app.route('/admin/song/<int:song_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_song_update(song_id=0):
  if song_id:
    song_db = model.Song.get_by_id(song_id)
  else:
    song_db = model.Song()
  if not song_db:
    flask.abort(404)

  form = SongUpdateAdminForm(obj=song_db)

  if flask.request.method == 'GET' and not form.errors:
    form.tags.data = ' '.join(form.tags.data)
  
  if form.validate_on_submit():
    form.tags.data = util.parse_tags(form.tags.data)
    form.populate_obj(song_db)
    song_db.put()
    return flask.redirect(flask.url_for('admin_song_list', song_id=song_db.key.id()))

  return flask.render_template(
      'song/admin_song_update.html',
      title=song_db.name if song_id else 'New Song',
      html_class='admin-song-update',
      form=form,
      song_db=song_db,
      back_url_for='admin_song_list',
      api_url=flask.url_for('api.admin.song', song_key=song_db.key.urlsafe() if song_db.key else ''),
    )