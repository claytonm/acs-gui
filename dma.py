import MySQLdb
import easygui as eg
import os
import sys

class IO(object):
    def __init__(self):
        pass
    
    def createList(self,filename):
        """
        Reads single column from filename.txt and creates a list.
        """
        List = []
        inputFile = open(filename)
        for line in inputFile:
            List.append(line.strip("\n"))
        return List
    
    def createDict(self,filename):
        """
        Reads two columns from filename.txt and creates a dictionary,
        with key values equal to the first column, and values equal to
        second column.
        """
        Dict = {}
        inputFile = open(filename)
        for line in inputFile:
            lst = line.rsplit(",", 1)
            Dict[lst[0]] = lst[1].strip("\n")
        return Dict

    

#----------------------------------- End of IO class -----------------------------------------------
#----------------------------------- Beginning of Session class ------------------------------------

class Session(object):
    def __init__(self):
        self.dbList = IO.createList("dbList.txt")
        self.dbDict = IO.createDict("dbDict.txt")
        
        
    def dbChoice(self):
        """
        Gives user a list of databases to choose from in human-readable form,
        as read-in from dbList.txt. Returns the database that the user chooses as
        string db, which matches the database name as it appears in MySQL.
        """
        while True:
            dbChoice = eg.multchoicebox(msg="Choose your dataset.", title="Dataset Selection",\
                                        choices=self.dbList)
            db = self.dbDict[dbChoice[0]]
            if db == None or db == []:
                    contButton = eg.buttonbox(msg="You must choose a geography. \n" + \
                                              "To try again, press 'Try Again.' \n" +\
                                           "To exit the program, choose 'Exit'.", \
                                           title="No geography chosen.", \
                                           choices=("Try Again", "Exit"))
                    if contButton == "Try Again": continue
                    if contButton == "Exit":
                            sys.exit()
            if len(dbChoice) > 1:
                contButton = eg.buttonbox(msg="You can only choose one geography at a time. \n" + \
                                              "To try again, press 'Try Again.' \n" +\
                                           "To exit the program, choose 'Exit'.", \
                                           title="More than one geography chosen.", \
                                           choices=("Try Again", "Exit"))
                if contButton == "Try Again": continue
                if contButton == "Exit":
                        sys.exit()
            return db

    def getGeo(self,db):
        """
        Gives user choice of geographies in human-readable form, as read-in from the list
        db+\\+db+"Geos.txt". Returns the value that corresponds to this geography in
        geoDict.txt. This geo is the name of a geography table in MySQL.
        """
        while True:
            geoChoice = eg.multchoicebox(msg="Choose your geography.", title="Geography Selection",\
                                         choices=IO.createList(db + "\\" + db + "Geos.txt"))
            geo = IO.createDict(db + "\\" + db + "GeosDict.txt")[geoChoice[0]]
            if geoChoice == None or geoChoice == []:
                    contButton = eg.buttonbox(msg="You must choose a geography. \n" + \
                                              "To try again, press 'Try Again.' \n" +\
                                           "To exit the program, choose 'Exit'.", \
                                           title="No geography chosen.", \
                                           choices=("Try Again", "Exit"))
                    if contButton == "Try Again": continue
                    if contButton == "Exit":
                            sys.exit()
            if len(geoChoice) > 1:
                contButton = eg.buttonbox(msg="You can only choose one geography at a time. \n" + \
                                              "To try again, press 'Try Again.' \n" +\
                                           "To exit the program, choose 'Exit'.", \
                                           title="More than one geography chosen.", \
                                           choices=("Try Again", "Exit"))
                if contButton == "Try Again": continue
                if contButton == "Exit":
                        sys.exit()
            if geo == 'MAPC Study Areas':
                while True:
                        studyArea = eg.choicebox(msg="Pick an MAPC Study Area.",\
                                                 choices=IO.createList("studyAreas.txt"))
                        if studyArea == None or studyArea == []:
                            contButton = eg.buttonbox(msg="You must choose some study area.", \
                                                      title="No study area chosen.", \
                                                      choices=("Try Again", "Exit"))
                            if contButton == "Try Again": continue
                            if contButton == "Exit": sys.exit()
                        else: break
                studyArea = IO.createDict("studyAreasDict.txt")[studyArea] # studyArea = NSP1, etc.
                geo = IO.createDict("studyAreaGeoTablesDict.txt")[studyArea]
                geoStudyArea = IO.createDict("studyAreaGeoDict.txt")[studyArea]
                return geo, studyArea, geoStudyArea
            if geo != "MAPC Study Areas":
                return geo, None, None
            
    def getVars(self,db):
        """
        Accepts the list of all variables, and returns the variables that the user has chosen.
        """
        while True:
                vList = eg.multchoicebox(msg="Choose the variables you want.", title="Variable Selection",\
                                         choices=IO.createList(db + "\\" + db + "Vars.txt"))
                if vList == None or vList == []:
                        contButton = eg.buttonbox(msg="You must choose some variables. \n" + \
                                                  "To try again, press 'Try Again.' \n" +\
                                               "To exit the program, choose 'Exit'.", \
                                               title="No variables chosen.", \
                                               choices=("Try Again", "Exit"))
                        if contButton == "Try Again": continue
                        if contButton == "Exit":
                                c.close()
                                conn.close()
                                sys.exit()
                else: return vList

    def sumDict(self, vList):
        """
        Accepts list of variables that the user has chosen.
        Returns a dictionary that maps newColumnNames ->
        list of variables from vList. The list of variables
        are variables whose sum the user wants to insert into
        newColumnName columns.
        """
        continueYN = eg.buttonbox(msg="Do you want to add some of your \n" \
                                   "variables together to create a new variable?", \
                                  choices=("Yes", "No"))
        if continueYN == "No": return None
        sumDict = {}
        Count = 0
        while True:
            Count = Count + 1
            newColName = eg.enterbox(msg="Name the column that will contain the sum of your variables. \n"\
                                     "Name must be a valid column name (cannot begin with a \n"\
                                     "number, cannot contain spaces, etc.)", title="Name your variable.",\
                                     strip=True, default="newColumn" + str(Count))
            if newColName in sumDict.keys():
                contButton = eg.buttonbox(msg="You cannot give a column the same name as another column. \n" \
                             "To pick another name, press 'Try Again.' \n" \
                             "To skip without adding more columns, press 'Skip.'", choices=("Try Again.", "Skip."))
                if contButton == 'Try Again.': pass
                if contButton == 'Skip.': break
            vListChoices = eg.multchoicebox(msg="Choose the variables you want to add together.", title="Variable Sum", \
                                             choices=vList)
            if vListChoices == None or vListChoices == []:
                contButton = eg.buttonbox(msg="Do you want to continue without adding any variables? \n" \
                                          "If so, press 'Do Not Add' \n" \
                                          " Otherwise, press 'Try again'.", \
                                          title="No variables chosen.", \
                                          choices=("Do Not Add", "Try Again"))
                if contButton == "Try Again": continue
                if contButton == "Do Not Add" and len(sumDict) == 0: return None
                if contButton == "Do Not Add" and len(sumDict) != 0: return sumDict
            sumDict[newColName] = vListChoices
            continueYN = eg.buttonbox(msg="Do you want to add more variables together?", choices=("Yes", "No"))
            if continueYN == "No": break
        if sumDict == {}: return None
        return sumDict

    def getPathName(self):
        """
        Asks user to specify a table name and path name to save to.
        Checks to make sure that table name does not already exist.
        """
        while True:
                tableSaveName = eg.filesavebox(msg="Choose your file name and location.")
                if tableSaveName == None:
                        contButton = eg.buttonbox(msg="You need to name your file.", \
                                               title="No table name or location chosen.", \
                                               choices=("Try Again", "Exit"))
                        if contButton == "Try Again": continue
                        if contButton == "Exit":
                                sys.exit() 
                if not os.path.exists(tableSaveName):
                        return tableSaveName.replace("\\", "/")
                        break
                continueChoice = eg.ccbox(msg="The table you have chosen already exists. \n " + \
                                          "Click 'Continue' to choose a different name")
                if continueChoice == 0:
                        sys.exit()

    def primaryKey(self, db):
        return IO.createDict("pkDict.txt")[db]
        

    

