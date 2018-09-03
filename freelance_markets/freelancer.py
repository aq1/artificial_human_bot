from freelancersdk.session import Session
from freelancersdk.resources.projects.projects import search_projects
from freelancersdk.resources.projects.helpers import create_search_projects_filter
from freelancersdk.resources.projects.exceptions import ProjectsNotFoundException

import settings
from utils.logging import logger
from utils import functions


def request_projects(query):
    session = Session(oauth_token=settings.FREELANCER_TOKEN)
    search_filter = create_search_projects_filter(
        sort_field='time_updated',
        or_search_query=True,
        from_time=functions.get_today_midnight(),
    )

    result = []
    offset = 0
    limit = 500
    try:

        while True:
            response = search_projects(
                session,
                query=query,
                active_only=True,
                limit=limit,
                offset=offset,
                search_filter=search_filter,
            )
            result += response['projects']
            offset += limit
            if offset > response['total_count']:
                break

    except ProjectsNotFoundException as e:
        logger.error('freelancer.get_projects {} {}'.format(e.error_code, e.args[0]))
        return []
    else:
        return result


def get_projects(query):
    result = request_projects(query)
    projects = []
    for each in result:
        project = {
            'query': query,
            'market': 'freelancer',
            'project_id': each['id'],
            'url': 'http://freelancer.com/projects/{}'.format(each['id']),
            'time_updated': functions.timestamp_to_iso_string(each['time_updated']),
            'time_submitted': functions.timestamp_to_iso_string(each['time_submitted']),
            'title': each['title'],
            'type': each['type'],
            'status': each['status'],
            'description': each['description'],
            'budget': {
                'min': (each['budget']['minimum'] or 0) * each['currency']['exchange_rate'],
                'max': (each['budget']['maximum'] or 0) * each['currency']['exchange_rate'],
            }
        }
        if project['type'] == 'hourly':
            project['hourly_info'] = each['hourly_project_info']
        projects.append(project)

    return projects
