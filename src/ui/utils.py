import torch
from collections import OrderedDict
from typing import Callable, Dict, Any, List, Optional
from supervisely.app import DataJson
from supervisely.app.widgets import Button, Widget, Container, Switch, Card, InputNumber


button_clicked = {}
select_params = {"icon": None, "plain": False, "text": "Select"}
reselect_params = {"icon": "zmdi zmdi-refresh", "plain": True, "text": "Reselect"}


def update_custom_params(
    btn: Button,
    params_dct: Dict[str, Any],
) -> None:
    btn_state = btn.get_json_data()
    for key in params_dct.keys():
        if key not in btn_state:
            raise AttributeError(f"Parameter {key} doesn't exists.")
        else:
            DataJson()[btn.widget_id][key] = params_dct[key]
    DataJson().send_changes()


def update_custom_button_params(
    btn: Button,
    params_dct: Dict[str, Any],
) -> None:
    params = params_dct.copy()
    if "icon" in params and params["icon"] is not None:
        new_icon = f'<i class="{params["icon"]}" style="margin-right: {btn._icon_gap}px"></i>'
        params["icon"] = new_icon
    update_custom_params(btn, params)


def get_switch_value(switch: Switch):
    return switch.is_switched()


def set_switch_value(switch: Switch, value: bool):
    if value:
        switch.on()
    else:
        switch.off()


class InputContainer(object):
    def __init__(self) -> None:
        self._widgets = {}
        self._custom_get_value = {}
        self._custom_set_value = {}

    def add_input(
        self,
        name: str,
        widget: Widget,
        custom_value_getter: Optional[Callable[[Widget], Any]] = None,
        custom_value_setter: Optional[Callable[[Widget, Any], None]] = None,
    ) -> None:
        self._widgets[name] = widget
        if custom_value_getter is not None:
            self._custom_get_value[name] = custom_value_getter
            self._custom_set_value[name] = custom_value_setter

    def get_params(self) -> Dict[str, Any]:
        params = {}
        for name in self._widgets.keys():
            params[name] = self._get_value(name)
        return params

    def set(self, name: str, value: Any) -> None:
        if name in self._widgets:
            self._set_value(name, value)
        else:
            raise AttributeError(
                f"Widget with name {name} does not exists, only {self._widgets.keys()}"
            )

    def _get_value(self, name: str):
        if name in self._custom_get_value:
            widget = self._widgets[name]
            return self._custom_get_value[name](widget)
        return self._widgets[name].get_value()

    def _set_value(self, name: str, value: Any):
        if name in self._custom_set_value:
            widget = self._widgets[name]
            self._custom_set_value[name](widget, value)
        else:
            self._widgets[name].value = value

    def __getattr__(self, __name: str) -> Any:
        if __name in self._widgets:
            return self._get_value(__name)
        raise AttributeError(
            f"Widget with name {__name} does not exists, only {self._widgets.keys()}"
        )


class OrderedWidgetWrapper(InputContainer):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._wraped_widgets = OrderedDict()
        self._container = None

    def add_input(
        self,
        name: str,
        widget: Widget,
        wraped_widget: Widget,
        custom_value_getter: Optional[Callable[[Widget], Any]] = None,
        custom_value_setter: Optional[Callable[[Widget, Any], None]] = None,
    ) -> None:
        super().add_input(name, widget, custom_value_getter, custom_value_setter)
        self._wraped_widgets[name] = wraped_widget

    def create_container(self, hide=False, update=False) -> Container:
        if self._container is not None and not update:
            return self._container
        widgets = [widget for widget in self._wraped_widgets.values()]
        self._container = Container(widgets)
        if hide:
            self.hide()
        return self._container

    def hide(self):
        if self._container is None:
            return
        self._container.hide()

    def show(self):
        if self._container is None:
            return
        self._container.show()

    def __repr__(self) -> str:
        return self._name


def disable_enable(widgets: List[Widget], disable: bool = True):
    for w in widgets:
        if disable:
            w.disable()
        else:
            w.enable()


def unlock_lock(cards: List[Card], unlock: bool = True):
    for w in cards:
        if unlock:
            w.unlock()
        else:
            w.lock()


def button_selected(
    select_btn: Button,
    disable_widgets: List[Widget],
    lock_cards: List[Card],
    lock_without_click: bool = False,
):
    global button_clicked
    bid = select_btn.widget_id

    if bid not in button_clicked:
        button_clicked[bid] = True
    else:
        button_clicked[bid] = not button_clicked[bid]

    if lock_without_click:
        disable_enable(disable_widgets, disable=False)
        unlock_lock(lock_cards, unlock=False)
        update_custom_button_params(select_btn, select_params)
        button_clicked[bid] = True
        return

    disable_enable(disable_widgets, disable=button_clicked[bid])
    unlock_lock(lock_cards, unlock=button_clicked[bid])

    if button_clicked[bid] is True:
        update_custom_button_params(select_btn, reselect_params)
    else:
        update_custom_button_params(select_btn, select_params)


def get_devices():
    cuda_names = [
        f"cuda:{i} ({torch.cuda.get_device_name(i)})" for i in range(torch.cuda.device_count())
    ]
    cuda_devices = [f"cuda:{i}" for i in range(torch.cuda.device_count())]
    device_names = cuda_names + ["cpu"]
    torch_devices = cuda_devices + ["cpu"]
    return device_names, torch_devices


def create_linked_getter(
    widget1: InputNumber,
    widget2: InputNumber,
    switcher: Switch,
    get_first: bool = True,
) -> Callable[[Widget], Any]:
    """Return getter for widgets depends on switcher value.

    :param widget1: first input
    :type widget1: InputNumber
    :param widget2: second input
    :type widget2: InputNumber
    :param switcher: switcher widget
    :type switcher: Switch
    :param get_first: if True return getter for first widget, defaults to True
    :type get_first: bool, optional
    :return: getter function
    :rtype: Callable[[InputNumber], Any]
    """

    def getter(any_widget: InputNumber):
        widget1_val = widget1.value
        widget2_val = widget2.value

        if switcher.is_switched():
            widget1_val = None
        else:
            widget2_val = None

        if get_first:
            return widget1_val
        return widget2_val

    return getter
