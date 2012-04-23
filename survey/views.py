from os import urandom
from datetime import datetime

from pyramid.response import Response
from pyramid.httpexceptions import (HTTPNotFound, HTTPFound)
from pyramid.view import view_config

from pyramid_mailer.message import Message

from sqlalchemy.exc import DBAPIError

from wtforms import (
    Form,
    validators,
    )

from wtforms.fields import RadioField

from .models import (
    DBSession,
    Group,
    User,
    Survey,
    Question,
    Choice,
    Result,
    Answer,
    )

@view_config (route_name = 'survey', renderer = 'survey:templates/survey.mako')
def survey (request):
    class SurveyForm (Form):
        pass

    def build_survey_form (survey, post_data):
        form = SurveyForm

        for q in survey.questions:
            setattr (form, 'question_' + str (q.id), RadioField (q.text, [validators.Required ()], choices = [(c.id, c.text) for c in q.choices], coerce = int) )

        return form (post_data)

    messages = []
    survey = None
    survey_form = None

    mysql = DBSession ()

    # the id actually points to a specific user's survey result
    # if no result is found, either the survey does not exist, or the user was not selected to take the survey
    result = mysql.query (Result).filter (Result.token == request.matchdict['token']).first ()

    # make sure the result exists, and the result is unsubmitted for the user
    if result and not result.submit_datetime:
        survey = result.survey

        if survey.open_datetime and datetime.now () >= survey.open_datetime:
            if not survey.close_datetime or datetime.now () <= survey.close_datetime:
                # generate a form class and pass it the POST data for validation
                survey_form = build_survey_form (survey, request.POST)

                # if the survey was submitted then we need to process it
                if 'submit' in request.POST:
                    if survey_form.validate ():
                        # save all the answers
                        for k, v in request.POST.iteritems ():
                            if k.startswith ('question_'):
                                mysql.add (Answer (v, k.replace ('question_', ''), result.id) )

                        survey = None
                        result.submit_datetime = datetime.now ()
                        messages.append ({'type': 'success', 'message': 'Your response was submitted successfully. Thank you.'})
            else:
                survey = None
                messages.append({'type': 'error', 'message': 'The survey is already closed'})
        else:
            survey = None
            messages.append({'type': 'error', 'message': 'The survey is not open yet'})
    else:
        messages.append ({'type': 'error', 'message': 'The survey you requested does not exist'})

    return {'messages': messages, 'survey': survey, 'survey_form': survey_form}

@view_config (route_name = 'list_surveys', renderer = 'survey:templates/survey_list.mako')
def list_surveys (request):
    mysql = DBSession ()

    surveys = mysql.query (Survey).order_by (Survey.created_datetime).all ()

    return {'surveys': surveys}

@view_config (route_name = 'open_survey')
def open_survey (request):
    mysql = DBSession ()

    survey = mysql.query (Survey).filter (Survey.id == request.matchdict['survey_id']).first ()

    # make sure the survey wasn't already opened
    if survey and not survey.open_datetime:
        survey.open_datetime = datetime.now ()
        
        # get all users in the same groups as the survey
        users = mysql.query (User).join (User.groups).join (Group.surveys).filter (Survey.id == request.matchdict['survey_id']).distinct ()

        # generate a result for each user, along with a token
        for u in users:
            newtoken = urandom (5).encode ('hex')
            while mysql.query (Result).filter (Result.token == newtoken).count () > 0:
                newtoken = urandom (5).encode ('hex')

            r = Result (newtoken, None, survey.id, u.id)
            mysql.add (r)

    return HTTPFound (location = request.referer)

@view_config (route_name = 'close_survey')
def close_survey (request):
    mysql = DBSession ()

    survey = mysql.query (Survey).filter (Survey.id == request.matchdict['survey_id']).first ()

    # make sure the survey wasn't already close
    if survey and not survey.close_datetime:
        survey.close_datetime = datetime.now ()

    return HTTPFound (location = request.referer)

@view_config (route_name = 'delete_survey')
def delete_survey (request):
    mysql = DBSession ()

    survey = mysql.query (Survey).filter (Survey.id == request.matchdict['survey_id']).first ()

    if survey:
        mysql.delete (survey)

    return HTTPFound (location = request.referer)

@view_config (route_name = 'list_results', renderer = 'survey:templates/result_list.mako')
def list_results (request):
    mysql = DBSession ()

    survey = mysql.query (Survey).filter (Survey.id == request.matchdict['survey_id']).first ()

    if survey:
        return {'results': survey.results}
    else:
        return {'results': None}

@view_config (route_name = 'delete_result')
def delete_result (request):
    mysql = DBSession ()

    result = mysql.query (Result).filter (Result.id == request.matchdict['result_id']).first ()

    if result:
       mysql.query (Answer).filter (Answer.result_id == result.id).delete ()
       result.submit_datetime = None

    return HTTPFound (location = request.referer)

@view_config (route_name = 'export_users')
def export_users (request):
    mysql = DBSession ()

    survey = mysql.query (Survey).filter (Survey.id == request.matchdict['survey_id']).first ()

    if survey:
        users = mysql.query (User.first_name.label ('first_name'),
                             User.last_name.label ('last_name'),
                             User.email.label ('email'),
                             Result.token.label ('token') ) \
                     .select_from (Result) \
                     .join (User, Result.user_id == User.id) \
                     .filter (Result.survey_id == request.matchdict['survey_id']) \
                     .all ()

        csv = ''
        csv = csv + '\r\n'.join ( ('%s,%s,%s,%s' % (u.first_name, u.last_name, u.email, request.application_url + '/survey/' + u.token) ) for u in users)

        title = survey.title.encode ('ascii', 'ignore').replace (' ', '_')
        title = title + '_users'
        r = Response (csv)
        r.headers['Content-Type'] = 'text/csv'
        r.headers['Content-Disposition'] = 'attachment;filename=%s.csv' % title

        return r

    return HTTPNotFound ()

@view_config (route_name = 'export_results')
def export_results (request):
    mysql = DBSession ()

    survey = mysql.query (Survey).filter (Survey.id == request.matchdict['survey_id']).first ()

    if survey:
        csv = ',,,'
        csv = csv + ','.join (q.text.replace (',', '') for q in survey.questions)
        csv = csv + '\r\n'
        csv = csv + '\r\n'.join ( ('%s,%s,%s,%s' % (r.user.first_name, r.user.last_name, r.user.email, ','.join (a.choice.text.replace (',', '') for a in r.answers) ) ) for r in survey.results)

        title = survey.title.encode ('ascii', 'ignore').replace (' ', '_')
        title = title + '_results'
        r = Response (csv)
        r.headers['Content-Type'] = 'text/csv'
        r.headers['Content-Disposition'] = 'attachment;filename=%s.csv' % title

        return r

    return HTTPNotFound ()
