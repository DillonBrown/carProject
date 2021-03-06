import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g

from forms import AddCarForm

app  = Flask(__name__)
app.config.from_object('_config')

def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))

@app.route('/', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] \
				or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please Try Again.'
			return render_template('login.html', error = error)
		else:
			session['logged_in'] = True
			flash('Welcome!')
			return redirect(url_for('cars'))
	return render_template('login.html')

@app.route('/cars/')
@login_required
def cars():
	g.db = connect_db()
	cur = g.db.execute(
		'select make, model, year, color, odometer, car_id from cars')# add ing stuff might mess up
	car_garage = [ dict(make=row[0], model=row[1], year=row[2], color=row[3], 
		odometer=row[4], car_id=row[5]) for row in cur.fetchall() ]
	g.db.close()
	return render_template(
		'cars.html',
		form=AddCarForm(request.form),
		car_garage=car_garage
	)

@app.route('/add/', methods=['POST'])
@login_required
def new_car():
	g.db = connect_db()
	make = request.form['make']
	model = request.form['model']
	year = request.form['year']
	color = request.form['color']
	if not make or not model or not year or not color:
		flash("All fields are required. Please try again.")
		return redirect(url_for('cars'))
	else:
		g.db.execute('insert into cars (make, model, year, color,\
		 odometer, maint_item) \
			values (?, ?, ?, ?, ?)',
			[	request.form['make'],
				request.form['model'],
				request.form['year'],
				request.form['color'],
				0, " "
			]
		)
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted. Thanks.')
		return redirect(url_for('cars'))

@app.route('/add/', methods=['POST'])
@login_required
def new_detail():
	g.db = connect_db()
	car_id=request.form['car_id']
	odometer=request.form['odometer']
	car_detail= request.form['car_detail']

	if not car_detail or not car_id or not odometer:
		flash("All fields are required. Please try again.")
		return redirect(url_for('details'))
	else:
		g.db.execute('update maint_items set odometer = ? where car_id = 1 (odometer) \
			values (?)',
			[	request.form['odometer'] ]
		)
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted. Thanks.')
		return redirect(url_for('details'))

@app.route('/delete/<int:car_id>/')
@login_required
def delete_entry(car_id):
	g.db = connect_db()
	g.db.execute('delete from cars where car_id='+str(car_id))
	g.db.commit()
	g.db.close()
	flash('The car was destroyed.')
	return redirect(url_for('cars'))

@app.route('/details/<int:car_id>/')
@login_required
def car_detail(car_id):
	g.db = connect_db()
	cur = g.db.execute(
		'select make, model, year, color, odometer, maint_item, car_id from cars')# add ing stuff might mess up
	maint_items = [ dict(make=row[0], model=row[1], year=row[2], color=row[3], 
		odometer=row[4],maint_item=row[5] , car_id=row[6]) for row in cur.fetchall() ]
	g.db.close()
	return render_template(
		'details.html',
		form=AddCarForm(request.form),
		maint_items=maint_items
		)
