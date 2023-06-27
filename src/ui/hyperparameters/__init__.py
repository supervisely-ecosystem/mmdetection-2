from supervisely.app.widgets import Tabs, Card

from src.ui.hyperparameters.checkpoints import checkpoints_tab, checkpoint_params
from src.ui.hyperparameters.general import general_tab, general_params
from src.ui.hyperparameters.optimizers import optimizers_tab, optimizers_params
from src.ui.hyperparameters.lr_scheduler import (
    schedulres_tab,
    schedulers_params,
    get_scheduler_params,
)
from src.train_parameters import TrainParameters

from src.ui.hyperparameters import general
from src.ui.hyperparameters import checkpoints
from src.ui.hyperparameters import optimizers
from src.ui.hyperparameters import lr_scheduler


content = Tabs(
    labels=[
        "General",
        "Checkpoints",
        "Optimizers (Advanced)",
        "Learning rate scheduler (Advanced)",
    ],
    contents=[general_tab, checkpoints_tab, optimizers_tab, schedulres_tab],
)

card = Card(
    title="6️⃣Training hyperparameters",
    description="Partially taken from default model configs",
    lock_message="Select model",
    content=content,
)
card.lock()


# def reset_widgets():
#     card.lock("Select a model to unlock.")


def update_widgets_with_params(params: TrainParameters):
    general.update_general_widgets_with_params(params)
    checkpoints.update_checkpoint_widgets_with_params(params)
    optimizers.update_optimizer_widgets_with_params(params)
    lr_scheduler.update_scheduler_widgets_with_params(params)


def update_params_with_widgets(params: TrainParameters):
    general.update_general_params_with_widgets(params)
    checkpoints.update_checkpoint_params_with_widgets(params)
    optimizers.update_optimizer_params_with_widgets(params)
    lr_scheduler.update_scheduler_params_with_widgets(params)


# reset_widgets()
