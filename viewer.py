from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QIcon
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QAction, QFileDialog, \
    QDockWidget, QListWidget, QVBoxLayout, QToolBar, QComboBox
import pydicom as dcm


from signup import Ui_Dialog
import pydicom

from pydicom.data import get_testdata_file

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        ab = pydicom.dcmread('ab.dcm')

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createToolBars()
        self.createStatusBar()

        self.setWindowTitle("20조 종합설계-Dicom Image Viewer")
        self.setWindowIcon(QIcon('icon_main.png'))
        self.resize(900, 700)

        self.lbl_patient_info = QLabel("Image Type : {0}\n"
                                       "SOP Class UID : {1}\n"
                                       "SOP Instance UID : {2}".format("Lung Image", ab.SOPClassUID, ab.SOPInstanceUID))

        self.lbl_disease_info = QLabel("Pe present on image : {0}\n"
                                       "Negative exam for pe : {1}\n"
                                       "Qa motion : {2}\n"
                                       "Qa contrast : {3}\n"
                                       "Rv lv ratio gte 1 : {4}\n"
                                       "Rv lv ratio lt 1 : {5}\n"
                                       "Leftsided pe : {6}\n"
                                       "Rightsided pe : {7}\n"
                                       "Central pe : {8}\n"
                                       "Chronic pe : {9}\n"
                                       "Acute and Chronic pe : {10}\n"
                                       "True filling detect not pe : {11}".format(0.98, 0.12, 0.1, 0.5 ,0.7, 0.9, 0.6, 0.10, 0.84, 0.65, 0.93, 0.4))
        self.lbl_study_info = QLabel("Modality : {0}\n"
                                     "Image Bits Allocated : {1}\n"
                                     "Image Rows, Columns : {2}. {3}".format(ab.Modality, ab.BitsAllocated, ab.Rows,
                                                                             ab.Columns))

        self.dock_patient_info = QDockWidget(self)
        self.dock_disease_info = QDockWidget(self)
        self.dock_study_info = QDockWidget(self)
        self.dock_patient_info.setWindowTitle("Patient Information")
        self.dock_disease_info.setWindowTitle("Disease Information for AI model")
        self.dock_study_info.setWindowTitle("Study Information")
        self.dock_patient_info.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.dock_disease_info.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.dock_study_info.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_patient_info)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_disease_info)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_study_info)
        self.dock_patient_info.setWidget(self.lbl_patient_info)
        self.dock_disease_info.setWidget(self.lbl_disease_info)
        self.dock_study_info.setWidget(self.lbl_study_info)
        self.dock_patient_info.hide()
        self.dock_disease_info.hide()
        self.dock_study_info.hide()



    def open(self):
        options = QFileDialog.Options()
        # fpath = dcm.dcmread('PE_CT.jpg')
        # sss = fpath.pixel_array
        # print(sss)
        # image = QImage(sss)
        #
        # self.imageLabel.setPixmap(QPixmap.fromImage(image))
        # self.scaleFactor = 1.0
        #
        # self.scrollArea.setVisible(True)
        # self.printAct.setEnabled(True)
        # self.fitToWindowAct.setEnabled(True)
        # self.updateActions()
        #
        # self.dock_patient_info.show()
        # self.dock_disease_info.show()
        # self.dock_study_info.show()


        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return
            print(image)
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            self.dock_patient_info.show()
            self.dock_disease_info.show()
            self.dock_study_info.show()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()
            self.lbl_patient_info = QLabel('eeee')

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    # def won(self):
    #     self.wonDialog = QtWidgets.QDialog()
    #     self.ui = Ui_Dialog_won()
    #     self.ui.setupUi(self.wonDialog)
    #     self.wonDialog.show()

    def zoomIn(self):
        self.scaleImage(1.25)


    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def createActions(self):
        self.openAct = QAction(QIcon('icon_fileOpen.png'), "&File Open", self, shortcut="Ctrl+O",
                               triggered=self.open, statusTip="File Open")
        self.printAct = QAction(QIcon('icon_print.png'), "&Print", self, shortcut="Ctrl+P", enabled=False,
                                triggered=self.print_, statusTip="Print")
        self.exitAct = QAction(QIcon('icon_exit.png'), "E&xit", self, shortcut="Ctrl+Q",
                               triggered=self.close, statusTip="Exit")
        self.zoomInAct = QAction(QIcon('icon_zoomIn.png'), "Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False,
                                 triggered=self.zoomIn, statusTip="Zoom In")
        self.zoomOutAct = QAction(QIcon('icon_zoomOut.png'), "Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False,
                                  triggered=self.zoomOut, statusTip="Zoom Out")
        self.normalSizeAct = QAction(QIcon('icon_normalSize.png'), "&Normal Size", self, shortcut="Ctrl+S",
                                     enabled=False,
                                     triggered=self.normalSize, statusTip="Return To Normal Size")
        self.fitToWindowAct = QAction(QIcon('icon_fitToWindow.png'), "&Fit to Window", self, enabled=False,
                                      checkable=True,
                                      shortcut="Ctrl+F", triggered=self.fitToWindow, statusTip="Fitting Size To Window")

    def createToolBars(self):
        FileOpenToolBar = self.addToolBar("&File Open")
        ZoomInToolBar = self.addToolBar("&Zoom In")
        ZoomOutToolBar = self.addToolBar("&Zoom Out")
        NormalSizeToolBar = self.addToolBar("&Normal Size")
        FittingSizeToolBar = self.addToolBar("&Fit To Window")
        PrintToolBar = self.addToolBar("&Print")
        ExitToolBar = self.addToolBar("&Exit")
        FileOpenToolBar.addAction(self.openAct)
        ZoomInToolBar.addAction(self.zoomInAct)
        ZoomOutToolBar.addAction(self.zoomOutAct)
        NormalSizeToolBar.addAction(self.normalSizeAct)
        FittingSizeToolBar.addAction(self.fitToWindowAct)
        PrintToolBar.addAction(self.printAct)
        ExitToolBar.addAction(self.exitAct)

    def createStatusBar(self):
        self.locationLabel = QLabel("")
        self.locationLabel.setAlignment(Qt.AlignHCenter)
        self.statusBar().addWidget(self.locationLabel)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 6.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