#------------------------------------------ End Session Class -----------------------------------------------
#------------------------------------------ Beginng of SQL Class --------------------------------------------


class SQL(object):
    def __init__(self, db, geo, pK, pathName, vList, studyArea = None, geoStudyArea = None, sumDict = None):
        self.db = db
        self.geo = geo
        self.pK = pK
        self.pathName = pathName
        self.tableName = pathName.split("/")[-1]
        self.tableName_agg = self.tableName + "_agg"
        self.studyArea = studyArea
        self.geoStudyArea = geoStudyArea
        self.vList = list(vList)
        self.sumDict = sumDict
        self.varDict = IO.createDict(db + "\\" + db + "VarTableDict.txt")

    def connect(self):
        conn = MySQLdb.connect(host="localhost", user="root", passwd="max1max2", db = self.db)
        c = conn.cursor()
        return c

    def dropTable(self):
        sql = "DROP TABLE IF EXISTS " + self.tableName +", " + self.tableName_agg
        c.execute(sql)
        

    def createTable(self):
        """
        Creates tables with GEOIDs and column names and types. Primary key is logrecno
        """
        if self.pK == "logrecno":
            sql = "CREATE TABLE " + self.tableName + " AS SELECT GEOID10, " + self.pK + ", geoname FROM " + self.geo
        else:
            sql = "CREATE TABLE " + self.tableName + " AS SELECT " + self.pK + ", LOGRECNO, geoname FROM " + self.geo
        c.execute(sql)
        sqlPK = "ALTER TABLE " + self.tableName + " ADD PRIMARY KEY(" + self.pK + ")"
        c.execute(sqlPK)

    def makeTable(self):
        """
        Accepts table name and variable list, and adds variables to
        table as blank columns. All variables are of type DOUBLE
        """
        for var in self.vList:
            c.execute("ALTER TABLE " + self.tableName + " ADD " + var + " DOUBLE")

    def addData(self):
        """
        Accepts table with column names and GEOIDs, a list of variables, and
        variableName -> seqTable dictionary. Returns table populated
        with data.
        """
        for var in self.vList:
            seqTable = self.varDict[var]
            sql = "UPDATE " + self.tableName + " INNER JOIN " + seqTable + \
                  " ON " + self.tableName + "." + self.pK + " = " + seqTable + "." + self.pK + " SET " + \
                  self.tableName + "." + var + " = " + seqTable + "." + var
            c.execute(sql)

    def createTableAgg(self):
        """
        Accepts variable list, studyArea name, and outputs SQL aggregation string.
        i.e. var1, var2 -> "SUM(e.var1) AS var1, SUM(e.var2)".
        """
        SQL = ""
        for i in range(0, len(self.vList) - 1):
                SQL = SQL + "SUM(e." + self.vList[i] + ") AS " + self.vList[i] + ", "
        SQL = SQL + "SUM(e." + self.vList[-1] + ") AS " + self.vList[-1]
        aggSQL = "CREATE TABLE " + self.tableName_agg + " AS SELECT sa." + self.studyArea + ", " + \
                 SQL + " FROM " + self.tableName + " e " + "INNER JOIN " + self.geoStudyArea + \
                 " sa ON e.GEOID10 = sa.GEOID10 WHERE NOT sa." + self.studyArea + " IS NULL GROUP BY sa." + self.studyArea
        alterSQL = "ALTER TABLE " + self.tableName_agg + " ADD PRIMARY KEY(" + self.studyArea + ")"
        c.execute(aggSQL)
        c.execute(alterSQL)

    def sumDictSQL(self):
        """
        Accepts dictionary mapping newVarNames -> list of columns to add to get newVar column.
        Also accepts list of original variables the user chose. Creates dictionary mapping
        newVarnames -> SQL sum statement (ie newVar1 -> 'col1 + col2 = ...'. Also adds the
        newVarNames to the original variableList.
        """
        sumDictSQL= {}
        for newVar in self.sumDict.keys():
                self.vList.append(newVar)
        for newVar in self.sumDict.keys():
                SQL = ""
                for i in range(0, len(self.sumDict[newVar]) - 1):
                               SQL = SQL + self.sumDict[newVar][i] + " + "
                SQL = SQL + self.sumDict[newVar][-1]
                sumDictSQL[newVar] = SQL
        return sumDictSQL


    def addSumColumns(self, table):
        for var in self.sumDict.keys():
                c.execute("ALTER TABLE " + table + " ADD " + var + " DOUBLE")

    def populateSumColumns(self,table, sumDictSQL):
        for varName in sumDictSQL.keys():
                SQL = "UPDATE " + table + " SET " + varName + " = " + sumDictSQL[varName]
                c.execute(SQL)

    def createHeader(self):
        SQL = ""
        if not self.studyArea == None:
                SQL = "'" + self.studyArea + "', "
                for i in range(0, len(self.vList)-1):
                        SQL = SQL + "'" + self.vList[i] + "', "
                SQL = SQL + "'" + self.vList[-1] + "'"
        if self.studyArea == None:
            SQL = "'GEOID10', 'logrecno', 'geoname', "
            for i in range(0, len(self.vList)-1):
                SQL = SQL + "'" + self.vList[i] + "', "
            SQL = SQL + "'" + self.vList[-1] + "'"
        return SQL
 
    def exportTable(self, studyArea, headerList):
        """
        Exports tables to csv files depending on whether the user has asked to aggregate data or not.
        """
        if not self.studyArea == None:
                SQL_E = "SELECT " + headerList + " UNION " +\
                        "SELECT * INTO OUTFILE '" + self.pathName + ".csv' FIELDS TERMINATED BY ','"\
                        "OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' FROM "  + self.tableName_agg
                
                c.execute(SQL_E)
        if self.studyArea == None:
                SQL_E = "SELECT " + headerList + " UNION " +\
                        "SELECT * INTO OUTFILE '" + self.pathName + ".csv' FIELDS TERMINATED BY ','"\
                        "OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' FROM "  + self.tableName

                
                c.execute(SQL_E)

