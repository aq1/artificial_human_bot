from freelance_markets import (
    freelancer,
)

import mongo
from utils.logging import logger


def find_projects():
    queries = mongo.users.get_queries()
    for query in queries:
        projects = freelancer.get_projects(query)
        if projects:
            saved_count = mongo.projects.save_projects(projects)
            mongo.projects.save_last_project_time(query, 'freelancer', projects[0]['time_updated'])
            logger.info('freelancer "{}" saved {} projects'.format(query, saved_count))
