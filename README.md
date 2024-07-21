# FunctionPlotter

FunctionPlotter is a Python-based graphical application designed to allow users to visualize mathematical functions. Built using PySide2 and Matplotlib, this tool provides an interactive environment to plot, zoom, and analyze function graphs dynamically.

## Features

- **Interactive Plotting**: Users can input any mathematical function (e.g., `5*x^3 + 2*x`) to see its graph.
- **Zoom and Pan**: The application includes a toolbar for zooming and panning, helping users explore details of the graph.
- **Input Validation**: Inputs are validated to ensure only correct mathematical expressions and numeric values are accepted.
- **Error Handling**: Provides user-friendly notifications for incorrect inputs or errors during the plotting process.
  
## Screenshots

<div align="center">
   <a href="https://ibb.co/xfPfGLZ"><img src="https://i.ibb.co/RBZBPb8/intro-screen.png" alt="intro-screen" border="0"></a>
    <br>
    <sup style="font-size: 24px;">Intro Screen</sup>
    <br>
    <br>
</div>


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

You need to have Python installed on your machine (Python 3.10 or less is recommended in order for PySide2 to work). Additionally, you should install the following packages:

```bash
pip install PySide2 numpy matplotlib
```
## Installing 

```bash
git clone https://github.com/yourusername/functionplotter.git
cd functionplotter
```

## Running

 ```bash
python main.py
```

## Usage

- **Start the Application**: Run the `main.py` script.
- **Enter a Function**: Type a function using `x` as the variable (e.g., `x^2`, `sin(x)`, etc.).
- **Set the Range**: Specify the minimum and maximum values for the `x-axis`.
- **Plot**: Click the "Plot Function" button to view the graph.
- **Interact**: Use the zoom and pan tools to explore different parts of the graph.

## Tests

To run tests, ensure you have `pytest` and `pytest-qt` installed:

```bash
pip install pytest pytest-qt
