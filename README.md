# pycci

Simple python client for the [CircleCI API](https://circleci.com/docs/api/v2/)

## Installation

```bash
pip install pycci
```

## Usage

Example usage can be found in the `examples` directory

### Configuration

Before using the api you'll need to generate a circleci api token, and initialize the package with the key and the name of your organization.

```python
from pycci import Config
Config.initialize('Your Org', 'Your Key')
```

If you want to store this configuration so you don't have to re-config everytime, pass in the `store` param

```python
Config.initialize('Your Org', 'Your Key', store=True)
```

### Models

#### Project

```python
from pycci import Project
project = Project('Project Name')
pipelines = project.get_pipelines(num=100) # default is 20 to limit api calls for testing
```

#### Pipeline/Workflow/Job/Test

These models can all be fetched from circle CI following the project

```python
from pycci import Pipeline, Workflow, Job, Test

pipelines = project.get_pipelines(num=100)
pipeline = pipelines[0]

workflows = pipeline.get_workflows(failed_only=True) # Get only failed workflows, False by default
workflow = workflows[0]

jobs = workflow.get_jobs(type='type of job', failed_only=True) # type is a String, the JOBTYPE enum has some values to use
job = jobs[0]

tests = job.get_tests(failed_only=True)
```

All of the data for the objects is stored in a dictionary under the `data` attribute.

### API

All model instances are initialized with an api object instance that is accessible under the `api` attribute

```python
project_api = project.api
pipeline_api = pipeline.api
workflow_api = workflow.api
job_api = job.api
# Test has no api
```

The api objects can also be created directly

```python
from pycci import ProjectApi, PipelineApi, WorkflowApi, JobApi, JOBTYPE

project_api = ProjectApi('Project name')
result = project_api.get_pipelines(page_token=None)
next_page_token = result['next_page_token']
pipelines = result['items']

pipeline_api = PipelineApi(pipelines[0])
result = pipeline_api.get_workflows(failed_only=True, page_token=None)
next_page_token = result['next_page_token']
workflows = result['items']

workflow_api = WorkflowApi(workflows[0])
result = workflow_api.get_jobs(type=JOBTYPE.BACKEND, failed_only=True, page_token=None)
next_page_token = result['next_page_token']
jobs = result['items']

job_id = jobs[0]['id']
job_number = jobs[0]['number']
job_project_slug = jobs[0]['project_slug']
job_api = JobApi(job_id, job_number, job_project_slug)
# project slug looks like gh/org/project where gh is your version control
result = job_api.get_tests(failed_only=True, page_token=None)
next_page_token = result['next_page_token']
tests = result['items']
```
