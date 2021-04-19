import math
from .jobtype import JOBTYPE
from .api import ProjectApi, PipelineApi, WorkflowApi, JobApi


class _BaseModel(object):
    def execute(self, apicall, params, limit=math.inf):
        result = apicall(**params)
        items = result['items']
        params['page_token'] = result['next_page_token']
        while params['page_token'] is not None and len(items) < limit:
            result = apicall(**params)
            items.extend(result['items'])
            params['page_token'] = result['next_page_token']
        return items


class _CCIObject(_BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.data = data


class Project(_BaseModel):
    def __init__(self, name):
        self.name = name
        self.pipelines = []
        self.api = ProjectApi(name)

    def get_pipelines(self, num=20):
        pipelines = self.execute(self.api.get_pipelines, {}, limit=num)
        self.pipelines = [Pipeline(p) for p in pipelines]
        return self.pipelines


class Pipeline(_CCIObject):
    def __init__(self, data):
        self.workflows = []
        self.api = PipelineApi(data['id'])
        super().__init__(data)

    def get_workflows(self, failed_only=False):
        workflows = self.execute(self.api.get_workflows, {'failed_only': failed_only})
        self.workflows = [Workflow(w) for w in workflows]
        return self.workflows


class Workflow(_CCIObject):
    def __init__(self, data):
        self.jobs = []
        self.api = WorkflowApi(data['id'])
        super().__init__(data)

    def get_jobs(self, type=JOBTYPE.ALL, failed_only=False):
        jobs = self.execute(self.api.get_jobs, {'type': type, 'failed_only': failed_only})
        self.jobs = [Job(j) for j in jobs]
        return self.jobs


class Job(_CCIObject):
    def __init__(self, data):
        self.tests = []
        self.api = JobApi(data['id'], data['job_number'], data['project_slug'])
        super().__init__(data)

    def get_tests(self, failed_only=False):
        tests = self.execute(self.api.get_tests, {'failed_only': failed_only})
        self.tests = [Test(t) for t in tests]
        return self.tests


class Test(object):
    def __init__(self, data):
        self.data = data
        self.result = data['result']
        self.message = data['message']
        self.file = data['file']
        self.name = data['name']
        self.classname = data['classname']

    def __str__(self):
        return f'{self.name} - {self.result} - {self.message}'
