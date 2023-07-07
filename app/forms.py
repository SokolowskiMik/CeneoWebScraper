import requests
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators


class SubmitForm(FlaskForm):
    #product_id = StringField('Wpisz id produktu', validators=[validators.DataRequired(), validators.length(4,14)])
    product_id = IntegerField('Wpisz id produktu', validators=[validators.DataRequired(), validators.NumberRange(1000,999999999)])

    @staticmethod
    def validate_url(url):
        test = requests.get(url)
        status_code = test.status_code
        return True if status_code == 200 else False