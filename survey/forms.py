from wtforms import Form, validators
from wtforms.fields import (
    RadioField,
    )

class SurveyForm (Form):
    pass

def build_survey_form (survey, post_data):
    form = SurveyForm

    for q in survey.questions:
        setattr (form, 'question_' + str (q.id), RadioField (q.text, [validators.Required ()], choices = [(c.id, c.text) for c in q.choices], coerce = int) )

    return form (post_data)