#---------------------------------------------End of SQL class --------------------------------------------------
#---------------------------------------------Beginning of sqlMOE class -----------------------------------------
                
class moeSQL(SQL):
    def __init__(self):
        self.db = SQL.db
        self.geo = SQL.geo
        self.pK = SQL.pK
        self.pathName = SQL.pathName + "_ME"
        self.tableName = SQL.tableName + "_ME"
        self.tableName_agg = self.tableName + "_agg"
        self.studyArea = SQL.studyArea
        self.geoStudyArea = SQL.geoStudyArea 
        self.vList = list(vList)
        self.sumDict = sumDict
        self.varDict = IO.createDict(db + "\\" + db + "VarTableDict_M.txt")

    def createTableAgg(self):
        SQL = ""
        for i in range(0, len(self.vList) - 1):
                SQL = SQL + "SQRT(SUM(POW(m." + self.vList[i] + ", 2))) AS " + self.vList[i] + ", "
        SQL = SQL + "SQRT(SUM(POW(m." + self.vList[-1] + ", 2))) AS " + self.vList[-1]
        aggSQL = "CREATE TABLE " + self.tableName_agg + " AS SELECT sa." + self.studyArea + ", " + \
                 SQL + " FROM " + self.tableName + " m INNER JOIN " + self.geoStudyArea + \
                 " sa ON m.GEOID10 = sa.GEOID10 WHERE NOT sa." + self.studyArea + " IS NULL GROUP BY sa." + self.studyArea
        alterSQL = "ALTER TABLE " + self.tableName_agg + " ADD PRIMARY KEY(" + self.studyArea + ")"
        c.execute(aggSQL)
        c.execute(alterSQL)

    def sumDictSQL(self):
        """
        Accepts dictionary mapping newVarNames -> list of columns to add to get newVar column.
        Also accepts list of original variables the user chose. Creates dictionary mapping
        newVarnames -> SQL sum statement (ie newVar1 -> 'col1 + col2 = ...'. Also adds the
        newVarNames to the original variableList.
        """
        sumDictSQL_M = {}
        for newVar in self.sumDict.keys():
                SQL = ""
                for i in range(0, len(self.sumDict[newVar]) - 1):
                               SQL = SQL + "POW(" + self.sumDict[newVar][i] + ", 2) + "
                SQL = SQL + "POW(" + self.sumDict[newVar][-1] + ", 2)"
                SQL = "SQRT(" + SQL + ")"
                sumDictSQL_M[newVar] = SQL
        return sumDictSQL_M


