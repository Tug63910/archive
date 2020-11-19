from flask import (
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp=Blueprint('application',__name__)

@bp.route('/')
def index():
    db=get_db()
    db.execute(
        'SELECT w.id,url,created'
        ' FROM websites w'
        ' ORDER BY created ASC'
    )
    posts=db.fetchall()
    return render_template('application/index.html',posts=posts)

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method=='POST':
        url=request.form['title']
        error=None

        if not url:
            error='URL required.'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                'INSERT INTO websites (url,directory)'
                ' VALUES (%s,%s);',
                (url,url)
            )
            return redirect(url_for('application.index'))

    return render_template('application/create.html')

def get_post(post_id):
    db=get_db()
    db.execute(
        'SELECT p.id,url,directory'
        ' FROM websites p'
        ' WHERE p.id=%s;',
        (post_id,)
    )
    post=db.fetchone()

    if post is None:
        abort(404, "URL id {0} doesn't exist.".format(post_id))

    return post

@bp.route('/<int:post_id>/update',methods=('GET','POST'))
@login_required
def update(post_id):
    post=get_post(post_id)

    if request.method=='POST':
        url=request.form['title']
        error=None

        if not url:
            error="URL is required."

        if error is not None:   
            flash(error)
        else:
            db=get_db()
            db.execute(
                'UPDATE websites SET url=%s,directory=%s'
                ' WHERE id=%s;',
                (url,url,post_id)
            )
            return redirect(url_for('application.index'))

    return render_template('application/update.html',post=post)

@bp.route('/<int:post_id>/delete',methods=('POST',))
@login_required
def delete(post_id):
    get_post(post_id)
    db=get_db()
    db.execute('DELETE FROM websites WHERE id=%s;',(post_id,))
    return redirect(url_for('application.index'))
