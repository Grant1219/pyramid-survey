import sys
from datetime import datetime
from ConfigParser import ConfigParser
from sqlalchemy import engine_from_config
import transaction
from survey.models import (
    initialize_sql,
    DBSession,
    Group,
    Survey,
    TextQuestion,
    ChoiceQuestion,
    Choice,
    )

config = ConfigParser ()

try:
    config.read (sys.argv[1])
except IndexError:
    print ('Error: No config filename given')
    quit ()

sql_options = {}
if config.has_section ('app:main'):
    for opt in config.items ('app:main'):
        sql_options[opt[0] ] = opt[1]
else:
    print ('Error: Could not locate \'app:main\' section in config file')

engine = engine_from_config (sql_options)
initialize_sql (engine)

mysql = DBSession ()
mysql.expire_on_commit = False

print ('Survey generator: At any time enter nothing for an input to stop entering choices or questions')

# get all the text input first before actually saving it in the database
survey = {'title': '', 'questions': [], 'groups': []}
survey['title'] = raw_input ('Survey title: ')

survey_done = False

if len (survey['title']) > 0:
    groups = mysql.query (Group).all ()

    print ('What groups is this survey part of?')
    for g in groups:
        print ('[%s] %s' % (g.id, g.name) )

    group_ids = raw_input ('Enter the group IDs (comma separated): ')
    group_ids = map (int, group_ids.split (',') )

    if len (groups) > 0:
        for g in group_ids:
            group = mysql.query (Group).filter (Group.id == g).first ()

            if group:
                survey['groups'].append (group)
            else:
                print ('Error: Group with ID %s does not exist' % g)
                survey_done = True
    else:
        print ('Error: You must choose at least one group')
        survey_done = True

    question_num = 1

    while not survey_done:
        question_text = raw_input ('Question #%s: ' % question_num)

        if len (question_text) > 0:
            question_type = raw_input ('Question type (1 = choice, 2 = text): ')
            question_done = False

            if question_type == '1':
                choices = []
                choice_num = 1

                while not question_done:
                    choice_text = raw_input ('  Choice #%s: ' % choice_num)
                    if len (choice_text) > 0:
                        choices.append (choice_text)
                        choice_num = choice_num + 1
                    else:
                        question_done = True

                if len (choices) > 0:
                    survey['questions'].append ( {'type': 'choice', 'text': question_text, 'choices': choices} )
                    question_num = question_num + 1
                    print ('')
            elif question_type == '2':
                limit = 512
                while not question_done:
                    try:
                        limit = int (raw_input ('  Character limit: ') )
                        question_done = True
                    except:
                        print ('Enter an integer')

                survey['questions'].append ( {'type': 'text', 'text': question_text, 'character_limit': limit} )
                question_num = question_num + 1
                print ('')
        else:
            survey_done = True

if len (survey['questions']) > 0 and len (survey['groups']) > 0:
    # now the survey can be saved in the database
    survey_obj = Survey (survey['title'], datetime.now (), None, None)
    mysql.add (survey_obj)

    for g in survey['groups']:
        survey_obj.groups.append (group)

    mysql.flush ()

    for q in survey['questions']:
        if q['type'] == 'choice':
            question = ChoiceQuestion (q['text'], survey_obj.id)
            survey_obj.questions.append (question)
            mysql.flush ()

            for c in q['choices']:
                choice = Choice (c, question.id)
                question.choices.append (choice)
        elif q['type'] == 'text':
            question = TextQuestion (q['text'], q['character_limit'], survey_obj.id)
            survey_obj.questions.append (question)

    mysql.flush ()
    transaction.commit ()

    print ('The survey has been created and saved successfully')