#----------------------------------------------------End sqlMOE Class -----------------------------------------
#----------------------------------------------------Run Program-----------------------------------------------


IO = IO()
session = Session()
db = session.dbChoice()
print db
geo, studyArea, geoStudyArea = session.getGeo(db)
print geo
vList = session.getVars(db)
sumDict = session.sumDict(vList)
pathName = session.getPathName()
print pathName
pK = session.primaryKey(db)
print pK



SQL = SQL(db,geo, pK, pathName, vList,studyArea, geoStudyArea, sumDict)
c = SQL.connect()
SQL.dropTable()
SQL.createTable()
SQL.makeTable()
SQL.addData()

#-------------aggregates data to study area, if user chose to do so ----------------
if not studyArea == None:
    SQL.createTableAgg()


#---- handles case where user creates new derived variables -------
    
if not sumDict == None:
    if studyArea == None:
        sumDictSQL = SQL.sumDictSQL()
        SQL.addSumColumns(SQL.tableName)
        SQL.populateSumColumns(SQL.tableName, sumDictSQL)
    if not studyArea == None:
        sumDictSQL = SQL.sumDictSQL()
        SQL.addSumColumns(SQL.tableName_agg)
        SQL.populateSumColumns(SQL.tableName_agg, sumDictSQL)


#-------creates table header and exports to .csv -----------------

headerList = SQL.createHeader()

SQL.exportTable(studyArea, headerList)
SQL.dropTable()


#---- creates MOE tables for those databases that have MOE tables -------

if db in IO.createList("moeDb.txt"):
    moeSQL = moeSQL()
    c = moeSQL.connect()
    moeSQL.dropTable()
    moeSQL.createTable()
    moeSQL.makeTable()
    moeSQL.addData()
    
    if not studyArea == None:
        moeSQL.createTableAgg()

    if not sumDict == None:
        if studyArea == None:
            sumDictSQL = moeSQL.sumDictSQL()
            moeSQL.addSumColumns(moeSQL.tableName)
            moeSQL.populateSumColumns(moeSQL.tableName, sumDictSQL)
        if not studyArea == None:
            sumDictSQL = moeSQL.sumDictSQL()
            moeSQL.addSumColumns(moeSQL.tableName_agg)
            moeSQL.populateSumColumns(moeSQL.tableName_agg, sumDictSQL)
            
    moeSQL.exportTable(studyArea, headerList)
    moeSQL.dropTable()

                                                 
        

    
        
        
