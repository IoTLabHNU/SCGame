import Tkinter as tk
from Tkinter import IntVar
import tkFont as font
#import write_orders
#from oauth2client.service_account import ServiceAccountCredentials
import atexit
import socket
import threading
import time

#new imports
import db_clients
import Write as write
import Read as read

class BeerGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.minsize(width=640, height=480)
        self.resizable(width=False, height=False)
        #global team_sheet
        #team_sheet = gspread.Spreadsheet
        #global master_sheet
        #master_sheet = gspread.Spreadsheet
        #global client
        client = None

        #definition of fonts and variables used
        global helv38
        helv38 = font.Font(family='Helvetica', size=38, weight='bold')
        global helv36
        helv36 = font.Font(family='Helvetica', size=36, weight='bold')
        global helv30
        helv30 = font.Font(family='Helvetica', size=30, weight='bold')
        global helv22b
        helv22b = font.Font(family='Helvetica', size=22, weight='bold')
        global helv22
        helv22 = font.Font(family='Helvetica', size=22, weight='normal')
        global helv18
        helv18 = font.Font(family='Helvetica', size=18, weight='normal')
        global helv18b
        helv18b = font.Font(family='Helvetica', size=18, weight='bold')
        global  helv13
        helv13 = font.Font(family='Helvetica', size=13, weight='normal')
        global  helv13b
        helv13b = font.Font(family='Helvetica', size=13, weight='bold')
        global  helv16
        helv16 = font.Font(family='Helvetica', size=16, weight='normal')
        global  helv16b
        helv16b = font.Font(family='Helvetica', size=16, weight='bold')
        global helv14
        helv14 = font.Font(family='Helvetica', size=14, weight='bold')
        global helv12
        helv12 = font.Font(family='Helvetica', size=12, weight='bold')
        global helv10
        helv10 = font.Font(family='Helvetica', size=10, weight='bold')
        global helv9b
        helv9b = font.Font(family='Helvetica', size=9, weight='bold')
        global helv9
        helv9 = font.Font(family='Helvetica', size=9, weight='normal')
        global helv8
        helv8 = font.Font(family='Helvetica', size=8, weight='normal')
        global helv8b
        helv8b = font.Font(family='Helvetica', size=8, weight='bold')
        global inputWidth
        inputWidth = 7
        global labelTimer
        labelTimer = tk.Label()
        self.team = 0
        global roundCount
        roundCount = 1
        global isRunning
        isRunning = False
        global timeOrdered
        timeOrdered = ""
        global gamePage


        gamePage = threading.Event()
        #show start page
        self.switch_frame(StartPage)

    def getTeam(self):
        return self.team

    def setTeam(self, selected_team):
        self.team = selected_team


    def nextRound(self):
        #show game page
        self.switch_frame(GamePage)
        labelroundCount.config(text="Runde: " + str(roundCount))
        hasPlayed=False

    def switch_frame(self, frame_class, *args):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
    def resetWorksheet(self):
        #Reset Balance to default value
        team_sheet.update_acell('B14', master_sheet.acell('B25').value)
        
        #Reset Inventories to Startinventories
        inventories = team_sheet.range('B9:B12')
        startinventories = master_sheet.range('B21:E21')
        for i in range(0,len(inventories)):
            inventories[i].value = startinventories[i].value 
        team_sheet.update_cells(inventories)

        #Clear out logged orders
        orders = team_sheet.range('B3:AY6')
        for order in orders:
            order.value = 0
        team_sheet.update_cells(orders)

        #Clear out open orders
        openOrders = team_sheet.range('E9:E12')
        for cell in openOrders:
            cell.value = 0
        team_sheet.update_cells(openOrders)

