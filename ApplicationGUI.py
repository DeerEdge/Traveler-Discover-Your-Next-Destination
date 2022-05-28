import ApplicationDatabase
import ApplicationFilterRequest
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    global filteredAttractionsList
    filteredAttractionsList = []

    def createLabel(self,type,Xcoor,Ycoor,width,length):
        if type == "groupBox":
            self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        self.label.setObjectName("label")
        return self.label

    def createComboBox(self,type,Xcoor,Ycoor,width,length):
        if type == "groupBox":
            self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        self.comboBox.setObjectName("comboBox")
        return self.comboBox

    def createCheckBox(self,type,Xcoor,Ycoor,width,length):
        if type == "groupBox":
            self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        self.checkBox.setObjectName("checkBox")
        return self.checkBox

    def createScrollAreaObject(self):
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContainer)
        self.label.setMinimumSize(QtCore.QSize(0, 100))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        return self.label

    def controlScrollArea(self):
        global filteredAttractionsList
        _translate = QtCore.QCoreApplication.translate

        for attraction in range(len(filteredAttractionsList)):
            self.createScrollAreaObject().setText(_translate("MainWindow", str(filteredAttractionsList[attraction-1])))
        self.scrollArea.setWidget(self.scrollAreaWidgetContainer)

    def getCurrentFieldValues(self, _):
        global filteredAttractionsList

        currentSelectedState = self.stateFilterComboBox.currentText()
        currentSelectedCity = self.cityFilterComboBox.currentText()
        currentSelectedType = self.typeFilterComboBox.currentText()
        currentCheckedWheelchairAccessibility = self.wheelchairAccessFilterCheckBox.isChecked()
        currentCheckedFamilyFriendliness = self.familyFriendlyFilterCheckBox.isChecked()
        currentCheckedPetFriendliness = self.petFriendlyFilterCheckBox.isChecked()
        print("Selected State?:", currentSelectedState, "| Selected City?:", currentSelectedCity,
              "| Selected Type?:", currentSelectedType, "| Wheelchair Accessibility is Checked?:",
              currentCheckedWheelchairAccessibility, "| Family Friendliness is Checked?:",
              currentCheckedFamilyFriendliness, "| Pet Friendliness is Checked?:",
              currentCheckedPetFriendliness)

        attributeList = [str(currentSelectedState),str(currentSelectedCity),str(currentSelectedType),
                         str(currentCheckedWheelchairAccessibility), str(currentCheckedFamilyFriendliness),
                         str(currentCheckedPetFriendliness)]
        for index in range(len(attributeList)):
            if (attributeList[index] == "None" or attributeList[index] == "False"):
                attributeList[index] = None
        filteredAttractions = ApplicationDatabase.getAttractions(filters=ApplicationFilterRequest.FilterRequest(attributeList[0], attributeList[1], attributeList[2], attributeList[3], attributeList[4], attributeList[5]))
        filteredAttractionsList = filteredAttractions
        print(filteredAttractionsList)
        self.controlScrollArea()

        attributeList = [None, None, None, None, None, None]

    def setupUi(self, MainWindow):
        # Sets up the window container
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 851, 631))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.gridWidget = QtWidgets.QWidget(self.tabWidgetPage1)
        self.gridWidget.setGeometry(QtCore.QRect(580, 0, 251, 49))
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.gridWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.comboBox_4 = QtWidgets.QComboBox(self.gridWidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_3.addWidget(self.comboBox_4, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.tabWidgetPage1)
        self.line.setGeometry(QtCore.QRect(210, -10, 21, 611))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget = QtWidgets.QWidget(self.tabWidgetPage1)
        self.widget.setGeometry(QtCore.QRect(0, 50, 221, 361))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")

        # Filtering by State - Format: (Label : ComboBox)
        self.stateFilterLabel = self.createLabel("groupBox",5, 25, 50, 50)
        self.stateFilterComboBox = self.createComboBox("groupBox",40, 40, 157, 26)
        self.stateFilterComboBox.addItems(["None","Alabama","Alaska","Arizona","Arkansas","California",
                                           "Colorado","Connecticut","Delaware","Florida","Georgia",
                                           "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas",
                                           "Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
                                           "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
                                           "New Hampshire","New Jersey","New Mexico","New York","North Carolina",
                                           "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
                                           "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
                                           "Virginia","Washington","West Virginia","Wisconsin","Wyoming"])
        self.stateFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by City - Format: (Label : ComboBox)
        self.cityFilterLabel = self.createLabel("groupBox", 5, 65, 50, 50)
        self.cityFilterComboBox = self.createComboBox("groupBox", 40, 80, 157, 26)
        self.cityFilterComboBox.addItems(["None", "City1", "City2", "Huntsville", "Birmingham"])
        self.cityFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by Type - Format: (Label : ComboBox)
        self.typeFilterLabel = self.createLabel("groupBox", 5, 105, 50, 50)
        self.typeFilterComboBox = self.createComboBox("groupBox", 40, 120, 157, 26)
        self.typeFilterComboBox.addItems(["None", "Sports", "Cultural/Historical"])
        self.typeFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by WheelChair Accessibility - Format: (CheckBox : Label)
        self.wheelchairAccessFilterLabel = self.createLabel("groupBox", 30, 145, 150, 50)
        self.wheelchairAccessFilterCheckBox = self.createCheckBox("groupBox", 5, 161, 20, 20)
        self.wheelchairAccessFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Filtering by Family Friendliness - Format: (CheckBox : Label)
        self.familyFriendlyFilterLabel = self.createLabel("groupBox", 30, 170, 150, 50)
        self.familyFriendlyFilterCheckBox = self.createCheckBox("groupBox", 5, 186, 20, 20)
        self.familyFriendlyFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Filtering by Pet Friendliness - Format: (CheckBox : Label)
        self.petFriendlyFilterLabel = self.createLabel("groupBox", 30, 195, 150, 50)
        self.petFriendlyFilterCheckBox = self.createCheckBox("groupBox", 5, 211, 20, 20)
        self.petFriendlyFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Setting ScrollArea
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea = QtWidgets.QScrollArea(self.tabWidgetPage1)
        self.scrollArea.setGeometry(QtCore.QRect(230, 50, 611, 511))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContainer = QtWidgets.QWidget()
        self.scrollAreaWidgetContainer.setGeometry(QtCore.QRect(0, 0, 609, 988))
        self.scrollAreaWidgetContainer.setObjectName("scrollAreaWidgetContainer")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContainer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Adds multiple tabs
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.stateFilterLabel.setText(_translate("MainWindow", "State:"))
        self.cityFilterLabel.setText(_translate("MainWindow", "City:"))
        self.typeFilterLabel.setText(_translate("MainWindow", "Type:"))

        self.wheelchairAccessFilterLabel.setText(_translate("MainWindow", "Wheelchair Accessible"))
        self.familyFriendlyFilterLabel.setText(_translate("MainWindow", "Family Friendly"))
        self.petFriendlyFilterLabel.setText(_translate("MainWindow", "Pet Friendly"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("MainWindow", "Attractions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "About Us"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Sources"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

