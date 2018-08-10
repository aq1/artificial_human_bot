from freelance_markets import (
    freelancer,
)

from utils import mongo
from utils.logging import logger


def find_projects(query):
    projects = freelancer.get_projects(query)
    if projects:
        mongo.save_projects(projects)
        mongo.save_last_project_time(query, 'freelancer', projects[0]['time_updated'])
        logger.info('freelancer "{}" saved {} projects'.format(query, len(projects)))
