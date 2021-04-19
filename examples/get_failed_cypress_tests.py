from pycci import JOBTYPE, Project, Pipeline, Workflow, Job, Test, Config

Config.initialize('Test Org', 'API_KEY', store=True)

project = Project('Test Project')
pipelines = project.get_pipelines(num=20)
workflows = [w for s in [p.get_workflows(failed_only=True) for p in pipelines] for w in s]
jobs = [j for s in [w.get_jobs(type=JOBTYPE.CYPRESS, failed_only=True) for w in workflows] for j in s]
tests = [t for s in [j.get_tests(failed_only=True) for j in jobs] for t in s]

print(tests)
