import socket
import time
import Tkinter as tk
import tkFont as font
import threading
#import gspread
from oauth2client.service_account import ServiceAccountCredentials
import operator
import db_clients

class Master(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # define lables
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
        global server
        global isRunning
        global rundenZeit
        runbdenZeit = 130
        isRunning = False
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        server.settimeout(0.2)
        server.bind(("", 44444))

        global startButton

        #reset all inital values when starting the admin page
        db_clients.resetValues()

        # set a label with the title of the page
        labelPage = tk.Label(self, text="Admin - Config", font=helv14)

        # set label for giving the Team 1 table a title
        labelTable1 = tk.Label(self, text="Team 1 Prod.Time", font=helv9b)

        # set labels for Team 1
        labelBlue1 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple1 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed1 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow1 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving the Initial Inventory Team 1  table a title
        labelTable2 = tk.Label(self, text="Initial Inventory Team 1", font=helv9b)

        # set labels for Initial Inventory Team 1 Table
        labelBlue2 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple2 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed2 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow2 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving Team 2 table a title
        labelTable3 = tk.Label(self, text="Team 2 Prod.Time", font=helv9b)

        # set labels for Team 3
        labelBlue3 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple3 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed3 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow3 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving the Initial Inventory Team 2 table a title
        labelTable4 = tk.Label(self, text="Initial Inventory Team 2", font=helv9b)

        # set labels for the Initial Inventory Team 2
        labelBlue4 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple4 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed4 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow4 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving Team 3 Input table a title
        labelTable5 = tk.Label(self, text="Team 3 Prod.Time", font=helv9b)

        # set labels for Team 3
        labelBlue5 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple5 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed5 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow5 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving Initial Inventory Team 3 table a title
        labelTable6 = tk.Label(self, text="Initial Inventory Team 3", font=helv9b)

        # set labels for the Initial Inventory Team 3
        labelBlue6 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple6 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed6 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow6 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving Team 4 Input table a title
        labelTable7 = tk.Label(self, text="Team 4 Prod.Time", font=helv9b)

        # set labels for Team 4
        labelBlue7 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple7 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed7 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow7 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set label for giving Initial Inventory Team 4 Input table a title
        labelTable8 = tk.Label(self, text="Initial Inventory Team 4", font=helv9b)

        # set labels for the Initial Inventory Team 4
        labelBlue8 = tk.Label(self, text="Blue product: ", font=helv9)
        labelPurple8 = tk.Label(self, text="Purple product: ", font=helv9)
        labelRed8 = tk.Label(self, text="Red product: ", font=helv9)
        labelYellow8 = tk.Label(self, text="Yellow product: ", font=helv9)

        # set labels for informational/administrative data
        labelgeneral = tk.Label(self, text="General Information", font=helv9b)

        labelduration = tk.Label(self, text="Duration: ", font=helv9)
        labelroundanzahl = tk.Label(self, text="Nr of rounds: ", font=helv9)
        labelTimer = tk.Label(self, text="Timer: ", font=helv9)
        labelcostBL = tk.Label(self, text="Cost Backlog: ", font=helv9)
        labelcostinboundWH = tk.Label(self, text="Cost Inbound - Warehouse: ", font=helv9)
        labelcostoutboundWH = tk.Label(self, text="Cost Outbound - Warehouse: ", font=helv9)
        labelbudget = tk.Label(self, text="Budget: ", font=helv9)

        # Place Page Title
        labelPage.grid(column="0", row="1", sticky="W")

        # Content Table 1 (Team 1 top)
        labelTable1.grid(column="0", row="5", sticky="W")

        labelBlue1.grid(column='0', row='6', sticky="W")
        labelPurple1.grid(column='0', row='7', sticky="W")
        labelRed1.grid(column='0', row='8', sticky="W")
        labelYellow1.grid(column='0', row='9', sticky="W")

        # Content Table 2 (Team 1 down - Inventory)
        labelTable2.grid(column="0", row="14", sticky="W")

        labelBlue2.grid(column='0', row='15', sticky="W")
        labelPurple2.grid(column='0', row='16', sticky="W")
        labelRed2.grid(column='0', row='17', sticky="W")
        labelYellow2.grid(column='0', row='18', sticky="W")

        # Content Table 3 (Team 2 top)
        labelTable3.grid(column="4", row="5", sticky="W")

        labelBlue3.grid(column='4', row='6', sticky="W")
        labelPurple3.grid(column='4', row='7', sticky="W")
        labelRed3.grid(column='4', row='8', sticky="W")
        labelYellow3.grid(column='4', row='9', sticky="W")

        # Content Table 4 (Team 2 down -  Inventory)
        labelTable4.grid(column="4", row="14", sticky="W")

        labelBlue4.grid(column='4', row='15', sticky="W")
        labelPurple4.grid(column='4', row='16', sticky="W")
        labelRed4.grid(column='4', row='17', sticky="W")
        labelYellow4.grid(column='4', row='18', sticky="W")

        # Content Table 5 (Team 3 top)
        labelTable5.grid(column="7", row="5", sticky="W")

        labelBlue5.grid(column='7', row='6', sticky="W")
        labelPurple5.grid(column='7', row='7', sticky="W")
        labelRed5.grid(column='7', row='8', sticky="W")
        labelYellow5.grid(column='7', row='9', sticky="W")

        # Content Table 6 (Team 3 down - Inventory)
        labelTable6.grid(column="7", row="14", sticky="W")

        labelBlue6.grid(column='7', row='15', sticky="W")
        labelPurple6.grid(column='7', row='16', sticky="W")
        labelRed6.grid(column='7', row='17', sticky="W")
        labelYellow6.grid(column='7', row='18', sticky="W")

        # Content Table 7 (Team 4 top)
        labelTable7.grid(column="10", row="5", sticky="W")

        labelBlue7.grid(column='10', row='6', sticky="W")
        labelPurple7.grid(column='10', row='7', sticky="W")
        labelRed7.grid(column='10', row='8', sticky="W")
        labelYellow7.grid(column='10', row='9', sticky="W")

        # Content Table 8 (Team 4 down - Inventory)
        labelTable8.grid(column="10", row="14", sticky="W")

        labelBlue8.grid(column='10', row='15', sticky="W")
        labelPurple8.grid(column='10', row='16', sticky="W")
        labelRed8.grid(column='10', row='17', sticky="W")
        labelYellow8.grid(column='10', row='18', sticky="W")

        # informational/administrative data
        labelgeneral.grid(column='13', row='5', sticky="W")

        labelduration.grid(column='13', row='6', sticky="W")
        labelroundanzahl.grid(column='13', row='7', sticky="W")
        labelTimer.grid(column='13', row='8', sticky="W")
        labelcostinboundWH.grid(column='13', row='9', sticky="W")
        labelcostoutboundWH.grid(column='13', row='10', sticky="W")
        labelcostBL.grid(column='13', row='11', sticky="W")
        labelbudget.grid(column='13', row='12', sticky='W')

        # input fields of Table 1 (Team 1 top) PRODUCTION TIME

        self.entry_blue1 = tk.StringVar()
        self.entry_blue1.set("5")
        self.blue1 = tk.Entry(self, textvariable=self.entry_blue1, font=helv12, width=inputWidth)
        self.blue1.grid(column=1, row=6)

        self.entry_purple1 = tk.StringVar()
        self.entry_purple1.set("10")
        self.purple1 = tk.Entry(self, textvariable=self.entry_purple1, font=helv12, width=inputWidth)
        self.purple1.grid(column=1, row=7)

        self.entry_red1 = tk.StringVar()
        self.entry_red1.set("15")
        self.red1 = tk.Entry(self, textvariable=self.entry_red1, font=helv12, width=inputWidth)
        self.red1.grid(column=1, row=8)

        self.entry_yellow1 = tk.StringVar()
        self.entry_yellow1.set("20")
        self.yellow1 = tk.Entry(self, textvariable=self.entry_yellow1, font=helv12, width=inputWidth)
        self.yellow1.grid(column=1, row=9)

        # input fields of Table 2 (Team 1 down - Inventory)

        self.entry_blue2 = tk.StringVar()
        self.entry_blue2.set("10")
        self.blue2 = tk.Entry(self, textvariable=self.entry_blue2, font=helv12, width=inputWidth)
        self.blue2.grid(column=1, row=15)

        self.entry_purple2 = tk.StringVar()
        self.entry_purple2.set("10")
        self.purple2 = tk.Entry(self, textvariable=self.entry_purple2, font=helv12, width=inputWidth)
        self.purple2.grid(column=1, row=16)

        self.entry_red2 = tk.StringVar()
        self.entry_red2.set("10")
        self.red2 = tk.Entry(self, textvariable=self.entry_red2, font=helv12, width=inputWidth)
        self.red2.grid(column=1, row=17)

        self.entry_yellow2 = tk.StringVar()
        self.entry_yellow2.set("10")
        self.yellow2 = tk.Entry(self, textvariable=self.entry_yellow2, font=helv12, width=inputWidth)
        self.yellow2.grid(column=1, row=18)

        # input fields of Table 3 (Team 2 top) PRODUCTION TIME

        self.entry_blue3 = tk.StringVar()
        self.entry_blue3.set("10")
        self.blue3 = tk.Entry(self, textvariable=self.entry_blue3, font=helv12, width=inputWidth)
        self.blue3.grid(column=5, row=6)

        self.entry_purple3 = tk.StringVar()
        self.entry_purple3.set("15")
        self.purple3 = tk.Entry(self, textvariable=self.entry_purple3, font=helv12, width=inputWidth)
        self.purple3.grid(column=5, row=7)

        self.entry_red3 = tk.StringVar()
        self.entry_red3.set("20")
        self.red3 = tk.Entry(self, textvariable=self.entry_red3, font=helv12, width=inputWidth)
        self.red3.grid(column=5, row=8)

        self.entry_yellow3 = tk.StringVar()
        self.entry_yellow3.set("5")
        self.yellow3 = tk.Entry(self, textvariable=self.entry_yellow3, font=helv12, width=inputWidth)
        self.yellow3.grid(column=5, row=9)

        # input fields of Table 4 (Team 2 down - Inventoy)

        self.entry_blue4 = tk.StringVar()
        self.entry_blue4.set("10")
        self.blue4 = tk.Entry(self, textvariable=self.entry_blue4, font=helv12, width=inputWidth)
        self.blue4.grid(column=5, row=15)

        self.entry_purple4 = tk.StringVar()
        self.entry_purple4.set("10")
        self.purple4 = tk.Entry(self, textvariable=self.entry_purple4, font=helv12, width=inputWidth)
        self.purple4.grid(column=5, row=16)

        self.entry_red4 = tk.StringVar()
        self.entry_red4.set("10")
        self.red4 = tk.Entry(self, textvariable=self.entry_red4, font=helv12, width=inputWidth)
        self.red4.grid(column=5, row=17)

        self.entry_yellow4 = tk.StringVar()
        self.entry_yellow4.set("10")
        self.yellow4 = tk.Entry(self, textvariable=self.entry_yellow4, font=helv12, width=inputWidth)
        self.yellow4.grid(column=5, row=18)

        # input fields of Table 5

        self.entry_blue5 = tk.StringVar()
        self.entry_blue5.set("15")
        self.blue5 = tk.Entry(self, textvariable=self.entry_blue5, font=helv12, width=inputWidth)
        self.blue5.grid(column=8, row=6)

        self.entry_purple5 = tk.StringVar()
        self.entry_purple5.set("20")
        self.purple5 = tk.Entry(self, textvariable=self.entry_purple5, font=helv12, width=inputWidth)
        self.purple5.grid(column=8, row=7)

        self.entry_red5 = tk.StringVar()
        self.entry_red5.set("5")
        self.red5 = tk.Entry(self, textvariable=self.entry_red5, font=helv12, width=inputWidth)
        self.red5.grid(column=8, row=8)

        self.entry_yellow5 = tk.StringVar()
        self.entry_yellow5.set("10")
        self.yellow5 = tk.Entry(self, textvariable=self.entry_yellow5, font=helv12, width=inputWidth)
        self.yellow5.grid(column=8, row=9)

        # input fields of Table 6 (Team down - Inventory)

        self.entry_blue6 = tk.StringVar()
        self.entry_blue6.set("10")
        self.blue6 = tk.Entry(self, textvariable=self.entry_blue6, font=helv12, width=inputWidth)
        self.blue6.grid(column=8, row=15)

        self.entry_purple6 = tk.StringVar()
        self.entry_purple6.set("10")
        self.purple6 = tk.Entry(self, textvariable=self.entry_purple6, font=helv12, width=inputWidth)
        self.purple6.grid(column=8, row=16)

        self.entry_red6 = tk.StringVar()
        self.entry_red6.set("10")
        self.red6 = tk.Entry(self, textvariable=self.entry_red6, font=helv12, width=inputWidth)
        self.red6.grid(column=8, row=17)

        self.entry_yellow6 = tk.StringVar()
        self.entry_yellow6.set("10")
        self.yellow6 = tk.Entry(self, textvariable=self.entry_yellow6, font=helv12, width=inputWidth)
        self.yellow6.grid(column=8, row=18)

        # input fields Table 7 (Team 4 top) PRODUCTION TIME

        self.entry_blue7 = tk.StringVar()
        self.entry_blue7.set("20")
        self.blue7 = tk.Entry(self, textvariable=self.entry_blue7, font=helv12, width=inputWidth)
        self.blue7.grid(column=11, row=6)

        self.entry_purple7 = tk.StringVar()
        self.entry_purple7.set("5")
        self.purple7 = tk.Entry(self, textvariable=self.entry_purple7, font=helv12, width=inputWidth)
        self.purple7.grid(column=11, row=7)

        self.entry_red7 = tk.StringVar()
        self.entry_red7.set("10")
        self.red7 = tk.Entry(self, textvariable=self.entry_red7, font=helv12, width=inputWidth)
        self.red7.grid(column=11, row=8)

        self.entry_yellow7 = tk.StringVar()
        self.entry_yellow7.set("15")
        self.yellow7 = tk.Entry(self, textvariable=self.entry_yellow7, font=helv12, width=inputWidth)
        self.yellow7.grid(column=11, row=9)

        # input fields Table 8 (Team 4 down - Inventory)

        self.entry_blue8 = tk.StringVar()
        self.entry_blue8.set("10")
        self.blue8 = tk.Entry(self, textvariable=self.entry_blue8, font=helv12, width=inputWidth)
        self.blue8.grid(column=11, row=15)

        self.entry_purple8 = tk.StringVar()
        self.entry_purple8.set("10")
        self.purple8 = tk.Entry(self, textvariable=self.entry_purple8, font=helv12, width=inputWidth)
        self.purple8.grid(column=11, row=16)

        self.entry_red8 = tk.StringVar()
        self.entry_red8.set("10")
        self.red8 = tk.Entry(self, textvariable=self.entry_red8, font=helv12, width=inputWidth)
        self.red8.grid(column=11, row=17)

        self.entry_yellow8 = tk.StringVar()
        self.entry_yellow8.set("10")
        self.yellow8 = tk.Entry(self, textvariable=self.entry_yellow8, font=helv12, width=inputWidth)
        self.yellow8.grid(column=11, row=18)

        # informational/administrative data input fields
        self.roundDuration = tk.StringVar()
        self.roundDuration.set("120")
        self.roundDuration = tk.Entry(self, textvariable=self.roundDuration, font=helv12, width=inputWidth)
        self.roundDuration.grid(column=14, row=6)

        self.nrRounds = tk.StringVar()
        self.nrRounds.set("30")
        self.nrRounds = tk.Entry(self, textvariable=self.nrRounds, font=helv12, width=inputWidth)
        self.nrRounds.grid(column=14, row=7)

        self.costInboundWH = tk.StringVar()
        self.costInboundWH.set("3")
        self.costInboundWH = tk.Entry(self, textvariable=self.costInboundWH, font=helv12, width=inputWidth)
        self.costInboundWH.grid(column=14, row=9)

        self.costOutboundWH = tk.StringVar()
        self.costOutboundWH.set("3")
        self.costOutboundWH = tk.Entry(self, textvariable=self.costOutboundWH, font=helv12, width=inputWidth)
        self.costOutboundWH.grid(column=14, row=10)


        self.costBL = tk.StringVar()
        self.costBL.set("5")
        self.costBL = tk.Entry(self, textvariable=self.costBL, font=helv12, width=inputWidth)
        self.costBL.grid(column=14, row=11)

        self.budget = tk.StringVar()
        self.budget.set("1000")
        self.budget = tk.Entry(self, textvariable=self.budget, font=helv12, width=inputWidth)
        self.budget.grid(column=14, row=12)

        startButton = tk.Button(self, text="START", font="helv36", command=lambda: self.background(self.onClickStart(),()))
        startButton.grid(column='0', row='20', sticky='W')


#function to start the game
    def onClickStart(self):
        #get the round duration and number of rounds
        iRoundDuration = self.roundDuration.get()
        iNrRounds = self.nrRounds.get()

        #write the values of the admin into the database
        for r in range(1, int(iNrRounds) + 1):
            db_clients.writeAdminRoundValues(r, iRoundDuration)

        iCostInboundWH = self.costInboundWH.get()
        iCostOutboundWH = self.costOutboundWH.get()
        iCostBacklog = self.costBL.get()
        iBudget = self.budget.get()
        #writing the startvalues into the database
        db_clients.setAdminTeamValues(iBudget, iCostInboundWH, iCostOutboundWH, iCostBacklog ) #i = input


        #Read all the entered values for initial production times and inventories per team and product
        productValues = [[1, 'blue'  , self.entry_blue1.get()  ,self.entry_blue2.get()],
                         [1, "purple", self.entry_purple1.get(), self.entry_purple2.get()],
                         [1, "red"   , self.entry_red1.get()   , self.entry_red2.get()],
                         [1, "yellow", self.entry_yellow1.get(), self.entry_yellow2.get()],

                         [2, "blue", self.entry_blue3.get(), self.entry_blue4.get()],
                         [2, "purple", self.entry_purple3.get(), self.entry_purple4.get()],
                         [2, "red", self.entry_red3.get(), self.entry_red4.get()],
                         [2, "yellow", self.entry_yellow3.get(), self.entry_yellow4.get()],

                         [3, "blue", self.entry_blue5.get(), self.entry_blue6.get()],
                         [3, "purple", self.entry_purple5.get(), self.entry_purple6.get()],
                         [3, "red", self.entry_red5.get(), self.entry_red6.get()],
                         [3, "yellow", self.entry_yellow5.get(), self.entry_yellow6.get()],

                         [4, "blue", self.entry_blue7.get(), self.entry_blue8.get()],
                         [4, "purple", self.entry_purple7.get(), self.entry_purple8.get()],
                         [4, "red", self.entry_red7.get(), self.entry_red8.get()],
                         [4, "yellow", self.entry_yellow7.get(), self.entry_yellow8.get()]]

        for i in productValues:
            #writing product values into the database
            db_clients.writeAdminProductValues(i[0], i[1], i[2], i[3])

        # sending the START Signal to the clients
        server.sendto("START", ('<broadcast>', 37020))
        print("Sent: " + "START")
        time.sleep(5)
        self.startTimer(int(iNrRounds), int(iRoundDuration))

    #starting thread
    def background(self, func, args):
        th = threading.Thread(target=func, args=args)
        th.daemon = True
        th.start()

    # function to start the timer
    def startTimer(self, numberOfRounds, rundenZeit):
        sheets = []
        balances = {}
        for i in range(0, numberOfRounds):
            server.sendto("RUNDE"+str(i+1), ('<broadcast>', 37020))
            print("Sent: "+"RUNDE"+str(i+1))
            for i in range(rundenZeit, 0, -1):
                server.sendto(str(i), ('<broadcast>', 37020))
                print("Sent: " + str(i))
                time.sleep(1)
            server.sendto("ENDOFROUND", ('<broadcast>', 37020))
            time.sleep(15)

        
if __name__ == "__main__":
    app = Master()
    app.mainloop()