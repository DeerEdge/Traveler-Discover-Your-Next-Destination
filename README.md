# Traveler
A simple, user-friendly, and powerful PyQt5 application made for the 2021-2022 FBLA Coding and Programming Challenge. 
![Title Window Image](README images/Application Title Window.png)

## Setup
For this project, PyCharm was used for the development of the application. To find the system requirements and installation process: https://www.jetbrains.com/help/pycharm/installation-guide.html

First up, the necessary libraries for the database its connection to the rest of the PyCharm project need to be installed. (Note: Only macOS and Windows platforms were used to develop this application. All libarary version testing and implementation corresponds to only these two platforms)
### psycopg2 v2.8.6 
```
pip install psycopg2
```
This library is used to connect PostgresSQL to the Python project. Over the course of the project, versions 2.8.6 and 2.9.1 were used. To find more about the library and its installation: https://pypi.org/project/psycopg2/

### PostgresSQL v14.2
This library is used to hold all attraction data, and to dynamically store filtered attractions within this project. For this project only version 14.2 was tested and implemented. To find information about the library and the installation process: https://www.postgresql.org/download/

### pgAdmin 5 v6.7
This application is used to manage Postgres databases. For this project only version 6.7 was tested and implemented. To find information about the library and the installation process: https://www.pgadmin.org/download/

Within pgAdmin 5, we can expand the folders until the Table folder is found. This is where our database table will be created to hold all of our attraction data. Navigating to the query editor we can paste the following code:
```
CREATE TABLE ATTRACTION
   (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(200) NOT NULL,
    DESCRIPTION VARCHAR(2000) NOT NULL,
    STATE VARCHAR(50) NOT NULL,
    CITY VARCHAR(50) NOT NULL,
    TYPE VARCHAR(50) NOT NULL,
    PRICE_LEVEL INTEGER,
    TRAFFIC_LEVEL INTEGER,
    RATING NUMERIC(2,1),
    WHEELCHAIR_ACCESSIBILITY BOOLEAN,
    FAMILY_FRIENDLY BOOLEAN,
    PET_FRIENDLY BOOLEAN,
    WEBSITE VARCHAR(500),
    LATITUDE NUMERIC(11,8),
	LONGITUDE NUMERIC(11,8),
	IMAGE_LINK_SRC VARCHAR(50000) 
    );

CREATE INDEX IDX_STATE ON ATTRACTION (STATE);
CREATE INDEX IDX_CITY ON ATTRACTION (CITY);
CREATE INDEX IDX_TYPE ON ATTRACTION (TYPE);
CREATE INDEX IDX_RATING ON ATTRACTION (RATING);
CREATE INDEX IDX_PRICE_LEVEL ON ATTRACTION (PRICE_LEVEL);
CREATE INDEX IDX_TRAFFIC_LEVEL ON ATTRACTION (TRAFFIC_LEVEL);
CREATE INDEX IDX_WC_ACCESSIBILITY ON ATTRACTION (WHEELCHAIR_ACCESSIBILITY);
CREATE INDEX IDX_FAMILY_FRIENDLY  ON ATTRACTION (FAMILY_FRIENDLY );
CREATE INDEX IDX_PET_FRIENDLY ON ATTRACTION (PET_FRIENDLY);
ALTER TABLE ATTRACTION ADD CONSTRAINT CHK_RATING CHECK (RATING >= 0 AND RATING <= 5)
```
Highlighting everything and clicking the run button in the menu bar (triangle shaped), a database table is created. Within this database table, all the necessary attraction attribute columns are added. Now all that needs to be done is to load all the atttraction data. Download the file containing all of the attraction data in our data csv project file: [complete_data.md](https://github.com/DeerEdge/2022-FBLA-Nationals-Coding-and-Programming/blob/main/complete_data.csv)







