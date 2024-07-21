# test_functionplotter.py

import pytest
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtCore import Qt
from main import FunctionPlotter

@pytest.fixture
def app(qtbot):
    """
    Fixture to create and return a FunctionPlotter instance with qtbot for GUI interaction.
    """
    test_app = FunctionPlotter()
    qtbot.addWidget(test_app)
    return test_app

def test_valid_function_input(app, qtbot):
    """
    Test that the application correctly plots a simple quadratic function.
    """
    qtbot.keyClicks(app.function_input, 'x^2')
    qtbot.keyClicks(app.min_input, '-10')
    qtbot.keyClicks(app.max_input, '10')
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    assert not app.ax.lines == [], "The plot should have lines after plotting."

def test_invalid_function_input(app, qtbot):
    """
    Test the app's response to an unbalanced parenthesis in the function input.
    """
    qtbot.keyClicks(app.function_input, 'sin(x')
    qtbot.keyClicks(app.min_input, '0')
    qtbot.keyClicks(app.max_input, '10')
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    assert app.findChild(QMessageBox), "Error evaluating function: '(' was never closed (<string>, line 1)"

def test_empty_input_fields(app, qtbot):
    """
    Test the response when the input fields are empty.
    """
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    assert app.findChild(QMessageBox), "Function cannot be empty"

def test_non_numeric_range_inputs(app, qtbot):
    """
    Test the application's response to non-numeric range inputs.
    """
    qtbot.keyClicks(app.function_input, 'x^3')
    qtbot.keyClicks(app.min_input, 'a')
    qtbot.keyClicks(app.max_input, 'b')
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    assert app.findChild(QMessageBox), "Min and Max values must be numbers"

def test_function_with_special_characters(app, qtbot):
    """
    Test handling of functions containing invalid special characters.
    """
    qtbot.keyClicks(app.function_input, 'x^2 + y^2')
    qtbot.keyClicks(app.min_input, '-5')
    qtbot.keyClicks(app.max_input, '5')
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    assert app.findChild(QMessageBox), "Error evaluating function: name 'y' is not defined"

def test_zoom_functionality(app, qtbot):
    """
    Simulates the zoom functionality to ensure the toolbar is interacting with the plot correctly.
    """
    qtbot.keyClicks(app.function_input, 'x^2')
    qtbot.keyClicks(app.min_input, '-10')
    qtbot.keyClicks(app.max_input, '10')
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    original_xlim = app.ax.get_xlim()
    qtbot.mouseClick(app.toolbar.actions()[4], Qt.LeftButton)
    assert app.ax.get_xlim() != original_xlim, "Zooming should change the x-axis limits."

