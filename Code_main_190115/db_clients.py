#great manual: https://www.w3schools.com/python/python_mysql_getstarted.asp
#manuar for sql statements: https://mariadb.com/kb/en/library/insert/#examples
#do not change any of the functions -> read will not work anymore
#globals


#imports
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="rp-admin.local",
  user="pi",
  passwd="pi",
  database="BeerGame"
)

#Initiate SQL-Statement
mycursor = mydb.cursor()

  
#Insert Data
#mycursor.execute("UPDATE `team` SET `already_taken`='49' WHERE  `team_id`=9")
#mydb.commit()
  
 
#SQL-Query
#mycursor.execute("SELECT * FROM team")
#myresult = mycursor.fetchall()
#for x in myresult:
#  print(x)
  
#Close Database-Connection
#mydb.close


# Display Teams for Team selection in Login Page Dropdown
def readTeams():
    mycursor.execute("SELECT team_id FROM team WHERE already_taken = 0")
    teams = mycursor.fetchall()
    return teams

# Check if team is already selected from other group
def readTeamTaken(selectedTeam):
    print (str(selectedTeam))
    statement = "SELECT already_taken FROM team WHERE team_id = '" + str(selectedTeam) + "'"
    mycursor.execute(statement)
    alreadyTaken = mycursor.fetchall()
    print(alreadyTaken)
    return alreadyTaken

# Read from db which values the admin entered per team
def readInitialTeamValues(team):
    statement = "SELECT budget, cost_inbound_wh, cost_outbound_wh, cost_backlog FROM team WHERE team_id = '" + str(team) + "'"
    mycursor.execute(statement)
    teamValues = mycursor.fetchall()
    statement2= "SELECT product_name, production_time, initial_inbound_amount FROM product WHERE team_id = '" + str(team) + "'"
    mycursor.execute(statement2)
    productValues = mycursor.fetchall()
    return teamValues, productValues

def setTeamTaken(team):
    statement3 = "UPDATE team SET already_taken = 1 WHERE team_id = " + str(team)
    print(statement3)
    mycursor.execute(statement3)
    mydb.commit()
    print("update oki")

#read from db the default values for game initiation
def readInitiatialProductValues():
    statement="SELECT team_id, product_name, production_time, initial_inbound_amount FROM product"
    mycursor.execute(statement)
    initialValues=mycursor.fetchall()
    for x in initialValues:
        print(x)

def setAdminTeamValues(budget, costInboundWH, costOutboundWH, costBacklog ):
    statement ="UPDATE team SET budget =" + budget + ", cost_inbound_wh = " + costInboundWH + ", cost_outbound_wh = "+ costOutboundWH +", cost_backlog = " + costBacklog
    mycursor.execute(statement)
    mydb.commit()

def writeAdminProductValues(teamID, productName, productionTime, initialInboundAmount):
    statement = "UPDATE product SET production_time = " + productionTime + ", initial_inbound_amount = " + initialInboundAmount + " WHERE product_name = '" + productName + "' AND team_id = '" + str(teamID) + "'"
    mycursor.execute(statement)
    mydb.commit()

def writeAdminRoundValues(roundNumber, roundDuration):
    statement = "INSERT INTO rounds(round_number, round_duration_fixed) VALUES (" + str(roundNumber) + ", " + str(roundDuration) + ")"
    mycursor.execute(statement)
    mydb.commit()


def readInbound(teamId):
    statement ="SELECT inbound_id, to_team, product_name, amount FROM inbound WHERE to_team = '" + str(teamId) + "'"
    mycursor.execute(statement)
    inbound = mycursor.fetchall()
    return inbound

def readOutbound(teamId):
    statement = "SELECT outbound_id, from_team, product_name, amount FROM outbound WHERE from_team = '" + str(teamId) + "'"
    mycursor.execute(statement)
    outbound = mycursor.fetchall()
    return outbound

