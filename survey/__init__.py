from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    initialize_sql
    )

def main(global_config, **settings):
    engine = engine_from_config (settings, 'sqlalchemy.')
    initialize_sql (engine)

    config = Configurator (settings = settings)

    config.add_static_view ('static', 'static', cache_max_age = 3600)

    config.add_route ('survey', '/survey/{token}')

    config.add_route ('list_surveys', '/admin/surveys/list')
    config.add_route ('open_survey', '/admin/survey/open/{survey_id}')
    config.add_route ('close_survey', '/admin/survey/close/{survey_id}')
    config.add_route ('delete_survey', '/admin/survey/delete/{survey_id}')

    config.add_route ('list_results', '/admin/results/list/{survey_id}')
    config.add_route ('delete_result', '/admin/result/delete/{result_id}')

    config.add_route ('export_users', '/admin/survey/export/users/{survey_id}')
    config.add_route ('export_results', '/admin/survey/export/results/{survey_id}')

    config.scan ()

    return config.make_wsgi_app ()

