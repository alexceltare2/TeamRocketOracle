from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired

class BasicForm(FlaskForm):
    Customer_Last_Name = StringField('Customer Last Name', validators=[InputRequired()])
    Address = StringField('Address', validators=[InputRequired()])
    Postcode = StringField('Postcode', validators=[InputRequired()])
    Phone_Number = StringField('Phone Number', validators=[InputRequired()])
    Visit_Type = SelectField('Visit Type', choices=[('DTH', 'DTH'), ('BB', 'BB'), ('SE', 'SE'), ('MDU', 'MDU'), ('FTTP', 'FTTP')], validators=[InputRequired()])
    Staff_ID = StringField('Staff ID')
    submit = SubmitField('Add job')
