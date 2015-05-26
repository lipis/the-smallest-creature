# coding: utf-8

import flask

import config
import model

from main import app


###############################################################################
# Welcome
###############################################################################
@app.route('/')
def welcome():
  member_dbs, member_cursor = model.Member.get_dbs(order='name')
  song_dbs, song_cursor = model.Song.get_dbs(order='rank')

  return flask.render_template(
      'welcome.html',
      html_class='welcome',
      member_dbs=member_dbs,
      song_dbs=song_dbs,
    )


###############################################################################
# Sitemap stuff
###############################################################################
@app.route('/sitemap.xml')
def sitemap():
  response = flask.make_response(flask.render_template(
      'sitemap.xml',
      lastmod=config.CURRENT_VERSION_DATE.strftime('%Y-%m-%d'),
    ))
  response.headers['Content-Type'] = 'application/xml'
  return response


###############################################################################
# Warmup request
###############################################################################
@app.route('/_ah/warmup')
def warmup():
  # TODO: put your warmup code here
  return 'success'
