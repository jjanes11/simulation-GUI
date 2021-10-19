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



# def bla(f):
#     @functools.wraps(f)
#     def wrapper(*args):
#         f(*args)
#         print("Lo!")
#     return wrapper


# class Yoda:
#     def __init__(self):
#         layout = self.create_widgets()

#     @bla
#     def create_widgets(self):
#         print("Hi!")

# @bla
# def create_widgets():
#     print("Hi!")

# create_widgets()


# yo = Yoda()