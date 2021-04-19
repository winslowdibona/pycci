from pycci import JOBTYPE, Project, Pipeline, Workflow, Job, Test, Config

# Initialize Configuration, pass in store if you want to store credentials
Config.initialize('Your Org', 'API_KEY', store=True)


'''
To get the pipelines for a project, you can either retrieve them through
the Project model class, or through the ProjectApi directly.
'''

project = Project('Your Project')
project_api = ProjectApi('BetterWorks')
# project.api == project_api but are not the same instance

pipelines = project.get_pipelines(num=20) # pipelines will also be stored on the project model instance
pipeline = pipelines[0]

result = project.api.get_pipelines(page_token=None)
result = project_api.get_pipelines(page_token=None)

pipeline = Pipeline(result['items'][0])

'''
To get the workflows for a pipeline, you can either retrieve them through
the Pipeline model class, or through the PipelineApi directly.
'''

pipeline_api = PipelineApi(pipeline.id)

workflows = pipeline.get_workflows(failed_only=True) # failed_only is False by default
workflow = workflows[0] # workflows will also be stored on the pipeline model instance

result = pipeline.api.get_workflows()
result = pipeline_api.get_workflows()

workflow = Workflow(result['items'][0])

'''
To get the jobs for a workflow, you can either retrieve them through
the Workflow model class, or through the WorkflowApi directly.
By default, the api will retirve all jobs within a given workflow, but you can
specify the name of the job you want to retrieve passing in a string to the
`type` parameter.
The JOBTYPE class provides a few values that can be used, see jobtype.py for more.
'''

workflow_api = WorkflowApi(workflow.id)

all_jobs = workflow.get_jobs() # jobs will also be stored on the workflow model instance
job = all_jobs[0]

all_jobs = workflow.api.get_jobs()
failed_jobs = workflow.api.get_jobs(failed_only=True)
failed_cypress_jobs = workflow.api.get_jobs(type=JOBTYPE.CYPRESS, failed_only=True)
custom_jobs_result = workflow_api.get_jobs(type='custom_job')

job = all_jobs[0]
job = Job(custom_jobs_result['items'][0])

'''
To get the tests for a job, you can either retrieve them through
the Job model class, or through the JobApi directly.
'''

job_api = JobApi(job.id, job.number, job.project_slug) # needs a few additional parameters

_ = job.get_tests() # tests will also be stored on the job model instance
test = job.tests[0]

failed_tests_result = job_api.get_tests(failed_only=True)

test = Test(failed_tests_result['items'][0])