#login page
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        
        """
        label = tk.Label(self, text = "Wilkommen zum Bierspiel!", font = helv36)
        loginButton = tk.Button(self, text="Login", relief="raised", command=self.callback_login)
        global labelStatus
        global statusTextVar
        self.statusTextVar = tk.StringVar()
        self.statusTextVar.set("Bitte legen Sie ihren NFC-Chip auf den Leser um sich einzuloggen")
        labelStatus = tk.Label(self, textvariable = self.statusTextVar, font = helv22)"""


        self.produceLimit = 0
        # set a label with the title of the page
        labelPage = tk.Label(self, text="Login - Team", font=helv22b)
        labelPage.grid(column=0, row=0)

        spacingrow = tk.Label(self, text="")
        spacingrow.grid(column=0, row=1)

        logindropdown = tk.Label(self, text="Choose a Team to login:", font=helv13b)
        # dropdown for team selection
        logindropdown.grid(column=0, row=2)
        # read available teams from db
        Teams = db_clients.readTeams()
        selected_team = tk.StringVar()
        selected_team.set(Teams[0])

        Team_menu = tk.OptionMenu(self, selected_team, *Teams)
        Team_menu.grid(column=0, row=3)

        self.button_login = tk.Button(self, text="Login", font=helv13, relief="raised", command=lambda: self.onClickLogin(selected_team.get()))
        self.button_login.grid(column=0, row=4)



    def onClickLogin(self, selected_team):
        taken = db_clients.readTeamTaken(selected_team[1])
        # avoid team that is already in use or chosen
        if taken == 1:
            popup = tk.Tk()
            popup.wm_title("Selection Error")
            label = tk.Label(popup, text="Team is taken, select an other one.", font=helv22)
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Okay", command=popup.destroy)
            B1.pack()
            popup.mainloop()
        else:
        # set team taken for selectetd team
            db_clients.setTeamTaken(selected_team[1])
            app.setTeam(selected_team[1])

            self.master.switch_frame(WaitForStartPage)


