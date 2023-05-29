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

class StaffForm(FlaskForm):
    Staff_ID = StringField('Staff ID', validators=[InputRequired()])
    First_Name = StringField('First Name', validators=[InputRequired()])
    Last_Name = StringField('Last Name', validators=[InputRequired()])
    Address = StringField('Address', validators=[InputRequired()])
    Postcode = StringField('Postcode', validators=[InputRequired()])
    Phone_Number = StringField('Phone Number', validators=[InputRequired()])
    DTH_Skill = SelectField('DTH Trained', choices=[('Yes', 'Yes'), ('No', 'No')])
    BB_Skill = SelectField('BB Trained', choices=[('Yes', 'Yes'), ('No', 'No')])
    SE_Skill = SelectField('SE Trained', choices=[('Yes', 'Yes'), ('No', 'No')])
    MDU_Skill = SelectField('MDU Trained', choices=[('Yes', 'Yes'), ('No', 'No')])
    FTTP_Skilll = SelectField('FTTP Trained', choices=[('Yes', 'Yes'), ('No', 'No')])
    Admin = SelectField('Set to Admin access?', choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField('Add staff')
