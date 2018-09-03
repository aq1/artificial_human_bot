from freelance_markets import (
    freelancer,
)

import mongo
from utils.logging import logger


def find_projects():
    queries = mongo.users.get_queries()
    total_inserted, total_updated = 0, 0

    for query in queries:
        projects = freelancer.get_projects(query)
        if projects:
            inserted, updated = mongo.projects.save_projects(projects)
            total_inserted += inserted
            total_updated += updated

            mongo.projects.save_last_project_time(query, 'freelancer', projects[0]['time_updated'])
            logger.info('freelancer "{}" new: {}, updated: {}'.format(query, inserted, updated))

    return total_inserted, total_updated
