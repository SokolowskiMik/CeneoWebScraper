from flask_wtf import FlaskForm
from wtforms import StringField, validators


class SubmitForm(FlaskForm):
    product_id = StringField('Wpisz id produktu', validators=[validators.DataRequired(), validators.length(4,14)])