def readProduction(teamId):
    statement = "SELECT production_id, team_id, product_name, amount FROM production WHERE team_id = '" + str(teamId) + "'"
    mycursor.execute(statement)
    production = mycursor.fetchall()
    return production

def readOrders(teamId):
    statement = "SELECT order_id, to_team, product_name, amount, round_number FROM orders WHERE to_team = '" + str(teamId) + "'"
    mycursor.execute(statement)
    order = mycursor.fetchall()
    return order

def readLastOutbound(teamId, roundCount):
    statement = "SELECT outbound_id, from_team, product_name, amount FROM outbound WHERE from_team = '" + str(teamId) + "' AND round_number = '" + str(roundCount) + "'"
    mycursor.execute(statement)
    outbound = mycursor.fetchall()
    return outbound

# set the actual start time of a round in the database
def writeRoundStartTimestamp(roundNumber):
    timestamp = datetime.datetime.now()
    statement = "UPDATE rounds SET start_time_actual = '" + str(timestamp) + "' WHERE round_number = '" + str(roundNumber) + "'"
    mycursor.execute(statement)
    mydb.commit()

# set the actual end time of a round in the database
def writeRoundEndTimestamp(roundNumber):
    timestamp = datetime.datetime.now()
    statement = "UPDATE rounds SET end_time_actual = '" + str(timestamp) + "' WHERE round_number = '" + str(roundNumber) + "'"
    mycursor.execute(statement)
    mydb.commit()

def resetValues():
    statement1 = "DELETE FROM rounds"
    statement2 = "UPDATE team SET already_taken = 0"
    statement3 = "DELETE FROM orders"
    statement4 = "DELETE FROM production"
    statement5 = "DELETE FROM inbound"
    statement6 = "DELETE FROM outbound"
    mycursor.execute(statement1)
    mycursor.execute(statement2)
    mycursor.execute(statement3)
    mycursor.execute(statement4)
    mycursor.execute(statement5)
    mycursor.execute(statement6)
    mydb.commit()


def writeOrder(toTeam, fromTeam, productName, roundNumber, amount):
    timestamp = datetime.datetime.now()
    statement = "INSERT INTO orders (to_team, from_team, product_name, round_number, amount, time_stamp) VALUES ('"+ str(toTeam)+"', '"+ str(fromTeam)+ "', '"+ str(productName) +"', '"+ str(roundNumber) +"', '"+ str(amount) +"', '"+ str(timestamp) +"')"
    mycursor.execute(statement)
    mydb.commit()

def writeProduction(teamId, productName, roundNumber, amount, totalProductionTime):
    timestamp = datetime.datetime.now()
    statement = "INSERT INTO production (team_id, product_name, round_number, amount, total_production_time, time_stamp) VALUES ('"+ str(teamId)+"', '"+ str(productName) +"', '"+ str(roundNumber) + "', '" + str(amount) +"', '" + str(totalProductionTime) + "', '" + str(timestamp) +"')"
    mycursor.execute(statement)
    mydb.commit()

def writeOutbound(fromTeam, toTeam, productName, roundNumber, amount):
    timestamp = datetime.datetime.now()
    statement = "INSERT INTO outbound (to_team, from_team, product_name, round_number, amount, time_stamp) VALUES ('"+ str(toTeam)+"', '"+ str(fromTeam)+ "', '"+ str(productName) +"', '"+ str(roundNumber) +"', '"+ str(amount) +"', '"+ str(timestamp) +"')"
    mycursor.execute(statement)
    mydb.commit()

def writeInbound(toTeam, fromTeam, productName, roundNumber, amount):
    timestamp = datetime.datetime.now()
    statement = "INSERT INTO inbound (to_team, from_team, product_name, round_number, amount, time_stamp) VALUES ('"+ str(toTeam)+"', '"+ str(fromTeam)+ "', '"+ str(productName) +"', '"+ str(roundNumber) +"', '"+ str(amount) +"', '"+ str(timestamp) +"')"
    mycursor.execute(statement)
    mydb.commit()
