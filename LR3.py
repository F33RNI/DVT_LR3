"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph.opengl as gl
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # Load GUI file
        uic.loadUi('LR3.ui', self)

        # Settings
        self.bars_width = 0.08
        self.bar_z_color = np.array(np.array([1., 0.4, 0.7, 1.]))
        self.bar_x_color = np.array(np.array([1., 1., 0., 1.]))
        self.bar_y_color = np.array(np.array([0., 1., 1., 1.]))

        # System variables
        self.points = []
        self.actual_points = []
        self.points_surface = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]))
        self.bar_graph_x = gl.GLBarGraphItem(pos=np.array([[0, 0, 0]]), size=np.array([0, 0, 0]))
        self.bar_graph_y = gl.GLBarGraphItem(pos=np.array([[0, 0, 0]]), size=np.array([0, 0, 0]))
        self.bar_graph_z = gl.GLBarGraphItem(pos=np.array([[0, 0, 0]]), size=np.array([0, 0, 0]))

        # Connect GUI controls
        self.btn_generate_data.clicked.connect(self.generate_data)
        self.btn_save_data.clicked.connect(self.save_data)
        self.btn_load_data.clicked.connect(self.load_data)
        self.btn_show_3d.clicked.connect(self.draw_points)
        self.btn_update_bars.clicked.connect(self.update_bars)

        # Initialize table
        self.init_table()

        # Initialize OpenGL widget
        self.init_opengl()

        # Show GUI
        self.show()

    def init_table(self):
        """
        Initializes table of points
        :return:
        """
        self.points_table.setColumnCount(3)
        self.points_table.verticalHeader().setVisible(False)
        self.points_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.points_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('X'))
        self.points_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Y'))
        self.points_table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Z'))
        header = self.points_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def init_opengl(self):
        """
        Initializes OpenGL Widget
        :return:
        """

        # Cube bottom square
        cube_bottom_square = gl.GLLinePlotItem(
            pos=np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]]),
            color=[1, 1, 1, 1])
        self.openGLWidget.addItem(cube_bottom_square)

        # Cube top square
        cube_top_square = gl.GLLinePlotItem(
            pos=np.array([[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1], [-1, -1, 1]]),
            color=[1, 1, 1, 1])
        self.openGLWidget.addItem(cube_top_square)

        # Cube sides
        cube_line_bl = gl.GLLinePlotItem(
            pos=np.array([[-1, -1, -1], [-1, -1, 1]]),
            color=[1, 1, 1, 1])
        self.openGLWidget.addItem(cube_line_bl)
        cube_line_br = gl.GLLinePlotItem(
            pos=np.array([[-1, 1, -1], [-1, 1, 1]]),
            color=[1, 1, 1, 1])
        self.openGLWidget.addItem(cube_line_br)
        cube_line_tr = gl.GLLinePlotItem(
            pos=np.array([[1, 1, -1], [1, 1, 1]]),
            color=[1, 1, 1, 1])
        self.openGLWidget.addItem(cube_line_tr)
        cube_line_tl = gl.GLLinePlotItem(
            pos=np.array([[1, -1, -1], [1, -1, 1]]),
            color=[1, 1, 1, 1])
        self.openGLWidget.addItem(cube_line_tl)

        # Add data elements
        self.openGLWidget.addItem(gl.GLAxisItem())
        self.openGLWidget.addItem(self.points_surface)
        self.openGLWidget.addItem(self.bar_graph_x)
        self.openGLWidget.addItem(self.bar_graph_y)
        self.openGLWidget.addItem(self.bar_graph_z)

    def generate_data(self):
        """
        Generates points cloud
        :return:
        """
        print('Generating data...')
        points_num = self.points_num.value()

        self.points = []
        for _ in range(points_num):
            self.points.append(np.random.uniform(-1, 1, 3))

        for i in range(points_num):
            pass
        self.points = np.array(self.points)

        self.show_on_table()
        self.btn_save_data.setEnabled(True)
        print('Data generated.')

    def show_on_table(self):
        """
        Shows points in table
        :return:
        """
        self.points_table.setRowCount(0)
        for point in self.points:
            row_position = self.points_table.rowCount()
            self.points_table.insertRow(row_position)
            self.points_table.setItem(row_position, 0, QTableWidgetItem(str(point[0])))
            self.points_table.setItem(row_position, 1, QTableWidgetItem(str(point[1])))
            self.points_table.setItem(row_position, 2, QTableWidgetItem(str(point[2])))
        self.btn_save_data.setEnabled(True)

    def update_bars(self):
        """
        Updates and draws 3D - bar charts
        """
        # Z (x:y)
        bar_pos, bar_size = self.count_blocks([item[0] for item in self.actual_points],
                                              [item[1] for item in self.actual_points], 2)
        self.openGLWidget.removeItem(self.bar_graph_z)
        self.bar_graph_z = gl.GLBarGraphItem(pos=np.array(bar_pos), size=np.array(bar_size))
        self.bar_graph_z.setColor(self.bar_z_color)
        self.openGLWidget.addItem(self.bar_graph_z)

        # Y (x:z)
        bar_pos, bar_size = self.count_blocks([item[0] for item in self.actual_points],
                                              [item[2] for item in self.actual_points], 1)
        self.openGLWidget.removeItem(self.bar_graph_y)
        self.bar_graph_y = gl.GLBarGraphItem(pos=np.array(bar_pos), size=np.array(bar_size))
        self.bar_graph_y.setColor(self.bar_y_color)
        self.openGLWidget.addItem(self.bar_graph_y)

        # X (y:z)
        bar_pos, bar_size = self.count_blocks([item[1] for item in self.actual_points],
                                              [item[2] for item in self.actual_points], 0)
        self.openGLWidget.removeItem(self.bar_graph_x)
        self.bar_graph_x = gl.GLBarGraphItem(pos=np.array(bar_pos), size=np.array(bar_size))
        self.bar_graph_x.setColor(self.bar_x_color)
        self.openGLWidget.addItem(self.bar_graph_x)

    def count_blocks(self, data_x, data_y, orientation):
        """
        Counts how many points in each block and returns bars data
        """
        max_block_value = 0
        bar_pos = []
        bar_size = []
        for x in range(-10, 10):
            for y in range(-10, 10):
                points_in_block = 0
                for i in range(len(data_x)):
                    if x / 10 <= data_x[i] < (x / 10 + 0.1) \
                            and y / 10 <= data_y[i] < (y / 10 + 0.1):
                        points_in_block += 1
                if points_in_block > max_block_value:
                    max_block_value = points_in_block

                if points_in_block > 0:
                    if orientation == 0:
                        pos = [1, x / 10 + ((0.1 - self.bars_width) / 2), y / 10 + ((0.1 - self.bars_width) / 2)]
                    elif orientation == 1:
                        pos = [x / 10 + ((0.1 - self.bars_width) / 2), 1, y / 10 + ((0.1 - self.bars_width) / 2)]
                    else:
                        pos = [x / 10 + ((0.1 - self.bars_width) / 2), y / 10 + ((0.1 - self.bars_width) / 2), 1]
                    size = [self.bars_width] * 3
                    size[orientation] = points_in_block
                    bar_pos.append(pos)
                    bar_size.append(size)

        bar_size_normalized = []
        for bar in bar_size:
            bar[orientation] /= max_block_value
            bar_size_normalized.append(bar)
        return bar_pos, bar_size_normalized

    def draw_points(self):
        """
        Draws 3D points with OpenGL
        :return:
        """
        thinning = self.thinning.value()
        if self.points is not None and len(self.points) > 0:
            # Create color map
            z = np.array(np.array([item[2] for item in self.points]))
            cmap = plt.get_cmap('hsv')
            min_z = np.min(z)
            max_z = np.max(z)
            rgba_img = cmap(1.0 - (z - min_z) / (max_z - min_z))

            # Draw points using defined thinning
            self.actual_points = []
            for i in range(len(self.points)):
                if i % thinning == 0:
                    self.actual_points.append(self.points[i])
            self.points_surface.setData(pos=np.array(self.actual_points), color=rgba_img)

    def save_data(self):
        """
        Saves points to CSV file
        :return:
        """
        print('Saving data...')
        np.savetxt(self.data_file.text(), self.points, delimiter=' ')
        print('File', self.data_file.text(), 'saved.')

    def load_data(self):
        """
        Loads points to CSV file
        :return:
        """
        if os.path.exists(self.data_file.text()):
            print('Loading data...')
            self.points = np.loadtxt(self.data_file.text(), delimiter=' ')
            self.show_on_table()
            print('File', self.data_file.text(), 'loaded.')
        else:
            print('File', self.data_file.text(), 'doesn\'t exist!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    win = Window()
    sys.exit(app.exec_())
