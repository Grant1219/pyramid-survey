from sqlalchemy import (
    Table,
    Column,
    Integer,
    Unicode,
    DateTime,
    ForeignKey,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session (sessionmaker (extension = ZopeTransactionExtension () ) )
Base = declarative_base ()

user_group_association = Table ('user_group_association', Base.metadata,
    Column ('user_id', Integer, ForeignKey ('user.id', ondelete = 'cascade') ),
    Column ('group_id', Integer, ForeignKey ('group.id', ondelete = 'cascade') ),
    mysql_engine = 'InnoDB'
)

survey_group_association = Table ('survey_group_association', Base.metadata,
    Column ('survey_id', Integer, ForeignKey ('survey.id', ondelete = 'cascade') ),
    Column ('group_id', Integer, ForeignKey ('group.id', ondelete = 'cascade') ),
    mysql_engine = 'InnoDB'
)

class InnoDB (object):
    __table_args__ = {'mysql_engine': 'InnoDB'}

class User (Base, InnoDB):
    __tablename__ = 'user'

    id = Column (Integer, primary_key = True)
    first_name = Column (Unicode (30) )
    last_name = Column (Unicode (30) )
    email = Column (Unicode (50) )

    groups = relationship ('Group', backref = 'users', secondary = user_group_association)
    results = relationship ('Result', backref = 'user', passive_deletes = True)

    def __init__ (self, first_name, last_name, email):
        self.first_name = first_nam
        self.last_name = last_name
        self.email = email

class Group (Base, InnoDB):
    __tablename__ = 'group'

    id = Column (Integer, primary_key = True)
    name = Column (Unicode (30) )

    def __init__ (self, name):
        self.name = name

class Survey (Base, InnoDB):
    __tablename__ = 'survey'

    id = Column (Integer, primary_key = True)
    title = Column (Unicode (50) )
    created_datetime = Column (DateTime)
    open_datetime = Column (DateTime)
    close_datetime = Column (DateTime)

    groups = relationship ('Group', backref = 'surveys', secondary = survey_group_association)
    questions = relationship ('Question', backref = 'survey', passive_deletes = True)
    results = relationship ('Result', backref = 'survey', passive_deletes = True)

    def __init__ (self, title, created_datetime, open_datetime, close_datetime):
        self.title = title
        self.created_datetime = created_datetime
        self.open_datetime = open_datetime
        self.close_datetime = close_datetime

class Question (Base, InnoDB):
    __tablename__ = 'question'

    id = Column (Integer, primary_key = True)
    text = Column (Unicode (512) )

    question_type = Column (Unicode (10) )
    __mapper_args__ = {'polymorphic_on': question_type}

    survey_id = Column (Integer, ForeignKey ('survey.id', ondelete = 'cascade') )

    def __init__ (self, text, survey_id):
        self.text = text
        self.survey_id = survey_id

class TextQuestion (Question):
    __tablename__ = 'text_question'
    __mapper_args__ = {'polymorphic_identity': 'text'}

    id = Column (Integer, ForeignKey ('question.id', ondelete = 'cascade'), primary_key = True)
    character_limit = Column (Integer)

    def __init__ (self, text, character_limit, survey_id):
        super (TextQuestion, self).__init__ (text, survey_id)
        self.character_limit = character_limit

class ChoiceQuestion (Question):
    __tablename__ = 'choice_question'
    __mapper_args__ = {'polymorphic_identity': 'choice'}

    id = Column (Integer, ForeignKey ('question.id', ondelete = 'cascade'), primary_key = True)
    choices = relationship ('Choice', backref = 'question', passive_deletes = True)

    def __init__ (self, text, survey_id):
        super (ChoiceQuestion, self).__init__ (text, survey_id)

class Choice (Base, InnoDB):
    __tablename__ = 'choice'

    id = Column (Integer, primary_key = True)
    text = Column (Unicode (128) )

    question_id = Column (Integer, ForeignKey ('choice_question.id', ondelete = 'cascade') )

    def __init__ (self, text, question_id):
        self.text = text
        self.question_id = question_id

class Result (Base, InnoDB):
    __tablename__ = 'result'

    id = Column (Integer, primary_key = True)
    token = Column (Unicode (10), unique = True)
    submit_datetime = Column (DateTime)

    survey_id = Column (Integer, ForeignKey ('survey.id', ondelete = 'cascade') )
    user_id = Column (Integer, ForeignKey ('user.id', ondelete = 'cascade') )

    answers = relationship ('Answer', backref = 'result', passive_deletes = True)

    def __init__ (self, token, submit_datetime, survey_id, user_id):
        self.token = token
        self.submit_datetime = submit_datetime
        self.survey_id = survey_id
        self.user_id = user_id

class Answer (Base, InnoDB):
    __tablename__ = 'answer'

    id = Column (Integer, primary_key = True)

    question_id = Column (Integer, ForeignKey ('question.id', ondelete = 'cascade') )
    result_id = Column (Integer, ForeignKey ('result.id', ondelete = 'cascade') )

    answer_type = Column (Unicode (10) )
    __mapper_args__ = {'polymorphic_on': answer_type}

    def __init__ (self, question_id, result_id):
        self.question_id = question_id
        self.result_id = result_id

class TextAnswer (Answer):
    __tablename__ = 'text_answer'
    __mapper_args__ = {'polymorphic_identity': 'text'}

    id = Column (Integer, ForeignKey ('answer.id', ondelete = 'cascade'), primary_key = True)
    response = Column (Text)

    def __init__ (self, response, question_id, result_id):
        super (TextAnswer, self).__init__ (question_id, result_id)
        self.response = response

class ChoiceAnswer (Answer):
    __tablename__ = 'choice_answer'
    __mapper_args__ = {'polymorphic_identity': 'choice'}

    id = Column (Integer, ForeignKey ('answer.id', ondelete = 'cascade'), primary_key = True)
    choice_id = Column (Integer, ForeignKey ('choice.id', ondelete = 'cascade') )

    choice = relationship ('Choice')

    def __init__ (self, choice_id, question_id, result_id):
        super (ChoiceAnswer, self).__init__ (question_id, result_id)
        self.choice_id = choice_id

def populate ():
    pass

def initialize_sql (engine):
    DBSession.configure (bind = engine)
    Base.metadata.bind = engine
    Base.metadata.create_all (engine)
    populate ()
