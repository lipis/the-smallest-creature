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
@app.route('/song/')
def song_list():
  song_dbs, song_cursor = model.Song.get_dbs(order='rank')
  return flask.render_template(
      'song/song_list.html',
      html_class='song-list',
      title='Songs & Lyrics',
      song_dbs=song_dbs,
      next_url=util.generate_next_url(song_cursor),
    )


###############################################################################
# View
###############################################################################
@app.route('/song/<int:song_id>/')
def song_view(song_id):
  song_db = model.Song.get_by_id(song_id)
  if not song_db:
    flask.abort(404)

  return flask.render_template(
      'song/song_view.html',
      html_class='song-view',
      title=song_db.name,
      song_db=song_db,
    )


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
  rank = wtforms.IntegerField(
      model.Song.rank._verbose_name,
      [wtforms.validators.optional()],
    )
  name = wtforms.StringField(
      model.Song.name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  album_key = wtforms.SelectField(
      model.Song.album_key._verbose_name,
      [wtforms.validators.optional()],
      choices=[],
    )
  writer_key = wtforms.SelectField(
      model.Song.writer_key._verbose_name,
      [wtforms.validators.optional()],
      choices=[],
    )
  release_date = wtforms.DateField(
      model.Song.release_date._verbose_name,
      [wtforms.validators.optional()],
    )
  soundcloud_id = wtforms.StringField(
      model.Song.soundcloud_id._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  youtube_id = wtforms.StringField(
      model.Song.youtube_id._verbose_name,
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

  album_dbs, album_cursor = model.Album.get_dbs()
  member_dbs, member_cursor = model.Member.get_dbs()
  form.album_key.choices = [('', u'-')] + [(c.key.urlsafe(), c.name) for c in album_dbs]
  form.writer_key.choices = [('', u'-')] + [(c.key.urlsafe(), c.name) for c in member_dbs]
  if flask.request.method == 'GET' and not form.errors:
    form.album_key.data = song_db.album_key.urlsafe() if song_db.album_key else None
    form.writer_key.data = song_db.writer_key.urlsafe() if song_db.writer_key else None
    form.tags.data = config.TAG_SEPARATOR.join(form.tags.data)

  if form.validate_on_submit():
    form.album_key.data = ndb.Key(urlsafe=form.album_key.data) if form.album_key.data else None
    form.writer_key.data = ndb.Key(urlsafe=form.writer_key.data) if form.writer_key.data else None
    form.tags.data = util.parse_tags(form.tags.data)
    form.populate_obj(song_db)
    song_db.put()
    return flask.redirect(flask.url_for('admin_song_list', order='-modified'))

  return flask.render_template(
      'song/admin_song_update.html',
      title=song_db.name if song_id else 'New Song',
      html_class='admin-song-update',
      form=form,
      song_db=song_db,
      back_url_for='admin_song_list',
      api_url=flask.url_for('api.admin.song', song_key=song_db.key.urlsafe() if song_db.key else ''),
    )
