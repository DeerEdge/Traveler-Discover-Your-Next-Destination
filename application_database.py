#!/usr/bin/python
import psycopg2
# import time

from application_filter_request import FilterRequest
from SQLParser import parse

sql = 'SELECT * from ATTRACTION'
whereClauseAdded = False

def getAttractions(filters):
    global sql
    conn = None
    try:
        # start = time.time()
        whereClauseAdded = False
        # read connection parameters
        params = parse()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        generateSQL(filters)
        cur.execute(sql)
        # display the PostgreSQL database server version
        results = cur.fetchall()
        # close the communication with the PostgreSQL
        cur.close()
        # print('Time taken for DB query: '+ str(end - start))
        # start = time.time()
        return results
    finally:
        if conn is not None:
            conn.close()
    return None

def generateSQL(filters):
    global sql
    global whereClauseAdded
    sql = 'SELECT * from ATTRACTION'
    whereClauseAdded = False
    if filters.state is not None:
        checkClause()
        sql += ' state = \'' + filters.state + '\''
    if filters.city is not None:
        checkClause()
        sql += 'city = \'' + filters.city + '\''
    if filters.type is not None:
        checkClause()
        sql += 'type = \'' + filters.type + '\''
    if filters.wheelchairAccess is not None:
        checkClause()
        sql += 'WHEELCHAIR_ACCESSIBILITY = ' + str(filters.wheelchairAccess)
    if filters.familyFriendly is not None:
        checkClause()
        sql += 'FAMILY_FRIENDLY = ' + str(filters.familyFriendly)
    if filters.petFriendly is not None:
        checkClause()
        sql += 'PET_FRIENDLY = ' + str(filters.petFriendly)
    # print('Time taken for generateSQL: ' + str(end - start))
    # start = time.time()

def checkClause():
    global sql
    global whereClauseAdded
    if not whereClauseAdded:
        sql += ' WHERE '
        whereClauseAdded = True
    else:
        sql += ' AND '

# if __name__ == '__main__':
#     getAttractions(filters=FilterRequest('Alaska', None, None, True, None, None))
#     print("===============================")
    # getAttractions(filters=FilterRequest('Alaska', 'Anchorage', 'Sports', None, None, None))
    # print("===============================")
    # getAttractions(filters=FilterRequest(state='Alaska', city='Anchorage'))
    # getAttractions(filters=FilterRequest(state='Alaska', city='Anchorage', container='Sports'))
