import os
import supervisely as sly
from dotenv import load_dotenv

from src.train_parameters import TrainParameters

load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")

PROJECT_ID = sly.env.project_id()
TEAM_ID = sly.env.team_id()

api: sly.Api = sly.Api.from_env()
app_dir = sly.app.get_data_dir()
app: sly.Application = None


stop_training = False
config_name: str = None
params: TrainParameters = None

# for Augmentations widget:
data_dir = app_dir
team = api.team.get_info_by_id(TEAM_ID)
project_meta: sly.ProjectMeta = sly.ProjectMeta.from_json(api.project.get_meta(PROJECT_ID))
# project_fs: sly.Project = None

COCO_MTERIC_KEYS = ["mAP", "mAP_50", "mAP_75"]
MAX_CLASSES_TO_SHOW_CLASSWISE_METRIC = 10
