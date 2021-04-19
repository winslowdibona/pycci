import requests
from .config import Config
from .jobtype import JOBTYPE

class ProjectApi:
    def __init__(self, name):
        self.name = name
        self.slug = f'{Config.ORG_SLUG()}/{name}'

    def get_pipelines(self, page_token=None):
        url = f'{Config.BASE_URL}/project/{self.slug}/pipeline'
        url = url if not page_token else f'{url}?page-token={page_token}'
        result = requests.get(url, headers=Config.API_HEADER()).json()
        return result

class PipelineApi:
    def __init__(self, id):
        self.id = id

    def get_workflows(self, failed_only=False, page_token=None):
        url = f'{Config.BASE_URL}/pipeline/{self.id}/workflow'
        url = url if not page_token else f'{url}&page-token={page_token}'
        result = requests.get(url, headers=Config.API_HEADER()).json()
        if failed_only:
            result['items'] = [w for w in result['items'] if w['status'] == 'failed']
        return result

class WorkflowApi:
    def __init__(self, id):
        self.id = id

    def get_jobs(self, type=JOBTYPE.ALL, failed_only=False, page_token=None):
        url = f'{Config.BASE_URL}/workflow/{self.id}/job'
        url = url if not page_token else f'{url}&page-token={page_token}'
        result = requests.get(url, headers=Config.API_HEADER()).json()
        if type != JOBTYPE.ALL:
            result['items'] = [j for j in result['items'] if j['name'] == type]
        if failed_only:
            result['items'] = [j for j in result['items'] if j['status'] == 'failed']
        return result

class JobApi:
    def __init__(self, id, number, project_slug):
        self.id = id
        self.number = number
        self.project_slug = project_slug

    def get_tests(self, failed_only=False, page_token=None):
        url = f'{Config.BASE_URL}/project/{self.project_slug}/{self.number}/tests'
        result = requests.get(url, headers=Config.API_HEADER()).json()
        if failed_only:
            result['items'] = [t for t in result['items'] if t['result'] == 'failure']
        return result

    def get_artifacts(self):
        url = f'{Config.BASE_URL}/project/{self.project_slug}/{self.number}/artifacts'
        result = requests.get(url, headers=Config.API_HEADER()).json()
        return result
