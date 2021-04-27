from flask import render_template, redirect

from app import db
from app import app
from app.forms import MessageForm
from app.models import User, Messages

db.create_all()

# add route '/' and also add the two methods to handle request: 'GET' and 'POST'
@app.route('/', methods = ['GET', 'POST'])

def home():
	form=MessageForm()
	if form.validate_on_submit():
        # check if user exits in database
		author = User.query.filter_by(author = form.author.data).first()
		if author is None:
			db.session.add(User(author = form.author.data))
			db.session.commit()
			m = Messages(message = form.message.data, user_id = User.query.filter_by(author = form.author.data).first().id)
			db.session.add(m)
			db.session.commit()
		
		else:
			m = Messages(message = form.message.data, user_id = User.query.filter_by(author = form.author.data).first().id)
			db.session.add(m)
			db.session.commit()
        # if not create user and add to database
        # create row in Message table with user (created/found) add to ta database

	posts = []
    # output all messages
	messages = Messages.query.all()
    # create a list of dictionaries with the following structure
    # [{'author':'carlos', 'message':'Yo! Where you at?!'},
    #  {'author':'Jerry', 'message':'Home. You?'}]
	for m in messages:
		author = {'author': m.author, 'message': m.message}
		posts.append(author)

	return render_template('home.html', posts=posts, form=form)

