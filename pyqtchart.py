from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer


class ChartDockWidget(QDockWidget):
    def __init__(self, title, parent=None ):
        super().__init__(title, parent)
        self.x = 5
        self.series = QLineSeries(self)
        self.series.append(0,6)
        self.series.append(1, 4)
        self.series.append(2, 8)
        self.series.append(3, 4)
        self.series.append(4, 5)
        self.chart =  QChart()

        self.chart.addSeries(self.series)

        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle(title)
        # make the x axis have default 100 ticks separated as 1
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        # add a label to the marker
        self.chart.legend().markers(self.series)[0].setLabel("HearRate")

        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)

        self.setWidget(self.chartview)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(1000)

    def updateData(self):
        self.x += 1 
        # Todos : read values from database instead of randomly adding them
        self.series.append(self.x , 5 ) # ADD VALUES HERE
        self.chart.axisX().setRange(0, self.x )
        self.chart.axisX().setTickCount(self.x)
        self.chart.axisX().setLabelFormat("%d")

        self.chart.axisY().setRange(0,  max([point.y() for point in self.series.points()]))

class Window(QMainWindow):

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("PyQtChart Line")
        self.setGeometry(100,100, 1000,700)

        self.show()

        self.dock1 = ChartDockWidget("Chart 1", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock1)

        self.dock2 = ChartDockWidget("Chart 2", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock2)

        self.dock3 = ChartDockWidget("Chart 3", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock3)

        self.dock4 = ChartDockWidget("Chart 4", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock4)



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())
