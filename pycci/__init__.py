__version__ = '1.0.0'

from .config import Config
from .jobtype import JOBTYPE
from .api import ProjectApi, PipelineApi, WorkflowApi, JobApi
from .models import Project, Pipeline, Workflow, Job, Test


if Config.API_KEY == None:
    Config._load_config()
