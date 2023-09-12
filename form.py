from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo


class AnalysisForm(FlaskForm):
    doc = FileField('Change Profile picture', validators=[FileAllowed(['pdf'])])
    option1 = SelectField(
        'ALLOW ACTIVATING OF CO-REFERENCING MODULE',
        validators=[DataRequired()],
        choices=[
            ('', 'Allow Activating of Co-referencing Module'),
            ('True', 'True'),
            ('False', 'False')
        ])
    option2 = SelectField(
        'ENABLE REMOVAL OF DUPLICATE NODES-EDGE',
        validators=[DataRequired()],
        choices=[
            ('', 'Enable removal of Duplicate Nodes-Edge'),
            ('True', 'True'),
            ('False', 'False')
        ])
    option3 = SelectField(
        'REPLACE ELIPSIS SUBJECT WITH SURROUNDING SUBJECT',
        validators=[DataRequired()],
        choices=[
            ('', 'Replace Elipsis subject with surrounding subject'),
            ('True', 'True'),
            ('False', 'False')
        ])

    submit = SubmitField('Analyze')
