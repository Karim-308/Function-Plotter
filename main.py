import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class FunctionPlotter(QMainWindow):
    """
    A comprehensive GUI application to plot user-defined mathematical functions dynamically.

    This class integrates a graphical interface using PySide2 for users to input mathematical functions
    and display their corresponding plots. Features include zooming, panning, and input validation.
    """

    def __init__(self):
        """
        Constructor to initialize the main window, set up the UI, and create necessary placeholders for the UI elements.
        """
        super().__init__()
        self.ax = None  # Placeholder for the matplotlib axis, set during plotting
        self.canvas = None  # Placeholder for matplotlib canvas
        self.plot_button = None  # Button to initiate plotting
        self.function_input = None  # Input field for functions
        self.min_input = None  # Input for the minimum x-value
        self.max_input = None  # Input for the maximum x-value
        self.initialize_ui()

    def initialize_ui(self):
        """
        Configures UI components and layouts, setting icons, titles, and initializing all widgets.
        """
        self.setWindowIcon(QIcon('images/plotter_icon.png'))
        self.setWindowTitle('Function Plotter')
        self.setGeometry(100, 100, 860, 640)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)

        # Add and scale an image at the top of the layout
        image_label = QLabel(self)
        pixmap = QPixmap('images/Master_Micro.png')
        scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setMargin(20)
        left_layout.addWidget(image_label)
        left_layout.addStretch(1)  # Provides spacing

        # Setting up user input fields with labels
        function_label = QLabel("Function:")
        self.function_input = QLineEdit(self)
        self.function_input.setPlaceholderText("Enter function of x (e.g., 5*x^3 + 2*x)")
        self.function_input.setAlignment(Qt.AlignCenter)

        min_label = QLabel("Min x:")
        self.min_input = QLineEdit(self)
        self.min_input.setPlaceholderText("Enter min value of x")
        self.min_input.setAlignment(Qt.AlignCenter)

        max_label = QLabel("Max x:")
        self.max_input = QLineEdit(self)
        self.max_input.setPlaceholderText("Enter max value of x")
        self.max_input.setAlignment(Qt.AlignCenter)

        # Setup and connect the plot button
        self.plot_button = QPushButton('Plot Function', self)
        self.plot_button.setObjectName("plot_button")
        self.plot_button.clicked.connect(self.plot_function)

        # Add widgets to the left layout
        left_layout.addWidget(function_label)
        left_layout.addWidget(self.function_input)
        left_layout.addWidget(min_label)
        left_layout.addWidget(self.min_input)
        left_layout.addWidget(max_label)
        left_layout.addWidget(self.max_input)
        left_layout.addWidget(self.plot_button)
        left_layout.addStretch(2)

        # Canvas and toolbar for plotting
        self.canvas = FigureCanvas(plt.Figure(facecolor='#f0ebd8'))
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_title('Function Plot')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid(True)
        self.toolbar = NavigationToolbar(self.canvas, self)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.toolbar)
        toolbar_layout.setAlignment(Qt.AlignCenter)

        # Right layout for canvas and toolbar
        right_layout = QVBoxLayout()
        right_layout.addStretch(2)
        right_layout.addWidget(self.canvas)
        right_layout.addLayout(toolbar_layout)
        right_layout.addStretch(3)

        # Main layout setup
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def plot_function(self):
        """
        Plots the function based on user input after validating the input.
        Handles plotting logic and updates the plot display.
        """
        function_str = self.function_input.text()
        min_x_str = self.min_input.text()
        max_x_str = self.max_input.text()

        if not self.validate_user_input(function_str, min_x_str, max_x_str):
            return

        min_x = float(min_x_str)
        max_x = float(max_x_str)
        x = np.linspace(min_x, max_x, 1000)

        try:
            y = eval(self.convert_to_python_syntax(function_str))
            self.canvas.figure.clear()
            self.ax = self.canvas.figure.add_subplot(111)
            self.ax.plot(x, y, label=function_str)
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            if str(e).__contains__("invalid decimal literal"):
                self.show_error_message(f"Please check using the mathmatical operators between numerals and the variable x")
            else:
                self.show_error_message(f"Error evaluating function: {str(e)} ")

    def validate_user_input(self, function_str, min_x_str, max_x_str):
        """
        Validates the user's input for function syntax and range values.
        Ensures that all inputs are correct before plotting can proceed.

        Parameters:
            function_str (str): The mathematical function entered by the user.
            min_x_str (str): The minimum x-value for the plot.
            max_x_str (str): The maximum x-value for the plot.

        Returns:
            bool: True if the input is valid, otherwise False.
        """
        if not function_str:
            self.show_error_message("Function cannot be empty.")
            return False

        if not min_x_str or not max_x_str:
            self.show_error_message("Please enter values for both Min x and Max x.")
            return False

        if not re.match(r'^[\d\w\s\+\-\*/\^\(\)]+$', function_str):
            self.show_error_message("Invalid function format.")
            return False

        try:
            float(min_x_str)
            float(max_x_str)
        except ValueError:
            self.show_error_message("Min and Max values must be numbers.")
            return False

        if float(min_x_str) >= float(max_x_str):
            self.show_error_message("Min value must be less than Max value.")
            return False

        return True

    def convert_to_python_syntax(self, function_str):
        """
        Converts user-input function syntax to Python executable syntax.

        Parameters:
            function_str (str): The user-input function string.

        Returns:
            str: A string of the function converted to Python syntax.
        """
        function_str = function_str.replace('^', '**')
        function_str = function_str.replace('log10', 'np.log10')
        function_str = function_str.replace('sqrt', 'np.sqrt')
        return function_str

    @staticmethod
    def show_error_message(message):
        """
        Displays an error message to the user using a QMessageBox.

        Parameters:
            message (str): The error message to be displayed.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())

    ex = FunctionPlotter()
    ex.show()
    sys.exit(app.exec_())