from freelance_markets import (
    freelancer,
)

import mongo
from utils.logging import logger


def find_projects():
    queries = mongo.get_queries()
    for query in queries:
        projects = freelancer.get_projects(query)
        if projects:
            saved_count = mongo.save_projects(projects)
            mongo.save_last_project_time(query, 'freelancer', projects[0]['time_updated'])
            logger.info('freelancer "{}" saved {} projects'.format(query, saved_count))
