from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class AddCarForm(Form):

	car_id = IntegerField()
	make = StringField('Car Make', validators=[DataRequired()])
	model = StringField('Car Model', validators=[DataRequired()])
	year = IntegerField('Car Year', validators=[DataRequired()]) # shady line
	color = StringField('Car Color', validators=[DataRequired()])
	