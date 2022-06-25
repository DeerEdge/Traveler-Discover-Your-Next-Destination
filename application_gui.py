import os
import webbrowser
import io
# folium v0.12.1 - Used to display geographical data
from random import random

import folium
from PyQt5.QtCore import QUrl

import application_database
import application_filter_request
import sys

# ipregistry v3.2.0 - Used to find current location of the user when called
from ipregistry import IpregistryClient
from time import gmtime, strftime
from operator import itemgetter
# PyQt5 v5.15.6 - Used to create interface and all visual components.
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
# PyQtWebEngine v5.15.5 - Used to display web widgets. Folium maps are displayed using this library.
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
# geopy v2.2.0 - Used to calculate distance between two points using latitude and longitude values.
from geopy import distance
# import module2
from geopy.geocoders import Nominatim




geolocator = Nominatim(user_agent="geoapiExercises")
# Connect to ip finder as a client in order to get information about the ip
client = IpregistryClient("72bw4jakulj27ism")
ipInfo = client.lookup()

class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

# Creates an the instance of QApplication, and creates all corresponding class functions
class Ui_MainWindow(object):
    global filtered_attractions_list
    global radius_checked
    radius_checked = False
    filtered_attractions_list = []

    # Upon being called, this function creates a QLabel associated with a container that is specified by the string
    # parameter (container). The QLabel's geometry is specified by the location parameters (x_coordinate, y_coordinate)
    # and the size parameters (width, length) passed through the function.
    #
    # Returns a QLabel object
    def create_QLabel(self, container, x_coordinate, y_coordinate, width, length):
        global location_and_filters_QGroupBox
        global attractions_QGroupBox_bar
        global attraction_QScrollArea_object

        # Creates and associates QLabel to specified container
        if container == "location_and_filters_QGroupBox":
            self.QLabel = QtWidgets.QLabel(self.location_and_filters_QGroupBox)
        elif container == "attraction_QScrollArea_object":
            self.QLabel = QtWidgets.QLabel(self.attraction_QScrollArea_object)
        elif container == "bookmarks_tab_QScrollArea_object":
            self.QLabel = QtWidgets.QLabel(self.bookmarks_tab_QScrollArea_object)
        elif container == "bookmarks_tab_top_groupBox_bar":
            self.QLabel = QtWidgets.QLabel(self.bookmarks_tab_top_groupBox_bar)
        elif container == "help_menu_groupBox":
            self.QLabel = QtWidgets.QLabel(self.help_menu_groupBox)
        elif container == "attractions_QGroupBox_bar":
            self.QLabel = QtWidgets.QLabel(self.attractions_QGroupBox_bar)
        elif container == "sources_tab_widget":
            self.QLabel = QtWidgets.QLabel(self.sources_tab_widget)
        elif container == "report_window_groupBox":
            self.QLabel = QtWidgets.QLabel(self.report_window)
        elif container == "documentation_window_QGroupBox":
            self.QLabel = QtWidgets.QLabel(self.documentation_window)
        elif container == "title_window_central_widget":
            self.QLabel = QtWidgets.QLabel(self.title_window_central_widget)

        # Geometry of QLabel is specified by the passed function parameters
        self.QLabel.setGeometry(QtCore.QRect(x_coordinate, y_coordinate, width, length))
        return self.QLabel

    # Upon being called, this function creates a QComboBox associated with a container that is specified by the string
    # parameter (container). The QLabel's geometry is specified by the location parameters (x_coordinate, y_coordinate)
    # and the size parameters (width, length) passed through the function.
    #
    # Returns a QComboBox object
    def create_QComboBox(self, container, x_coordinate, y_coordinate, width, length):
        global location_and_filters_QGroupBox
        global attraction_QScrollArea_object
        global attractions_QGroupBox_bar


        # Creates and associates QComboBox to specified container
        if container == "location_and_filters_QGroupBox":
            self.QComboBox = QtWidgets.QComboBox(self.location_and_filters_QGroupBox)
        elif container == "attractions_QGroupBox_bar":
            self.QComboBox = QtWidgets.QComboBox(self.attractions_QGroupBox_bar)
        elif container == "title_window_central_widget":
            self.QComboBox = QtWidgets.QComboBox(self.title_window_central_widget)

        # Geometry of QComboBox is specified by the passed function parameters
        self.QComboBox.setGeometry(QtCore.QRect(x_coordinate, y_coordinate, width, length))
        return self.QComboBox

    # Upon being called, this function creates a QCheckBox associated with a container that is specified by the string
    # parameter (container). The QLabel's geometry is specified by the location parameters (x_coordinate, y_coordinate)
    # and the size parameters (width, length) passed through the function.
    #
    # Returns a QComboBox object
    def create_QCheckBox(self, container, x_coordinate, y_coordinate, width, length):
        global location_and_filters_QGroupBox
        global attraction_QScrollArea_object

        # Creates and associates QComboBox to specified container
        if container == "location_and_filters_QGroupBox":
            self.QCheckBox = QtWidgets.QCheckBox(self.location_and_filters_QGroupBox)

        # Geometry of QCheckBox is specified by the passed function parameters
        self.QCheckBox.setGeometry(QtCore.QRect(x_coordinate, y_coordinate, width, length))
        return self.QCheckBox

    # This function creates an object container that holds all of the attraction's information and displays it within
    # the application's scrollable area. The object consists of the attraction image, attraction details, and
    # corresponding geographical maps that mark the attraction's location. Buttons are also included to expand the
    # geographical map preview and to link the user to the attraction's official website.
    #
    # Returns a QGroupBox object
    def create_QScrollArea_object(self, Ycoor, attraction):
        global attraction_QScrollArea_object

        # The QGroupBox container is created and added to the QScrollArea layout
        self.attraction_QScrollArea_object = QtWidgets.QGroupBox(self.widget)
        self.attraction_QScrollArea_object.setFixedSize(884, 220)
        self.attraction_QScrollArea_object.setLayout(QtWidgets.QVBoxLayout())

        # A QLabel is created to display an image of the attraction set using QPixmap
        self.attraction_image = QtWidgets.QLabel(self.attraction_QScrollArea_object)
        image_address = "./Attraction Pictures/" + str(attraction[0]) + " - " + str(attraction[4]) + ".jpg"
        self.attraction_image.setPixmap(QtGui.QPixmap(image_address))
        self.attraction_image.setScaledContents(True)
        self.attraction_image.setFixedSize(220, 220)
        self.attraction_image.show()

        # A QToolButton is created to display the bookmark icon set using QPixmap and performs actions specified by the
        # control_bookmarks function.
        self.bookmark_icon = QtWidgets.QToolButton(self.attraction_QScrollArea_object)
        self.bookmark_icon.setObjectName("bookmark")
        self.bookmark_icon.setProperty("unactivated", True)
        self.bookmark_icon.setGeometry(10, 10, 30, 30)
        self.bookmark_icon.setIcon(QtGui.QIcon("Application Pictures/Bookmark Icons/unchecked bookmark.png"))
        self.bookmark_icon.setIconSize(QtCore.QSize(512, 512))
        self.bookmark_icon.setStyleSheet("QToolButton { background-color: transparent; border: 0px }");

        # When the bookmark icon is clicked, the bookmark can be added or removed based on the icon's state of activation
        self.bookmark_icon.clicked.connect(self.control_bookmarks)

        labelXPos = 230
        labelYPos = 95

        converted_list = ''
        for element in attraction:
            if element == attraction[0]:
                converted_list = converted_list + str(element)
            else:
                converted_list = converted_list + ',|' + str(element)
        attraction_details_string = "[" + (converted_list) + "]"

        # A hidden QLabel holds the attraction's information so the object's attributes can be read after creation
        self.attraction_info_QLabel = self.create_QLabel("attraction_QScrollArea_object", 0, 0, 600, 50)
        self.attraction_info_QLabel.setObjectName("attraction_info_QLabel")
        self.attraction_info_QLabel.setText(attraction_details_string)
        self.attraction_info_QLabel.setHidden(True)

        # A QLabel is created to display the attraction title
        self.attraction_title_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, -5, 450, 50)
        self.attraction_title_QLabel.setObjectName("attractionName")
        self.attraction_title_QLabel.setText((str(attraction[1])))

        # A QLabel is created to display the attraction's numeric rating [0-5]
        self.rating_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos + 350, -5, 50, 50)
        self.rating_QLabel.setObjectName("rating")
        self.rating_QLabel.setText((str(attraction[8])))

        # A QLabel is created and set to display an image of the attraction's rating through star icons. The rating
        # displayed through the icons is the floored to the nearest 0.5 decimal.
        # Ex. 4.8 would be represented as 4.5 and 2.9 would be represented as 2.5
        # The rating decimal is intially set to 5.0
        min_star_rating = 5.0
        # The rating decimal is decreased in increments of 0.5 until the nearest 0.5 floored decimal
        for i in range(10):
            if (float(attraction[8]) < min_star_rating):
                min_star_rating = min_star_rating - 0.5
            else:
                # Rating icon label is created and set to the specified rating image using QPixmap
                self.rating_icon = QtWidgets.QLabel(self.attraction_QScrollArea_object)
                self.rating_icon.setPixmap(QtGui.QPixmap("./Application Pictures/Star Ratings/" + str(min_star_rating)
                                                         + " star.png"))
                self.rating_icon.setScaledContents(True)
                self.rating_icon.setFixedSize(85, 16)
                self.rating_icon.move(600, 12)
                self.rating_icon.show()
                break

        # A QLabel representing the distance from the specified location is conditionally created. If the latitudinal
        # and longitudinal fields are not empty and are integers then the distance is calculated and shown by a QLabel.
        # If the condition is not met, only the attraction's location (city, state) is displayed.
        if self.latitude_input.text() != "" and self.longitude_input.text() != "" and \
                self.is_float(str(self.latitude_input.text())) and self.is_float(str(self.longitude_input.text())):
            # Distance from specified location and attraction is calculated
            distance_from_user_location = distance.distance(
                ((self.latitude_input.text()), (self.longitude_input.text())), (attraction[13], attraction[14])).miles

            # A QLabel is created to show the attraction's location and calculated distance
            self.location_Qlabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, 17, 300, 50)
            self.location_Qlabel.setObjectName("locationAndDistance")
            self.location_Qlabel.setText((str(attraction[4]) + ", " + str(attraction[3])) + " - "
                                         + str('%.1f' % (distance_from_user_location)) + " miles away")
        else:
            # A QLabel is created to only show the attraction's location
            self.location_Qlabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, 17, 200, 50)
            self.location_Qlabel.setObjectName("locationAndDistance")
            self.location_Qlabel.setText((str(attraction[4]) + ", " + str(attraction[3])))

        # A QLabel is created to show the attraction's type. The type can be one of the four attraction types: Food,
        # Nature/Outdoor, Entertainment, or Cultural/Historical.
        self.type_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, labelYPos + 20, 200, 50)
        self.type_QLabel.setText((str(attraction[5])))

        # A QLabel is created to display the attraction's relative cost
        self.price_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, labelYPos + 40, 200, 50)
        if (str(attraction[6])) == '1':
            self.price_QLabel.setText("Price Level - $")
        elif (str(attraction[6])) == '2':
            self.price_QLabel.setText("Price Level - $$")
        else:
            self.price_QLabel.setText("Price Level - $$$")

        # A QLabel is created to display the attraction's relative busyness level
        self.busyness_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, labelYPos + 60, 200, 50)
        if (str(attraction[7])) == '1':
            self.busyness_QLabel.setText("Low Busyness")
        elif (str(attraction[7])) == '2':
            self.busyness_QLabel.setText("Moderately Busy")
        else:
            self.busyness_QLabel.setText("Very Busy")

        # A QLabel is created to display whether an attraction is wheelchair accessible
        self.wheelchair_accessibility_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos + 170,
                                                                  labelYPos + 20, 200, 50)
        if ((attraction[9])):
            self.wheelchair_accessibility_QLabel.setText("Wheelchair Accessible? - Yes")
        else:
            self.wheelchair_accessibility_QLabel.setText("Wheelchair Accessible? - No")

        # A QLabel is created to display whether an attraction is family friendly
        self.family_friendly_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos + 170,
                                                         labelYPos + 40, 200, 50)
        if ((attraction[10])):
            self.family_friendly_QLabel.setText("Family Friendly? - Yes")
        else:
            self.family_friendly_QLabel.setText("Family Friendly? - No")

        # A QLabel is created to display whether an attraction is pet friendly
        self.pet_friendly_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos + 170, labelYPos + 60,
                                                      200, 50)
        if ((attraction[11])):
            self.pet_friendly_QLabel.setText("Pet Friendly? - Yes")
        else:
            self.pet_friendly_QLabel.setText("Pet Friendly? - No")

        # A QLabel is created to display the coordinate location of the attraction (latitude, longitude)
        self.coordinate_location_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, labelYPos + 80,
                                                             200, 50)
        self.coordinate_location_QLabel.setText(
            "Location: (" + str('%.3f' % (attraction[13])) + "," + str('%.3f' % (attraction[14])) + ")")

        # A hidden QLabel is created to be accessed later after the creation of the object
        self.coordinate_info_QLabel = self.create_QLabel("attraction_QScrollArea_object", 0, 0, 200, 50)
        self.coordinate_info_QLabel.setObjectName("Location")
        self.coordinate_info_QLabel.setText(str('%.6f' % (attraction[14])) + "," + str('%.6f' % (attraction[13])))
        self.coordinate_info_QLabel.hide()

        # A QLabel is created to display the attraction's description
        self.description_QLabel = self.create_QLabel("attraction_QScrollArea_object", labelXPos, 10, 454, 125)
        self.description_QLabel.setWordWrap(True)
        self.description_QLabel.setText((str(attraction[2])))

        #  A QGroupBox is created to hold the map data
        self.map_container = QtWidgets.QGroupBox(self.attraction_QScrollArea_object)
        self.map_container.setGeometry(QtCore.QRect(675, -10, 220, 220))
        self.map_container.setEnabled(True)
        self.map_container.setFlat(True)

        # The created QGroupBox container"s layout is set to hold the web widget
        self.map_frame = QtWidgets.QVBoxLayout(self.map_container)

        # The attraction map is centered around the coordinates of the attraction
        coordinate = (attraction[13], attraction[14])
        map = folium.Map(zoom_start=15, location=coordinate)
        folium.Marker(location=coordinate).add_to(map)
        # Save map data to data object
        data = io.BytesIO()
        map.save(data, close_file=False)
        webView = QWebEngineView()
        # Sets the web widget to the map data
        webView.setHtml(data.getvalue().decode())
        # Adds the map data to the QGroupBox layout
        self.map_frame.addWidget(webView)

        # A QToolButton is made to create an expanded map window when clicked
        self.expand_map_button = QtWidgets.QToolButton(self.attraction_QScrollArea_object)
        self.expand_map_button.setGeometry(690, 198, 94, 17)
        self.expand_map_button.setText("Expand Map ↗︎")

        # When this QToolButton is pressed, an expanded window of the object's coordinates is created
        self.expand_map_button.clicked.connect(self.show_expanded_map_window)

        # A QToolButton is created to open the website of an attraction in a new window when clicked
        self.website_button = QtWidgets.QToolButton(self.attraction_QScrollArea_object)
        self.website_button.setGeometry(786, 198, 94, 17)
        self.website_button.setText("Website ↗︎")

        # When this QToolButton is pressed, a redirect to the attraction's website occurs
        self.website_button.clicked.connect(lambda: webbrowser.open(str(attraction[12])))

        # A QFrame.Hline is created to organize different parts of the attraction object
        self.object_line = QtWidgets.QFrame(self.attraction_QScrollArea_object)
        self.object_line.setGeometry(QtCore.QRect(235, 110, 440, 10))
        self.object_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.object_line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # The QScrollArea's layout adds the attraction object to itself to display
        self.verticalLayout_3.addWidget(self.attraction_QScrollArea_object)
        return self.attraction_QScrollArea_object

    # A function that contols the addition and deletion of QScrollArea attraction objects
    def control_attractions_QScrollArea(self):
        global filtered_attractions_list

        # Removes any previously displayed result objects
        if (len(self.attractions_QScrollArea_widget_container.children()) > 0):
            attractions_QScrollArea_widget_list = self.attractions_QScrollArea_widget_container.children()
            for i in reversed(range(len(self.attractions_QScrollArea_widget_container.children()))):
                if i > 0:
                    attractions_QScrollArea_widget_list[i].deleteLater()

        # Adds all filtered result objects to the attractions_QScrollArea
        Ycoor = 0
        for index in range(len(filtered_attractions_list)):
            self.create_QScrollArea_object(Ycoor, filtered_attractions_list[index])
            Ycoor = Ycoor + 200
        self.attractions_QScrollArea.setWidget(self.attractions_QScrollArea_widget_container)

    # A function to rerun the suggesting algorithm, based on user changes. This function gets the entered preferences
    # in the state, city, and type QComboBoxes as well as the wheelchair accessibility, family friendly, and pet friendly
    # QCheckBoxes. Using the entered values, a request to the database is sent to create a list of attractions that
    # satisfy the user's preferences. Using the filtered attractions, attraction objects are created to display the
    # attractions.
    def get_current_filter_field_values(self, _):
        global filtered_attractions_list
        global location_and_filters_QGroupBox
        _translate = QtCore.QCoreApplication.translate

        # Choosing which state to filter by, based on the state dropdown menu choice
        if self.state_filter_QComboBox.currentText() == "No preference":
            current_selected_state = "None"
        else:
            current_selected_state = self.state_filter_QComboBox.currentText()

        # Choosing which city to filter by, based on the city dropdown menu choice
        if self.city_filter_QComboBox.currentText() == "No preference":
            current_selected_city = "None"
        else:
            current_selected_city = self.city_filter_QComboBox.currentText()

        # Choosing which container to filter by, based on the container dropdown menu choice
        if self.type_filter_QComboBox.currentText() == "No preference":
            current_selected_type = "None"
        else:
            current_selected_type = self.type_filter_QComboBox.currentText()

        # Choosing whether or not to filter by wheelchair accessibility, based on if its respective checkbox is checked
        current_checked_wheelchair_accessibility = self.wheelchair_access_filter_QCheckBox.isChecked()

        # Choosing whether or not to filter by family friendly, based on if its respective checkbox is checked
        current_checked_family_friendliness = self.family_friendly_filter_QCheckBox.isChecked()

        # Choosing whether or not to filter by pet friendly, based on if its respective checkbox is checked
        current_checked_pet_friendliness = self.pet_friendly_filter_QCheckBox.isChecked()

        # Choosing what attribute to sort by, based on the selection of the sorting dropdown menu
        current_sorter = self.sorting_QComboBox.currentText()

        # Creating a list of attributes to filter and sort by based on the entered attributes
        attribute_list = [str(current_selected_state), str(current_selected_city), str(current_selected_type),
                          str(current_checked_wheelchair_accessibility), str(current_checked_family_friendliness),
                          str(current_checked_pet_friendliness)]

        # Since database filters take a None keyword or a string name value, all "None" or "False" entered values are
        # converted to the accepted None keyword
        for index in range(len(attribute_list)):
            if (attribute_list[index] == "None" or attribute_list[index] == "False"):
                attribute_list[index] = None

        # All attractions are stored in a separate storage in order to retrieve all sources and references of all
        # attractions to later display in the sources tab of the application
        all_attractions = application_database.getAttractions(filters=application_filter_request.FilterRequest(None, None,
                                                                                                               None, None,
                                                                                                               None, None))

        # Filtering attractions based on the entered filter attributes. A request with the entered attributes is sent to
        # retrieve values from the PostgresSQL database. A dynamic database containing all satisfactory attractions is
        # formed. Changes in filters updates the filtered database based on the new set of filters
        filtered_attractions = application_database.getAttractions(
            filters=application_filter_request.FilterRequest(attribute_list[0], attribute_list[1], attribute_list[2],
                                                           attribute_list[3], attribute_list[4], attribute_list[5]))
        filtered_attractions_list = filtered_attractions

        # Selective display of singular or plural "Attraction" + "Found"
        if (len(filtered_attractions_list)) == 1:
            self.num_of_attractions_QLabel.setText((str(len(filtered_attractions_list))) + " Attraction Found")
        else:
            self.num_of_attractions_QLabel.setText(
                _translate("MainWindow", (str(len(filtered_attractions_list))) + " Attractions Found"))

        # Sort the filtered attractions
        self.sort_attractions()

        # Display the filtered and sorted attractions
        self.control_attractions_QScrollArea()

        # The distance from entered location and number of objects displayed are calculated. If the QComboBox specifying
        # desired distance is enabled (when both latitude and longitude are correctly entered) then distance is
        # calculated. Simultaenously, a QLabel is updated to reflect the number of objects being shown in the QScrollArea.
        if (self.radius_QComboBox.isEnabled()):
            global radius_checked
            # Holds the boolean value to whether the radius_QComoBox has been checked
            radius_checked = True

            # If a specific desired distance is specified, attractions not in a radius of that distance will be hidden.
            # This desired distance value will be compared with the distance calculated for every attraction in order to
            # determine if that attraction lies within the inputted radius.
            if (self.radius_QComboBox.currentText() != "Any distance"):
                # The total count of all attraction objects being displayed within attraction_QScrollArea
                count_of_objects_shown = len(self.attractions_QScrollArea_widget_container.children()) - 1


                for index in range(len(self.attractions_QScrollArea_widget_container.children())):
                    if index != 0:
                        object_distance_QLabel = self.attractions_QScrollArea_widget_container.children()[
                            index].findChild(QtWidgets.QLabel, 'locationAndDistance').text()
                        index_of_letter_m = object_distance_QLabel.index("miles")
                        index_of_hyphen = object_distance_QLabel.index("-")

                        if (float(object_distance_QLabel[(index_of_hyphen + 1):(index_of_letter_m - 1)]) < float(
                                self.radius_QComboBox.currentText()[10:12])):
                            self.attractions_QScrollArea_widget_container.children()[index].show()
                        else:
                            self.attractions_QScrollArea_widget_container.children()[index].hide()
                            count_of_objects_shown = count_of_objects_shown - 1

                # The QLabel displaying the total number of results is updated as the number of shown attractions changes
                if (count_of_objects_shown) == 1:
                    self.num_of_attractions_QLabel.setText((str(count_of_objects_shown)) + " Attraction Found")
                else:
                    self.num_of_attractions_QLabel.setText((str(count_of_objects_shown)) + " Attractions Found")
        attribute_list = [None, None, None, None, None, None]

        # Create an output report text file, based on the attributes the user selected
        with open('outputreport.txt', 'a') as f:
            stringAccessedTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            locationOfSpace = stringAccessedTime.index(" ")
            f.write("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
            f.write("Activity Logged Date: " + stringAccessedTime[
                                               :locationOfSpace] + " Time Of Action: " + stringAccessedTime[
                                                                                         (locationOfSpace + 1):])
            f.write("\n")
            f.write("Selected State: ")
            f.write(current_selected_state)
            f.write("\n")
            f.write("Selected City: ")
            f.write(current_selected_city)
            f.write("\n")
            f.write("Selected Type: ")
            f.write(current_selected_type)
            f.write("\n")
            f.write("Wheelchair Accessibility is Checked: ")
            f.write(str(current_checked_wheelchair_accessibility))
            f.write("\n")
            f.write("Family Friendliness is Checked: ")
            f.write(str(current_checked_family_friendliness))
            f.write("\n")
            f.write("Pet Friendliness is Checked: ")
            f.write(str(current_checked_pet_friendliness))
            f.write("\n")
            f.write("Currently sorting by: ")
            f.write(current_sorter)
            f.write("\n")
            for element in filtered_attractions_list:
                f.write("Filtered Attraction: " + "(id: " + str(element[0]) + ")" + ", " +
                        str(element[1]) + ", " + str(element[5]) + ", " + str(element[4]) + ", " + str(element[2]))
                f.write("\n")
            f.close()

        # Creating a text file, to properly source and credit each attraction
        # Used to create a file with all sources. Run only once and then comment out
        with open('Application Data and Documentation Files/sources.txt', 'w') as f:
            for attraction in all_attractions:
                f.write(str(attraction[1]) + ", " + str(attraction[4]) + ", " + str(attraction[3]) + " ")
                f.write("\n")
                f.write("Website: https://" + str(attraction[12]) + " ")
                f.write("\n")
                f.write("Attraction Image: " + str(attraction[15]) + " ")
                f.write("\n")
                f.write("\n")

    # The function to sort the displayed attractions, by some attribute (price, distance, busyness, rating)
    def sort_attractions(self):

        # A function to find the distance between an attraction and a given set of coordinates
        def calculate_distance_to_entered_location(data):
            return distance.distance(((self.latitude_input.text()), (self.longitude_input.text())),
                                     (data[13], data[14])).miles

        # Sort by nearest attractions
        if self.sorting_QComboBox.currentText() == "Nearest attractions":
            filtered_attractions_list.sort(key=calculate_distance_to_entered_location)

        # Sorting by lowest rating
        if self.sorting_QComboBox.currentText() == "Rating: Lowest to Highest":
            filtered_attractions_list.sort(key=itemgetter(8), reverse=False)

        # Sorting by highest rating
        if self.sorting_QComboBox.currentText() == "Rating: Highest to Lowest":
            filtered_attractions_list.sort(key=itemgetter(8), reverse=True)

        # Sorting by lowest price
        if self.sorting_QComboBox.currentText() == "Price: Lowest to Highest":
            filtered_attractions_list.sort(key=itemgetter(6), reverse=False)

        # Sorting by highest price
        if self.sorting_QComboBox.currentText() == "Price: Highest to Lowest":
            filtered_attractions_list.sort(key=itemgetter(6), reverse=True)

        # Sorting by lowest traffic
        if self.sorting_QComboBox.currentText() == "Traffic: Lowest to Highest":
            filtered_attractions_list.sort(key=itemgetter(7), reverse=False)

        # Sorting by highest traffic
        if self.sorting_QComboBox.currentText() == "Traffic: Highest to Lowest":
            filtered_attractions_list.sort(key=itemgetter(7), reverse=True)

    # Changes to bookmark icon when it is clicked
    def control_bookmarks(self, _):
        self.bookmark_icon = self.attraction_QScrollArea_object.sender().parent().findChild(QtWidgets.QToolButton,
                                                                                            'bookmark')

        # If the bookmark is not selected, change it to activated, change its icon, add its bookmark to the bookmarks tab
        if (self.bookmark_icon.property("unactivated") == True):
            self.bookmark_icon.setProperty("unactivated", False)
            self.bookmark_icon.setIcon(QtGui.QIcon("Application Pictures/Bookmark Icons/checked bookmark.png"))
            self.add_bookmark(_)
            if len(self.bookmarks_scrollArea_object_container.children()) == 2:
                self.num_of_bookmarks_QLabel.setText(
                    (str(len(self.bookmarks_scrollArea_object_container.children()) - 1) + " Total Bookmark Saved"))
            else:
                self.num_of_bookmarks_QLabel.setText(
                    (str(len(self.bookmarks_scrollArea_object_container.children()) - 1) + " Total Bookmarks Saved"))
            self.bookmark_icon.setIconSize(QtCore.QSize(1024, 1024))
            self.bookmarks_scrollArea.setWidget(self.bookmarks_scrollArea_object_container)

        # If the bookmark is selected, change it to unactivated, change its icon, add remove bookmark from the bookmarks tab
        else:
            self.bookmark_icon.setProperty("unactivated", True)
            self.bookmark_icon.setIcon(QtGui.QIcon("Application Pictures/Bookmark Icons/unchecked bookmark.png"))
            self.remove_bookmark(_)
            if len(self.bookmarks_scrollArea_object_container.children()) == 3:
                self.num_of_bookmarks_QLabel.setText(
                    (str(len(self.bookmarks_scrollArea_object_container.children()) - 2) + " Total Bookmark Saved"))
            else:
                self.num_of_bookmarks_QLabel.setText(
                    (str(len(self.bookmarks_scrollArea_object_container.children()) - 2) + " Total Bookmarks Saved"))
            self.bookmark_icon.setIconSize(QtCore.QSize(1024, 1024))
        self.bookmark_icon.setStyleSheet("QToolButton { background-color: transparent; border: 0px }");

    # A function ran to clear all bookmarks
    def clear_all_bookmarks(self, _):
        for object in self.bookmarks_scrollArea_object_container.children():
            try:
                attraction = object.findChild(QtWidgets.QLabel, 'attractionName').text()
                for object_2 in self.attractions_QScrollArea_widget_container.children():
                    try:
                        if (object_2.findChild(QtWidgets.QLabel, 'attractionName').text() == object.findChild(
                                QtWidgets.QLabel, 'attractionName').text()):
                            object_2.findChild(QtWidgets.QToolButton, 'bookmark').setIcon(
                                QtGui.QIcon("Application Pictures/Bookmark Icons/unchecked bookmark.png"))
                    except:
                        continue
                object.deleteLater()
            except:
                continue
        self.num_of_bookmarks_QLabel.setText("0 Total Bookmarks Saved")

    # A function for the code to remove a function
    def remove_bookmark(self, _):
        name = self.attraction_QScrollArea_object.sender().parent().findChild(QtWidgets.QLabel, 'attractionName').text()
        for object in self.bookmarks_scrollArea_object_container.children():
            try:
                if (object.findChild(QtWidgets.QLabel, 'attractionName').text() == name):
                    for object_2 in self.attractions_QScrollArea_widget_container.children():
                        try:
                            object_2.findChild(QtWidgets.QToolButton, 'bookmark').setIcon(
                                QtGui.QIcon("Application Pictures/Bookmark Icons/unchecked bookmark.png"))
                        except:
                            continue
                    object.deleteLater()
            except:
                continue

    # The function to add a new attraction to the bookmarks tab, with all of its attribute information
    def add_bookmark(self, _):
        attraction = (self.attraction_QScrollArea_object.sender().parent().findChild(QtWidgets.QLabel,
                                                                                     'attraction_info_QLabel').text()).strip(
            '][').split(',|')
        _translate = QtCore.QCoreApplication.translate

        # Creating an area for multiple bookmarks to be displayed, with a scrollbar
        self.bookmarks_tab_QScrollArea_object = QtWidgets.QGroupBox(self.bookmarks_scrollArea_object_container)
        self.bookmarks_tab_QScrollArea_object.setFixedSize(884, 220)
        self.bookmarks_tab_QScrollArea_object.setLayout(QtWidgets.QVBoxLayout())

        labelXPos = 230
        labelYPos = 25

        # Display the bookmarked attraction's title
        self.bookmarks_tab_attraction_title = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos, -5, 450,
                                                                 50)
        self.bookmarks_tab_attraction_title.setObjectName("attractionName")
        self.bookmarks_tab_attraction_title.setText((str(attraction[1])))

        # Display the bookmarked attraction's rating
        self.bookmarks_tab_rating_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos + 350, -5,
                                                             50, 50)
        self.bookmarks_tab_rating_label.setObjectName("rating")
        self.bookmarks_tab_rating_label.setText((str(attraction[8])))

        bookmark_object_min_star_rating = 5.0

        # Display different star icon based on its rating
        for i in range(10):
            if (float(attraction[8]) < bookmark_object_min_star_rating):
                bookmark_object_min_star_rating = bookmark_object_min_star_rating - 0.5
            else:
                self.rating_icon = QtWidgets.QLabel(self.bookmarks_tab_QScrollArea_object)
                self.rating_icon.setPixmap(
                    QtGui.QPixmap(
                        "./Application Pictures/Star Ratings/" + str(bookmark_object_min_star_rating) + " star.png"))
                self.rating_icon.setScaledContents(True)
                self.rating_icon.setFixedSize(85, 16)
                self.rating_icon.move(600, 12)
                self.rating_icon.show()
                break

        # Display the bookmarked attraction's location
        if (self.latitude_input.text() != "" and self.longitude_input.text() != "" and self.is_float(
                str(self.latitude_input.text())) and self.is_float(str(self.longitude_input.text()))):
            self.location_Qlabel = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos, labelYPos - 8, 350,
                                                      50)
            self.location_Qlabel.setObjectName("locationAndDistance")
            distanceFromUserLocation = distance.distance(((self.latitude_input.text()), (self.longitude_input.text())),
                                                         (attraction[13], attraction[14])).miles
            self.location_Qlabel.setText((str(attraction[4]) + ", " + str(attraction[3])) + " - " + str(
                '%.1f' % (distanceFromUserLocation)) + " miles away")
        else:
            self.bookmarks_tab_location_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos,
                                                                   labelYPos - 3, 200, 50)
            self.bookmarks_tab_location_label.setObjectName("locationAndDistance")
            self.bookmarks_tab_location_label.setText((str(attraction[4]) + ", " + str(attraction[3])))

        self.bookmarks_tab_type_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos,
                                                           labelYPos + 20, 200, 50)
        self.bookmarks_tab_type_label.setText((str(attraction[5])))
        self.bookmarks_tab_price_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos,
                                                            labelYPos + 40, 200, 50)

        # Display the bookmarked attraction's price
        if (str(attraction[6])) == '1':
            self.bookmarks_tab_price_label.setText("Price Level - $")
        elif (str(attraction[6])) == '2':
            self.bookmarks_tab_price_label.setText("Price Level - $$")
        else:
            self.bookmarks_tab_price_label.setText("Price Level - $$$")

        # Display the bookmarked attraction's busyness
        self.bookmarks_tab_busyness_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos,
                                                               labelYPos + 60, 200, 50)
        if (str(attraction[7])) == '1':
            self.bookmarks_tab_busyness_label.setText("Low Busyness")
        elif (str(attraction[7])) == '2':
            self.bookmarks_tab_busyness_label.setText("Moderately Busy")
        else:
            self.bookmarks_tab_busyness_label.setText("Very Busy")

        # Display the bookmarked attraction's wheelchair accessibility
        self.bookmarks_tab_wheelchair_accessibility_label = self.create_QLabel("bookmarks_tab_QScrollArea_object",
                                                                               labelXPos + 170, labelYPos + 20, 200,
                                                                               50)
        if ((attraction[9])):
            self.bookmarks_tab_wheelchair_accessibility_label.setText("Wheelchair Accessible? - Yes")
        else:
            self.bookmarks_tab_wheelchair_accessibility_label.setText("Wheelchair Accessible? - No")

        # Display the bookmarked attraction's family friendliness
        self.bookmarks_tab_family_friendly_label = self.create_QLabel("bookmarks_tab_QScrollArea_object",
                                                                      labelXPos + 170, labelYPos + 40, 200, 50)
        if ((attraction[10])):
            self.bookmarks_tab_family_friendly_label.setText("Family Friendly? - Yes")
        else:
            self.bookmarks_tab_family_friendly_label.setText("Family Friendly? - No")

        # Display the bookmarked attraction's pet friendliness
        self.bookmarks_tab_pet_friendly_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos + 170,
                                                                   labelYPos + 60, 200, 50)
        if ((attraction[11])):
            self.bookmarks_tab_family_friendly_label.setText("Pet Friendly? - Yes")
        else:
            self.bookmarks_tab_family_friendly_label.setText("Pet Friendly? - No")

        # Display the bookmarked attraction's coordinates
        self.bookmarks_tab_coordinate_location_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos,
                                                                          labelYPos + 80, 200, 50)
        self.bookmarks_tab_coordinate_location_label.setText(
            "Location: (" + str('%.3f' % (float(attraction[13]))) + "," + str('%.3f' % float((attraction[14]))) + ")")
        self.bookmarks_tab_coordinate_location_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", 0, 0, 200,
                                                                          50)
        self.bookmarks_tab_coordinate_location_label.setText(
            str('%.6f' % float(attraction[14])) + "," + str('%.6f' % float(attraction[13])))
        self.bookmarks_tab_coordinate_location_label.setObjectName("Location")
        self.bookmarks_tab_coordinate_location_label.hide()

        # Display the bookmarked attraction's brief description
        self.bookmarks_tab_description_label = self.create_QLabel("bookmarks_tab_QScrollArea_object", labelXPos,
                                                                  labelYPos + 93, 454, 125)
        self.bookmarks_tab_description_label.setWordWrap(True)
        self.bookmarks_tab_description_label.setText(("     " + str(attraction[2])))

        # Display the bookmarked attraction's image
        imageAddress = "./Attraction Pictures/" + str(attraction[0]) + " - " + str(attraction[4]) + ".jpg"
        self.bookmark_object_attraction_image = QtWidgets.QLabel(self.bookmarks_tab_QScrollArea_object)
        self.bookmark_object_attraction_image.setPixmap(QtGui.QPixmap(imageAddress))
        self.bookmark_object_attraction_image.setScaledContents(True)
        self.bookmark_object_attraction_image.setFixedSize(220, 220)
        self.bookmark_object_attraction_image.show()

        # Display the bookmarked attraction's bookmarked status
        self.bookmark_object_bookmark_icon = QtWidgets.QToolButton(self.bookmarks_tab_QScrollArea_object)
        self.bookmark_object_bookmark_icon.setObjectName("bookmark")
        self.bookmark_object_bookmark_icon.setProperty("unactivated", False)
        self.bookmark_object_bookmark_icon.setGeometry(10, 10, 30, 30)
        self.bookmark_object_bookmark_icon.setIcon(
            QtGui.QIcon("Application Pictures/Bookmark Icons/checked bookmark.png"))
        self.bookmark_object_bookmark_icon.setIconSize(QtCore.QSize(512, 512))
        self.bookmark_object_bookmark_icon.setStyleSheet("QToolButton { background-color: transparent; border: 0px }");
        self.bookmark_object_bookmark_icon.clicked.connect(self.control_bookmarks)

        # Display the bookmarked attraction's map window
        self.bookmark_object_map_container = QtWidgets.QGroupBox(self.bookmarks_tab_QScrollArea_object)
        self.bookmark_object_map_container.setGeometry(QtCore.QRect(675, -10, 220, 220))
        self.bookmark_object_map_container.setEnabled(True)
        self.bookmark_object_map_container.setFlat(True)
        self.bookmark_object_map_frame = QtWidgets.QVBoxLayout(self.bookmark_object_map_container)

        # The bookmarked attraction's map is centered around its coordinate
        coordinate = (float(attraction[13]), float(attraction[14]))
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
        self.bookmark_object_map_frame.addWidget(webView)

        # Creating a button to expand the button
        self.bookmark_object_expand_map_button = QtWidgets.QToolButton(self.bookmarks_tab_QScrollArea_object)
        self.bookmark_object_expand_map_button.setGeometry(690, 198, 94, 17)
        self.bookmark_object_expand_map_button.setText("Expand Map ↗︎")
        self.bookmark_object_expand_map_button.clicked.connect(self.show_expanded_map_window)

        # Create a button to open the attraction's website
        self.bookmark_object_website_redirect = QtWidgets.QToolButton(self.bookmarks_tab_QScrollArea_object)
        self.bookmark_object_website_redirect.setGeometry(786, 198, 94, 17)
        self.bookmark_object_website_redirect.setText(_translate("MainWindow", "Website ↗︎"))
        self.bookmark_object_website_redirect.clicked.connect(lambda: webbrowser.open(str(attraction[12])))

        # Create a line on the bookmark tab
        self.bookmark_object_line = QtWidgets.QFrame(self.bookmarks_tab_QScrollArea_object)
        self.bookmark_object_line.setGeometry(QtCore.QRect(235, 138, 440, 10))
        self.bookmark_object_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.bookmark_object_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.bookmarks_container_vertical_layout.addWidget(self.bookmarks_tab_QScrollArea_object)

    # Detect a change in radius
    def detect_change_in_desired_distance(self, _):
        global radius_checked
        if (radius_checked):
            count_of_objects_shown = len(self.attractions_QScrollArea_widget_container.children()) - 1
            if (self.radius_QComboBox.isEnabled()):
                for index in range(len(self.attractions_QScrollArea_widget_container.children())):
                    if index != 0:
                        object_distance_QLabel = self.attractions_QScrollArea_widget_container.children()[
                            index].findChild(QtWidgets.QLabel, 'locationAndDistance').text()

                        index_of_letter_m = object_distance_QLabel.index("m")
                        index_of_hyphen = object_distance_QLabel.index("-")
                        if (self.radius_QComboBox.currentText() != "Any distance"):
                            if (float(object_distance_QLabel[(index_of_hyphen + 1):(index_of_letter_m - 1)]) < float(
                                    self.radius_QComboBox.currentText()[10:12])):
                                self.attractions_QScrollArea_widget_container.children()[index].show()
                            else:
                                self.attractions_QScrollArea_widget_container.children()[index].hide()
                                count_of_objects_shown = count_of_objects_shown - 1
                        else:
                            self.attractions_QScrollArea_widget_container.children()[index].show()
                if (count_of_objects_shown) == 1:
                    self.num_of_attractions_QLabel.setText((str(count_of_objects_shown)) + " Attraction Found")
                else:
                    self.num_of_attractions_QLabel.setText((str(count_of_objects_shown)) + " Attractions Found")

    # A function to check if latitude and longitude are filled, then allowing the user to access functions related to their location
    def check_if_location_fields_are_filled(self, _):
        if (self.latitude_input.text() != "" and self.longitude_input.text() != "" and self.is_float(
                str(self.latitude_input.text())) and self.is_float(str(self.longitude_input.text()))):
            self.radius_QComboBox.setEnabled(True)
            self.show_entered_location_map_button.setEnabled((True))
            try:
                if (float(self.latitude_input.text()) != float(ipInfo.__getattr__("location")["latitude"]) or
                        float(self.longitude_input.text()) != float(ipInfo.__getattr__("location")["longitude"])):
                    location = geolocator.reverse((self.latitude_input.text()) + "," + (self.longitude_input.text()))
                    address = location.raw['address']
                    city = address.get('city', '')
                    state = address.get('state', '')
                    if (city != "" and city != " "):
                        self.current_location_QLabel.setText(str(city) + ", " + str(state))
                    elif (city == "" and state == ""):
                        self.current_location_QLabel.setText("Please enter a valid location")
                    else:
                        self.current_location_QLabel.setText(str(state))
                else:
                    self.current_location_QLabel.setText("Please enter a valid location")
            except:
                self.current_location_QLabel.setText("Please enter a valid location")
        else:
            self.radius_QComboBox.setEnabled(False)
            self.show_entered_location_map_button.setEnabled((False))

    # The function ran to obtain user's latitude and longitude, when prompted
    def find_current_location(self, _):
        self.latitude_input.setText(str(ipInfo.__getattr__("location")["latitude"]))
        self.longitude_input.setText(str(ipInfo.__getattr__("location")["longitude"]))
        self.check_if_location_fields_are_filled
        self.current_location_QLabel.setText(str(ipInfo.__getattr__("location")["city"]) + ", " + str(
            ipInfo.__getattr__("location")["region"]["name"]))

    # A function with logic to determine if the help menu should be shown, toggled on/off by the user
    def control_help_menu_display(self, _):
        global help_menu_QGroupBox
        global click_count

        if (click_count != 1):
            click_count = click_count + 1
            self.help_menu_groupBox.show()
        else:
            self.help_menu_groupBox.hide()
            click_count = 0

    # Showing documentation when clicked
    def read_documentation(self, _):
        # Creating the window that shows documentation
        self.documentation_window = QtWidgets.QLabel()
        self.documentation_window.setObjectName("documentation_window")
        self.documentation_window.setFixedSize(800, 600)
        self.documentation_window.setWindowTitle("Read Documentation")

        self.documentation_window_central_widget = QtWidgets.QWidget(self.documentation_window)
        self.documentation_window_central_widget.setFixedSize(800, 600)

        self.documentation_window_QGroupBox = QtWidgets.QGroupBox(self.documentation_window_central_widget)
        self.documentation_window_QGroupBox.setFixedSize(784, 554)
        self.documentation_window_QGroupBox.move(8, 35)
        self.documentation_window_QGroupBox.setEnabled(True)
        self.documentation_window_QGroupBox.setFlat(True)
        self.documentation_window_QGroupBox.setObjectName("documentationTextContainer")

        self.documentation_QLabel = self.create_QLabel("documentation_window_QGroupBox", 343, 0, 200, 50)
        self.documentation_QLabel.setText("Documentation")
        self.documentation_QLabel.setObjectName("documentationTitle")

        filename = os.path.abspath('Application Data and Documentation Files/FBLA Manual + Documentation.pdf')
        view = QtWebEngineWidgets.QWebEngineView(self.documentation_window_QGroupBox)
        settings = view.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        url = QtCore.QUrl.fromLocalFile(filename)
        view.load(url)
        view.resize(780, 550)
        view.move(2,2)
        view.show()
        self.documentation_window.show()

    def show_QandA_window(self, _):

        all_questions = [["Does the attraction finder cover all states?", "Yes, this application suggests attractions from all 50 states, covering each state’s largest cities."],
                         ["Can I download my suggested attractions for further use?", "Yes, when running our application, we generate an output report for your further use."],
                         ["How can I suggest an edit to an attraction?", "On the main window, the help menu offers you the ability to create a report. This gives you the option to tell us of an error by generating a user report."],
                         ["I need some more information on the program.", "Sure, we have created a file for documentation of our program. Visit the help menu for program documentation."],
                         ["How do I use the ‘my location’ feature?", "Our application is able to take your location and use it when looking for nearest attractions. By changing the sorting dropdown in the top right, you can sort attractions based on their distance to you. Each displayed attraction will also tell you its physical distance from you."],
                         ["Why do some features not work?", "Most likely, you may have some wifi problems that prevent full use of internet features, such as finding your location and redirecting you to each attraction’s homepage. \nYou can also generate a user report in the event you encounter an error. \nWe also have created a documentation file that covers required libraries, system requirements, and more."],
                         ["How do I find attractions close to where I am?", "You can do this by navigating to the location details window and selecting an option in the dropout menu under the area labelled \"Desired Distance From You.\""],
                         ["How do I filter for whether attractions are pet friendly?", "You can do this by navigating to the \"Filter By:\" area and checking the box on the pet friendly option."],
                         ["How do I find out how expensive it is to visit an attraction?", "This may be done by navigating to the center area where all the attractions are displayed and looking at the price rating. The price of an attraction is displayed as $, $$ or $$$."]]


        self.QandA_window = QtWidgets.QLabel()
        self.QandA_window.setObjectName("QandA_window")
        self.QandA_window.setFixedSize(800, 600)
        self.QandA_window.setWindowTitle("Frequently Asked Questions and their Answers")

        self.QandA_window_central_widget = QtWidgets.QWidget(self.QandA_window)
        self.QandA_window_central_widget.setFixedSize(800, 600)

        self.QandA_search_bar = QtWidgets.QLineEdit(self.QandA_window_central_widget)
        self.QandA_search_bar.setObjectName("search_bar")
        self.QandA_search_bar.setStyleSheet("font: 14px")
        self.QandA_search_bar.setGeometry(QtCore.QRect(200, 8, 301, 30))
        self.QandA_search_bar.setPlaceholderText("Search by Keyword")

        self.QandA_search_attractions_button = QtWidgets.QToolButton(self.QandA_window_central_widget)
        self.QandA_search_attractions_button.setGeometry(QtCore.QRect(500, 9, 55, 28))
        self.QandA_search_attractions_button.setText("Search")
        self.QandA_search_attractions_button.clicked.connect(self.search_QandA)

        self.QandA_search_bar_icon = QtWidgets.QLabel(self.QandA_window_central_widget)
        self.QandA_search_bar_icon.setPixmap(QtGui.QPixmap("Application Pictures/magnifyingIcon.png"))
        self.QandA_search_bar_icon.setScaledContents(True)
        self.QandA_search_bar_icon.setFixedSize(25, 25)
        self.QandA_search_bar_icon.move(171, 10)
        self.QandA_search_bar_icon.show()


        self.QandA_clear_search_bar_button = QtWidgets.QToolButton(self.QandA_window_central_widget)
        self.QandA_clear_search_bar_button.setGeometry(QtCore.QRect(554, 9, 55, 28))
        self.QandA_clear_search_bar_button.setText("Clear")
        self.QandA_clear_search_bar_button.clicked.connect(self.clear_QandA_search_bar)


        scroll = QtWidgets.QScrollArea(self.QandA_window_central_widget)
        content = QtWidgets.QWidget()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.resize(784, 500)
        scroll.move(8, 100)
        vlay = QtWidgets.QVBoxLayout(content)
        for element in all_questions:
            box = CollapsibleBox(element[0])
            box.thetext = element[0]
            vlay.addWidget(box)
            lay = QtWidgets.QVBoxLayout()

            label = QtWidgets.QLabel(element[1])
            #label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)
            width = 0
            if len(element[1]) <= 110:
                width = 30
            if len(element[1]) < 200 and len(element[1]) > 110:
                width = 60
            if len(element[1]) >= 200:
                width = 100
            label.setFixedSize(700, width)
            print(len(element[1]))
            lay.addWidget(label)

            box.setContentLayout(lay)
        vlay.addStretch()

        self.QandA_no_questions_match = QtWidgets.QLabel(self.QandA_window_central_widget)
        self.QandA_no_questions_match.setFixedSize(500, 50)
        self.QandA_no_questions_match.move(200, 150)


        # self.QandA_window_QGroupBox = QtWidgets.QGroupBox(self.QandA_window_central_widget)
        # self.QandA_window_QGroupBox.setFixedSize(784, 554)
        # self.QandA_window_QGroupBox.move(8, 35)
        # self.QandA_window_QGroupBox.setEnabled(True)
        # self.QandA_window_QGroupBox.setFlat(True)
        # self.QandA_window_QGroupBox.setObjectName("QandATextContainer")
        #
        # self.QandA_QLabel = self.create_QLabel("QandA_window_QGroupBox", 343, 0, 200, 50)
        # self.QandA_QLabel.setText("QandA")
        # self.QandA_QLabel.setObjectName("QandATitle")
        #
        # self.QandA = QtWidgets.QPlainTextEdit(self.QandA_window_QGroupBox)
        # self.QandA.setObjectName("QandA")
        # self.QandA.setFixedSize(780, 550)
        # self.QandA.move(2, 2)
        # text = open('qanda.txt').read()
        # self.QandA.setPlainText(text)
        # self.QandA.setReadOnly(True)
        self.QandA_window.show()

    # Show the maps window for around the user's location, based on their latitude and longitude
    def show_entered_location_map_window(self, _):
        if (self.latitude_input.text() != "" and self.longitude_input.text() != "" and self.is_float(
                str(self.latitude_input.text())) and self.is_float(str(self.longitude_input.text()))):
            self.window = QtWidgets.QLabel()
            self.window.setFixedSize(800, 600)
            self.window.setWindowTitle("Location Map View")
            self.window.setObjectName("location_map_window")

            self.central_widget = QtWidgets.QWidget(self.window)
            self.central_widget.setFixedSize(800, 600)
            self.central_widget.setObjectName("central_widget")

            self.expanded_map_container = QtWidgets.QGroupBox(self.central_widget)
            self.expanded_map_container.setObjectName("expanded_map")
            self.expanded_map_container.setFixedSize(820, 620)
            self.expanded_map_container.move(-10, -10)
            self.expanded_map_container.setEnabled(True)
            self.expanded_map_container.setFlat(True)

            self.map_frame = QtWidgets.QVBoxLayout(self.expanded_map_container)

            # The map window is centered around the latitude and longitude in their respective inputs
            coordinate = (float(self.latitude_input.text()), float(self.longitude_input.text()))
            expanded_map = folium.Map(
                zoom_start=15,
                location=coordinate,
                popup="test"
            )
            folium.Marker(
                location=coordinate
            ).add_to(expanded_map)

            # save map data to data object
            data = io.BytesIO()
            expanded_map.save(data, close_file=False)
            webView = QWebEngineView()
            webView.setHtml(data.getvalue().decode())

            self.map_frame.addWidget(webView)
            self.window.show()


    # Allowing the user to open an enlarged map window
    def show_expanded_map_window(self, _):
        self.window = QtWidgets.QLabel()
        self.window.setFixedSize(800, 600)
        self.window.setWindowTitle("Expanded Map View")
        self.window.setObjectName("expanded_map_window")

        self.central_widget = QtWidgets.QWidget(self.window)
        self.central_widget.setFixedSize(800, 600)
        self.central_widget.setObjectName("central_widget")

        self.expanded_map_container = QtWidgets.QGroupBox(self.central_widget)
        self.expanded_map_container.setObjectName("expanded_map")
        self.expanded_map_container.setFixedSize(820, 620)
        self.expanded_map_container.move(-10, -10)
        self.expanded_map_container.setEnabled(True)
        self.expanded_map_container.setFlat(True)

        self.map_frame = QtWidgets.QVBoxLayout(self.expanded_map_container)
        object_coordinate = self.attraction_QScrollArea_object.sender().parent().findChild(QtWidgets.QLabel,
                                                                                           'Location').text()
        index_of_comma = object_coordinate.index(",")
        long = float(object_coordinate[:index_of_comma])
        lat = float(object_coordinate[(index_of_comma + 1):])
        coordinate = (lat, long)
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

        self.map_frame.addWidget(webView)
        self.window.show()

    # Displaying results based on keywords when search bar is used
    def search_attractions(self, _):
        count_of_objects_shown = len(self.attractions_QScrollArea_widget_container.children()) - 1

        # If the search bar keywords match the name of attraction, it will be displayed as a suggested attraction
        for index in range(len(self.attractions_QScrollArea_widget_container.children())):

            if index != 0:
                if (self.search_bar.text().lower() in self.attractions_QScrollArea_widget_container.children()[
                    index].findChild(QtWidgets.QLabel, 'attractionName').text().lower()):
                    self.attractions_QScrollArea_widget_container.children()[index].show()
                else:
                    self.attractions_QScrollArea_widget_container.children()[index].hide()
                    count_of_objects_shown = count_of_objects_shown - 1

        # Display either singular or plural "Attraction"
        if (count_of_objects_shown) == 1:
            self.num_of_attractions_QLabel.setText((str(count_of_objects_shown)) + " Attraction Found")
        else:
            self.num_of_attractions_QLabel.setText((str(count_of_objects_shown)) + " Attractions Found")

    # A function to clear the searchbar
    def clear_find_attractions_search_bar(self, _):
        self.search_bar.setText("")
        for index in range(len(self.attractions_QScrollArea_widget_container.children())):
            # Display either singular or plural "Attraction"
            if index != 0:
                self.attractions_QScrollArea_widget_container.children()[index].show()
                if len(self.attractions_QScrollArea_widget_container.children()) == 2:
                    self.num_of_attractions_QLabel.setText(
                        (str(len(self.attractions_QScrollArea_widget_container.children()) - 1) + " Attraction Found"))
                else:
                    self.num_of_attractions_QLabel.setText(
                        (str(len(self.attractions_QScrollArea_widget_container.children()) - 1) + " Attractions Found"))

    # Another searchbar, enabled for the bookmarks tab
    def search_bookmarks(self, _):
        for index in range(len(self.bookmarks_scrollArea_object_container.children())):
            if index != 0:
                if (self.bookmarks_tab_search_bar.text().lower() in
                        self.bookmarks_scrollArea_object_container.children()[index].findChild(QtWidgets.QLabel,
                                                                                               'attractionName').text().lower()):
                    self.bookmarks_scrollArea_object_container.children()[index].show()
                else:
                    self.bookmarks_scrollArea_object_container.children()[index].hide()

    # The ability to clear the search bar in the bookmarks tab
    def clear_bookmarks_tab_search_bar(self, _):
        self.bookmarks_tab_search_bar.setText("")
        for index in range(len(self.bookmarks_scrollArea_object_container.children())):
            if index != 0:
                self.bookmarks_scrollArea_object_container.children()[index].show()

    # The ability to search for questions in the QnA menu
    def search_QandA(self, _):
        number_of_question_shown = len(self.QandA_window_central_widget.children()[4].children()[0].children()[0].children()) - 1
        for index in range(len(self.QandA_window_central_widget.children()[4].children()[0].children()[0].children())):
            if index != 0:
                if (self.QandA_search_bar.text().lower()) in (self.QandA_window_central_widget.children()[4].children()[0].children()[0].findChildren(CollapsibleBox)[index-1].thetext.lower()):
                    self.QandA_window_central_widget.children()[4].children()[0].children()[0].children()[index].show()
                else:
                    self.QandA_window_central_widget.children()[4].children()[0].children()[0].children()[index].hide()
                    number_of_question_shown = number_of_question_shown - 1

        if number_of_question_shown == 0:
            self.QandA_no_questions_match.setText("Sorry, we couldn't find any questions related to your search.")
        else:
            self.QandA_no_questions_match.setText("")


    # The ability to clear the search bar in the QnA menu
    def clear_QandA_search_bar(self, _):
        self.QandA_search_bar.setText("")
        for index in range(len(self.QandA_window_central_widget.children()[4].children()[0].children()[0].children())):
            if index != 0:
                self.QandA_window_central_widget.children()[4].children()[0].children()[0].children()[index].show()
        self.QandA_no_questions_match.setText("")

    # The code to create a user report text file
    def create_report_file(self, _):
        path = "./User Reports"
        directory = os.listdir(path)

        # Creating the first user report, in the correct file location
        if len(directory) == 0:
            fileName = 'User Report 1'
            fileLocation = os.path.join(path, fileName)

            # The user report is generated based on the information the user typed in the report window
            with open(fileLocation, 'w') as f:
                f.write(
                    "User Information: " + "Full Name - " + self.name_field.text() + "Email - " + self.email_field.text())
                f.write("\n")
                f.write(self.report_topic_field.text())
                f.write("\n")
                f.write(self.user_report_field.toPlainText())
                f.write("\n")
                f.write(self.output_logs.toPlainText())
                f.close()

        # Creation of more user reports, in the correct file location
        else:
            fileName = ('User Report ' + (str(len(directory) + 1)))
            fileLocation = os.path.join(path, fileName)

            # The user report is generated based on the information the user typed in the report window
            with open(fileLocation, 'w') as f:
                f.write(
                    "User Information: " + "Full Name - " + self.name_field.text() + "Email - " + self.email_field.text())
                f.write("\n")
                f.write(self.report_topic_field.text())
                f.write("\n")
                f.write(self.user_report_field.toPlainText())
                f.write("\n")
                f.write(self.output_logs.toPlainText())
                f.close()
        # After generating a user report, close the report window
        self.report_window.close()

    # The window that enables the user to create a user report
    def create_user_report(self, _):

        # Creating the report window
        self.report_window = QtWidgets.QLabel()
        self.report_window.setObjectName("create_user_report_window")
        self.report_window.setFixedSize(800, 600)
        self.report_window.setWindowTitle("Create a Report")

        self.report_window_central_widget = QtWidgets.QWidget(self.report_window)
        self.report_window_central_widget.setFixedSize(800, 600)

        # Creating the area for report labels
        self.report_window_groupBox = QtWidgets.QGroupBox(self.report_window_central_widget)
        self.report_window_groupBox.setFixedSize(800, 600)
        self.report_window_groupBox.setEnabled(True)
        self.report_window_groupBox.setFlat(True)

        # Displaying what the user has searched for, their output logs
        self.output_log_QLabel = self.create_QLabel("report_window_groupBox", 8, 0, 200, 50)
        self.output_log_QLabel.setObjectName("user_report_window_title")
        self.output_log_QLabel.setText("Action Log Report:")

        self.output_logs = QtWidgets.QPlainTextEdit(self.report_window_groupBox)
        self.output_logs.setFixedSize(784, 250)
        self.output_logs.move(8, 35)
        text = open('outputreport.txt').read()
        self.output_logs.setPlainText(text)
        self.output_logs.setReadOnly(True)

        # Labels for where to enter the user's name
        self.name_QLabel = self.create_QLabel("report_window_groupBox", 8, 275, 200, 50)
        self.name_QLabel.setObjectName("user_report_window_field_labels")
        self.name_QLabel.setText("Full Name:")

        self.name_field = QtWidgets.QLineEdit(self.report_window_groupBox)
        self.name_field.setFixedSize(387, 25)
        self.name_field.move(8, 310)
        self.name_field.setPlaceholderText(" Enter your full name here")
        # self.name_field.selectionChanged.connect(lambda: self.name_field.setSelection(0, 0))

        # Labels for where to enter the user's email address
        self.email_QLabel = self.create_QLabel("report_window_groupBox", 404, 275, 200, 50)
        self.email_QLabel.setObjectName("user_report_window_field_labels")
        self.email_QLabel.setText("Email Address:")

        self.email_field = QtWidgets.QLineEdit(self.report_window_groupBox)
        self.email_field.setFixedSize(387, 25)
        self.email_field.move(404, 310)
        self.email_field.setPlaceholderText(" Enter your email address here")
        # self.email_field.selectionChanged.connect(lambda: self.email_field.setSelection(0, 0))

        # Labels for where to enter the topic of the report
        self.report_topic_QLabel = self.create_QLabel("report_window_groupBox", 8, 325, 200, 50)
        self.report_topic_QLabel.setObjectName("user_report_window_field_labels")
        self.report_topic_QLabel.setText("Title:")

        self.report_topic_field = QtWidgets.QLineEdit(self.report_window_groupBox)
        self.report_topic_field.setFixedSize(784, 25)
        self.report_topic_field.move(8, 360)
        self.report_topic_field.setPlaceholderText(" Provide a short title for the issue/report")
        # self.report_topic_field.selectionChanged.connect(lambda: self.report_topic_field.setSelection(0, 0))

        # Labels for where to enter a description of the report
        self.user_report_QLabel = self.create_QLabel("report_window_groupBox", 8, 375, 200, 50)
        self.user_report_QLabel.setObjectName("user_report_window_field_labels")
        self.user_report_QLabel.setText("Description:")

        self.user_report_field = QtWidgets.QPlainTextEdit(self.report_window_groupBox)
        self.user_report_field.setFixedSize(784, 160)
        self.user_report_field.move(8, 410)
        self.user_report_field.setPlaceholderText("Provide a detailed description of the problem you are facing. "
                                                  " Include any actions made prior to the issue arising and the  resulting erroneous output. "
                                                  " If the report is created to inform of incorrect data, provide the attraction name and details about the data.")

        # The button to submit the user report
        self.submit_button = QtWidgets.QToolButton(self.report_window_groupBox)
        self.submit_button.setGeometry(640, 575, 150, 20)
        self.submit_button.setText("Submit")
        self.submit_button.clicked.connect(self.create_report_file)

        self.report_window.show()

    # A function to check if an input is a float, used for latitude/longitude container validation
    def is_float(self, num):
        # if the input can be turned into a float, return True for this isfloat function
        try:
            float(num)
            return True

        # if the input returns a Value Error when trying to be converted into a float, return False
        except ValueError:
            return False

    # The feature in which state, city or container options are not available until a parent is chosen
    def title_window_input_dependencies(self, _):

        # If the user has selected a state on the title page:
        if (self.title_window_state_input.currentText() != "Select a State"):
            # Enable use of the city dropdown
            self.title_window_city_input.setEnabled(True)
            # Hide the warning that says the state is not selected
            self.title_window_state_unselected_error_label.hide()

            # If the user has selected a city on the title page:
            if (self.title_window_city_input.currentText() != "Select a City"):
                # Enable use of the container dropdown
                self.title_window_type_input.setEnabled(True)
                # Hide the warning that says the city is not selected
                self.title_window_city_unselected_error_label.hide()

            # If city is not selected:
            else:
                # Disable use of the container dropdown
                self.title_window_type_input.setEnabled(False)
                # Reset the selected container
                self.title_window_type_input.setCurrentText("Select a Type")

        # If the state is not selected
        else:
            # Disable use of the city dropdown
            self.title_window_city_input.setEnabled(False)
            # Reset any selections for city and container dropdowns
            self.title_window_type_input.setCurrentText("Select a Type")
            self.title_window_city_input.setCurrentText("Select a City")

    # When the user clicks the search button on the title page, check if both state and city are selected
    def state_and_city_is_selected(self, _):
        # If state is not selected, show the warning that informs the user of so
        if self.title_window_state_input.currentText() == "Select a State":
            self.title_window_state_unselected_error_label.show()
        # If city is not selected, show the warning that informs the user of so
        if self.title_window_city_input.currentText() == "Select a City":
            self.title_window_city_unselected_error_label.show()
        # If both state and city are selected, run the search algorithm
        if (self.title_window_state_input.currentText() != "Select a State") and (
                self.title_window_city_input.currentText() != "Select a City"):
            self.change_to_search_attractions_window(self)

    # The window change from title to the main window, with user selected attributes carrying over
    def change_to_search_attractions_window(self, _):

        # Carry over the title's selection of state, city, container and searchbar to the main window
        title_selected_state = self.title_window_state_input.currentText()
        title_selected_city = self.title_window_city_input.currentText()
        title_selected_type = self.title_window_type_input.currentText()
        title_search_input = self.title_window_search_bar.text()

        # Change the displayed window from title page to main window
        self.title_window_central_widget.deleteLater()
        ui.setup_application_window(MainWindow)
        self.find_current_location(_)

        # On the main window, set the state, city, container and searchbar to the selections on the title page
        self.state_filter_QComboBox.setCurrentText(title_selected_state)
        self.city_filter_QComboBox.addItems(
            self.state_filter_QComboBox.itemData(self.state_filter_QComboBox.findText(title_selected_state)))
        self.city_filter_QComboBox.setCurrentText(title_selected_city)
        self.city_filter_QComboBox.removeItem(0)
        self.type_filter_QComboBox.setCurrentText(title_selected_type)
        self.search_bar.setText(title_search_input)
        self.get_current_filter_field_values(_)
        self.search_attractions(_)

    # Switching to the bookmarks tab
    def change_to_bookmarks_tab(self, _):
        self.title_window_central_widget.deleteLater()
        ui.setup_application_window(MainWindow)
        self.tab_widget.setCurrentIndex(1)

    # Switching to the sources tab
    def change_to_sources_tab(self, _):
        self.title_window_central_widget.deleteLater()
        ui.setup_application_window(MainWindow)
        self.tab_widget.setCurrentIndex(2)

    # Everything needed to set up and display the title page
    def setup_title_window(self, MainWindow):
        MainWindow.setWindowTitle("Traveler")
        MainWindow.setFixedSize(1150, 645)

        # Create widget container for window
        self.title_window_central_widget = QtWidgets.QWidget(MainWindow)
        self.title_window_central_widget.setFixedSize(1150, 645)
        # Set background image of the widget container
        self.title_window_background = QtWidgets.QLabel(self.title_window_central_widget)
        self.title_window_background.setFixedSize(1150, 645)
        self.title_window_background.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowPicture.jpeg"))
        self.title_window_background.setScaledContents(True)
        self.title_window_background.show()

        # Show logo image on the title window
        self.title_window_logo = QtWidgets.QLabel(self.title_window_central_widget)
        self.title_window_logo.setFixedSize(500, 500)
        self.title_window_logo.move(310, 50)
        self.title_window_logo.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowLogo.png"))
        self.title_window_logo.setScaledContents(True)
        self.title_window_logo.show()

        # Adding drop down menus for states, with its cities
        self.title_window_state_input = self.create_QComboBox("title_window_central_widget", 150, 250, 150, 50)
        self.title_window_state_input.setStyleSheet("QComboBox"
                                                    "{"
                                                    "color: white;"
                                                    "border: 3px solid;"
                                                    "border-color: rgb(245, 245, 245);"
                                                    "background-color: rgba(20, 52, 124, 170);"
                                                    "}"
                                                    "QComboBox QAbstractItemView {"
                                                    "background-color: #3C4571;"
                                                    "color: white;"
                                                    "width: 200px;"
                                                    "selection-background-color: #0060AC;"
                                                    "}"
                                                    )
        self.title_window_state_input.setFont(QtGui.QFont("Arial", 14))
        self.title_window_state_input.addItem("Select a State", ["Select a City"])
        self.title_window_state_input.addItem("Alabama",
                                              ["Select a City", "Huntsville", "Birmingham", "Montgomery", "Mobile",
                                               "Tuscaloosa"])
        self.title_window_state_input.addItem("Alaska",
                                              ["Select a City", "Anchorage", "Juneau", "Fairbanks", "Badger",
                                               "Knik-Fairview"])
        self.title_window_state_input.addItem("Arizona",
                                              ["Select a City", "Phoenix", "Tucson", "Sedona", "Mesa", "Scottsdale"])
        self.title_window_state_input.addItem("Arkansas",
                                              ["Select a City", "Little Rock", "Fort Smith", "Fayetteville",
                                               "Springsdale",
                                               "Jonesboro"])
        self.title_window_state_input.addItem("California",
                                              ["Select a City", "San Francisco", "Los Angeles", "San Diego", "San Jose",
                                               "Fresno"])
        self.title_window_state_input.addItem("Colorado",
                                              ["Select a City", "Denver", "Colorado Springs", "Pueblo", "Aspen",
                                               "Fort Collins"])
        self.title_window_state_input.addItem("Connecticut",
                                              ["Select a City", "Bridgeport", "Hartford", "New Haven", "Stamford",
                                               "Waterbury"])
        self.title_window_state_input.addItem("Delaware",
                                              ["Select a City", "Dover", "Wilmington", "Middletown", "New Castle",
                                               "Newark"])
        self.title_window_state_input.addItem("Florida",
                                              ["Select a City", "Orlando", "Tallahassee", "Jacksonville", "Miami",
                                               "Tampa"])
        self.title_window_state_input.addItem("Georgia",
                                              ["Select a City", "Atlanta", "Columbus", "Athens", "Augusta", "Savannah"])
        self.title_window_state_input.addItem("Hawaii",
                                              ["Select a City", "Kailua", "Waipahu", "Honolulu", "Hilo", "Kahului"])
        self.title_window_state_input.addItem("Idaho",
                                              ["Select a City", "Idaho Falls", "Boise", "Twin Falls", "Pocatello",
                                               "Coeur d'alene"])
        self.title_window_state_input.addItem("Illinois",
                                              ["Select a City", "Chicago", "Naperville", "St. Louis", "Rockford",
                                               "Springfield"])
        self.title_window_state_input.addItem("Indiana",
                                              ["Select a City", "Indianapolis", "Gary", "Lafayette", "Evansville",
                                               "Fort Wayne"])
        self.title_window_state_input.addItem("Iowa",
                                              ["Select a City", "Des Moines", "Waterloo", "Dubuque", "Cedar Rapids",
                                               "Davenport"])
        self.title_window_state_input.addItem("Kansas", ["Select a City", "Olathe", "Topeka", "Wichita", "Lawrence",
                                                         "Kansas City"])
        self.title_window_state_input.addItem("Kentucky",
                                              ["Select a City", "Lexington", "Bowling Green", "Louisville", "Florence",
                                               "Jeffersontown"])
        self.title_window_state_input.addItem("Louisiana", ["Select a City", "Alexandria", "Shreveport", "New Orleans",
                                                            "Baton Rouge",
                                                            "Lafayette"])
        self.title_window_state_input.addItem("Maine",
                                              ["Select a City", "Portland", "Bangor", "Camden", "Augusta", "Brunswick"])
        self.title_window_state_input.addItem("Maryland",
                                              ["Select a City", "Washington D.C.", "Annapolis", "Gaithersburg",
                                               "Baltimore",
                                               "Columbia"])
        self.title_window_state_input.addItem("Massachusetts",
                                              ["Select a City", "Plymouth", "Springfield", "Salem", "Worcester",
                                               "Boston"])
        self.title_window_state_input.addItem("Michigan",
                                              ["Select a City", "Detroit", "Grand Rapids", "Ann Arbor", "Lansing",
                                               "Traverse City"])
        self.title_window_state_input.addItem("Minnesota",
                                              ["Select a City", "Minneapolis", "Duluth", "St Paul", "Rochester",
                                               "Richfield"])
        self.title_window_state_input.addItem("Mississippi",
                                              ["Select a City", "Southaven", "Vicksburg", "Meridian", "Jackson",
                                               "Gulfport"])
        self.title_window_state_input.addItem("Missouri",
                                              ["Select a City", "St. Louis", "Jefferson City", "Independence",
                                               "Columbia",
                                               "Springfield"])
        self.title_window_state_input.addItem("Montana",
                                              ["Select a City", "Bozeman", "Great Falls", "Helena", "Billings",
                                               "Helena"])
        self.title_window_state_input.addItem("Nebraska",
                                              ["Select a City", "Omaha", "Lincoln", "Bellevue", "Scottsbluff",
                                               "Kearney"])
        self.title_window_state_input.addItem("Nevada",
                                              ["Select a City", "Las Vegas", "Carson City", "Reno", "Mesquite",
                                               "Henderson"])
        self.title_window_state_input.addItem("New Hampshire",
                                              ["Select a City", "Manchester", "Nashua", "Littleton", "Portsmouth"])
        self.title_window_state_input.addItem("New Jersey",
                                              ["Select a City", "Trenton", "Cherry Hill", "Atlantic City", "Newark",
                                               "New Brunswick"])
        self.title_window_state_input.addItem("New Mexico",
                                              ["Select a City", "Santa Fe", "Los Lunas", "Rio Rancho", "Las Cruces",
                                               "Albuquerque"])
        self.title_window_state_input.addItem("New York",
                                              ["Select a City", "New York", "Albany", "Yonkers", "Syracuse", "Buffalo"])
        self.title_window_state_input.addItem("North Carolina",
                                              ["Select a City", "Raleigh", "Charlotte", "Greensboro", "Durham",
                                               "Winston-Salem"])
        self.title_window_state_input.addItem("North Dakota",
                                              ["Select a City", "Bismarck", "Grand Forks", "Williston", "Fargo",
                                               "Minot"])
        self.title_window_state_input.addItem("Ohio", ["Select a City", "Cleveland", "Toledo", "Columbus", "Cincinnati",
                                                       "Akron"])
        self.title_window_state_input.addItem("Oklahoma",
                                              ["Select a City", "Oklahoma City", "Tulsa", "Lawton", "Muskogee",
                                               "Broken Arrow"])
        self.title_window_state_input.addItem("Oregon",
                                              ["Select a City", "Portland", "Oregon City", "Bend", "Eugene", "Salem"])
        self.title_window_state_input.addItem("Pennsylvania",
                                              ["Select a City", "Pittsburgh", "Harrisburg", "Scranton", "Allentown",
                                               "Philadelphia"])
        self.title_window_state_input.addItem("Rhode Island",
                                              ["Select a City", "Providence", "Warwick", "Woonsocket", "Cranston",
                                               "Newport"])
        self.title_window_state_input.addItem("South Carolina",
                                              ["Select a City", "Charleston", "Mt Pleasant", "Sumter", "Columbia",
                                               "Rock Hill"])
        self.title_window_state_input.addItem("South Dakota",
                                              ["Select a City", "Pierre", "Sioux Falls", "Deadwood", "Watertown",
                                               "Rapid City"])
        self.title_window_state_input.addItem("Tennessee",
                                              ["Select a City", "Nashville", "Knoxville", "Gatlinburg", "Chattanooga",
                                               "Memphis"])
        self.title_window_state_input.addItem("Texas", ["Select a City", "Austin", "Dallas", "El Paso", "San Antonio",
                                                        "Houston"])
        self.title_window_state_input.addItem("Utah", ["Select a City", "Salt Lake City", "Park City", "Moab", "Ogden",
                                                       "St. George"])
        self.title_window_state_input.addItem("Vermont",
                                              ["Select a City", "Burlington", "Barre", "Montpelier", "Woodstock",
                                               "Rutland", "Stowe"])
        self.title_window_state_input.addItem("Virginia",
                                              ["Select a City", "Chesapeake", "Hampton", "Alexandria", "Richmond",
                                               "Norfolk"])
        self.title_window_state_input.addItem("Washington",
                                              ["Select a City", "Seattle", "Kent", "Spokane", "Tacoma", "Vancouver"])
        self.title_window_state_input.addItem("West Virginia",
                                              ["Select a City", "Charleston", "Morgantown", "Huntington", "Wheeling"])
        self.title_window_state_input.addItem("Wisconsin",
                                              ["Select a City", "Madison", "Milwaukee", "Eau Claire", "Green Bay",
                                               "Appleton"])
        self.title_window_state_input.addItem("Wyoming",
                                              ["Select a City", "Jackson", "Cody", "Cheyenne", "Casper", "Laramie"])
        self.title_window_state_input.activated.connect(self.show_cities_from_state_on_title_window)
        self.title_window_state_input.activated.connect(self.title_window_input_dependencies)

        # State Not Selected Error Label
        self.title_window_state_unselected_error_label = self.create_QLabel("title_window_central_widget", 150, 200,
                                                                            150, 50)
        self.title_window_state_unselected_error_label = QtWidgets.QLabel(self.title_window_central_widget)
        self.title_window_state_unselected_error_label.setText("Please select a state")
        self.title_window_state_unselected_error_label.setFixedSize(150, 10)
        self.title_window_state_unselected_error_label.move(150, 240)
        self.title_window_state_unselected_error_label.setStyleSheet("QLabel"
                                                                     "{"
                                                                     "color: red;"
                                                                     "font-weight: bold;"
                                                                     "}")
        self.title_window_state_unselected_error_label.hide()

        # QCombobox to input city field
        self.title_window_city_input = self.create_QComboBox("title_window_central_widget", 297, 250, 150, 50)
        self.title_window_city_input.setEnabled(False)
        self.title_window_city_input.setStyleSheet("QComboBox"
                                                   "{"
                                                   "color: white;"
                                                   "border: 3px solid;"
                                                   "border-color: rgb(245, 245, 245);"
                                                   "background-color: rgba(20, 52, 124, 170);"
                                                   "}"
                                                   "QComboBox QAbstractItemView {"
                                                   "background-color: #3C4571;"
                                                    "color: white;"
                                                    "width: 200px;"
                                                    "selection-background-color: #0060AC;"
                                                   "}"
                                                   )
        self.title_window_city_input.setFont(QtGui.QFont("Arial", 14))
        self.title_window_city_input.addItem("Select a City", ["None"])
        self.title_window_city_input.activated.connect(self.title_window_input_dependencies)

        # City Not Selected Error Label
        self.title_window_city_unselected_error_label = self.create_QLabel("title_window_central_widget", 150, 200, 150,
                                                                           50)
        self.title_window_city_unselected_error_label = QtWidgets.QLabel(self.title_window_central_widget)
        self.title_window_city_unselected_error_label.setText("Please select a city")
        self.title_window_city_unselected_error_label.setFixedSize(150, 10)
        self.title_window_city_unselected_error_label.move(300, 240)
        self.title_window_city_unselected_error_label.setStyleSheet("QLabel"
                                                                    "{"
                                                                    "color: red;"
                                                                    "font-weight: bold;"
                                                                    "}")
        self.title_window_city_unselected_error_label.hide()

        # QCombobox to input container field
        self.title_window_type_input = self.create_QComboBox("title_window_central_widget", 444, 250, 160, 50)
        self.title_window_type_input.setEnabled(False)
        self.title_window_type_input.setStyleSheet("QComboBox"
                                                   "{"
                                                   "color: white;"
                                                   "border: 3px solid;"
                                                   "border-color: rgb(245, 245, 245);"
                                                   "background-color: rgba(20, 52, 124, 170);"
                                                   "}"
                                                   "QComboBox QAbstractItemView {"
                                                   "background-color: #3C4571;"
                                                    "color: white;"
                                                    "width: 200px;"
                                                    "selection-background-color: #0060AC;"
                                                   "}")
        self.title_window_type_input.setFont(QtGui.QFont("Arial", 14))
        self.title_window_type_input.addItems(
            ["Select a Type", "Food", "Nature/Outdoor", "Entertainment", "Cultural/Historical"])

        # QLineEdit to search by attraction name
        self.title_window_search_bar = QtWidgets.QLineEdit(self.title_window_central_widget)
        self.title_window_search_bar.setGeometry(QtCore.QRect(601, 250, 302, 50))
        self.title_window_search_bar.setPlaceholderText("Search by Attraction Name")
        self.title_window_search_bar.setStyleSheet("QLineEdit"
                                                   "{"
                                                   "color: white;"
                                                   "border: 3px solid;"
                                                   "border-color: rgb(245, 245, 245);"
                                                   "background-color: rgba(20, 52, 124, 170);"
                                                   "}")
        self.title_window_search_bar.setFont(QtGui.QFont("Arial", 14))

        # Search button that changes windows
        self.title_window_change_window_button = QtWidgets.QToolButton(self.title_window_central_widget)
        self.title_window_change_window_button.setGeometry(900, 250, 100, 50)
        self.title_window_change_window_button.setText("Search")
        self.title_window_change_window_button.setStyleSheet("QToolButton"
                                                             "{"
                                                             "color: white;"
                                                             "border: 3px solid;"
                                                             "border-color: rgb(245, 245, 245);"
                                                             "background-color: rgba(20, 52, 124, 170);"
                                                             "}"
                                                             )
        self.title_window_change_window_button.setFont(QtGui.QFont("Arial", 14))
        self.title_window_change_window_button.clicked.connect(self.state_and_city_is_selected)

        # Set widget container to window
        MainWindow.setCentralWidget(self.title_window_central_widget)

    # Everything needed to setup and display the main window
    def setup_application_window(self, MainWindow):
        global click_count
        global location_and_filters_QGroupBox
        global attractions_QGroupBox_bar
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle("Traveler")
        MainWindow.setFixedSize(1150, 645)

        # Sets up the window container
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("display")

        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 1151, 626))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)

        self.search_attractions_tab = QtWidgets.QWidget()
        self.search_attractions_tab.setObjectName("tab1")

        # Creating the area to display user location details
        self.widget = QtWidgets.QWidget(self.search_attractions_tab)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1151, 601))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.location_details_backdrop = QtWidgets.QGroupBox(self.widget)
        self.location_details_backdrop.setObjectName("backdrop")
        self.location_details_backdrop.setEnabled(True)
        self.location_details_backdrop.setFlat(True)
        self.location_details_backdrop.setFixedSize(222, 240)
        self.location_details_backdrop.move(7, 50)

        self.location_and_filters_QGroupBox = QtWidgets.QGroupBox(self.widget)
        self.location_and_filters_QGroupBox.setEnabled(True)
        self.location_and_filters_QGroupBox.setFlat(True)

        # Setting attractions_QGroupBox_bar
        self.attractions_QGroupBox_bar = QtWidgets.QGroupBox(self.widget)
        self.attractions_QGroupBox_bar.setFixedSize(907, 40)
        self.attractions_QGroupBox_bar.move(234, 10)
        self.attractions_QGroupBox_bar.setEnabled(True)
        self.attractions_QGroupBox_bar.setFlat(True)

        # The QLabel that displays the number of shown attractions
        self.num_of_attractions_QLabel = self.create_QLabel("attractions_QGroupBox_bar", 10, 20, 200, 20)
        self.num_of_attractions_QLabel.setObjectName("numAttractions")

        # The dropdown menu of different attributes to sort by
        self.sorting_QLabel = self.create_QLabel("attractions_QGroupBox_bar", 643, 13, 100, 20)
        self.sorting_QLabel.setObjectName("sortByLabel")

        self.sorting_QComboBox = self.create_QComboBox("attractions_QGroupBox_bar", 700, 7, 208, 30)
        self.sorting_QComboBox.setObjectName("sorting_QComboBox")
        self.sorting_QComboBox.addItems(["Recommended",
                                         "Nearest attractions",
                                         "Rating: Highest to Lowest",
                                         "Rating: Lowest to Highest",
                                         "Price: Highest to Lowest",
                                         "Price: Lowest to Highest",
                                         "Traffic: Highest to Lowest",
                                         "Traffic: Lowest to Highest"])
        self.sorting_QComboBox.activated.connect(self.get_current_filter_field_values)

        # Search Field and Search Button
        self.search_bar = QtWidgets.QLineEdit(self.attractions_QGroupBox_bar)
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setStyleSheet("font: 14px")
        self.search_bar.setGeometry(QtCore.QRect(200, 8, 301, 30))
        self.search_bar.setPlaceholderText("Search by Keyword")

        self.search_attractions_button = QtWidgets.QToolButton(self.attractions_QGroupBox_bar)
        self.search_attractions_button.setGeometry(QtCore.QRect(500, 9, 55, 28))
        self.search_attractions_button.setText(_translate("MainWindow", "Search"))

        self.search_bar_icon = QtWidgets.QLabel(self.attractions_QGroupBox_bar)
        self.search_bar_icon.setPixmap(QtGui.QPixmap("Application Pictures/magnifyingIcon.png"))
        self.search_bar_icon.setScaledContents(True)
        self.search_bar_icon.setFixedSize(25, 25)
        self.search_bar_icon.move(171, 10)
        self.search_bar_icon.show()
        self.search_attractions_button.clicked.connect(self.search_attractions)

        self.clear_search_bar_button = QtWidgets.QToolButton(self.attractions_QGroupBox_bar)
        self.clear_search_bar_button.setGeometry(QtCore.QRect(554, 9, 55, 28))
        self.clear_search_bar_button.setText("Clear")
        self.clear_search_bar_button.clicked.connect(self.clear_find_attractions_search_bar)

        # App Logo
        self.application_logo = QtWidgets.QLabel(self.search_attractions_tab)
        self.application_logo.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowLogo.png"))
        self.application_logo.setScaledContents(True)
        self.application_logo.setFixedSize(190, 190)
        self.application_logo.move(23, -22)
        self.application_logo.show()

        # Filter Title
        Xcoor = 10
        Ycoor = 230
        self.filter_title = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor + 60, 120, 50)
        self.filter_title.setObjectName("filterByTitle")

        # Filtering by State - Format: (Label : ComboBox)
        self.state_filter_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor + 95, 50, 50)
        self.state_filter_QLabel.setObjectName("filters")

        self.state_filter_QComboBox = self.create_QComboBox("location_and_filters_QGroupBox", Xcoor + 47, Ycoor + 108,
                                                            173, 26)
        self.state_filter_QComboBox.setObjectName("filterComboboxes")
        self.state_filter_QComboBox.addItem("No preference", ["No preference"])
        self.state_filter_QComboBox.addItem("Alabama",
                                            ["No preference", "Huntsville", "Birmingham", "Montgomery", "Mobile",
                                             "Tuscaloosa"])
        self.state_filter_QComboBox.addItem("Alaska", ["No preference", "Anchorage", "Juneau", "Fairbanks", "Badger",
                                                       "Knik-Fairview"])
        self.state_filter_QComboBox.addItem("Arizona",
                                            ["No preference", "Phoenix", "Tucson", "Sedona", "Mesa", "Scottsdale"])
        self.state_filter_QComboBox.addItem("Arkansas", ["No preference", "Little Rock", "Fort Smith", "Fayetteville",
                                                         "Springsdale", "Jonesboro"])
        self.state_filter_QComboBox.addItem("California",
                                            ["No preference", "San Francisco", "Los Angeles", "San Diego", "San Jose",
                                             "Fresno"])
        self.state_filter_QComboBox.addItem("Colorado",
                                            ["No preference", "Denver", "Colorado Springs", "Pueblo", "Aspen",
                                             "Fort Collins"])
        self.state_filter_QComboBox.addItem("Connecticut",
                                            ["No preference", "Bridgeport", "Hartford", "New Haven", "Stamford",
                                             "Waterbury"])
        self.state_filter_QComboBox.addItem("Delaware",
                                            ["No preference", "Dover", "Wilmington", "Middletown", "New Castle",
                                             "Newark"])
        self.state_filter_QComboBox.addItem("Florida",
                                            ["No preference", "Orlando", "Tallahassee", "Jacksonville", "Miami",
                                             "Tampa"])
        self.state_filter_QComboBox.addItem("Georgia",
                                            ["No preference", "Atlanta", "Columbus", "Athens", "Augusta", "Savannah"])
        self.state_filter_QComboBox.addItem("Hawaii",
                                            ["No preference", "Kailua", "Waipahu", "Honolulu", "Hilo", "Kahului"])
        self.state_filter_QComboBox.addItem("Idaho",
                                            ["No preference", "Idaho Falls", "Boise", "Twin Falls", "Pocatello",
                                             "Coeur d'alene"])
        self.state_filter_QComboBox.addItem("Illinois",
                                            ["No preference", "Chicago", "Naperville", "St. Louis", "Rockford",
                                             "Springfield"])
        self.state_filter_QComboBox.addItem("Indiana",
                                            ["No preference", "Indianapolis", "Gary", "Lafayette", "Evansville",
                                             "Fort Wayne"])
        self.state_filter_QComboBox.addItem("Iowa",
                                            ["No preference", "Des Moines", "Waterloo", "Dubuque", "Cedar Rapids",
                                             "Davenport"])
        self.state_filter_QComboBox.addItem("Kansas",
                                            ["No preference", "Olathe", "Topeka", "Wichita", "Lawrence", "Kansas City"])
        self.state_filter_QComboBox.addItem("Kentucky",
                                            ["No preference", "Lexington", "Bowling Green", "Louisville", "Florence",
                                             "Jeffersontown"])
        self.state_filter_QComboBox.addItem("Louisiana",
                                            ["No preference", "Alexandria", "Shreveport", "New Orleans", "Baton Rouge",
                                             "Lafayette"])
        self.state_filter_QComboBox.addItem("Maine",
                                            ["No preference", "Portland", "Bangor", "Camden", "Augusta", "Brunswick"])
        self.state_filter_QComboBox.addItem("Maryland",
                                            ["No preference", "Washington D.C.", "Annapolis", "Gaithersburg",
                                             "Baltimore", "Columbia"])
        self.state_filter_QComboBox.addItem("Massachusetts",
                                            ["No preference", "Plymouth", "Springfield ", "Salem", "Worcester",
                                             "Boston"])
        self.state_filter_QComboBox.addItem("Michigan",
                                            ["No preference", "Detroit", "Grand Rapids", "Ann Arbor", "Lansing",
                                             "Traverse City"])
        self.state_filter_QComboBox.addItem("Minnesota",
                                            ["No preference", "Minneapolis", "Duluth", "St Paul", "Rochester",
                                             "Richfield"])
        self.state_filter_QComboBox.addItem("Mississippi",
                                            ["No preference", "Southaven", "Vicksburg", "Meridian", "Jackson",
                                             "Gulfport"])
        self.state_filter_QComboBox.addItem("Missouri",
                                            ["No preference", "St. Louis", "Jefferson City", "Independence", "Columbia",
                                             "Springfield"])
        self.state_filter_QComboBox.addItem("Montana",
                                            ["No preference", "Bozeman", "Great Falls", "Helena", "Billings", "Helena"])
        self.state_filter_QComboBox.addItem("Nebraska",
                                            ["No preference", "Omaha", "Lincoln", "Bellevue", "Scottsbluff", "Kearney"])
        self.state_filter_QComboBox.addItem("Nevada", ["No preference", "Las Vegas", "Carson City", "Reno", "Mesquite",
                                                       "Henderson"])
        self.state_filter_QComboBox.addItem("New Hampshire",
                                            ["No preference", "Manchester", "Nashua", "Littleton", "Portsmouth"])
        self.state_filter_QComboBox.addItem("New Jersey",
                                            ["No preference", "Trenton", "Cherry Hill", "Atlantic City", "Newark",
                                             "New Brunswick"])
        self.state_filter_QComboBox.addItem("New Mexico",
                                            ["No preference", "Santa Fe", "Los Lunas", "Rio Rancho", "Las Cruces",
                                             "Albuquerque"])
        self.state_filter_QComboBox.addItem("New York",
                                            ["No preference", "New York", "Albany", "Yonkers", "Syracuse", "Buffalo"])
        self.state_filter_QComboBox.addItem("North Carolina",
                                            ["No preference", "Raleigh", "Charlotte", "Greensboro", "Durham",
                                             "Winston-Salem"])
        self.state_filter_QComboBox.addItem("North Dakota",
                                            ["No preference", "Bismarck", "Grand Forks", "Williston", "Fargo", "Minot"])
        self.state_filter_QComboBox.addItem("Ohio",
                                            ["No preference", "Cleveland", "Toledo", "Columbus", "Cincinnati", "Akron"])
        self.state_filter_QComboBox.addItem("Oklahoma",
                                            ["No preference", "Oklahoma City", "Tulsa", "Lawton", "Muskogee",
                                             "Broken Arrow"])
        self.state_filter_QComboBox.addItem("Oregon",
                                            ["No preference", "Portland", "Oregon City", "Bend", "Eugene", "Salem"])
        self.state_filter_QComboBox.addItem("Pennsylvania",
                                            ["No preference", "Pittsburgh", "Harrisburg", "Scranton", "Allentown",
                                             "Philadelphia"])
        self.state_filter_QComboBox.addItem("Rhode Island",
                                            ["No preference", "Providence", "Warwick", "Woonsocket", "Cranston",
                                             "Newport"])
        self.state_filter_QComboBox.addItem("South Carolina",
                                            ["No preference", "Charleston", "Mt Pleasant", "Sumter", "Columbia",
                                             "Rock Hill"])
        self.state_filter_QComboBox.addItem("South Dakota",
                                            ["No preference", "Pierre", "Sioux Falls", "Deadwood", "Watertown",
                                             "Rapid City"])
        self.state_filter_QComboBox.addItem("Tennessee",
                                            ["No preference", "Nashville", "Knoxville", "Gatlinburg", "Chattanooga",
                                             "Memphis"])
        self.state_filter_QComboBox.addItem("Texas",
                                            ["No preference", "Austin", "Dallas", "El Paso", "San Antonio", "Houston"])
        self.state_filter_QComboBox.addItem("Utah", ["No preference", "Salt Lake City", "Park City", "Moab", "Ogden",
                                                     "St. George"])
        self.state_filter_QComboBox.addItem("Vermont",
                                            ["No preference", "Burlington", "Barre", "Montpelier", "Woodstock",
                                             "Rutland", "Stowe"])
        self.state_filter_QComboBox.addItem("Virginia",
                                            ["No preference", "Chesapeake", "Hampton", "Alexandria", "Richmond",
                                             "Norfolk"])
        self.state_filter_QComboBox.addItem("Washington",
                                            ["No preference", "Seattle", "Kent", "Spokane", "Tacoma", "Vancouver"])
        self.state_filter_QComboBox.addItem("West Virginia",
                                            ["No preference", "Charleston", "Morgantown", "Huntington", "Wheeling"])
        self.state_filter_QComboBox.addItem("Wisconsin",
                                            ["No preference", "Madison", "Milwaukee", "Eau Claire", "Green Bay",
                                             "Appleton"])
        self.state_filter_QComboBox.addItem("Wyoming",
                                            ["No preference", "Jackson", "Cody", "Cheyenne", "Casper", "Laramie"])
        self.state_filter_QComboBox.activated.connect(self.show_cities_from_state)
        self.state_filter_QComboBox.activated.connect(self.get_current_filter_field_values)

        # Filtering by City - Format: (Label : ComboBox)
        self.city_filter_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor + 130, 50, 50)
        self.city_filter_QLabel.setObjectName("filters")
        self.city_filter_QComboBox = self.create_QComboBox("location_and_filters_QGroupBox", Xcoor + 47, Ycoor + 143,
                                                           173, 26)
        self.city_filter_QComboBox.setObjectName("filterComboboxes")
        self.city_filter_QComboBox.addItems(["None"])
        self.city_filter_QComboBox.activated.connect(self.get_current_filter_field_values)

        # Filtering by Type - Format: (Label : ComboBox)
        self.type_filter_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor + 165, 50, 50)
        self.type_filter_QLabel.setObjectName("filters")
        self.type_filter_QComboBox = self.create_QComboBox("location_and_filters_QGroupBox", Xcoor + 47, Ycoor + 178,
                                                           173, 26)
        self.type_filter_QComboBox.setObjectName("filterComboboxes")
        self.type_filter_QComboBox.addItems(
            ["No preference", "Food", "Nature/Outdoor", "Entertainment", "Cultural/Historical"])
        self.type_filter_QComboBox.activated.connect(self.get_current_filter_field_values)

        # Filtering by WheelChair Accessibility - Format: (CheckBox : Label)
        self.wheelchair_access_filter_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 30,
                                                                  Ycoor + 205, 150, 50)
        self.wheelchair_access_filter_QLabel.setObjectName("filters")
        self.wheelchair_access_filter_QCheckBox = self.create_QCheckBox("location_and_filters_QGroupBox", Xcoor + 5,
                                                                        Ycoor + 221, 20, 20)
        self.wheelchair_access_filter_QCheckBox.stateChanged.connect(self.get_current_filter_field_values)

        # Filtering by Family Friendliness - Format: (CheckBox : Label)
        self.family_friendly_filter_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 30,
                                                                Ycoor + 230, 150, 50)
        self.family_friendly_filter_QLabel.setObjectName("filters")
        self.family_friendly_filter_QCheckBox = self.create_QCheckBox("location_and_filters_QGroupBox", Xcoor + 5,
                                                                      Ycoor + 246, 20, 20)
        self.family_friendly_filter_QCheckBox.stateChanged.connect(self.get_current_filter_field_values)

        # Filtering by Pet Friendliness - Format: (CheckBox : Label)
        self.pet_friendly_filter_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 30, Ycoor + 255,
                                                             150, 50)
        self.pet_friendly_filter_QLabel.setObjectName("filters")
        self.pet_friendly_filter_QCheckBox = self.create_QCheckBox("location_and_filters_QGroupBox", Xcoor + 5,
                                                                   Ycoor + 271, 20, 20)
        self.pet_friendly_filter_QCheckBox.stateChanged.connect(self.get_current_filter_field_values)

        # Enter Coordinates QLineEdit
        self.location_details_title = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor - 175, 200,
                                                         25)
        self.location_details_title.setObjectName("locationDetailsTitle")
        self.location_details_title.setText("Location Details")

        # A QLabel that shows your current location
        self.current_location_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor - 145, 200,
                                                          25)
        self.current_location_QLabel.setObjectName("enteredLocation")

        # Latitude QLabel and input
        self.latitude_input_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor - 115, 200,
                                                        25)
        self.latitude_input_QLabel.setText("Latitude:")
        self.latitude_input = QtWidgets.QLineEdit(self.location_and_filters_QGroupBox)
        self.latitude_input.setGeometry(QtCore.QRect(Xcoor + 70, Ycoor - 115, 138, 25))
        self.latitude_input.setPlaceholderText(" Enter latitude")
        self.latitude_input.textChanged.connect(self.check_if_location_fields_are_filled)

        # Longitude QLabel and input
        self.longitude_input_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor - 80, 200,
                                                         25)
        self.longitude_input_QLabel.setText("Longitude:")

        self.longitude_input = QtWidgets.QLineEdit(self.location_and_filters_QGroupBox)
        self.longitude_input.setGeometry(QtCore.QRect(Xcoor + 70, Ycoor - 80, 138, 25))
        self.longitude_input.setPlaceholderText(" Enter longitude")
        self.longitude_input.textChanged.connect(self.check_if_location_fields_are_filled)

        # Label and dropdown menu for radius of distance
        self.radius_QLabel = self.create_QLabel("location_and_filters_QGroupBox", Xcoor + 5, Ycoor - 45, 200, 25)
        self.radius_QLabel.setText("Desired Distance From You:")

        self.radius_QComboBox = self.create_QComboBox("location_and_filters_QGroupBox", Xcoor + 5, Ycoor - 20, 205, 25)
        self.radius_QComboBox.setObjectName("radius_QComboBox")
        self.radius_QComboBox.addItems(
            ["Any distance", "Less than 5 miles", "Less than 10 miles", "Less than 20 miles", "Less than 50 miles"])
        self.radius_QComboBox.setEnabled(False)
        self.radius_QComboBox.activated.connect(self.detect_change_in_desired_distance)

        # The button to show your location in a maps popup
        self.show_entered_location_map_button = QtWidgets.QToolButton(self.location_and_filters_QGroupBox)
        self.show_entered_location_map_button.setGeometry(Xcoor + 5, Ycoor + 10, 205, 20)
        self.show_entered_location_map_button.setText("Show location in maps")
        self.show_entered_location_map_button.setEnabled(False)
        self.show_entered_location_map_button.clicked.connect(self.show_entered_location_map_window)

        # The button to find the user's location
        self.find_user_location_button = QtWidgets.QToolButton(self.location_and_filters_QGroupBox)
        self.find_user_location_button.setGeometry(Xcoor + 5, Ycoor + 35, 205, 20)
        self.find_user_location_button.setText("Find my location")
        self.find_user_location_button.clicked.connect(self.find_current_location)

        # Adding a Dynamic Help Menu
        self.help_menu_button = QtWidgets.QToolButton(self.location_and_filters_QGroupBox)
        self.help_menu_button.setObjectName("help_menu_button")
        self.help_menu_button.setGeometry(7, 560, 223, 20)
        click_count = 0
        self.help_menu_groupBox = QtWidgets.QGroupBox(self.location_and_filters_QGroupBox)
        self.help_menu_groupBox.setObjectName("help_menu_groupBox")
        self.help_menu_groupBox.setGeometry(QtCore.QRect(7, 480, 223, 80))
        self.help_menu_groupBox.hide()

        # The button to open program documentation
        self.read_documentation_button = QtWidgets.QToolButton(self.help_menu_groupBox)
        self.read_documentation_button.setGeometry(6, 30, 211, 20)
        self.read_documentation_button.clicked.connect(self.read_documentation)

        # The button to show QnA
        self.show_QandA_button = QtWidgets.QToolButton(self.help_menu_groupBox)
        self.show_QandA_button.setGeometry(6, 5, 211, 20)
        self.show_QandA_button.clicked.connect(self.show_QandA_window)

        # The button to create a user report
        self.create_user_report_button = QtWidgets.QToolButton(self.help_menu_groupBox)
        self.create_user_report_button.setGeometry(6, 55, 211, 20)
        self.create_user_report_button.setText("Create a Report")
        self.create_user_report_button.clicked.connect(self.create_user_report)

        self.read_documentation_button.setText(_translate("MainWindow", " Read Documentation"))

        self.show_QandA_button.setText(_translate("MainWindow", "Q ＆ A"))

        self.help_menu_button.setText(_translate("MainWindow", "Help Menu"))
        self.help_menu_button.clicked.connect(self.control_help_menu_display)

        # Setting ScrollArea, where attractions are displayed
        self.attractions_QScrollArea_widget_container = QtWidgets.QWidget()
        self.verticalLayout.addWidget(self.location_and_filters_QGroupBox)

        self.attractions_QScrollArea = QtWidgets.QScrollArea(self.search_attractions_tab)
        self.attractions_QScrollArea.setFixedWidth(907)
        self.attractions_QScrollArea.setMinimumHeight(531)
        self.attractions_QScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.attractions_QScrollArea.horizontalScrollBar().setDisabled(True)
        self.attractions_QScrollArea.move(236, 50)
        self.attractions_QScrollArea.setWidgetResizable(True)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.attractions_QScrollArea_widget_container)
        self.attractions_QScrollArea_widget_container.setLayout(self.verticalLayout_3)

        # Adds multiple tabs
        self.tab_widget.addTab(self.search_attractions_tab, " ")

        # The Bookmarks Tab
        self.bookmarks_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.bookmarks_tab, " ")

        self.bookmarks_tab_top_groupBox_bar = QtWidgets.QGroupBox(self.bookmarks_tab)
        self.bookmarks_tab_top_groupBox_bar.setFixedSize(907, 40)
        self.bookmarks_tab_top_groupBox_bar.move(120, 10)
        self.bookmarks_tab_top_groupBox_bar.setEnabled(True)
        self.bookmarks_tab_top_groupBox_bar.setFlat(True)

        self.bookmarks_scrollArea_backdrop = QtWidgets.QGroupBox(self.bookmarks_tab)
        self.bookmarks_scrollArea_backdrop.setObjectName("bookmarks_scrollArea_backdrop")
        self.bookmarks_scrollArea_backdrop.setFixedSize(913, 531)
        self.bookmarks_scrollArea_backdrop.move(121, 50)
        self.bookmarks_scrollArea_backdrop.setEnabled(True)
        self.bookmarks_scrollArea_backdrop.setFlat(True)

        # Bookmarks Tab: Searchbar, Label, Buttons, Icons, and ScrollArea
        # QLabel that displays the number of bookmarks attractions
        self.num_of_bookmarks_QLabel = self.create_QLabel("bookmarks_tab_top_groupBox_bar", 10, 20, 200, 20)
        self.num_of_bookmarks_QLabel.setObjectName("num_of_bookmark_results")
        self.num_of_bookmarks_QLabel.setText("0 Total Bookmarks Saved")
        # Search Bar Icon
        self.bookmarks_tab_search_icon = QtWidgets.QLabel(self.bookmarks_tab_top_groupBox_bar)
        self.bookmarks_tab_search_icon.setPixmap(QtGui.QPixmap("Application Pictures/magnifyingIcon.png"))
        self.bookmarks_tab_search_icon.setScaledContents(True)
        self.bookmarks_tab_search_icon.setFixedSize(25, 25)
        self.bookmarks_tab_search_icon.move(221, 10)
        self.bookmarks_tab_search_icon.show()
        # Search Bar
        self.bookmarks_tab_search_bar = QtWidgets.QLineEdit(self.bookmarks_tab_top_groupBox_bar)
        self.bookmarks_tab_search_bar.setObjectName("search_bar")
        self.bookmarks_tab_search_bar.setStyleSheet("font: 14px")
        self.bookmarks_tab_search_bar.setGeometry(QtCore.QRect(250, 8, 371, 30))
        self.bookmarks_tab_search_bar.setPlaceholderText("Search by Keyword")
        # Search Button
        self.bookmarks_tab_search_button = QtWidgets.QToolButton(self.bookmarks_tab_top_groupBox_bar)
        self.bookmarks_tab_search_button.clicked.connect(self.search_bookmarks)
        self.bookmarks_tab_search_button.setGeometry(QtCore.QRect(620, 9, 55, 28))
        self.bookmarks_tab_search_button.setText(_translate("MainWindow", "Search"))
        # Clear Button
        self.bookmarks_tab_clear_search_bar = QtWidgets.QToolButton(self.bookmarks_tab_top_groupBox_bar)
        self.bookmarks_tab_clear_search_bar.setGeometry(QtCore.QRect(674, 9, 55, 28))
        self.bookmarks_tab_clear_search_bar.setText("Clear")
        self.bookmarks_tab_clear_search_bar.clicked.connect(self.clear_bookmarks_tab_search_bar)
        # Clear All Bookmarks Button
        self.bookmarks_tab_clear_bookmarks = QtWidgets.QToolButton(self.bookmarks_tab_top_groupBox_bar)
        self.bookmarks_tab_clear_bookmarks.setGeometry(QtCore.QRect(760, 9, 150, 28))
        self.bookmarks_tab_clear_bookmarks.setText("Clear All Bookmarks")
        self.bookmarks_tab_clear_bookmarks.clicked.connect(self.clear_all_bookmarks)
        # ScrollArea
        self.bookmarks_scrollArea_object_container = QtWidgets.QWidget()
        self.bookmarks_scrollArea = QtWidgets.QScrollArea(self.bookmarks_tab)
        self.bookmarks_scrollArea.setFixedWidth(905)
        self.bookmarks_scrollArea.setMinimumHeight(523)
        self.bookmarks_scrollArea.move(125, 54)
        self.bookmarks_scrollArea.setWidgetResizable(True)
        self.bookmarks_container_vertical_layout = QtWidgets.QVBoxLayout(self.bookmarks_scrollArea_object_container)
        self.bookmarks_scrollArea_object_container.setLayout(self.bookmarks_container_vertical_layout)

        # The tab to display sources for all attractions
        self.sources_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.sources_tab, " ")

        self.sources_tab_widget = QtWidgets.QWidget(self.sources_tab)
        self.sources_tab_widget.setGeometry(QtCore.QRect(0, 0, 1150, 601))

        # App Logo
        self.sources_application_logo = QtWidgets.QLabel(self.sources_tab)
        self.sources_application_logo.setPixmap(QtGui.QPixmap("Application Pictures/titleWindowLogo.png"))
        self.sources_application_logo.setScaledContents(True)
        self.sources_application_logo.setFixedSize(190, 190)
        self.sources_application_logo.move(23, -22)
        self.sources_application_logo.show()

        self.sources_title_QLabel = self.create_QLabel("sources_tab_widget", 455, 20, 300, 40)
        self.sources_title_QLabel.setObjectName("sources_title_QLabel")
        self.sources_title_QLabel.setText("Sources, Licenses, and References")

        self.sources_text_container = QtWidgets.QGroupBox(self.sources_tab_widget)
        self.sources_text_container.setObjectName("sources_text_container")
        self.sources_text_container.setFixedSize(1137, 531)
        self.sources_text_container.move(8, 50)

        filename = os.path.abspath('Application Data and Documentation Files/Sources, Licenses, and References.pdf')
        view = QtWebEngineWidgets.QWebEngineView(self.sources_text_container)
        settings = view.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        url = QtCore.QUrl.fromLocalFile(filename)
        view.load(url)
        view.resize(1133, 527)
        view.move(2, 2)
        view.show()

        # Setting up the main window, and its default tab
        MainWindow.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.status_bar)
        self.retranslateUI(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # Changing the sort by dropdown to "Nearest attractions", if the user chooses to sort by distance
    def changeSortingToDistance(self):
        self.sorting_QComboBox.setCurrentIndex(1)

    # The options to select a city are based on the state chosen
    def show_cities_from_state(self, index):
        self.city_filter_QComboBox.clear()
        self.city_filter_QComboBox.addItems(self.state_filter_QComboBox.itemData(index))

    # The options to select a city are based on the state chosen, but for the title page
    def show_cities_from_state_on_title_window(self, index):
        self.title_window_city_input.clear()
        self.title_window_city_input.addItems(self.title_window_state_input.itemData(index))

    # Retranslating the UI
    def retranslateUI(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.filter_title.setText(_translate("MainWindow", "Filter By:"))
        self.state_filter_QLabel.setText(_translate("MainWindow", "State:"))
        self.city_filter_QLabel.setText(_translate("MainWindow", "City:"))
        self.type_filter_QLabel.setText(_translate("MainWindow", "Type:"))
        self.wheelchair_access_filter_QLabel.setText(_translate("MainWindow", "Wheelchair Accessible"))
        self.family_friendly_filter_QLabel.setText(_translate("MainWindow", "Family Friendly"))
        self.pet_friendly_filter_QLabel.setText(_translate("MainWindow", "Pet Friendly"))
        self.sorting_QLabel.setText(_translate("MainWindow", "Sort By:"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.search_attractions_tab),
                                   _translate("MainWindow", "           Find Attractions          "))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.bookmarks_tab),
                                   _translate("MainWindow", "        Bookmarked Attractions       "))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.sources_tab),
                                   _translate("MainWindow", "Sources, Licenses, and References"))


# Running the application
if __name__ == "__main__":
    # Clear all user action logs

    with open("outputreport.txt", "r+") as f:
        f.seek(0)
        f.truncate()
    import sys

    app = QtWidgets.QApplication(sys.argv)
    with open("application_styling.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    ui.setup_title_window(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())