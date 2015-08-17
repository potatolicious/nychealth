import csv
import os
import sys
import psycopg2
from datetime import datetime

dbHost = os.environ['SQL_HOST']
dbPort = os.environ['SQL_PORT']
dbUser = os.environ['SQL_WRITE_USER']
dbPwd = os.environ['SQL_WRITE_PASSWORD']
dbName = os.environ['SQL_DBNAME']

print "Running load script..."

if len(sys.argv) < 2:
    sys.exit("Input file is required - run this script again with the path to the CSV data file")

csvpath = sys.argv[1]

if not dbHost or not dbPort or not dbUser:
    sys.exit("No database credentials defined - are you sure you've sourced your credentials file?")

print "Testing connection to `%s` with provided credentials..." % dbHost

try:
    dbConn = psycopg2.connect(host=dbHost, password=dbPwd, user=dbUser, database=dbName, port=dbPort)
except psycopg2.Error as e:
    sys.exit("Error connecting to database: %s" % e)

try:
    dbCur = dbConn.cursor()
    dbCur.execute("SELECT * FROM information_schema.tables WHERE table_name='inspections'")
    if dbCur.rowcount > 0:
        print "Table already exists."
    else:
        print "Creating table..."
        dbCur.execute("CREATE TABLE inspections(id serial PRIMARY KEY, dba varchar, \
        camis varchar, borough varchar, zipcode varchar, streetnum varchar, \
        streetname varchar, biztype varchar, violationcode varchar, \
        violationdescription text, action text, criticalflag varchar, \
        score varchar, grade varchar, inspectiontype varchar, inspectiondate date, \
        gradedate date, recorddate date);")

        dbCur.execute("CREATE INDEX bizname ON inspections ((lower(dba)))")
except psycopg2.Error as e:
    sys.exit("Error creating table: %s" % e)

print "Drop existing rows..."
try:
    dbCur.execute("DELETE FROM inspections")
except psycopg2.Error as e:
    sys.exit("Unable to delete existing data from table: %s" %e)

print "Loading CSV data from %s" % csvpath

with open(csvpath, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    dateFormat = '%m/%d/%Y'
    rowsProcessed = 0
    for row in reader:
        bizName = row['DBA']
        camis = row['CAMIS']
        borough = row['BORO']
        zipCode = row['ZIPCODE']
        streetNum = row['BUILDING']
        streetName = row['STREET']
        bizType = row['CUISINE DESCRIPTION']
        inspectDateStr = row['INSPECTION DATE']
        violationCode = row['VIOLATION CODE']
        violationDesc = row['VIOLATION DESCRIPTION']
        action = row['ACTION']
        criticalFlag = row['CRITICAL FLAG']
        score = row['SCORE']
        grade = row['GRADE']
        gradeDateStr = row['GRADE DATE']
        recordDateStr = row['RECORD DATE']
        inspectionType = row['INSPECTION TYPE']

        inspectionDate = None
        gradeDate = None
        recordDate = None
        if inspectDateStr:
            inspectionDate = datetime.strptime(inspectDateStr, dateFormat)
        if gradeDateStr:
            gradeDate = datetime.strptime(gradeDateStr, dateFormat)
        if recordDateStr:
            recordDate = datetime.strptime(recordDateStr, dateFormat)

        values = {'dba': bizName, 'camis': camis, 'borough': borough,
        'zipcode': zipCode, 'streetnum': streetNum, 'streetname': streetName,
        'biztype': bizType, 'violationcode': violationCode,
        'violationdescription': violationDesc, 'action': action,
        'criticalflag': criticalFlag, 'score': score, 'grade': grade,
        'inspectiontype': inspectionType, 'inspectiondate': inspectionDate,
        'gradedate': gradeDate, 'recorddate': recordDate}

        dbCur.execute("INSERT INTO inspections (dba, camis, borough, zipcode, \
            streetnum, streetname, biztype, violationcode, \
            violationdescription, action, criticalflag, score, grade, inspectiontype, \
            inspectiondate, gradedate, recorddate) VALUES(%(dba)s, %(camis)s, \
            %(borough)s, %(zipcode)s, %(streetnum)s, %(streetname)s, \
            %(biztype)s, %(violationcode)s, %(violationdescription)s, \
            %(action)s, %(criticalflag)s, %(score)s, %(grade)s, %(inspectiontype)s, \
            %(inspectiondate)s, %(gradedate)s, %(recorddate)s)", values)

        rowsProcessed += 1
        if (rowsProcessed % 50 == 0):
            print "Loaded %s rows" % rowsProcessed

print "Commit changes..."
dbConn.commit()

print "Shutting down DB connection..."
dbCur.close()
dbConn.close()

print "*** DONE ***"
