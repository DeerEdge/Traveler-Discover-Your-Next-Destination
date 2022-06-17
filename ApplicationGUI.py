import os
import webbrowser
import ApplicationDatabase
import ApplicationFilterRequest
import io
import folium

from ipregistry import IpregistryClient
from time import gmtime, strftime
from operator import itemgetter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from geopy import distance


client = IpregistryClient("72bw4jakulj27ism")
ipInfo = client.lookup()

# clear logs
def clearLog():
    with open("outputreport.txt", "r+") as f:
        f.seek(0)
        f.truncate()

class Ui_MainWindow(object):
    global currentAttraction
    global filteredAttractionsList
    global radiusChecked
    radiusChecked = False
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
        elif type == "sourcesTabWidget":
            self.label = QtWidgets.QLabel(self.sourcesTabWidget)
        elif type == "reportWindowGroupBox":
            self.label = QtWidgets.QLabel(self.reportWindow)
        elif type == "documentationWindowGroupBox":
            self.label = QtWidgets.QLabel(self.documentationWindow)
        elif type == "titleCentralWidget":
            self.label = QtWidgets.QLabel(self.titleCentralwidget)
        self.label.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        return self.label

    def createComboBox(self,type,Xcoor,Ycoor,width,length):
        global groupBox
        global scrollAreaGroupBox
        global topGroupBoxBar
        if type == "groupBox":
            self.comboBox = QtWidgets.QComboBox(self.groupBox)
        elif type == "topGroupBoxBar":
            self.comboBox = QtWidgets.QComboBox(self.topGroupBoxBar)
        elif type == "titleCentralWidget":
            self.comboBox = QtWidgets.QComboBox(self.titleCentralwidget)
        self.comboBox.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        return self.comboBox

    def createCheckBox(self,type,Xcoor,Ycoor,width,length):
        global groupBox
        global scrollAreaGroupBox
        if type == "groupBox":
            self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(Xcoor,Ycoor,width,length))
        return self.checkBox

    def createScrollAreaObject(self,Ycoor,attraction):
        global scrollAreaGroupBox
        _translate = QtCore.QCoreApplication.translate

        self.scrollAreaGroupBox = QtWidgets.QGroupBox(self.widget)
        self.scrollAreaGroupBox.setFixedSize(884, 220)
        self.scrollAreaGroupBox.setLayout(QtWidgets.QVBoxLayout())

        labelXPos = 230
        labelYPos = 25
        self.attractionTitle = self.createLabel("scrollAreaGroupBox", labelXPos, -5, 450, 50)
        self.attractionTitle.setObjectName("attractionName")
        self.attractionTitle.setText((str(attraction[1])))
        self.ratingLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 350, -5, 50, 50)
        self.ratingLabel.setObjectName("rating")
        self.ratingLabel.setText((str(attraction[8])))
        minStarRating = 5.0
        for i in range(10):
            if (float(attraction[8]) < minStarRating):
                minStarRating = minStarRating - 0.5
            else:
                self.ratingIcon = QtWidgets.QLabel(self.scrollAreaGroupBox)
                self.ratingIcon.setPixmap(QtGui.QPixmap("./Application Pictures/Star Ratings/" + str(minStarRating) + " star.png"))
                self.ratingIcon.setScaledContents(True)
                self.ratingIcon.setFixedSize(85, 16)
                self.ratingIcon.move(600, 12)
                self.ratingIcon.show()
                break
        if (self.latitudeInput.text() != "" and self.longitudeInput.text() != "" and self.isfloat(str(self.latitudeInput.text())) and self.isfloat(str(self.longitudeInput.text()))):
            self.locationLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos - 8, 250, 50)
            self.locationLabel.setObjectName("locationAndDistance")
            distanceFromUserLocation = distance.distance(((self.latitudeInput.text()), (self.longitudeInput.text())),(attraction[13], attraction[14])).miles
            self.locationLabel.setText((str(attraction[4]) + ", " + str(attraction[3])) + " - " + str('%.1f'%(distanceFromUserLocation)) + " miles away")
        else:
            self.locationLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos - 3, 200, 50)
            self.locationLabel.setObjectName("locationAndDistance")
            self.locationLabel.setText((str(attraction[4]) + ", " + str(attraction[3])))
        self.typeLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 20, 200, 50)
        self.typeLabel.setText((str(attraction[5])))
        self.priceLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 40, 200, 50)
        if (str(attraction[6])) == '1':
            self.priceLabel.setText("Price Level - $")
        elif (str(attraction[6])) == '2':
            self.priceLabel.setText("Price Level - $$")
        else:
            self.priceLabel.setText("Price Level - $$$")
        self.busynessLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 60, 200, 50)
        if (str(attraction[7])) == '1':
            self.busynessLabel.setText("Low Busyness")
        elif (str(attraction[7])) == '2':
            self.busynessLabel.setText("Moderately Busy")
        else:
            self.busynessLabel.setText("Very Busy")
        self.wheelChairAccessibilityLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 170, labelYPos + 20, 200, 50)
        if ((attraction[9])):
            self.wheelChairAccessibilityLabel.setText("Wheelchair Accessible? - Yes")
        else:
            self.wheelChairAccessibilityLabel.setText("Wheelchair Accessible? - No")
        self.familyFriendlyLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 170, labelYPos + 40, 200, 50)
        if ((attraction[10])):
            self.familyFriendlyLabel.setText("Family Friendly? - Yes")
        else:
            self.familyFriendlyLabel.setText("Family Friendly? - No")
        self.petFriendlyLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 170, labelYPos + 60, 200, 50)
        if ((attraction[11])):
            self.petFriendlyLabel.setText("Pet Friendly? - Yes")
        else:
            self.petFriendlyLabel.setText("Pet Friendly? - No")
        # if (self.latitudeInput.text() != "" and self.longitudeInput.text() != "" and self.isfloat(str(self.latitudeInput.text())) and self.isfloat(str(self.longitudeInput.text()))):
        #     distanceFromUserLocation = distance.distance(((self.latitudeInput.text()), (self.longitudeInput.text())),(attraction[14], attraction[15])).miles
        #     self.distanceLabel = self.createLabel("scrollAreaGroupBox", labelXPos + 310, labelYPos + 40, 200, 50)
        #     self.distanceLabel.setText(str('%.1f'%(distanceFromUserLocation)) + " miles from you")
        #     self.distanceLabel.setObjectName("Distance")
        self.coordinateLocationLabel = self.createLabel("scrollAreaGroupBox", labelXPos, labelYPos + 80, 200, 50)
        self.coordinateLocationLabel.setText("Location: (" + str('%.3f'%(attraction[13])) + "," + str('%.3f'%(attraction[14])) + ")")
        self.coordinateInfoLabel = self.createLabel("scrollAreaGroupBox", 0, 0, 200, 50)
        self.coordinateInfoLabel.setText(str('%.6f'%(attraction[14])) + "," + str('%.6f'%(attraction[13])))
        self.coordinateInfoLabel.setObjectName("Location")
        self.coordinateInfoLabel.hide()
        self.descriptionLabel = self.createLabel("scrollAreaGroupBox",labelXPos, labelYPos + 93, 454, 125)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setText(("     " + str(attraction[2])))

        self.attractionImage = QtWidgets.QLabel(self.scrollAreaGroupBox)
        imageAddress = "./Attraction Pictures/" + str(attraction[0]) + " - " + str(attraction[4]) + ".jpg"
        self.attractionImage.setPixmap(QtGui.QPixmap(imageAddress))
        self.attractionImage.setScaledContents(True)
        self.attractionImage.setFixedSize(220, 220)
        self.attractionImage.show()

        self.mapBox = QtWidgets.QGroupBox(self.scrollAreaGroupBox)
        self.mapBox.setGeometry(QtCore.QRect(675, -10, 220, 220))
        self.mapBox.setEnabled(True)
        self.mapBox.setFlat(True)
        self.mapHolder = QtWidgets.QVBoxLayout(self.mapBox)
        coordinate = (attraction[13],attraction[14])
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
        self.expandMapButton.setText("Expand Map ↗︎")
        self.expandMapButton.clicked.connect(self.showExpandedMapViewWindow)

        self.expandMapButton.clicked.connect(self.showExpandedMapViewWindow)
        self.googleMapsButton = QtWidgets.QToolButton(self.scrollAreaGroupBox)
        self.googleMapsButton.setGeometry(786, 198, 94, 17)
        self.googleMapsButton.setText(_translate("MainWindow", "Website ↗︎"))
        self.googleMapsButton.clicked.connect(lambda: webbrowser.open(str(attraction[12])))

        self.line = QtWidgets.QFrame(self.scrollAreaGroupBox)
        self.line.setGeometry(QtCore.QRect(235, 138, 440, 10))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
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
        allAttractions = ApplicationDatabase.getAttractions(filters=ApplicationFilterRequest.FilterRequest(None, None, None, None, None, None))
        filteredAttractions = ApplicationDatabase.getAttractions(filters=ApplicationFilterRequest.FilterRequest(attributeList[0], attributeList[1], attributeList[2], attributeList[3], attributeList[4], attributeList[5]))
        filteredAttractionsList = filteredAttractions
        if (len(filteredAttractionsList)) == 1:
            self.numOfAttractionsLabel.setText(_translate("MainWindow", (str(len(filteredAttractionsList))) + " Attraction Found"))
        else:
            self.numOfAttractionsLabel.setText(_translate("MainWindow",(str(len(filteredAttractionsList))) + " Attractions Found"))
        self.sortingAttractions()
        self.controlScrollArea()
        if (self.radiusComboBox.isEnabled()):
            global radiusChecked
            radiusChecked = True
            if (self.radiusComboBox.currentText() != "Any distance"):
                countOfObjectsShown = len(self.scrollAreaWidgetContainer.children()) - 1
                for index in range(len(self.scrollAreaWidgetContainer.children())):
                    if index != 0:
                        objectDistanceLabel = self.scrollAreaWidgetContainer.children()[index].findChild(QtWidgets.QLabel,
                                                                                                         'locationAndDistance').text()
                        indexOfLetterM = objectDistanceLabel.index("miles")
                        indexOfHyphen = objectDistanceLabel.index("-")
                        if (float(objectDistanceLabel[(indexOfHyphen + 1):(indexOfLetterM - 1)]) < float(self.radiusComboBox.currentText()[10:12])):
                            self.scrollAreaWidgetContainer.children()[index].show()
                        else:
                            self.scrollAreaWidgetContainer.children()[index].hide()
                            countOfObjectsShown = countOfObjectsShown - 1
                if (countOfObjectsShown) == 1:
                    self.numOfAttractionsLabel.setText((str(countOfObjectsShown)) + " Attraction Found")
                else:
                    self.numOfAttractionsLabel.setText((str(countOfObjectsShown)) + " Attractions Found")
        attributeList = [None, None, None, None, None, None]

        with open('outputreport.txt', 'a') as f:
            stringAccessedTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            locationOfSpace = stringAccessedTime.index(" ")
            f.write("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
            f.write("Activity Logged Date: " +  stringAccessedTime[:locationOfSpace] + " Time Of Action: " + stringAccessedTime[(locationOfSpace+1):])
            f.write("\n")
            f.write("Selected State: ")
            f.write(currentSelectedState)
            f.write("\n")
            f.write("Selected City: ")
            f.write(currentSelectedCity)
            f.write("\n")
            f.write("Selected Type: ")
            f.write(currentSelectedType)
            f.write("\n")
            f.write("Wheelchair Accessibility is Checked: ")
            f.write(str(currentCheckedWheelchairAccessibility))
            f.write("\n")
            f.write("Family Friendliness is Checked: ")
            f.write(str(currentCheckedFamilyFriendliness))
            f.write("\n")
            f.write("Pet Friendliness is Checked: ")
            f.write(str(currentCheckedPetFriendliness))
            f.write("\n")
            f.write("Currently sorting by: ")
            f.write(currentSorter)
            f.write("\n")
            for element in filteredAttractionsList:
                f.write("Filtered Attraction: " + "(id: " + str(element[0]) + ")" + ", " +
                        str(element[1]) + ", " + str(element[5]) + ", " + str(element[4]) + ", " + str(element[2]))
                f.write("\n")
            f.close()

        # Used to create a file with all sources. Run only once and then comment out
        # with open('sources.txt', 'w') as f:
        #     for attraction in allAttractions:
        #         f.write(" ")
        #         f.write(str(attraction[1]) + ", " + str(attraction[5]) + ", " + str(attraction[4]) + ", " + str(attraction[2]))
        #         f.write("\n")
        #         f.write(" ")
        #         f.write(str(attraction[13]))
        #         f.write("\n")
        #         f.write("\n")

    def sortingAttractions(self):
        def findDistanceToInput(data):
            return distance.distance(((self.latitudeInput.text()), (self.longitudeInput.text())),(data[13], data[14])).miles

        if self.sortingComboBox.currentText() == "Nearest attractions":
            filteredAttractionsList.sort(key=findDistanceToInput)
        if self.sortingComboBox.currentText() == "Rating: Lowest to Highest":
            filteredAttractionsList.sort(key=itemgetter(8), reverse=False)
        if self.sortingComboBox.currentText() == "Rating: Highest to Lowest":
            filteredAttractionsList.sort(key=itemgetter(8), reverse=True)
        if self.sortingComboBox.currentText() == "Price: Lowest to Highest":
            filteredAttractionsList.sort(key=itemgetter(6), reverse=False)
        if self.sortingComboBox.currentText() == "Price: Highest to Lowest":
            filteredAttractionsList.sort(key=itemgetter(6), reverse=True)
        if self.sortingComboBox.currentText() == "Traffic: Lowest to Highest":
            filteredAttractionsList.sort(key=itemgetter(7), reverse=False)
        if self.sortingComboBox.currentText() == "Traffic: Highest to Lowest":
            filteredAttractionsList.sort(key=itemgetter(7), reverse=True)

    def detectChangeInRadius(self, _):
        global radiusChecked
        if (radiusChecked):
            countOfObjectsShown = len(self.scrollAreaWidgetContainer.children()) - 1
            if (self.radiusComboBox.isEnabled()):
                for index in range(len(self.scrollAreaWidgetContainer.children())):
                    if index != 0:
                        objectDistanceLabel = self.scrollAreaWidgetContainer.children()[index].findChild(QtWidgets.QLabel, 'locationAndDistance').text()

                        indexOfLetterM = objectDistanceLabel.index("m")
                        indexOfHyphen = objectDistanceLabel.index("-")
                        if (self.radiusComboBox.currentText() != "Any distance"):
                            if (float(objectDistanceLabel[(indexOfHyphen + 1):(indexOfLetterM - 1)]) < float(self.radiusComboBox.currentText()[10:12])):
                                self.scrollAreaWidgetContainer.children()[index].show()
                            else:
                                self.scrollAreaWidgetContainer.children()[index].hide()
                                countOfObjectsShown = countOfObjectsShown - 1
                        else:
                            self.scrollAreaWidgetContainer.children()[index].show()
                if (countOfObjectsShown) == 1:
                    self.numOfAttractionsLabel.setText((str(countOfObjectsShown)) + " Attraction Found")
                else:
                    self.numOfAttractionsLabel.setText((str(countOfObjectsShown)) + " Attractions Found")

    def checkIfLocationIsFilled(self, _):
        if (self.latitudeInput.text() != "" and self.longitudeInput.text() != "" and self.isfloat(str(self.latitudeInput.text())) and self.isfloat(str(self.longitudeInput.text()))):
            self.radiusComboBox.setEnabled(True)
            self.showLocationMapButton.setEnabled((True))
        else:
            self.radiusComboBox.setEnabled(False)
            self.showLocationMapButton.setEnabled((False))

    def getCurrentLocation(self, _):
        self.latitudeInput.setText(str(ipInfo.__getattr__("location")["latitude"]))
        self.longitudeInput.setText(str(ipInfo.__getattr__("location")["longitude"]))
        self.checkIfLocationIsFilled
        self.currentLocationLabel.setText(str(ipInfo.__getattr__("location")["city"]) + ", " + str(ipInfo.__getattr__("location")["region"]["name"]))

    def helpMenuListener(self, _):
        global helpMenuGroupBox
        global clickCount

        if (clickCount != 1):
            clickCount = clickCount + 1
            self.helpMenuGroupBox.show()
        else:
            self.helpMenuGroupBox.hide()
            clickCount = 0

    def showDocumentation(self, _):
        self.documentationWindow = QtWidgets.QLabel()
        self.documentationWindow.setFixedSize(800, 600)
        self.documentationWindow.setWindowTitle("Read Documentation")
        self.documentationWindowCentralwidget = QtWidgets.QWidget(self.documentationWindow)
        self.documentationWindowCentralwidget.setFixedSize(800, 600)
        self.documentationWindowGroupBox = QtWidgets.QGroupBox(self.documentationWindowCentralwidget)
        self.documentationWindowGroupBox.setFixedSize(800, 600)
        self.documentationWindowGroupBox.setEnabled(True)
        self.documentationWindowGroupBox.setFlat(True)
        self.documentationLabel = self.createLabel("documentationWindowGroupBox", 8, 0, 200, 50)
        self.documentationLabel.setText("Documentation:")
        self.documentation = QtWidgets.QPlainTextEdit(self.documentationWindowGroupBox)
        self.documentation.setFixedSize(784, 550)
        self.documentation.move(8, 35)
        text = open('documentation.txt').read()
        self.documentation.setPlainText(text)
        self.documentation.setReadOnly(True)
        self.documentationWindow.show()

    def showDescriptions(self, _):
        self.latitudeInput.setToolTip("Enter a latitudinal location here \n"
                                      "or select the find my location \n"
                                      "button to autofill these fields \n"
                                      "with your current latitudinal \n"
                                      "location. If both the latitude \n"
                                      "and longitude fields are entered \n"
                                      "correctly (in the form of integers), \n"
                                      "you will be able to enter the desired \n"
                                      "radius of distance away that an \n"
                                      "attraction should be.")
        self.longitudeInput.setToolTip("Enter a longitudinal location here \n"
                                      "or select the find my location \n"
                                      "button to autofill these fields \n"
                                      "with your current longitudinal \n"
                                      "location." "If both the latitude \n"
                                      "and longitude fields are entered \n"
                                      "correctly (in the form of integers), \n"
                                      "you will be able to enter the desired \n"
                                      "radius of distance away that an \n"
                                      "attraction should be.")

    def showLocationMap(self, _):
        if (self.latitudeInput.text() != "" and self.longitudeInput.text() != "" and self.isfloat(str(self.latitudeInput.text())) and self.isfloat(str(self.longitudeInput.text()))):
            self.window = QtWidgets.QLabel()
            self.window.setFixedSize(800, 600)
            self.window.setWindowTitle("Entered Location Map")
            self.centralwidget = QtWidgets.QWidget(self.window)
            self.centralwidget.setFixedSize(800, 600)
            self.centralwidget.setObjectName("centralwidget")
            self.expandedMapBox = QtWidgets.QGroupBox(self.centralwidget)
            self.expandedMapBox.setFixedSize(820, 610)
            self.expandedMapBox.move(-10, 0)
            self.expandedMapBox.setEnabled(True)
            self.expandedMapBox.setFlat(True)
            self.mapHolder = QtWidgets.QVBoxLayout(self.expandedMapBox)
            coordinate = (float(self.latitudeInput.text()), float(self.longitudeInput.text()))
            expandedMap = folium.Map(
                zoom_start=15,
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
            self.window.show()

    def showExpandedMapViewWindow(self, _):
        self.window = QtWidgets.QLabel()
        self.window.setFixedSize(800, 600)
        self.window.setWindowTitle("Expanded Map View")
        self.centralwidget = QtWidgets.QWidget(self.window)
        self.centralwidget.setFixedSize(800, 600)
        self.centralwidget.setObjectName("centralwidget")
        self.expandedMapBox = QtWidgets.QGroupBox(self.centralwidget)
        self.expandedMapBox.setFixedSize(820, 610)
        self.expandedMapBox.move(-10, 0)
        self.expandedMapBox.setEnabled(True)
        self.expandedMapBox.setFlat(True)
        self.mapHolder = QtWidgets.QVBoxLayout(self.expandedMapBox)
        objectCoordinate = self.scrollAreaGroupBox.sender().parent().findChild(QtWidgets.QLabel,'Location').text()
        indexOfComma = objectCoordinate.index(",")
        long = float(objectCoordinate[:indexOfComma])
        lat = float(objectCoordinate[(indexOfComma + 1):])
        coordinate = (lat,long)
        expandedMap = folium.Map(
            zoom_start=15,
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
        self.window.show()

    def searchResults(self, _):
        _translate = QtCore.QCoreApplication.translate
        countOfObjectsShown = len(self.scrollAreaWidgetContainer.children()) - 1
        for index in range(len(self.scrollAreaWidgetContainer.children())):
            if index != 0:
                if (self.searchBar.text().lower() in self.scrollAreaWidgetContainer.children()[index].findChild(QtWidgets.QLabel,'attractionName').text().lower()):
                    self.scrollAreaWidgetContainer.children()[index].show()
                else:
                    self.scrollAreaWidgetContainer.children()[index].hide()
                    countOfObjectsShown = countOfObjectsShown - 1
        if (countOfObjectsShown) == 1:
            self.numOfAttractionsLabel.setText(
                _translate("MainWindow", (str(countOfObjectsShown)) + " Attraction Found"))
        else:
            self.numOfAttractionsLabel.setText(
                _translate("MainWindow", (str(countOfObjectsShown)) + " Attractions Found"))

    def clearSearch(self, _):
        self.searchBar.setText("")
        for index in range(len(self.scrollAreaWidgetContainer.children())):
            if index != 0:
                self.scrollAreaWidgetContainer.children()[index].show()
                if len(self.scrollAreaWidgetContainer.children()) == 2:
                    self.numOfAttractionsLabel.setText((str(len(self.scrollAreaWidgetContainer.children()) - 1) + " Attraction Found"))
                else:
                    self.numOfAttractionsLabel.setText((str(len(self.scrollAreaWidgetContainer.children()) - 1) + " Attractions Found"))

    def createUserReportFile(self, _):
        path = "./User Reports"
        directory = os.listdir(path)
        if len(directory) == 0:
            fileName = 'User Report 1'
            fileLocation = os.path.join(path,fileName)
            with open(fileLocation, 'w') as f:
                f.write("User Information: " + "Full Name - " + self.nameField.text() + "Email - " + self.emailField.text())
                f.write("\n")
                f.write(self.reportTopicField.text())
                f.write("\n")
                f.write(self.userReportField.toPlainText())
                f.write("\n")
                f.write(self.outputLogs.toPlainText())
                f.close()
        else:
            fileName = ('User Report ' + (str(len(directory) + 1)))
            fileLocation = os.path.join(path, fileName)
            with open(fileLocation, 'w') as f:
                f.write("User Information: " + "Full Name - " + self.nameField.text() + "Email - " + self.emailField.text())
                f.write("\n")
                f.write(self.reportTopicField.text())
                f.write("\n")
                f.write(self.userReportField.toPlainText())
                f.write("\n")
                f.write(self.outputLogs.toPlainText())
                f.close()
        self.reportWindow.close()

    def createReport(self, _):
        self.reportWindow = QtWidgets.QLabel()
        self.reportWindow.setFixedSize(800, 600)
        self.reportWindow.setWindowTitle("Create a Report")
        self.reportWindowCentralwidget = QtWidgets.QWidget(self.reportWindow)
        self.reportWindowCentralwidget.setFixedSize(800, 600)
        self.reportWindowGroupBox = QtWidgets.QGroupBox(self.reportWindowCentralwidget)
        self.reportWindowGroupBox.setFixedSize(800, 600)
        self.reportWindowGroupBox.setEnabled(True)
        self.reportWindowGroupBox.setFlat(True)
        self.outputLogLabel = self.createLabel("reportWindowGroupBox", 8, 0, 200, 50)
        self.outputLogLabel.setText("Output Report:")
        self.outputLogs = QtWidgets.QPlainTextEdit(self.reportWindowGroupBox)
        self.outputLogs.setFixedSize(784, 250)
        self.outputLogs.move(8, 35)
        text = open('outputreport.txt').read()
        self.outputLogs.setPlainText(text)
        self.outputLogs.setReadOnly(True)
        self.nameLabel = self.createLabel("reportWindowGroupBox", 8, 275, 200, 50)
        self.nameLabel.setText("Full Name:")
        self.nameField = QtWidgets.QLineEdit(self.reportWindowGroupBox)
        self.nameField.setFixedSize(387, 25)
        self.nameField.move(8, 310)
        self.nameField.setPlaceholderText(" Enter your full name here")
        # self.nameField.selectionChanged.connect(lambda: self.nameField.setSelection(0, 0))
        self.emailLabel = self.createLabel("reportWindowGroupBox", 404, 275, 200, 50)
        self.emailLabel.setText("Email Address:")
        self.emailField = QtWidgets.QLineEdit(self.reportWindowGroupBox)
        self.emailField.setFixedSize(387, 25)
        self.emailField.move(404, 310)
        self.emailField.setPlaceholderText(" Enter your email address here")
        # self.emailField.selectionChanged.connect(lambda: self.emailField.setSelection(0, 0))
        self.reportTopicLabel = self.createLabel("reportWindowGroupBox", 8, 325, 200, 50)
        self.reportTopicLabel.setText("Title:")
        self.reportTopicField = QtWidgets.QLineEdit(self.reportWindowGroupBox)
        self.reportTopicField.setFixedSize(784, 25)
        self.reportTopicField.move(8, 360)
        self.reportTopicField.setPlaceholderText(" Provide a short title for the issue/report")
        # self.reportTopicField.selectionChanged.connect(lambda: self.reportTopicField.setSelection(0, 0))
        self.userReportLabel = self.createLabel("reportWindowGroupBox", 8, 375, 200, 50)
        self.userReportLabel.setText("Description:")
        self.userReportField = QtWidgets.QPlainTextEdit(self.reportWindowGroupBox)
        self.userReportField.setFixedSize(784, 160)
        self.userReportField.move(8, 410)
        self.userReportField.setPlaceholderText("Provide a detailed description of the problem you are facing. "
                                           " Include any actions made prior to the issue arising and the  resulting erroneous output. "
                                           " If the report is created to inform of incorrect data, provide the attraction name and details about the data.")
        self.submitButton = QtWidgets.QToolButton(self.reportWindowGroupBox)
        self.submitButton.setGeometry(640, 575, 150, 20)
        self.submitButton.setText("Submit")
        self.submitButton.clicked.connect(self.createUserReportFile)
        self.reportWindow.show()

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def titleInputDependencies(self, _):
        if (self.titleStateInput.currentText() != "Select a State"):
            self.titleCityInput.setEnabled(True)
            if (self.titleCityInput.currentText() != "Select a City"):
                self.titleTypeInput.setEnabled(True)
                self.windowChangeButton.setEnabled(True)
            else:
                self.titleTypeInput.setEnabled(False)
                self.titleTypeInput.setCurrentText("Select a Type")
                self.windowChangeButton.setEnabled(False)
        else:
            self.titleCityInput.setEnabled(False)
            self.titleTypeInput.setCurrentText("Select a Type")
            self.titleCityInput.setCurrentText("Select a City")

    def changeWindow(self, _):
        titleSelectedState = self.titleStateInput.currentText()
        titleSelectedCity = self.titleCityInput.currentText()
        titleSelectedType = self.titleTypeInput.currentText()
        titleSearchInput = self.titleSearchBar.text()
        self.titleCentralwidget.deleteLater()
        ui.setupUi(MainWindow)
        self.getCurrentLocation(_)
        self.stateFilterComboBox.setCurrentText(titleSelectedState)
        self.cityFilterComboBox.addItems(
        self.stateFilterComboBox.itemData(self.stateFilterComboBox.findText(titleSelectedState)))
        self.cityFilterComboBox.setCurrentText(titleSelectedCity)
        self.typeFilterComboBox.setCurrentText(titleSelectedType)
        self.searchBar.setText(titleSearchInput)
        self.getCurrentFieldValues(_)
        self.searchResults(_)

    def changeToExploreTab(self, _):
        self.titleCentralwidget.deleteLater()
        ui.setupUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)

    def changeToSourcesTab(self, _):
        self.titleCentralwidget.deleteLater()
        ui.setupUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)

    def setupTitle(self, MainWindow):
        MainWindow.setWindowTitle("Traveler")
        MainWindow.setFixedSize(1150, 645)
        self.titleCentralwidget = QtWidgets.QWidget(MainWindow)
        self.titleCentralwidget.setFixedSize(1150, 645)
        self.titleWindowPicture = QtWidgets.QLabel(self.titleCentralwidget)
        self.titleWindowPicture.setFixedSize(1150,645)
        self.titleWindowPicture.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowPicture.jpeg"))
        self.titleWindowPicture.setScaledContents(True)
        self.titleWindowPicture.show()
        self.titleWindowLogo = QtWidgets.QLabel(self.titleCentralwidget)
        self.titleWindowLogo.setFixedSize(500, 500)
        self.titleWindowLogo.move(310,50)
        self.titleWindowLogo.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowLogo.png"))
        self.titleWindowLogo.setScaledContents(True)
        self.titleWindowLogo.show()
        self.titleStateInput = self.createComboBox("titleCentralWidget", 150, 250, 150, 50)
        self.titleStateInput.setStyleSheet("QComboBox"
                                           "{"
                                           "color: white;"
                                            "border: 3px solid;" 
                                           "border-color: rgb(245, 245, 245);"
                                           "background-color: rgba(20, 52, 124, 170);"
                                           "}"
                                           "QComboBox QAbstractItemView {" 
                                           "background-color: rgb(140, 140, 140);"
                                           "color: white;"
                                           "width: 200px;"
                                            "selection-background-color: lightgrey;"
                                            "}"
                                           )
        self.titleStateInput.setFont(QtGui.QFont("Lato", 14))
        self.titleStateInput.addItem("None", ["None"])
        self.titleStateInput.addItem("Alabama",
                                         ["None", "Huntsville", "Birmingham", "Montgomery", "Mobile", "Tuscaloosa"])
        self.titleStateInput.addItem("Alaska",
                                         ["None", "Anchorage", "Juneau", "Fairbanks", "Badger", "Knik-Fairview"])
        self.titleStateInput.addItem("Arizona", ["None", "Phoenix", "Tucson", "Sedona", "Mesa", "Scottsdale"])
        self.titleStateInput.addItem("Arkansas",
                                         ["None", "Little Rock", "Fort Smith", "Fayetteville", "Springsdale",
                                          "Jonesboro"])
        self.titleStateInput.addItem("California",
                                         ["None", "San Francisco", "Los Angeles", "San Diego", "San Jose", "Fresno"])
        self.titleStateInput.addItem("Colorado",
                                         ["None", "Denver", "Colorado Springs", "Pueblo", "Aspen", "Fort Collins"])
        self.titleStateInput.addItem("Connecticut",
                                         ["None", "Bridgeport", "Hartford", "New Haven", "Stamford", "Waterbury"])
        self.titleStateInput.addItem("Delaware",
                                         ["None", "Dover", "Wilmington", "Middletown", "New Castle", "Newark"])
        self.titleStateInput.addItem("Florida",
                                         ["None", "Orlando", "Tallahassee", "Jacksonville", "Miami", "Tampa"])
        self.titleStateInput.addItem("Georgia", ["None", "Atlanta", "Columbus", "Athens", "Augusta", "Savannah"])
        self.titleStateInput.addItem("Hawaii", ["None", "Kailua", "Waipahu", "Honolulu", "Hilo", "Kahului"])
        self.titleStateInput.addItem("Idaho",
                                         ["None", "Naperville", "Chicago", "St. Louis", "Rockford", "Springfield"])
        self.titleStateInput.addItem("Illinois",
                                         ["None", "San Francisco", "Los Angeles", "San Diego", "San Jose", "Fresno"])
        self.titleStateInput.addItem("Indiana",
                                         ["None", "Indianapolis", "Gary", "Lafayette", "Evansville", "Fort Wayne"])
        self.titleStateInput.addItem("Iowa",
                                         ["None", "Des Moines", "Waterloo", "Dubuque", "Cedar Rapids", "Davenport"])
        self.titleStateInput.addItem("Kansas", ["None", "Olathe", "Topeka", "Wichita", "Lawrence", "Kansas City"])
        self.titleStateInput.addItem("Kentucky", ["None", "Lexington", "Bowling Green", "Louisville", "Florence",
                                                      "Jeffersontown"])
        self.titleStateInput.addItem("Louisiana", ["None", "Alexandria", "Shreveport", "New Orleans", "Baton Rouge",
                                                       "Lafayette"])
        self.titleStateInput.addItem("Maine", ["None", "Portland", "Bangor", "Camden", "Augusta", "Brunswick"])
        self.titleStateInput.addItem("Maryland",
                                         ["None", "Washington D.C.", "Annapolis", "Gaithersburg", "Baltimore",
                                          "Gaithersburg"])
        self.titleStateInput.addItem("Massachusetts",
                                         ["None", "Plymouth", "Springfield ", "Salem", "Worcester", "Boston"])
        self.titleStateInput.addItem("Michigan",
                                         ["None", "Detroit", "Grand Rapids", "Ann Arbor", "Lansing", "Traverse City"])
        self.titleStateInput.addItem("Minnesota",
                                         ["None", "Minneapolis", "Duluth", "St Paul", "Rochester", "Richfield"])
        self.titleStateInput.addItem("Mississippi",
                                         ["None", "Southaven", "Vicksburg", "Meridian", "Jackson", "Gulfport"])
        self.titleStateInput.addItem("Missouri", ["None", "St. Louis", "Jefferson City", "Independence", "Columbia",
                                                      "Springfield"])
        self.titleStateInput.addItem("Montana", ["None", "Bozeman", "Great Falls", "Helena", "Billings", "Helena"])
        self.titleStateInput.addItem("Nebraska", ["None", "Omaha", "Lincoln", "Bellevue", "Scottsbluff"])
        self.titleStateInput.addItem("Nevada",
                                         ["None", "Las Vegas", "Carson City", "Reno", "Mesquite", "Henderson"])
        self.titleStateInput.addItem("New Hampshire", ["None", "Manchester", "Nashua", "Littleton", "Portsmouth"])
        self.titleStateInput.addItem("New Jersey",
                                         ["None", "Trenton", "Cherry Hill", "Atlantic City", "Newark", "New Brunswick"])
        self.titleStateInput.addItem("New Mexico",
                                         ["None", "Santa Fe", "Los Lunas", "Rio Rancho", "Las Cruces", "Albuquerque"])
        self.titleStateInput.addItem("New York", ["None", "New York", "Albany", "Yonkers", "Syracuse", "Buffalo"])
        self.titleStateInput.addItem("North Carolina",
                                         ["None", "Raleigh", "Charlotte", "Greensboro", "Durham", "Winston-Salem"])
        self.titleStateInput.addItem("North Dakota",
                                         ["None", "Bismarck", "Grand Forks", "Williston", "Fargo", "Minot"])
        self.titleStateInput.addItem("Ohio", ["None", "Cleveland", "Toledo", "Columbus", "Cincinnati", "Akron"])
        self.titleStateInput.addItem("Oklahoma",
                                         ["None", "Oklahoma City", "Tulsa", "Lawton", "Muskogee", "Broken Arrow"])
        self.titleStateInput.addItem("Oregon", ["None", "Portland", "Oregon City", "Bend", "Eugene", "Salem"])
        self.titleStateInput.addItem("Pennsylvania",
                                         ["None", "Pittsburgh", "Harrisburg", "Scranton", "Allentown", "Philadelphia"])
        self.titleStateInput.addItem("Rhode Island",
                                         ["None", "Providence", "Warwick", "Woonsocket", "Cranston", "Newport"])
        self.titleStateInput.addItem("South Carolina",
                                         ["None", "Charleston", "Mt Pleasant", "Sumter", "Columbia", "Rock Hill"])
        self.titleStateInput.addItem("South Dakota",
                                         ["None", "Pierre", "Sioux Falls", "Deadwood", "Watertown", "Rapid City"])
        self.titleStateInput.addItem("Tennessee",
                                         ["None", "Nashville", "Knoxville", "Gatlinburg", "Chattanooga", "Memphis"])
        self.titleStateInput.addItem("Texas", ["None", "Austin", "Dallas", "El Paso", "San Antonio", "Houston"])
        self.titleStateInput.addItem("Utah", ["None", "Salt Lake City", "Park City", "Moab", "Ogden", "St. George"])
        self.titleStateInput.addItem("Vermont",
                                         ["None", "Burlington", "Barre", "Montpelier", "Woodstock", "Rutland", "Stowe"])
        self.titleStateInput.addItem("Virginia",
                                         ["None", "Chesapeake", "Hampton", "Alexandria", "Richmond", "Norfolk"])
        self.titleStateInput.addItem("Washington", ["None", "Seattle", "Kent", "Spokane", "Tacoma", "Vancouver"])
        self.titleStateInput.addItem("West Virginia",
                                         ["None", "Charleston", "Morgantown", "Huntington", "Wheeling"])
        self.titleStateInput.addItem("Wisconsin",
                                         ["None", "Madison", "Milwaukee", "Eau Claire", "Green Bay", "Appleton"])
        self.titleStateInput.addItem("Wyoming", ["None", "Jackson", "Cody", "Cheyenne", "Casper", "Laramie"])
        self.titleStateInput.activated.connect(self.selectTitleCityFromTitleState)
        self.titleStateInput.activated.connect(self.titleInputDependencies)

        #Title City Input
        self.titleCityInput = self.createComboBox("titleCentralWidget", 297, 250, 150, 50)
        self.titleCityInput.setEnabled(False)
        self.titleCityInput.setStyleSheet("QComboBox"
                                           "{"
                                           "color: white;"
                                           "border: 3px solid;"
                                           "border-color: rgb(245, 245, 245);"
                                           "background-color: rgba(20, 52, 124, 170);"
                                           "}"
                                           "QComboBox QAbstractItemView {"
                                           "background-color: rgb(140, 140, 140);"
                                           "color: white;"
                                           "width: 200px;"
                                           "selection-background-color: lightgrey;"
                                           "}"
                                           )
        self.titleCityInput.setFont(QtGui.QFont("Lato", 14))
        self.titleCityInput.addItem("Select a City", ["None"])
        self.titleCityInput.activated.connect(self.titleInputDependencies)

        # Title Type Input
        self.titleTypeInput = self.createComboBox("titleCentralWidget", 444, 250, 160, 50)
        self.titleTypeInput.setEnabled(False)
        self.titleTypeInput.setStyleSheet("QComboBox"
                                          "{"
                                          "color: white;"
                                          "border: 3px solid;"
                                          "border-color: rgb(245, 245, 245);"
                                          "background-color: rgba(20, 52, 124, 170);"
                                          "}"
                                          "QComboBox QAbstractItemView {"
                                          "background-color: rgb(140, 140, 140);"
                                          "color: white;"
                                          "width: 200px;"
                                          "selection-background-color: lightgrey;"
                                          "}"
                                          )
        self.titleTypeInput.setFont(QtGui.QFont("Lato", 14))
        self.titleTypeInput.addItems(["Select a Type", "Food", "Nature/Outdoor", "Entertainment", "Cultural/Historical"])

        # Title Search Input
        self.titleSearchBar = QtWidgets.QLineEdit(self.titleCentralwidget)
        self.titleSearchBar.setGeometry(QtCore.QRect(601, 250, 302, 50))
        self.titleSearchBar.setPlaceholderText("Search by Attraction Name")
        self.titleSearchBar.setStyleSheet("QLineEdit"
                                          "{"
                                          "color: white;"
                                          "border: 3px solid;"
                                          "border-color: rgb(245, 245, 245);"
                                          "background-color: rgba(20, 52, 124, 170);"
                                          "}"
                                          )
        self.titleSearchBar.setFont(QtGui.QFont("Lato", 14))

        # Search button that changes windows
        self.windowChangeButton = QtWidgets.QToolButton(self.titleCentralwidget)
        self.windowChangeButton.setEnabled(False)
        self.windowChangeButton.setGeometry(900, 250, 100, 50)
        self.windowChangeButton.setText("Search")
        self.windowChangeButton.setStyleSheet("QToolButton"
                                          "{"
                                          "color: white;"
                                          "border: 3px solid;"
                                          "border-color: rgb(245, 245, 245);"
                                          "background-color: rgba(20, 52, 124, 170);"
                                          "}"
                                          )
        self.windowChangeButton.setFont(QtGui.QFont("Lato", 14))
        self.windowChangeButton.clicked.connect(self.changeWindow)

        # Explore Cities Feature Preview Picture
        # self.titleWindowExplorePicture = QtWidgets.QLabel(self.titleCentralwidget)
        # self.titleWindowExplorePicture.setStyleSheet("QLabel"
        #                                   "{"
        #                                   "border: 2px solid;"
        #                                   "border-color: rgb(245, 245, 245);"
        #                                   "}"
        #                                   )
        # # self.titleWindowExplorePicture.setFixedSize(469, 330)
        # self.titleWindowExplorePicture.move(150, 290)
        # self.titleWindowExplorePicture.setPixmap(QtGui.QPixmap("./Application Pictures/exploreCities.png"))
        # self.titleWindowExplorePicture.setScaledContents(True)
        # self.titleWindowExplorePicture.show()

        # Explore Cities Button
        # self.exploreCitiesButton = QtWidgets.QToolButton(self.titleCentralwidget)
        # self.exploreCitiesButton.setGeometry(160, 320, 370, 30)
        # self.exploreCitiesButton.setText("Explore Top Cities and Attractions")
        # self.exploreCitiesButton.setStyleSheet("QToolButton"
        #                                       "{"
        #                                       "color: white;"
        #                                       "border: 2px solid;"
        #                                       "border-color: rgb(245, 245, 245);"
        #                                       "background-color: rgba(20, 52, 124, 170);"
        #                                       "}"
        #                                       )
        # self.exploreCitiesButton.setFont(QtGui.QFont("Lato", 12))
        # self.exploreCitiesButton.clicked.connect(self.changeToExploreTab)
        #
        # # Description of Explore Feature
        # self.exploreCitiesFeatureDescription = self.createLabel("titleCentralWidget", 160, 355, 370, 200)
        # self.exploreCitiesFeatureDescription.setText("     Not sure where to go or what types of attractions are best? Using our"
        #                                              "\n unique explore feature, you can instantly find the top attractions across the"
        #                                              "\n country! These attractions come from the biggest cities in the nation and"
        #                                              "\n boast high ratings and extravagant qualities. From the iconic Golden Gate"
        #                                              "\n Bridge to the skyscrapers of New York City, an extensive collection of"
        #                                              "\n attractions await you! To explore these attractions click the button above.")
        # self.exploreCitiesFeatureDescription.setWordWrap(True)
        # self.exploreCitiesFeatureDescription.setStyleSheet("QLabel"
        #                                        "{"
        #                                        "color: white;"
        #                                        "background-color: rgba(20, 52, 124, 170);"
        #                                        "}"
        #                                        )
        # self.exploreCitiesFeatureDescription.setFont(QtGui.QFont("Lato", 10))
        #
        # # Sources button
        # self.sourcesButton = QtWidgets.QToolButton(self.titleCentralwidget)
        # self.sourcesButton.setGeometry(550, 320, 370, 30)
        # self.sourcesButton.setText("View Sources, Licenses, and References")
        # self.sourcesButton.setStyleSheet("QToolButton"
        #                                        "{"
        #                                        "color: white;"
        #                                        "border: 2px solid;"
        #                                        "border-color: rgb(245, 245, 245);"
        #                                        "background-color: rgba(20, 52, 124, 170);"
        #                                        "}"
        #                                        )
        # self.sourcesButton.setFont(QtGui.QFont("Lato", 12))
        # self.sourcesButton.clicked.connect(self.changeToSourcesTab)
        #
        # # Sources Button Description
        # self.sourcesFeatureDescription = self.createLabel("titleCentralWidget", 550, 355, 370, 53)
        # self.sourcesFeatureDescription.setText("     Find all sources, licenses, and references used within this application by"
        #                                        "\n clicking the button above. If you spot any missing citations, please create"
        #                                        "\n a report on the search attractions page.")
        # self.sourcesFeatureDescription.setWordWrap(True)
        # self.sourcesFeatureDescription.setStyleSheet("QLabel"
        #                                  "{"
        #                                  "color: white;"
        #                                  "background-color: rgba(20, 52, 124, 170);"
        #                                  "}"
        #                                  )
        # self.sourcesFeatureDescription.setFont(QtGui.QFont("Lato", 10))

        MainWindow.setCentralWidget(self.titleCentralwidget)


    def setupUi(self, MainWindow):
        global clickCount
        global groupBox
        global topGroupBoxBar
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle("Traveler")
        MainWindow.setFixedSize(1150, 645)
        # Sets up the window container
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("display")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1151, 626))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tab1")
        self.gridWidget = QtWidgets.QWidget(self.tabWidgetPage1)
        self.gridWidget.setGeometry(QtCore.QRect(880, 0, 251, 49))
        # self.line = QtWidgets.QFrame(self.tabWidgetPage1)
        # self.line.setGeometry(QtCore.QRect(210, -10, 21, 611))
        # self.line.setFrameShape(QtWidgets.QFrame.VLine)
        # self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.widget = QtWidgets.QWidget(self.tabWidgetPage1)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1151, 601))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.designGroupBox = QtWidgets.QGroupBox(self.widget)
        self.designGroupBox.setObjectName("backdrop")
        self.designGroupBox.setEnabled(True)
        self.designGroupBox.setFlat(True)
        self.designGroupBox.setFixedSize(218,240)
        self.designGroupBox.move(5,50)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setEnabled(True)
        self.groupBox.setFlat(True)

        # Setting topGroupBoxBar
        self.topGroupBoxBar = QtWidgets.QGroupBox(self.widget)
        self.topGroupBoxBar.setFixedSize(907, 40)
        self.topGroupBoxBar.move(230,10)
        self.topGroupBoxBar.setEnabled(True)
        self.topGroupBoxBar.setFlat(True)
        self.numOfAttractionsLabel = self.createLabel("topGroupBoxBar", 10, 20, 200, 20)
        self.numOfAttractionsLabel.setObjectName("numAttractions")
        self.sortingComboBoxLabel = self.createLabel("topGroupBoxBar", 643, 13, 100, 20)
        self.sortingComboBoxLabel.setObjectName("sortByLabel")
        self.sortingComboBox = self.createComboBox("topGroupBoxBar", 700, 7, 208, 30)
        self.sortingComboBox.setObjectName("sortingComboBox")
        self.sortingComboBox.addItems(["Recommended",
                                "Nearest attractions",
                                  "Rating: Highest to Lowest",
                                  "Rating: Lowest to Highest",
                                  "Price: Highest to Lowest",
                                  "Price: Lowest to Highest",
                                  "Traffic: Highest to Lowest",
                                  "Traffic: Lowest to Highest"])
        self.sortingComboBox.activated.connect(self.getCurrentFieldValues)

        # Search Field and Search Button
        self.searchBar = QtWidgets.QLineEdit(self.topGroupBoxBar)
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setStyleSheet("font: 14px")
        self.searchBar.setGeometry(QtCore.QRect(200,8,301,30))
        self.searchBar.setPlaceholderText("Search by Keyword")
        self.searchButton = QtWidgets.QToolButton(self.topGroupBoxBar)
        self.searchButton.setGeometry(QtCore.QRect(500, 9, 55, 28))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.searchIcon = QtWidgets.QLabel(self.topGroupBoxBar)
        self.searchIcon.setPixmap(QtGui.QPixmap("./Application Pictures/magnifyingIcon.png"))
        self.searchIcon.setScaledContents(True)
        self.searchIcon.setFixedSize(25, 25)
        self.searchIcon.move(171,10)
        self.searchIcon.show()
        self.searchButton.clicked.connect(self.searchResults)
        self.clearButton = QtWidgets.QToolButton(self.topGroupBoxBar)
        self.clearButton.setGeometry(QtCore.QRect(554, 9, 55, 28))
        self.clearButton.setText("Clear")
        self.clearButton.clicked.connect(self.clearSearch)

        # App Logo
        self.appLogo = QtWidgets.QLabel(self.groupBox)
        self.appLogo.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowLogo.png"))
        self.appLogo.setScaledContents(True)
        self.appLogo.setFixedSize(190, 190)
        self.appLogo.move(5, -22)
        self.appLogo.show()

        # Filter Title
        Xcoor = 6
        Ycoor = 230
        self.filterTitle = self.createLabel("groupBox",Xcoor+5, Ycoor+60, 120, 50)
        self.filterTitle.setObjectName("filterByTitle")

        # Filtering by State - Format: (Label : ComboBox)
        self.stateFilterLabel = self.createLabel("groupBox",Xcoor+5, Ycoor+90, 50, 50)
        self.stateFilterLabel.setObjectName("filters")
        self.stateFilterComboBox = self.createComboBox("groupBox",Xcoor+47, Ycoor+103, 171, 26)
        self.stateFilterComboBox.setObjectName("filterComboboxes")
        self.stateFilterComboBox.addItem("None", ["None"])
        self.stateFilterComboBox.addItem("Alabama", ["None", "Huntsville", "Birmingham", "Montgomery", "Mobile", "Tuscaloosa"])
        self.stateFilterComboBox.addItem("Alaska", ["None", "Anchorage", "Juneau", "Fairbanks", "Badger", "Knik-Fairview"])
        self.stateFilterComboBox.addItem("Arizona", ["None", "Phoenix", "Tucson", "Sedona", "Mesa", "Scottsdale"])
        self.stateFilterComboBox.addItem("Arkansas", ["None", "Little Rock", "Fort Smith", "Fayetteville", "Springsdale", "Jonesboro"])
        self.stateFilterComboBox.addItem("California", ["None", "San Francisco", "Los Angeles", "San Diego", "San Jose", "Fresno"])
        self.stateFilterComboBox.addItem("Colorado", ["None", "Denver", "Colorado Springs", "Pueblo", "Aspen", "Fort Collins"])
        self.stateFilterComboBox.addItem("Connecticut", ["None", "Bridgeport", "Hartford", "New Haven", "Stamford", "Waterbury"])
        self.stateFilterComboBox.addItem("Delaware", ["None", "Dover", "Wilmington", "Middletown", "New Castle", "Newark"])
        self.stateFilterComboBox.addItem("Florida", ["None", "Orlando", "Tallahassee", "Jacksonville", "Miami", "Tampa"])
        self.stateFilterComboBox.addItem("Georgia", ["None", "Atlanta", "Columbus", "Athens", "Augusta", "Savannah"])
        self.stateFilterComboBox.addItem("Hawaii", ["None", "Kailua", "Waipahu", "Honolulu", "Hilo", "Kahului"])
        self.stateFilterComboBox.addItem("Idaho", ["None", "Naperville", "Chicago", "St. Louis", "Rockford", "Springfield"])
        self.stateFilterComboBox.addItem("Illinois", ["None", "San Francisco", "Los Angeles", "San Diego", "San Jose", "Fresno"])
        self.stateFilterComboBox.addItem("Indiana", ["None", "Indianapolis", "Gary", "Lafayette", "Evansville", "Fort Wayne"])
        self.stateFilterComboBox.addItem("Iowa", ["None", "Des Moines", "Waterloo", "Dubuque", "Cedar Rapids", "Davenport"])
        self.stateFilterComboBox.addItem("Kansas", ["None", "Olathe", "Topeka", "Wichita", "Lawrence", "Kansas City"])
        self.stateFilterComboBox.addItem("Kentucky", ["None", "Lexington", "Bowling Green", "Louisville", "Florence", "Jeffersontown"])
        self.stateFilterComboBox.addItem("Louisiana", ["None", "Alexandria", "Shreveport", "New Orleans", "Baton Rouge", "Lafayette"])
        self.stateFilterComboBox.addItem("Maine", ["None", "Portland", "Bangor", "Camden", "Augusta", "Brunswick"])
        self.stateFilterComboBox.addItem("Maryland", ["None", "Washington D.C.", "Annapolis", "Gaithersburg", "Baltimore", "Gaithersburg"])
        self.stateFilterComboBox.addItem("Massachusetts", ["None", "Plymouth", "Springfield ", "Salem", "Worcester", "Boston"])
        self.stateFilterComboBox.addItem("Michigan", ["None", "Detroit", "Grand Rapids", "Ann Arbor", "Lansing", "Traverse City"])
        self.stateFilterComboBox.addItem("Minnesota", ["None", "Minneapolis", "Duluth", "St Paul", "Rochester", "Richfield"])
        self.stateFilterComboBox.addItem("Mississippi", ["None", "Southaven", "Vicksburg", "Meridian", "Jackson", "Gulfport"])
        self.stateFilterComboBox.addItem("Missouri", ["None", "St. Louis", "Jefferson City", "Independence", "Columbia", "Springfield"])
        self.stateFilterComboBox.addItem("Montana", ["None", "Bozeman", "Great Falls", "Helena", "Billings", "Helena"])
        self.stateFilterComboBox.addItem("Nebraska", ["None", "Omaha", "Lincoln", "Bellevue", "Scottsbluff"])
        self.stateFilterComboBox.addItem("Nevada", ["None", "Las Vegas", "Carson City", "Reno", "Mesquite", "Henderson"])
        self.stateFilterComboBox.addItem("New Hampshire", ["None", "Manchester", "Nashua", "Littleton", "Portsmouth"])
        self.stateFilterComboBox.addItem("New Jersey", ["None", "Trenton", "Cherry Hill", "Atlantic City", "Newark", "New Brunswick"])
        self.stateFilterComboBox.addItem("New Mexico", ["None", "Santa Fe", "Los Lunas", "Rio Rancho", "Las Cruces", "Albuquerque"])
        self.stateFilterComboBox.addItem("New York", ["None", "New York", "Albany", "Yonkers", "Syracuse", "Buffalo"])
        self.stateFilterComboBox.addItem("North Carolina", ["None", "Raleigh", "Charlotte", "Greensboro", "Durham", "Winston-Salem"])
        self.stateFilterComboBox.addItem("North Dakota", ["None", "Bismarck", "Grand Forks", "Williston", "Fargo", "Minot"])
        self.stateFilterComboBox.addItem("Ohio", ["None", "Cleveland", "Toledo", "Columbus", "Cincinnati", "Akron"])
        self.stateFilterComboBox.addItem("Oklahoma", ["None", "Oklahoma City", "Tulsa", "Lawton", "Muskogee", "Broken Arrow"])
        self.stateFilterComboBox.addItem("Oregon", ["None", "Portland", "Oregon City", "Bend", "Eugene", "Salem"])
        self.stateFilterComboBox.addItem("Pennsylvania", ["None", "Pittsburgh", "Harrisburg", "Scranton", "Allentown", "Philadelphia"])
        self.stateFilterComboBox.addItem("Rhode Island", ["None", "Providence", "Warwick", "Woonsocket", "Cranston", "Newport"])
        self.stateFilterComboBox.addItem("South Carolina", ["None", "Charleston", "Mt Pleasant", "Sumter", "Columbia", "Rock Hill"])
        self.stateFilterComboBox.addItem("South Dakota", ["None", "Pierre", "Sioux Falls", "Deadwood", "Watertown", "Rapid City"])
        self.stateFilterComboBox.addItem("Tennessee", ["None", "Nashville", "Knoxville", "Gatlinburg", "Chattanooga", "Memphis"])
        self.stateFilterComboBox.addItem("Texas", ["None", "Austin", "Dallas", "El Paso", "San Antonio", "Houston"])
        self.stateFilterComboBox.addItem("Utah", ["None", "Salt Lake City", "Park City", "Moab", "Ogden", "St. George"])
        self.stateFilterComboBox.addItem("Vermont", ["None", "Burlington", "Barre", "Montpelier", "Woodstock", "Rutland", "Stowe"])
        self.stateFilterComboBox.addItem("Virginia", ["None", "Chesapeake", "Hampton", "Alexandria", "Richmond", "Norfolk"])
        self.stateFilterComboBox.addItem("Washington", ["None", "Seattle", "Kent", "Spokane", "Tacoma", "Vancouver"])
        self.stateFilterComboBox.addItem("West Virginia", ["None", "Charleston", "Morgantown", "Huntington", "Wheeling"])
        self.stateFilterComboBox.addItem("Wisconsin", ["None", "Madison", "Milwaukee", "Eau Claire", "Green Bay", "Appleton"])
        self.stateFilterComboBox.addItem("Wyoming", ["None", "Jackson", "Cody", "Cheyenne", "Casper", "Laramie"])
        self.stateFilterComboBox.activated.connect(self.selectCityFromState)
        self.stateFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by City - Format: (Label : ComboBox)
        self.cityFilterLabel = self.createLabel("groupBox", Xcoor+5, Ycoor+125, 50, 50)
        self.cityFilterLabel.setObjectName("filters")
        self.cityFilterComboBox = self.createComboBox("groupBox", Xcoor+47, Ycoor+138, 171, 26)
        self.cityFilterComboBox.setObjectName("filterComboboxes")
        self.cityFilterComboBox.addItems(["None"])
        self.cityFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by Type - Format: (Label : ComboBox)
        self.typeFilterLabel = self.createLabel("groupBox", Xcoor+5, Ycoor+160, 50, 50)
        self.typeFilterLabel.setObjectName("filters")
        self.typeFilterComboBox = self.createComboBox("groupBox", Xcoor+47, Ycoor+173, 171, 26)
        self.typeFilterComboBox.setObjectName("filterComboboxes")
        self.typeFilterComboBox.addItems(["None", "Food", "Nature/Outdoor", "Entertainment", "Cultural/Historical"])
        self.typeFilterComboBox.activated.connect(self.getCurrentFieldValues)

        # Filtering by WheelChair Accessibility - Format: (CheckBox : Label)
        self.wheelchairAccessFilterLabel = self.createLabel("groupBox", Xcoor+30, Ycoor+200, 150, 50)
        self.wheelchairAccessFilterLabel.setObjectName("filters")
        self.wheelchairAccessFilterCheckBox = self.createCheckBox("groupBox", Xcoor+5, Ycoor+216, 20, 20)
        self.wheelchairAccessFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Filtering by Family Friendliness - Format: (CheckBox : Label)
        self.familyFriendlyFilterLabel = self.createLabel("groupBox", Xcoor+30, Ycoor+225, 150, 50)
        self.familyFriendlyFilterLabel.setObjectName("filters")
        self.familyFriendlyFilterCheckBox = self.createCheckBox("groupBox", Xcoor+5, Ycoor+241, 20, 20)
        self.familyFriendlyFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Filtering by Pet Friendliness - Format: (CheckBox : Label)
        self.petFriendlyFilterLabel = self.createLabel("groupBox", Xcoor+30, Ycoor+250, 150, 50)
        self.petFriendlyFilterLabel.setObjectName("filters")
        self.petFriendlyFilterCheckBox = self.createCheckBox("groupBox", Xcoor+5, Ycoor+266, 20, 20)
        self.petFriendlyFilterCheckBox.stateChanged.connect(self.getCurrentFieldValues)

        # Enter Coordinates QLineEdit
        self.userLocationTitle = self.createLabel("groupBox", Xcoor + 5, Ycoor - 175, 200, 25)
        self.userLocationTitle.setObjectName("locationDetailsTitle")
        self.userLocationTitle.setText("Location Details")
        self.currentLocationLabel = self.createLabel("groupBox", Xcoor + 5, Ycoor - 145, 200, 25)
        self.currentLocationLabel.setObjectName("enteredLocation")
        self.latitudeInputLabel = self.createLabel("groupBox", Xcoor + 5, Ycoor - 115, 200, 25)
        self.latitudeInputLabel.setText("Latitude:")
        self.latitudeInput = QtWidgets.QLineEdit(self.groupBox)
        self.latitudeInput.setGeometry(QtCore.QRect(Xcoor + 65, Ycoor - 115, 120, 25))
        self.latitudeInput.setPlaceholderText(" Enter latitude")
        self.latitudeInput.textChanged.connect(self.checkIfLocationIsFilled)
        self.longitudeInputLabel = self.createLabel("groupBox", Xcoor + 5, Ycoor - 80, 200, 25)
        self.longitudeInputLabel.setText("Longitude:")
        self.longitudeInput = QtWidgets.QLineEdit(self.groupBox)
        self.longitudeInput.setGeometry(QtCore.QRect(Xcoor + 75, Ycoor - 80, 120, 25))
        self.longitudeInput.setPlaceholderText(" Enter longitude")
        self.longitudeInput.textChanged.connect(self.checkIfLocationIsFilled)
        self.radiusLabel = self.createLabel("groupBox", Xcoor + 5, Ycoor - 45, 200, 25)
        self.radiusLabel.setText("Desired Distance From You:")
        self.radiusComboBox = self.createComboBox("groupBox", Xcoor + 5, Ycoor - 20, 205, 25)
        self.radiusComboBox.setObjectName("radiusComboBox")
        self.radiusComboBox.addItems(["Any distance", "Less than 5 miles", "Less than 10 miles", "Less than 20 miles", "Less than 50 miles"])
        self.radiusComboBox.setEnabled(False)
        self.radiusComboBox.activated.connect(self.detectChangeInRadius)
        self.showLocationMapButton = QtWidgets.QToolButton(self.groupBox)
        self.showLocationMapButton.setGeometry(Xcoor + 5, Ycoor + 10, 205, 20)
        self.showLocationMapButton.setText("Show location in maps")
        self.showLocationMapButton.setEnabled(False)
        self.showLocationMapButton.clicked.connect(self.showLocationMap)
        self.getLocationButton = QtWidgets.QToolButton(self.groupBox)
        self.getLocationButton.setGeometry(Xcoor + 5, Ycoor + 35, 205, 20)
        self.getLocationButton.setText("Find my location")
        self.getLocationButton.clicked.connect(self.getCurrentLocation)

        # Adding a Dynamic Help Menu
        self.helpButton = QtWidgets.QToolButton(self.groupBox)
        self.helpButton.setObjectName("helpButton")
        self.helpButton.setGeometry(5,535,219,20)
        clickCount = 0
        self.helpMenuGroupBox = QtWidgets.QGroupBox(self.groupBox)
        self.helpMenuGroupBox.setGeometry(QtCore.QRect(5, 455, 205, 80))
        self.helpMenuGroupBox.hide()
        self.reportButton = QtWidgets.QToolButton(self.groupBox)
        self.reportButton.setGeometry(5, 560, 219, 20)
        self.reportButton.setText("Create a Report")
        self.reportButton.clicked.connect(self.createReport)
        self.documentationButton = QtWidgets.QToolButton(self.helpMenuGroupBox)
        self.documentationButton.setGeometry(5, 30, 195, 20)
        self.documentationButton.clicked.connect(self.showDocumentation)
        self.supportButton = QtWidgets.QToolButton(self.helpMenuGroupBox)
        self.supportButton.setGeometry(5, 5, 195, 20)
        self.showToolDescriptionButton = QtWidgets.QToolButton(self.helpMenuGroupBox)
        self.showToolDescriptionButton.setGeometry(5, 55, 195, 20)
        self.showToolDescriptionButton.clicked.connect(self.showDescriptions)
        self.documentationButton.setText(_translate("MainWindow", " Read Documentation"))
        self.supportButton.setText(_translate("MainWindow", "Q ＆ A"))
        self.showToolDescriptionButton.setText(_translate("MainWindow", "Show Tool Descriptions"))
        self.helpButton.setText(_translate("MainWindow", "Help"))
        self.helpButton.clicked.connect(self.helpMenuListener)

        # Setting ScrollArea
        self.scrollAreaWidgetContainer = QtWidgets.QWidget()
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea = QtWidgets.QScrollArea(self.tabWidgetPage1)
        self.scrollArea.setFixedWidth(907)
        self.scrollArea.setMinimumHeight(531)
        self.scrollArea.move(230,50)
        self.scrollArea.setWidgetResizable(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContainer)
        self.scrollAreaWidgetContainer.setLayout(self.verticalLayout_3)

        # Adds multiple tabs
        self.tabWidget.addTab(self.tabWidgetPage1, " ")
        self.tab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab, " ")

        self.sourcesTab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.sourcesTab, " ")
        self.sourcesTabWidget = QtWidgets.QWidget(self.sourcesTab)
        self.sourcesTabWidget.setGeometry(QtCore.QRect(0, 0, 1150, 601))
        self.sourcesTabAppLogo = QtWidgets.QLabel(self.sourcesTabWidget)
        self.sourcesTabAppLogo.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowLogo.png"))
        self.sourcesTabAppLogo.setScaledContents(True)
        self.sourcesTabAppLogo.setFixedSize(190, 190)
        self.sourcesTabAppLogo.move(5, -22)
        self.sourcesTabAppLogo.show()
        self.sourcesLabel = self.createLabel("sourcesTabWidget", 465, 20, 250, 40)
        self.sourcesText = QtWidgets.QPlainTextEdit(self.sourcesTabWidget)
        self.sourcesText.setFixedSize(1129,531)
        self.sourcesText.move(8, 50)
        text = open('sources.txt').read()
        self.sourcesText.setPlainText(text)
        self.sourcesText.setReadOnly(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def changeSortingToDistance(self):
        self.sortingComboBox.setCurrentIndex(1)

    def selectCityFromState(self, index):
        self.cityFilterComboBox.clear()
        self.cityFilterComboBox.addItems(self.stateFilterComboBox.itemData(index))

    def selectTitleCityFromTitleState(self, index):
        self.titleCityInput.clear()
        self.titleCityInput.addItems(self.titleStateInput.itemData(index))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.filterTitle.setText(_translate("MainWindow", "Filter By:"))
        self.stateFilterLabel.setText(_translate("MainWindow", "State:"))
        self.cityFilterLabel.setText(_translate("MainWindow", "City:"))
        self.typeFilterLabel.setText(_translate("MainWindow", "Type:"))
        self.wheelchairAccessFilterLabel.setText(_translate("MainWindow", "Wheelchair Accessible"))
        self.familyFriendlyFilterLabel.setText(_translate("MainWindow", "Family Friendly"))
        self.petFriendlyFilterLabel.setText(_translate("MainWindow", "Pet Friendly"))
        self.sortingComboBoxLabel.setText(_translate("MainWindow", "Sort By:"))
        self.sourcesLabel.setText(_translate("MainWindow", "Sources, Liscenses, and References"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("MainWindow", "Find Attractions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Bookmarked Attractions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sourcesTab), _translate("MainWindow", "Sources, Licenses, and References"))

if __name__ == "__main__":
    # Clears action log
    clearLog()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    with open("design.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupTitle(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