# actual game page during each round
class GamePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        gamePage.set()

        self.produceLimit =0
        self.timeLeft = 0
        #getting all data per team from db
        team = app.getTeam()
        self.teamValues, self.productValues = db_clients.readInitialTeamValues(team)
        self.inboundValues = db_clients.readInbound(team)
        self.outboundValues = db_clients.readOutbound(team)
        self.production = db_clients.readProduction(team)
        self.orders = db_clients.readOrders(team)
        #print ('team :' + team)

        # set Warehouse  inventory variables
        self.inventoryRawBlue = self.productValues[0][2]
        self.inventoryRawPurple = self.productValues[1][2]
        self.inventoryRawRed = self.productValues[2][2]
        self.inventoryRawYellow = self.productValues[3][2]

        for amount in self.inboundValues:
            if amount[2] == "blue":
                self.inventoryRawBlue += amount[3]
            if amount[2] == "purple":
                self.inventoryRawPurple += amount[3]
            if amount[2] == "red":
                self.inventoryRawRed += amount[3]
            if amount[2] == "yellow":
                self.inventoryRawYellow += amount[3]

        for amount2 in self.production:
            if amount2[2] == "blue":
                self.inventoryRawBlue -= amount2[3]
            if amount2[2] == "purple":
                self.inventoryRawPurple -= amount2[3]
            if amount2[2] == "red":
                self.inventoryRawRed -= amount2[3]
            if amount2[2] == "yellow":
                self.inventoryRawYellow -= amount2[3]

        # set Open Orders values variables (orders that WE have to deliver to the next team)
        openBlue = 0
        openPurple = 0
        openRed = 0
        openYellow = 0
        for order in self.orders:
            if order[4] == (roundCount - 1):
                if order[2] == "blue":
                    openBlue += order[3]
                if order[2] == "purple":
                    openPurple += order[3]
                if order[2] == "red":
                    openRed += order[3]
                if order[2] == "yellow":
                    openYellow += order[3]


        # set Warehouse inventory variables (outbound)
        self.fgBlue = 0
        self.fgPurple = 0
        self.fgRed = 0
        self.fgYellow = 0
        for production in self.production:
            if production[2] == "blue":
                self.fgBlue += production[3]
            if production[2] == "purple":
                self.fgPurple += production[3]
            if production[2] == "red":
                self.fgRed += production[3]
            if production[2] == "yellow":
                self.fgYellow += production[3]

        for outbound in self.outboundValues:
            if outbound[2] == "blue":
                self.fgBlue -= outbound[3]
            if outbound[2] == "purple":
                self.fgPurple -= outbound[3]
            if outbound[2] == "red":
                self.fgRed -= outbound[3]
            if outbound[2] == "yellow":
                self.fgYellow -= outbound[3]

        # set Backlog variables
        blBlue = 0
        blPurple = 0
        blRed = 0
        blYellow = 0
        for order in self.orders:
            if order[4] != (roundCount - 1):
                if order[2] == "blue":
                    blBlue += order[3]
                if order[2] == "purple":
                    blPurple += order[3]
                if order[2] == "red":
                    blRed += order[3]
                if order[2] == "yellow":
                    blYellow += order[3]

        for outbound in self.outboundValues:
            if outbound[2] == "blue":
                blBlue -= outbound[3]
            if outbound[2] == "purple":
                blPurple -= outbound[3]
            if outbound[2] == "red":
                blRed -= outbound[3]
            if outbound[2] == "yellow":
                blYellow -= outbound[3]


        # set administrative/information variables
        costInWH = self.teamValues[0][1]
        costOutWH = self.teamValues[0][2]
        costBL = self.teamValues[0][3]
        budgetLeft = self.teamValues[0][0]

        # set production time per product
        self.ptBlue = 0
        self.ptPurple = 0
        self.ptRed = 0
        self.ptYellow = 0
        for prod in self.productValues:
            if prod[0] == "blue":
                self.ptBlue += prod[1]
            if prod[0] == "purple":
                self.ptPurple += prod[1]
            if prod[0] == "red":
                self.ptRed += prod[1]
            if prod[0] == "yellow":
                self.ptYellow += prod[1]


        # set a label with the title of the page
        labelPage = tk.Label(self, text="Game", font=helv14)

        # Done-Button
        self.buttonDone = tk.Button(self, text="Done", relief='raised', font=helv9,
                                    command=lambda: self.background(self.onClickDone, ()))

        # set a label with the team (variable of class BeerGame)
        labelTeam = tk.Label(self, text="Team: " + str(team), font=helv12)

        # set label for giving the RM Warehouse table a title
        labelTable1 = tk.Label(self, text="Warehouse RM", font=helv9b)

        # set labels for the Warehouse
        self.labelBlue1 = tk.Label(self, text="Blue product: " + str(self.inventoryRawBlue), font=helv9)
        self.labelPurple1 = tk.Label(self, text="Purple product: " + str(self.inventoryRawPurple), font=helv9)
        self.labelRed1 = tk.Label(self, text="Red product: " + str(self.inventoryRawRed), font=helv9)
        self.labelYellow1 = tk.Label(self, text="Yellow product: " + str(self.inventoryRawYellow), font=helv9)


        # set label for giving the Open Deliveries table a title
        labelTable2 = tk.Label(self, text="Open Order", font=helv9b)

        # set labels for the Open Deliveries Table
        labelBlue2 = tk.Label(self, text="Blue product: " + str(openBlue), font=helv9)
        labelPurple2 = tk.Label(self, text="Purple product: " + str(openPurple), font=helv9)
        labelRed2 = tk.Label(self, text="Red product: " + str(openRed), font=helv9)
        labelYellow2 = tk.Label(self, text="Yellow product: " + str(openYellow), font=helv9)

        # set label for giving the FG Warehouse table a title
        labelTable3 = tk.Label(self, text="Warehouse FG", font=helv9b)

        # set labels for the FG Warehouse
        self.labelBlue3 = tk.Label(self, text="Blue product: " + str(self.fgBlue), font=helv9)
        self.labelPurple3 = tk.Label(self, text="Purple product: " + str(self.fgPurple), font=helv9)
        self.labelRed3 = tk.Label(self, text="Red product: " + str(self.fgRed), font=helv9)
        self.labelYellow3 = tk.Label(self, text="Yellow product: " + str(self.fgYellow), font=helv9)

        # set label for giving the Backlog table a title
        labelTable4 = tk.Label(self, text="Backlog", font=helv9b)

        # set labels for the Backlog
        labelBlue4 = tk.Label(self, text="Blue product: " + str(blBlue), font=helv9)
        labelPurple4 = tk.Label(self, text="Purple product: " + str(blPurple), font=helv9)
        labelRed4 = tk.Label(self, text="Red product: " + str(blRed), font=helv9)
        labelYellow4 = tk.Label(self, text="Yellow product: " + str(blYellow), font=helv9)

        # set label for giving the Production Input table a title
        labelTable5 = tk.Label(self, text="Production quantity?", font=helv9b)

        # set labels for the Production
        labelBlue5 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple5 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed5 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow5 = tk.Label(self, text="Yellow product: ", font=helv9)

        # Order-Button
        self.buttonProduce = tk.Button(self, text="Start production", relief='raised', font=helv9,
                                       command=lambda: self.background(self.onClickProduce(), ()))

        # set input fields for production
        self.entryBlueVarProduction = tk.IntVar()
        self.entryBlue5 = tk.Entry(self, textvariable=self.entryBlueVarProduction, font=helv9, width=inputWidth)
        self.entryPurpleVarProduction = tk.IntVar()
        self.entryPurple5 = tk.Entry(self, textvariable=self.entryPurpleVarProduction, font=helv9, width=inputWidth)
        self.entryRedVarProduction = tk.IntVar()
        self.entryRed5 = tk.Entry(self, textvariable=self.entryRedVarProduction, font=helv9, width=inputWidth)
        self.entryYellowVarProduction = tk.IntVar()
        self.entryYellow5 = tk.Entry(self, textvariable=self.entryYellowVarProduction, font=helv9, width=inputWidth)

        # set label for giving the Delivery Input table a title
        labelTable7 = tk.Label(self, text="Delivery quantity?", font=helv9b)

        # set labels for the Delivery
        labelBlue7 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple7 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed7 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow7 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set input fields for delivery
        self.entryBlueVarDelivery = tk.IntVar()
        self.entryBlue7 = tk.Entry(self, textvariable=self.entryBlueVarDelivery, font=helv9, width=inputWidth)
        self.entryPurpleVarDelivery = tk.IntVar()
        self.entryPurple7 = tk.Entry(self, textvariable=self.entryPurpleVarDelivery, font=helv9, width=inputWidth)
        self.entryRedVarDelivery = tk.IntVar()
        self.entryRed7 = tk.Entry(self, textvariable=self.entryRedVarDelivery, font=helv9, width=inputWidth)
        self.entryYellowVarDelivery = tk.IntVar()
        self.entryYellow7 = tk.Entry(self, textvariable=self.entryYellowVarDelivery, font=helv9, width=inputWidth)

        # Delivery-Button
        self.buttonDeliver = tk.Button(self, text="Start delivery", relief='raised', font=helv9,
                                       command=lambda: self.background(self.onClickDeliver, ()))

        # set label for giving the Order Input table a title
        labelTable6 = tk.Label(self, text="Order quantity?", font=helv9b)

        # set labels for the Order table
        labelBlue6 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple6 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed6 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow6 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set input fields for ordering
        self.entryBlueVarOrder = tk.IntVar()
        self.entryBlue5Order = tk.Entry(self, textvariable=self.entryBlueVarOrder, font=helv9, width=inputWidth)
        self.entryPurpleVarOrder = tk.IntVar()
        self.entryPurple5Order = tk.Entry(self, textvariable=self.entryPurpleVarOrder, font=helv9, width=inputWidth)
        self.entryRedVarOrder = tk.IntVar()
        self.entryRed5Order = tk.Entry(self, textvariable=self.entryRedVarOrder, font=helv9, width=inputWidth)
        self.entryYellowVarOrder = tk.IntVar()
        self.entryYellow5Order = tk.Entry(self, textvariable=self.entryYellowVarOrder, font=helv9, width=inputWidth)

        # Order-Button
        self.buttonOrder = tk.Button(self, text="Order now", relief='raised', font=helv9,
                                     command=lambda: self.background(self.onClickOrder, ()))

        # set labels for informational/administrative data
        global labelroundCount
        global labelTimer
        labelroundCount = tk.Label(self, text="Round Number: " + str(roundCount), font=helv8)
        labelTimer = tk.Label(self, text="Timer: 0", font=helv8)
        labelcostBL = tk.Label(self, text="Cost Backlog: " + str(costBL), font=helv8)
        labelcostInWH = tk.Label(self, text="Cost Inbound-WH: " + str(costInWH), font=helv8)
        labelcostOutWH = tk.Label(self, text="Cost Outbound-WH: " + str(costOutWH), font=helv8)
        self.labelBudgetLeft = tk.Label(self, text="Remaining Budget: " + str(budgetLeft), font=helv8)

        # set table for productiontime overview per product
        product_productiontable = tk.Label(self, text="Production Times", font=helv8b)
        blue_productiontable = tk.Label(self, text="Blue: " + str(self.ptBlue), font=helv8)
        purple_productiontable = tk.Label(self, text="Purple: " + str(self.ptPurple), font=helv8)
        red_productiontable = tk.Label(self, text="Red: " + str(self.ptRed), font=helv8)
        yellow_productiontable = tk.Label(self, text="Yellow: " + str(self.ptYellow), font=helv8)

        # set spacing columns / Rows
        spacingcolumn0 = tk.Label(self, text="              ", font=helv8)
        spacingcolumn = tk.Label(self, text="              ", font=helv8)
        spacingcolumn2 = tk.Label(self, text="              ", font=helv8)
        spacingrow1 = tk.Label(self, text=""

                                          "", font=helv8)
        spacingrow2 = tk.Label(self, text=""

                                          "", font=helv8)

        # Place Page Title
        labelPage.grid(column="1", row="1", sticky="W")

        # Place Team Number
        labelTeam.grid(column="1", row="3", sticky="W")

        # Content Table 1 (Warehouse RM)
        labelTable1.grid(column="1", row="5", sticky="W")

        self.labelBlue1.grid(column='1', row='6', sticky="W")
        self.labelPurple1.grid(column='1', row='7', sticky="W")
        self.labelRed1.grid(column='1', row='8', sticky="W")
        self.labelYellow1.grid(column='1', row='9', sticky="W")

        # Content Table 2 (Open Deliveres)
        labelTable2.grid(column="1", row="14", sticky="W")

        labelBlue2.grid(column='1', row='15', sticky="W")
        labelPurple2.grid(column='1', row='16', sticky="W")
        labelRed2.grid(column='1', row='17', sticky="W")
        labelYellow2.grid(column='1', row='18', sticky="W")

        # spacing column0
        spacingcolumn0.grid(column='2', row='1')

        # Content Table 3 (Warehouse)
        labelTable3.grid(column="4", row="5", sticky="W")

        self.labelBlue3.grid(column='4', row='6', sticky="W")
        self.labelPurple3.grid(column='4', row='7', sticky="W")
        self.labelRed3.grid(column='4', row='8', sticky="W")
        self.labelYellow3.grid(column='4', row='9', sticky="W")

        # Content Table 4 (Backlog)
        labelTable4.grid(column="4", row="14", sticky="W")

        labelBlue4.grid(column='4', row='15', sticky="W")
        labelPurple4.grid(column='4', row='16', sticky="W")
        labelRed4.grid(column='4', row='17', sticky="W")
        labelYellow4.grid(column='4', row='18', sticky="W")

        # spacing column
        spacingcolumn.grid(column='6', row='15')

        # Content Table 5 (Production)
        labelTable5.grid(column="7", row="5", sticky="W")

        labelBlue5.grid(column='7', row='6', sticky="W")
        labelPurple5.grid(column='7', row='7', sticky="W")
        labelRed5.grid(column='7', row='8', sticky="W")
        labelYellow5.grid(column='7', row='9', sticky="W")

        self.entryBlue5.grid(column="8", row="6")
        self.entryPurple5.grid(column="8", row="7")
        self.entryRed5.grid(column="8", row="8")
        self.entryYellow5.grid(column="8", row="9")

        self.buttonProduce.grid(column="8", row="10", sticky='W')

        # spacing row
        spacingrow1.grid(column="1", row="12")

        # Content Table 6 (Order)
        labelTable6.grid(column="7", row="14", sticky="W")

        labelBlue6.grid(column='7', row='15', sticky="W")
        labelPurple6.grid(column='7', row='16', sticky="W")
        labelRed6.grid(column='7', row='17', sticky="W")
        labelYellow6.grid(column='7', row='18', sticky="W")

        self.entryBlue5Order.grid(column="8", row="15")
        self.entryPurple5Order.grid(column="8", row="16")
        self.entryRed5Order.grid(column="8", row="17")
        self.entryYellow5Order.grid(column="8", row="18")

        self.buttonOrder.grid(column="8", row="20", sticky='W')

        # Content Table 7 (Delivery)
        labelTable7.grid(column="7", row="22", sticky="W")

        labelBlue7.grid(column='7', row='23', sticky="W")
        labelPurple7.grid(column='7', row='24', sticky="W")
        labelRed7.grid(column='7', row='25', sticky="W")
        labelYellow7.grid(column='7', row='26', sticky="W")

        self.entryBlue7.grid(column="8", row="23")
        self.entryPurple7.grid(column="8", row="24")
        self.entryRed7.grid(column="8", row="25")
        self.entryYellow7.grid(column="8", row="26")

        self.buttonDeliver.grid(column="8", row="27", sticky='W')

        # spacing row2
        spacingrow2.grid(column="1", row="21")

        # spacing column2
        spacingcolumn2.grid(column='9', row='15')

        # informational/administrative data
        labelroundCount.grid(column='10', row='5', sticky="W")
        labelTimer.grid(column='10', row='6', sticky="W")
        labelcostInWH.grid(column='10', row='7', sticky="W")
        labelcostOutWH.grid(column='10', row='8', sticky="W")
        labelcostBL.grid(column='10', row='9', sticky="W")
        self.labelBudgetLeft.grid(column='10', row='10', sticky="W")

        # production time label
        product_productiontable.grid(column="10", row="14", sticky="W")
        blue_productiontable.grid(column="10", row="15", sticky="W")
        purple_productiontable.grid(column="10", row="16", sticky="W")
        red_productiontable.grid(column="10", row="17", sticky="W")
        yellow_productiontable.grid(column="10", row="18", sticky="W")

        # Done Button
        self.buttonDone.grid(column="10", row="27", sticky='W')
        db_clients.writeRoundStartTimestamp(roundCount)   
    
    # is the end of round for this team -> this should only happen when order and commission is done
    def onClickDone(self):
        self.master.switch_frame(WaitForEndOfRoundPage)

    def onClickProduce(self):
        # get team and production input values
        team = int(app.getTeam())
        blueProduce = self.entryBlueVarProduction.get()
        purpleProduce = self.entryPurpleVarProduction.get()
        redProduce = self.entryRedVarProduction.get()
        yellowProduce = self.entryYellowVarProduction.get()

        # check if the raw invatrory will suffice
        rawFlag = True
        rawFlagB = True
        rawFlagP = True
        rawFlagR = True
        rawFlagY = True

        if(self.inventoryRawBlue < blueProduce):
            rawFlagB = False
        if(self.inventoryRawPurple < purpleProduce):
            rawFlagP = False
        if(self.inventoryRawRed < redProduce):
            rawFlagR = False
        if(self.inventoryRawYellow < yellowProduce):
            rawFlagY = False
        arr = [rawFlagB,rawFlagP,rawFlagR,rawFlagY]

        c = 0

        for i in arr:
            if i == False:
                c=c+1
        if(c>0):
            rawFlag = False

        
        # calculate production time of each product group
        totalProductionTimeBlue = int(blueProduce) * int(self.ptBlue)
        totalProductionTimePurple = int(purpleProduce) * int(self.ptPurple)
        totalProductionTimeRed = int(redProduce) * int(self.ptRed)
        totalProductionTimeYellow = int(yellowProduce) * int(self.ptYellow)

        # calculate total production time
        totalProductionTime = totalProductionTimeBlue +  totalProductionTimePurple + totalProductionTimeRed +  totalProductionTimeYellow
        pLim = self.produceLimit + totalProductionTime
        # check if enough time for production is left and if it is, write it into the database and update lables. Otherwise display errormessage
        timer = int((labelTimer.cget("text"))[7:])

        if pLim >= timer or rawFlag == False:
            text = ""
            timelocal = timer-self.produceLimit
            if(timelocal < 0):
                timelocal =0
            if (rawFlag == False):
                text = "Insufficient raw materials !"
            else: 
                text = "You do not have enough time left in this round to produce this amount of products!Production  Time left : " + str(timelocal)

            popup = tk.Tk()
            popup.wm_title("Not enough time")
            label = tk.Label(popup, text=text, font=helv22)
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Okay", command=popup.destroy)
            B1.pack()
            popup.mainloop()
        else:
            # write production into database
            db_clients.writeProduction(team, "blue", roundCount, blueProduce, totalProductionTimeBlue)
            db_clients.writeProduction(team, "purple", roundCount, purpleProduce, totalProductionTimePurple)
            db_clients.writeProduction(team, "red", roundCount, redProduce, totalProductionTimeRed)
            db_clients.writeProduction(team, "yellow", roundCount, yellowProduce, totalProductionTimeYellow)
            
            # set input value to 0
            self.entryBlueVarProduction.set("0")
            self.entryPurpleVarProduction.set("0")
            self.entryRedVarProduction.set("0")
            self.entryYellowVarProduction.set("0")
            
            # reduce inbound  and update inbound label

            self.inventoryRawBlue -= int(blueProduce)
            self.inventoryRawPurple -= int(purpleProduce)
            self.inventoryRawRed -= int(redProduce)
            self.inventoryRawYellow -= int(yellowProduce)

            self.labelBlue1.config(text = "Blue product: " + str(self.inventoryRawBlue))
            self.labelPurple1.config(text = "Purple product: " + str(self.inventoryRawPurple))
            self.labelRed1.config(text = "Red product: " + str(self.inventoryRawRed))
            self.labelYellow1.config(text = "Yellow product: " + str(self.inventoryRawYellow))

            # add produced goods to outbound and update label
            self.fgBlue += blueProduce
            self.fgPurple += purpleProduce
            self.fgRed += redProduce
            self.fgYellow += yellowProduce

            self.labelBlue3.config(text = "Blue product: " + str(self.fgBlue))
            self.labelPurple3.config(text = "Purple product: " + str(self.fgPurple))
            self.labelRed3.config(text = "Red product: " + str(self.fgRed))
            self.labelYellow3.config(text = "Yellow product: " + str(self.fgYellow))

            self.produceLimit = self.produceLimit + totalProductionTime


    def onClickOrder(self):
        # write order in database
        team = int(app.getTeam())
        blueOrder = self.entryBlueVarOrder.get()
        purpleOrder = self.entryPurpleVarOrder.get()
        redOrder = self. entryRedVarOrder.get()
        yellowOrder = self.entryYellowVarOrder.get()

        # team 1 has to be treated differently because it has no team to order from
        if team == 1:
            db_clients.writeOrder(team, team, 'blue', roundCount, blueOrder)
            db_clients.writeOrder(team, team, 'purple', roundCount, purpleOrder)
            db_clients.writeOrder(team, team, 'red', roundCount, redOrder)
            db_clients.writeOrder(team, team, 'yellow', roundCount, yellowOrder)
        else:
            db_clients.writeOrder(team - 1, team, 'blue', roundCount, blueOrder)
            db_clients.writeOrder(team - 1, team, 'purple', roundCount, purpleOrder)
            db_clients.writeOrder(team - 1, team, 'red', roundCount, redOrder)
            db_clients.writeOrder(team - 1, team, 'yellow', roundCount, yellowOrder)

        #reset variables
        self.entryBlueVarOrder.set("0")
        self.entryPurpleVarOrder.set("0")
        self.entryRedVarOrder.set("0")
        self.entryYellowVarOrder.set("0")

    def onClickDeliver(self):
        team = int(app.getTeam())
        # read values from inputfields and write them into variables
        blueDeliver = int(self.entryBlueVarDelivery.get())
        purpleDeliver = int(self.entryPurpleVarDelivery.get())
        redDeliver = int(self.entryRedVarDelivery.get())
        yellowDeliver = int(self.entryYellowVarDelivery.get())

        #check if delivery is possible
        if(blueDeliver > self.fgBlue or purpleDeliver > self.fgPurple or redDeliver > self.fgRed or yellowDeliver > self.fgYellow):
            popup = tk.Tk()
            popup.wm_title("Not enough time")
            label = tk.Label(popup, text="Not enough raw material!", font=helv22)
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Okay", command=popup.destroy)
            B1.pack()
            popup.mainloop()
        else:
            # call function for writing on nfc chip
            # call function write in write.py => Writing the variables on the NFC
            write.write(blueDeliver,purpleDeliver,redDeliver,yellowDeliver)
       
            # reduce stock outbound warehouse
            self.fgBlue -= blueDeliver
            self.fgPurple -= purpleDeliver
            self.fgRed -= redDeliver
            self.fgYellow -= yellowDeliver

            self.labelBlue3.config(text = "Blue product: " + str(self.fgBlue))
            self.labelPurple3.config(text = "Purple product: " + str(self.fgPurple ))
            self.labelRed3.config(text = "Red product: " + str(self.fgRed))
            self.labelYellow3.config(text = "Yellow product: " + str(self.fgYellow))

            # write delivery in database
            # team 4 has to be treated differently because there is no other team to deliver to
            if team == 4:
                db_clients.writeOutbound(team, team, 'blue', roundCount, blueDeliver)
                db_clients.writeOutbound(team, team, 'purple', roundCount, purpleDeliver)
                db_clients.writeOutbound(team, team, 'red', roundCount, redDeliver)
                db_clients.writeOutbound(team, team, 'yellow', roundCount, yellowDeliver)
            else:
                db_clients.writeOutbound(team, team + 1, 'blue', roundCount, blueDeliver)
                db_clients.writeOutbound(team, team + 1, 'purple', roundCount, purpleDeliver)
                db_clients.writeOutbound(team, team + 1, 'red', roundCount, redDeliver)
                db_clients.writeOutbound(team, team + 1, 'yellow', roundCount, yellowDeliver)
            #set input values to zero
            self.entryBlueVarDelivery.set("0")
            self.entryPurpleVarDelivery.set("0")
            self.entryRedVarDelivery.set("0")
            self.entryYellowVarDelivery.set("0")

    # start thread
    def background(self, func, args):
        th = threading.Thread(target=func, args=args)
        th.start()

