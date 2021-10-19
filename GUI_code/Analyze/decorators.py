import functools
from PyQt5.QtWidgets import (
    QVBoxLayout
)

'''decorator for adding widgets to a layout'''
def wrap_widgets_in_layout(widgets):
    @functools.wraps(widgets)
    def wrapper(*args):
        layout = QVBoxLayout()
        widgets_ = []
        for widget in widgets(*args):
            layout.addWidget(widget)
            widgets_.append(widget)
        return layout, widgets_
    return wrapper


