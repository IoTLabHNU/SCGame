import tkinter as tk
from tkinter import font
#from tkinter import IntVar
import atexit
import socket
import threading
#import time
class BeerGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.minsize(width=640, height=480)
        self.resizable(width=False, height=False)
        global team_sheet
        team_sheet = ''
        global master_sheet
        master_sheet = ''
        global client
        client = None
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
        inputWidth=7
        global labelTimer
        labelTimer = tk.Label()
        global team
        team = 0
        global roundCount
        roundCount = 1
        global isRunning
        isRunning = False
        global timeOrdered
        timeOrdered = ""
        global gamePage
        #global client
        scope = ['']
        #creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = ''
        gamePage = threading.Event()
        self.switch_frame(GamePage) #changed frame to GamePage

    def nextRound(self):
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

# actual game page during each round -> change connection to database, implement production (commission) with NFC tag, adjust interface
class GamePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        gamePage.set()

        # get data from the database: balance (guthaben), products in warehouse
        #balance = '0'

        #set Warehouse RM inventory variables
        inventoryRawBlue = '1'
        inventoryRawPurple = '2'
        inventoryRawRed = '3'
        inventoryRawYellow = '4'

        # set Open Deliveries values variables
        openBlue = '5'
        openPurple = '6'
        openRed = '7'
        openYellow = '8'

        # set Warehouse FG inventory variables
        fgBlue = '9'
        fgPurple = '10'
        fgRed = '11'
        fgYellow = '12'

        # set Backlog variables
        blBlue = '13'
        blPurple = '14'
        blRed = '15'
        blYellow = '16'

        # set administrative/information variables
        print(roundCount)
        roundCount = '17'
        timer='18'
        costInWH= '21'
        costOutWH='20'
        costBL='20'
        costTotal='21'

        # set production time p product
        ptBlue = '22'
        ptPurple = '23'
        ptRed = '24'
        ptYellow = '25'


        # set a label with the title of the page
        labelPage =tk.Label(self, text="Game", font=helv14)

        # Done-Button
        self.buttonDone = tk.Button(self, text="Done", relief='raised', font=helv9, command=lambda: self.background(self.OnButtonClick, ()))

        # set a label with the team (variable of class BeerGame)
        labelTeam = tk.Label(self, text="Team: " + str(team), font=helv12)

        #set label for giving the RM Warehouse table a title
        labelTable1 = tk.Label(self, text="Warehouse RM", font=helv9b)

        
        #set labels for the RM Warehouse
        labelBlue1 = tk.Label(self, text="Blue product: " + str(inventoryRawBlue), font=helv9)
        labelPurple1 = tk.Label(self, text="Purple product: "+ str(inventoryRawPurple), font=helv9)
        labelRed1 = tk.Label(self, text="Red product: " + str(inventoryRawRed), font=helv9)
        labelYellow1 = tk.Label(self, text="Yellow product: " + str(inventoryRawYellow), font=helv9)

        #labelInventoryBlue1 = tk.Label(self, str(inventoryBlue1), font=helv22)

        # set label for giving the Open Deliveries table a title
        labelTable2 = tk.Label(self, text="Open Deliveries", font=helv9b)

        # set labels for the Open Deliveries Table
        labelBlue2 = tk.Label(self, text="Blue product: " + str(openBlue), font=helv9)
        labelPurple2 = tk.Label(self, text="Purple product: " + str(openPurple), font=helv9)
        labelRed2 = tk.Label(self, text="Red product: " + str(openRed), font=helv9)
        labelYellow2 = tk.Label(self, text="Yellow product: " + str(openYellow), font=helv9)

        # set label for giving the FG Warehouse table a title
        labelTable3 = tk.Label(self, text="Warehouse FG", font=helv9b)

        # set labels for the FG Warehouse
        labelBlue3 = tk.Label(self, text="Blue product: " + str(fgBlue), font=helv9)
        labelPurple3 = tk.Label(self, text="Purple product: " + str(fgPurple), font=helv9)
        labelRed3 = tk.Label(self, text="Red product: " + str(fgRed), font=helv9)
        labelYellow3 = tk.Label(self, text="Yellow product: " + str(fgYellow), font=helv9)

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
        self.buttonProduce = tk.Button(self, text="Start production", relief='raised', font=helv9, command=lambda: self.background(self.OnButtonClick, ()))

        # set input fields for production
        self.entryBlueVar = tk.IntVar()
        self.entryBlue5 = tk.Entry(self, textvariable=self.entryBlueVar, font= helv9, width=inputWidth)
        self.entryPurpleVar = tk.IntVar()
        self.entryPurple5 = tk.Entry(self, textvariable=self.entryPurpleVar, font=helv9, width=inputWidth)
        self.entryRedVar = tk.IntVar()
        self.entryRed5 = tk.Entry(self, textvariable=self.entryRedVar, font=helv9, width=inputWidth)
        self.entryYellowVar = tk.IntVar()
        self.entryYellow5 = tk.Entry(self, textvariable=self.entryYellowVar, font=helv9, width=inputWidth)

        # set label for giving the Delivery Input table a title
        labelTable7 = tk.Label(self, text="Delivery quantity?", font=helv9b)

        # set labels for the Delivery
        labelBlue7 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple7 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed7 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow7 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set input fields for delivery
        self.entryBlueVar = tk.IntVar()
        self.entryBlue7 = tk.Entry(self, textvariable=self.entryBlueVar, font=helv9, width=inputWidth)
        self.entryPurpleVar = tk.IntVar()
        self.entryPurple7 = tk.Entry(self, textvariable=self.entryPurpleVar, font=helv9, width=inputWidth)
        self.entryRedVar = tk.IntVar()
        self.entryRed7 = tk.Entry(self, textvariable=self.entryRedVar, font=helv9, width=inputWidth)
        self.entryYellowVar = tk.IntVar()
        self.entryYellow7 = tk.Entry(self, textvariable=self.entryYellowVar, font=helv9, width=inputWidth)

        # Delivery-Button
        self.buttonDeliver = tk.Button(self, text="Start delivery", relief='raised', font=helv9, command=lambda: self.background(self.OnButtonClick, ()))

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

        #Order-Button
        self.buttonOrder = tk.Button(self, text="Order now", relief='raised', font=helv9, command=lambda: self.background(self.OnButtonClick, ()))

        # set labels for informational/administrative data
        global labelroundCount
        labelroundCount = tk.Label(self, text="Round Number: " + str(roundCount), font=helv8)
        labelTimer = tk.Label(self, text="Timer: " + str(timer), font=helv8)
        labelcostBL = tk.Label(self, text="Cost Backlog: " + str(costBL), font=helv8)
        labelcostInWH = tk.Label(self, text="Cost Inbound-WH: " + str(costInWH), font=helv8)
        labelcostOutWH = tk.Label(self, text="Cost Outbound-WH: " + str(costOutWH), font=helv8)
        labelcostTotal = tk.Label(self, text="Total Costs: " + str(costTotal), font=helv8)

        #set table for productiontime overview per product
        product_productiontable = tk.Label(self, text="Production Times", font=helv8b)
        blue_productiontable = tk.Label(self, text="Blue: " + str(ptBlue), font=helv8)
        purple_productiontable = tk.Label(self, text="Purple: " + str(ptPurple), font=helv8)
        red_productiontable = tk.Label(self, text="Red: " + str(ptRed), font=helv8)
        yellow_productiontable = tk.Label(self, text="Yellow: " + str(ptYellow), font=helv8)

        #set spacing columns / Rows
        spacingcolumn0 = tk.Label(self, text="              ", font=helv8)
        spacingcolumn = tk.Label(self, text="              ", font=helv8)
        spacingcolumn2 = tk.Label(self, text="              ", font=helv8)
        spacingrow1=tk.Label(self, text=""
                                        
                                        "", font=helv8)
        spacingrow2 = tk.Label(self, text=""

                                          "", font=helv8)


        #Place Page Title
        labelPage.grid(column="1", row="1", sticky="W")



        # Place Team Number
        labelTeam.grid(column = "1", row = "3", sticky="W")

        # Content Table 1 (Warehouse RM)
        labelTable1.grid(column="1", row="5", sticky="W")

        labelBlue1.grid(column='1', row='6', sticky="W")
        labelPurple1.grid(column='1', row='7', sticky="W")
        labelRed1.grid(column='1', row='8', sticky="W")
        labelYellow1.grid(column='1', row='9', sticky="W")

        #self.labelInventoryBlue1.grid(column='2', row='6', sticky='E')

        # Content Table 2 (Open Deliveres)
        labelTable2.grid(column="1", row="14", sticky="W")

        labelBlue2.grid(column='1', row='15', sticky="W")
        labelPurple2.grid(column='1', row='16', sticky="W")
        labelRed2.grid(column='1', row='17', sticky="W")
        labelYellow2.grid(column='1', row='18', sticky="W")

        # spacing column0
        spacingcolumn0.grid(column='2', row='1')

        # Content Table 3 (Warehouse FG)
        labelTable3.grid(column="4", row="5", sticky="W")

        labelBlue3.grid(column='4', row='6', sticky="W")
        labelPurple3.grid(column='4', row='7', sticky="W")
        labelRed3.grid(column='4', row='8', sticky="W")
        labelYellow3.grid(column='4', row='9', sticky="W")

        # Content Table 4 (Backlog)
        labelTable4.grid(column="4", row="14", sticky="W")

        labelBlue4.grid(column='4', row='15', sticky="W")
        labelPurple4.grid(column='4', row='16', sticky="W")
        labelRed4.grid(column='4', row='17', sticky="W")
        labelYellow4.grid(column='4', row='18', sticky="W")

        #spacing column
        spacingcolumn.grid(column='6', row='15')

        # Content Table 5 (Production)
        labelTable5.grid(column="7", row="5", sticky="W")

        labelBlue5.grid(column='7', row='6', sticky="W")
        labelPurple5.grid(column='7', row='7', sticky="W")
        labelRed5.grid(column='7', row='8', sticky="W")
        labelYellow5.grid(column='7', row='9', sticky="W")

        self.entryBlue5.grid(column = "8", row ="6")
        self.entryPurple5.grid(column="8", row="7")
        self.entryRed5.grid(column="8", row="8")
        self.entryYellow5.grid(column="8", row="9")

        self.buttonProduce.grid(column="8", row="10", sticky='W')

        #spacing row
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

        self.buttonOrder.grid(column = "8", row = "20", sticky='W')

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

        #informational/administrative data
        labelroundCount.grid(column='10', row='5', sticky="W")
        labelTimer.grid(column='10', row='6', sticky="W")
        labelcostInWH.grid(column='10', row='7', sticky="W")
        labelcostOutWH.grid(column='10', row='8', sticky="W")
        labelcostBL.grid(column='10', row='9', sticky="W")
        labelcostTotal.grid(column='10', row='10', sticky="W")

        #production time label
        product_productiontable.grid(column="10", row="14", sticky="W")
        #time_productiontable.grid(column="11", row="14", sticky="W")
        blue_productiontable.grid(column="10", row="15", sticky="W")
        purple_productiontable.grid(column="10", row="16", sticky="W")
        red_productiontable.grid(column="10", row="17", sticky="W")
        yellow_productiontable.grid(column="10", row="18", sticky="W")

        #Done Button
        self.buttonDone.grid(column="10", row="27", sticky='W')
    
    # is the end of round for this team -> this should only happen when order and commission is done
    def OnButtonClick(self):
        pass
        # self.buttonOrder.config(state="disabled")
        # self.master.switch_frame(WaitForEndOfRoundPage)
        # orderedValues = [self.entryBlueVar.get(), self.entryPurpleVar.get(), self.entryRedVar.get(), self.entryYellowVar.get()]
        # print orderedValues
        # write_orders.__init__(team, roundCount, orderedValues)

    def background(self, func, args):
        th = threading.Thread(target=func, args=args)
        th.start()

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
                labelTimer.config(text="Rundenzeit: " + data)


if __name__ == "__main__":
    app = BeerGame()
    listenerThread = listenerThread(1, "Listener Thread", 1)
    listenerThread.daemon = True
    listenerThread.start()
    app.mainloop()