import webbrowser
import ApplicationDatabase
import ApplicationFilterRequest
import io
import folium # pip install folium

from operator import itemgetter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine

class Ui_MainWindow(object):
    global currentAttraction
    global filteredAttractionsList
    filteredAttractionsList = []

    def createLabel(self,type,Xcoor,Ycoor,width,length):
        global groupBox
        global topGroupBoxBar
        global scrollAreaGroupBox
        if type == "groupBox":
            self.label = QtWidgets.QLabel(self.groupBox)
        elif type == "scrollAreaGroupBox":
            self.label = QtWidgets.QLabel(self.scrollAreaGroupBox)
        elif type == "helpMenuGroupBox":
            self.label = QtWidgets.QLabel(self.helpMenuGroupBox)
        elif type == "topGroupBoxBar":
            self.label = QtWidgets.QLabel(self.topGroupBoxBar)
        self.label.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        self.label.setObjectName("label")
        return self.label

    def createComboBox(self,type,Xcoor,Ycoor,width,length):
        global groupBox
        global scrollAreaGroupBox
        global topGroupBoxBar
        if type == "groupBox":
            self.comboBox = QtWidgets.QComboBox(self.groupBox)
        elif type == "topGroupBoxBar":
            self.comboBox = QtWidgets.QComboBox(self.topGroupBoxBar)
        self.comboBox.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        self.comboBox.setObjectName("comboBox")
        return self.comboBox

    def createCheckBox(self,type,Xcoor,Ycoor,width,length):
        global groupBox
        global scrollAreaGroupBox
        if type == "groupBox":
            self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        self.checkBox.setObjectName("checkBox")
        return self.checkBox

    def helpMenuListener(self, _):
        global helpMenuGroupBox
        global clickCount

        if (clickCount != 1):
            clickCount = clickCount + 1
            self.helpMenuGroupBox.show()
        else:
            self.helpMenuGroupBox.hide()
            clickCount = 0

    def showWindow(self, _):
        self.window.show()

    def createScrollAreaObject(self,Ycoor,attraction):
        global scrollAreaGroupBox
        _translate = QtCore.QCoreApplication.translate

        self.scrollAreaGroupBox = QtWidgets.QGroupBox(self.widget)
        self.scrollAreaGroupBox.setFixedSize(884, 220)
        self.scrollAreaGroupBox.setLayout(QtWidgets.QVBoxLayout())

        labelXPos = 230
        labelYPos = 25
        self.attractionTitle = self.createLabel("scrollAreaGroupBox", labelXPos, 0, 400, 50)
        self.ratingLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 420, 0, 50, 50)
        self.locationLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos - 8, 200, 50)
        # self.dateLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 20, 200, 50)
        self.typeLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 20, 200, 50)
        self.priceLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 40, 200, 50)
        self.busynessLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 60, 200, 50)

        self.wheelChairAccessibilityLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 150, labelYPos + 20, 200, 50)
        self.familyFriendlyLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 150, labelYPos + 40, 200, 50)
        self.petFriendlyLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 150, labelYPos + 60, 200, 50)

        self.descriptionLabel = self.createLabel("scrollAreaGroupBox",labelXPos, labelYPos + 80, 460, 130)
        self.descriptionLabel.setWordWrap(True)

        self.attractionMapLabel = QtWidgets.QLabel(self.scrollAreaGroupBox)
        self.attractionMapLabel.setPixmap(QtGui.QPixmap("attractionImage.jpg"))
        self.attractionMapLabel.setScaledContents(True)
        self.attractionMapLabel.setFixedSize(220, 220)
        self.attractionMapLabel.show()

        # self.googleMapLabel = QtWidgets.QLabel(self.scrollAreaGroupBox)
        # self.googleMapLabel.setPixmap(QtGui.QPixmap("googleMap.jpg"))
        # self.googleMapLabel.setScaledContents(True)
        # self.googleMapLabel.setFixedSize(190, 190)
        # self.googleMapLabel.move(700, 0)
        # self.googleMapLabel.show()

        self.mapBox = QtWidgets.QGroupBox(self.scrollAreaGroupBox)
        self.mapBox.setGeometry(QtCore.QRect(675, -10, 220, 220))
        self.mapBox.setEnabled(True)
        self.mapBox.setFlat(True)
        self.mapHolder = QtWidgets.QVBoxLayout(self.mapBox)
        coordinate = (34.71137031,-86.65391484)
        map = folium.Map(
            zoom_start=15,
            location=coordinate
        )
        folium.Marker(
            location=coordinate
        ).add_to(map)
        # save map data to data object
        data = io.BytesIO()
        map.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.mapHolder.addWidget(webView)
        self.expandMapButton = QtWidgets.QToolButton(self.scrollAreaGroupBox)
        self.expandMapButton.setGeometry(690, 198, 94, 17)
        self.expandMapButton.setText(_translate("MainWindow", "Expand Map ↗︎"))
        # self.expandedMapWindow = QtWidgets.QMainWindow()
        # self.ui = Ui_expandedMapWindow()
        # self.ui.setupUi(self.expandedMapWindow)
        self.window = QtWidgets.QLabel()
        self.window.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.window)
        self.centralwidget.setFixedSize(800, 600)
        self.centralwidget.setObjectName("centralwidget")
        self.expandedMapBox = QtWidgets.QGroupBox(self.centralwidget)
        self.expandedMapBox.setFixedSize(820, 610)
        self.expandedMapBox.move(-10, 0)
        self.expandedMapBox.setEnabled(True)
        self.expandedMapBox.setFlat(True)
        self.mapHolder = QtWidgets.QVBoxLayout(self.expandedMapBox)

        coordinate = (34.71137031, -86.65391484)
        expandedMap = folium.Map(
            zoom_start=14,
            location=coordinate,
            popup="test"
        )
        folium.Marker(
            location=coordinate
        ).add_to(expandedMap)
        # save map data to data object
        data = io.BytesIO()
        expandedMap.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.mapHolder.addWidget(webView)
        self.expandMapButton.clicked.connect(self.showWindow)
        self.googleMapsButton = QtWidgets.QToolButton(self.scrollAreaGroupBox)
        self.googleMapsButton.setGeometry(786, 198, 94, 17)
        self.googleMapsButton.setText(_translate("MainWindow", "Website ↗︎"))
        self.googleMapsButton.clicked.connect(lambda: webbrowser.open(str(attraction[13])))

        self.line = QtWidgets.QFrame(self.scrollAreaGroupBox)
        self.line.setGeometry(QtCore.QRect(280, 125, 350, 10))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.attractionTitle.setText(_translate("MainWindow", (str(attraction[1]) + "  - (Est. " + (str(attraction[2])) + ")")))
        self.ratingLabel.setText(_translate("MainWindow", (str(attraction[9]))))
        self.locationLabel.setText(_translate("MainWindow", (str(attraction[5]) + ",  " + str(attraction[4]))))
        # self.dateLabel.setText(_translate("MainWindow", (str(attraction[2]))))
        self.typeLabel.setText(_translate("MainWindow", (str(attraction[6]))))
        if (str(attraction[7])) == '1':
            self.priceLabel.setText(_translate("MainWindow", "Price Level - $"))
        elif (str(attraction[7])) == '2':
            self.priceLabel.setText(_translate("MainWindow", "Price Level - $$"))
        elif (str(attraction[7])) == '3':
            self.priceLabel.setText(_translate("MainWindow", "Price Level - $$$"))
        if (str(attraction[8])) == '1':
            self.busynessLabel.setText(_translate("MainWindow", "Low Busyness"))
        elif (str(attraction[8])) == '2':
            self.busynessLabel.setText(_translate("MainWindow", "Moderately Busy"))
        elif (str(attraction[8])) == '3':
            self.busynessLabel.setText(_translate("MainWindow", "Very Busy"))
        if ((attraction[10])):
            self.wheelChairAccessibilityLabel.setText(_translate("MainWindow", "WheelChair Accessible? - Yes"))
        else:
            self.wheelChairAccessibilityLabel.setText(_translate("MainWindow", "WheelChair Accessible? - No"))
        if ((attraction[11])):
            self.familyFriendlyLabel.setText(_translate("MainWindow", "Family Friendly? - Yes"))
        else:
            self.familyFriendlyLabel.setText(_translate("MainWindow", "Family Friendly? - No"))
        if ((attraction[12])):
            self.petFriendlyLabel.setText(_translate("MainWindow", "Pet Friendly? - Yes"))
        else:
            self.petFriendlyLabel.setText(_translate("MainWindow", "Pet Friendly? - No"))
        self.descriptionLabel.setText(_translate("MainWindow", ("     " + str(attraction[3]))))
        self.verticalLayout_3.addWidget(self.scrollAreaGroupBox)
        return self.scrollAreaGroupBox

    def controlScrollArea(self):
        global filteredAttractionsList
        # Removes any previously displayed result objects
        if (len(self.scrollAreaWidgetContainer.children()) > 0):
            scrollAreaWidgetList = self.scrollAreaWidgetContainer.children()
            for i in reversed(range(len(self.scrollAreaWidgetContainer.children()))):
                if i > 0:
                    scrollAreaWidgetList[i].deleteLater()
        # Adds all filtered result objects to the scrollArea
        Ycoor = 0
        for index in range(len(filteredAttractionsList)):
            self.createScrollAreaObject(Ycoor,filteredAttractionsList[index])
            Ycoor = Ycoor + 200
        self.scrollArea.setWidget(self.scrollAreaWidgetContainer)

    def getCurrentFieldValues(self, _):
        global filteredAttractionsList
        global groupBox
        _translate = QtCore.QCoreApplication.translate
        currentSelectedState = self.stateFilterComboBox.currentText()
        currentSelectedCity = self.cityFilterComboBox.currentText()
        currentSelectedType = self.typeFilterComboBox.currentText()
        currentCheckedWheelchairAccessibility = self.wheelchairAccessFilterCheckBox.isChecked()
        currentCheckedFamilyFriendliness = self.familyFriendlyFilterCheckBox.isChecked()
        currentCheckedPetFriendliness = self.petFriendlyFilterCheckBox.isChecked()
        currentSorter = self.sortingComboBox.currentText()
        attributeList = [str(currentSelectedState),str(currentSelectedCity),str(currentSelectedType),
                         str(currentCheckedWheelchairAccessibility), str(currentCheckedFamilyFriendliness),
                         str(currentCheckedPetFriendliness)]
        for index in range(len(attributeList)):
            if (attributeList[index] == "None" or attributeList[index] == "False"):
                attributeList[index] = None
        filteredAttractions = ApplicationDatabase.getAttractions(filters=ApplicationFilterRequest.FilterRequest(attributeList[0], attributeList[1], attributeList[2], attributeList[3], attributeList[4], attributeList[5]))
        filteredAttractionsList = filteredAttractions
        if (len(filteredAttractionsList)) == 1:
            self.numOfAttractionsLabel.setText(_translate("MainWindow", (str(len(filteredAttractionsList))) + " Attraction Found"))
        else:
            self.numOfAttractionsLabel.setText(_translate("MainWindow",(str(len(filteredAttractionsList))) + " Attractions Found"))
        self.sortingAttractions()
        print(*filteredAttractionsList, sep="\n")
        self.controlScrollArea()
        attributeList = [None, None, None, None, None, None]

        with open('output_report.txt', 'w') as f:
            f.write("Selected State?:")
            f.write(currentSelectedState)
            f.write("| Selected City?:")
            f.write(currentSelectedCity)
            f.write("| Selected Type?:")
            f.write(currentSelectedType)
            f.write("| Wheelchair Accessibility is Checked?:")
            f.write(str(currentCheckedWheelchairAccessibility))
            f.write("| Family Friendliness is Checked?:")
            f.write(str(currentCheckedFamilyFriendliness))
            f.write("| Pet Friendliness is Checked?:")
            f.write(str(currentCheckedPetFriendliness))
            f.write("| Currently sorting by:")
            f.write(currentSorter)
            for element in filteredAttractionsList:
                f.write(str(element))
                f.write("\n")

    def sortingAttractions(self):
        if self.sortingComboBox.currentText() == "Rating: lowest to highest":
            filteredAttractionsList.sort(key=itemgetter(9), reverse=False)
        if self.sortingComboBox.currentText() == "Rating: highest to lowest":
            filteredAttractionsList.sort(key=itemgetter(9), reverse=True)
        if self.sortingComboBox.currentText() == "Price: lowest to highest":
            filteredAttractionsList.sort(key=itemgetter(7), reverse=False)
        if self.sortingComboBox.currentText() == "Price: highest to lowest":
            filteredAttractionsList.sort(key=itemgetter(7), reverse=True)
        if self.sortingComboBox.currentText() == "Traffic: lowest to highest":
            filteredAttractionsList.sort(key=itemgetter(8), reverse=False)
        if self.sortingComboBox.currentText() == "Traffic: highest to lowest":
            filteredAttractionsList.sort(key=itemgetter(8), reverse=True)

    def setupUi(self, MainWindow):
        global clickCount
        global groupBox
        global topGroupBoxBar
        _translate = QtCore.QCoreApplication.translate
        # Sets up the window container
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1150, 645)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1151, 626))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.gridWidget = QtWidgets.QWidget(self.tabWidgetPage1)
        self.gridWidget.setGeometry(QtCore.QRect(880, 0, 251, 49))
        self.gridWidget.setObjectName("gridWidget")
        self.line = QtWidgets.QFrame(self.tabWidgetPage1)
        self.line.setGeometry(QtCore.QRect(210, -10, 21, 611))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget = QtWidgets.QWidget(self.tabWidgetPage1)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1151, 601))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setEnabled(True)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")

        # Filtering by State - Format: (Label : ComboBox)
        self.stateFilterLabel = self.createLabel("groupBox",5, 75, 50, 50)
        self.stateFilterComboBox = self.createComboBox("groupBox",40, 90, 157, 26)
        self.stateFilterComboBox.addItem("None", ["None"])
        self.stateFilterComboBox.addItem("Alabama", ["None", "Huntsville", "Birmingham", "Montgomery", "Mobile", "Tuscaloosa"])
        self.stateFilterComboBox.addItem("Alaska", ["None", "Anchorage", "Juneau", "Fairbanks", "Badger", "Knik-Fairview"])
        self.stateFilterComboBox.addItem("Arizona")
        self.stateFilterComboBox.addItem("Arkansas")
        self.stateFilterComboBox.addItem("California")
        self.stateFilterComboBox.addItem("Colorado")
        self.stateFilterComboBox.addItem("Connecticut")
        self.stateFilterComboBox.addItem("Delaware")
        self.stateFilterComboBox.addItem("Florida")
        self.stateFilterComboBox.addItem("Georgia")
        self.stateFilterComboBox.addItem("Hawaii")
        self.stateFilterComboBox.addItem("Idaho")
        self.stateFilterComboBox.addItem("Illinois")
        self.stateFilterComboBox.addItem("Indiana")
        self.stateFilterComboBox.addItem("Iowa")
        self.stateFilterComboBox.addItem("Kansas")
        self.stateFilterComboBox.addItem("Kentucky")
        self.stateFilterComboBox.addItem("Louisiana")
        self.stateFilterComboBox.addItem("Maine")
        self.stateFilterComboBox.addItem("Maryland")
        self.stateFilterComboBox.addItem("Massachusetts")
        self.stateFilterComboBox.addItem("Michigan")
        self.stateFilterComboBox.addItem("Minnesota")
        self.stateFilterComboBox.addItem("Mississippi")
        self.stateFilterComboBox.addItem("Missouri")
        self.stateFilterComboBox.addItem("Montana")
        self.stateFilterComboBox.addItem("Nebraska")
        self.stateFilterComboBox.addItem("Nevada")
        self.stateFilterComboBox.addItem("New Hampshire")
        self.stateFilterComboBox.addItem("New Jersey")
        self.stateFilterComboBox.addItem("New Mexico")
        self.stateFilterComboBox.addItem("New York")
        self.stateFilterComboBox.addItem("North Carolina")
        self.stateFilterComboBox.addItem("North Dakota")
        self.stateFilterComboBox.addItem("Ohio")
        self.stateFilterComboBox.addItem("Oklahoma")
        self.stateFilterComboBox.addItem("Oregon")
        self.stateFilterComboBox.addItem("Pennsylvania")
        self.stateFilterComboBox.addItem("Rhode Island")
        self.stateFilterComboBox.addItem("South Carolina")
        self.stateFilterComboBox.addItem("South Dakota")
        self.stateFilterComboBox.addItem("Tennessee")
        self.stateFilterComboBox.addItem("Texas")
        self.stateFilterComboBox.addItem("Utah")
        self.stateFilterComboBox.addItem("Vermont")
        self.stateFilterComboBox.addItem("Virginia")
        self.stateFilterComboBox.addItem("Washington")
        self.stateFilterComboBox.addItem("West Virginia")
        self.stateFilterComboBox.addItem("Wisconsin")
        self.stateFilterComboBox.addItem("Wyoming")
        self.stateFilterComboBox.activated.connect(self.selectCityFromState)
        self.stateFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by City - Format: (Label : ComboBox)
        self.cityFilterLabel = self.createLabel("groupBox", 5, 115, 50, 50)
        self.cityFilterComboBox = self.createComboBox("groupBox", 40, 130, 157, 26)
        self.cityFilterComboBox.addItems(["None"])
        self.cityFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by Type - Format: (Label : ComboBox)
        self.typeFilterLabel = self.createLabel("groupBox", 5, 155, 50, 50)
        self.typeFilterComboBox = self.createComboBox("groupBox", 40, 170, 157, 26)
        self.typeFilterComboBox.addItems(["None", "Sports", "Cultural/Historical"])
        self.typeFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by WheelChair Accessibility - Format: (CheckBox : Label)
        self.wheelchairAccessFilterLabel = self.createLabel("groupBox", 30, 195, 150, 50)
        self.wheelchairAccessFilterCheckBox = self.createCheckBox("groupBox", 5, 211, 20, 20)
        self.wheelchairAccessFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Filtering by Family Friendliness - Format: (CheckBox : Label)
        self.familyFriendlyFilterLabel = self.createLabel("groupBox", 30, 220, 150, 50)
        self.familyFriendlyFilterCheckBox = self.createCheckBox("groupBox", 5, 236, 20, 20)
        self.familyFriendlyFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Filtering by Pet Friendliness - Format: (CheckBox : Label)
        self.petFriendlyFilterLabel = self.createLabel("groupBox", 30, 245, 150, 50)
        self.petFriendlyFilterCheckBox = self.createCheckBox("groupBox", 5, 261, 20, 20)
        self.petFriendlyFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Adding a Dynamic Help Menu
        self.helpButton = QtWidgets.QToolButton(self.groupBox)
        self.helpButton.setGeometry(13,565,190,20)
        clickCount = 0
        self.helpMenuGroupBox = QtWidgets.QGroupBox(self.groupBox)
        self.helpMenuGroupBox.setGeometry(QtCore.QRect(13, 475, 190, 80))
        self.helpMenuGroupBox.hide()
        self.documentationButton = QtWidgets.QToolButton(self.helpMenuGroupBox)
        self.documentationButton.setGeometry(5, 5, 180, 20)
        self.supportButton = QtWidgets.QToolButton(self.helpMenuGroupBox)
        self.supportButton.setGeometry(5, 30, 180, 20)
        self.showToolDescriptionButton = QtWidgets.QToolButton(self.helpMenuGroupBox)
        self.showToolDescriptionButton.setGeometry(5, 55, 180, 20)
        self.documentationButton.setText(_translate("MainWindow", "Documentation"))
        self.supportButton.setText(_translate("MainWindow", "Support"))
        self.showToolDescriptionButton.setText(_translate("MainWindow", "Show Tool Descriptions"))
        self.helpButton.setText(_translate("MainWindow", "Help"))
        self.helpButton.clicked.connect(self.helpMenuListener)

        # Setting topGroupBoxBar and ScrollArea
        self.topGroupBoxBar = QtWidgets.QGroupBox(self.widget)
        self.topGroupBoxBar.setFixedSize(907, 40)
        self.topGroupBoxBar.move(230,10)
        self.topGroupBoxBar.setEnabled(True)
        self.topGroupBoxBar.setFlat(True)
        self.numOfAttractionsLabel = self.createLabel("topGroupBoxBar", 10, 20, 200, 20)
        self.sortingComboBoxLabel = self.createLabel("topGroupBoxBar", 653, 13, 50, 20)
        self.sortingComboBox = self.createComboBox("topGroupBoxBar", 700, 10, 200, 30)
        self.sortingComboBox.addItems(["Recommended (placeholder)",
                                  "Rating: lowest to highest",
                                  "Rating: highest to lowest",
                                  "Price: lowest to highest",
                                  "Price: highest to lowest",
                                  "Traffic: lowest to highest",
                                  "Traffic: highest to lowest"])
        self.sortingComboBox.activated.connect(self.getCurrentFieldValues)
        self.scrollAreaWidgetContainer = QtWidgets.QWidget()
        self.scrollAreaWidgetContainer.setObjectName("scrollAreaWidgetContainer")
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea = QtWidgets.QScrollArea(self.tabWidgetPage1)
        self.scrollArea.setFixedWidth(907)
        self.scrollArea.setMinimumHeight(531)
        self.scrollArea.move(230,50)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContainer)
        self.scrollAreaWidgetContainer.setLayout(self.verticalLayout_3)
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

    def selectCityFromState(self, index):
        self.cityFilterComboBox.clear()
        self.cityFilterComboBox.addItems(self.stateFilterComboBox.itemData(index))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.stateFilterLabel.setText(_translate("MainWindow", "State:"))
        self.cityFilterLabel.setText(_translate("MainWindow", "City:"))
        self.typeFilterLabel.setText(_translate("MainWindow", "Type:"))
        self.wheelchairAccessFilterLabel.setText(_translate("MainWindow", "Wheelchair Accessible"))
        self.familyFriendlyFilterLabel.setText(_translate("MainWindow", "Family Friendly"))
        self.petFriendlyFilterLabel.setText(_translate("MainWindow", "Pet Friendly"))
        self.sortingComboBoxLabel.setText(_translate("MainWindow", "Sort By:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("MainWindow", "Attractions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "About Us"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Sources"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('mac')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