# site to wait for start of the admin raspberry
class WaitForStartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label1 = tk.Label(self, text = "Please wait", font = helv13)
        label2 = tk.Label(self, text = "until the admin has started the game", font = helv13)
        label1.pack()
        label2.pack()

# site to wait for the end of the round
class WaitForEndOfRoundPage(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            labelTop = tk.Label(self, text = "Please wait until the end of the round", font=helv18)
            labelBottom = tk.Label(self, text = ":)", font = helv13)
            global labelTimer
            labelTimer = tk.Label(self, text="Timer: ", font=helv13)
           
            labelTop.grid(column = 1, row = 0)
            labelBottom.grid(column = 1, row = 1)
            labelTimer.grid(column = 1, row = 2)

# End of Round Page to summarise
class EndOfRoundPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self , master)
        blue = 0
        purple = 0
        red = 0
        yellow = 0
        self.labelTop = tk.Label(self, text = "End of Round", font = helv13)
        self.labelBottom = tk.Label(self, text = "You got blue: " + str(blue) + " purple: " + str(purple) + " red: "+ str(red) + " yellow: " + str(yellow), font = helv13)

        self.labelTop.grid(column = 1, row = 0)
        self.labelBottom.grid(column = 1, row = 1)
        
        self.buttonInbound = tk.Button(self, text="Get Delivery!", relief='raised', font=helv9,
                                       command=lambda: self.onClickInbound())
        self.buttonInbound.grid(column=1, row=2)

    # function to read the NFC and write the content of the NFC into the database
    def onClickInbound(self):
        team = int(app.getTeam())
        blue = 0
        purple = 0
        red = 0
        yellow = 0

        if team == 1:
            outboundValues = db_clients.readLastOutbound(team, roundCount)
            for outbound in outboundValues:
                if outbound[2] == "blue":
                    blue += outbound[3]
                if outbound[2] == "purple":
                    purple += outbound[3]
                if outbound[2] == "red":
                    red += outbound[3]
                if outbound[2] == "yellow":
                    yellow += outbound[3]
         
            db_clients.writeInbound(team, team, 'blue', roundCount, blue)
            db_clients.writeInbound(team, team, 'purple', roundCount, purple)
            db_clients.writeInbound(team, team, 'red', roundCount, red)
            db_clients.writeInbound(team, team, 'yellow', roundCount, yellow)
        else:
            blue, purple, red, yellow = read.read()
            
            db_clients.writeInbound(team, team - 1, 'blue', roundCount, blue)
            db_clients.writeInbound(team, team - 1, 'purple', roundCount, purple)
            db_clients.writeInbound(team, team - 1, 'red', roundCount, red)
            db_clients.writeInbound(team, team - 1, 'yellow', roundCount, yellow)

        self.labelBottom.config(text="You got blue: " + str(blue) + " purple: " + str(purple) + " red: "+ str(red) + " yellow: " + str(yellow))

        
# Logic to communicate with Client Raspberrys
class listenerThread(threading.Thread):
    def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
    def run(self):
        global isRunning
        global gamePage
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(("", 37020))
        while True:
            data, addr = client.recvfrom(1024)
            print(data)
            print(gamePage.isSet())
            if data == "START":
                isRunning = True
                BeerGame.switch_frame(app, GamePage)        
            if "RUNDE" in data: 
                global hasPlayed
                global roundCount
                roundCount = int(data[5:7])
                hasPlayed = True
                BeerGame.nextRound(app)
            if "ENDOFROUND" in data:
                gamePage.clear()
                BeerGame.switch_frame(app, EndOfRoundPage)
            if gamePage.isSet() == True:
                labelTimer.config(text="Timer: " + data)

# start main loop
if __name__ == "__main__":
    app = BeerGame()
    listenerThread = listenerThread(1, "Listener Thread", 1)
    listenerThread.daemon = True
    listenerThread.start()
    app.mainloop()

    