import tkinter as tk
import random

class TopFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.createWidgets()

    def createWidgets(self):
        self.createTopFrame()
    
    def createTopFrame(self):
        self.topFrame = tk.Frame(self, bg="yellow", pady=5)
        self.topFrame.pack(fill="x")

        self.lblCardNo = tk.Label(self.topFrame, text="How many cards?", font=("arial", 10, "bold"), bg="yellow")
        self.lblCardNo.pack(side="left", padx=(70, 0), anchor="center")

        self.spnCardNo = tk.Spinbox(self.topFrame, from_=1, to=4, width=5)
        self.spnCardNo.pack(side="left", padx=5, anchor="center")

        self.btnStart = tk.Button(self.topFrame, text="START", font=("arial", 9, "bold"), bg="yellow", padx=10, pady=3,
                                  command=self.startGame)
        self.btnStart.pack(side="left", padx=(5, 40), anchor="center")

        
        
    # create a startGame method that will start all of the instance bingoboard 
    
    def startGame(self):
        num_boards = int(self.spnCardNo.get())
        self.parent.start_all(num_boards)
        

    

class BingoBoard(tk.Frame):
    def __init__(self, parent, top_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.top_frame = top_frame
        self.createWidgets()
        self.loadImages()
        
        self.numberOfImage = 150

    def createWidgets(self):
        self.createTopFrame()
        self.createBottomFrame()
        self.createStatusLabel()
        
    def createTopFrame(self):
        

        self.middleFrame = tk.Frame(self)
        self.middleFrame.pack()


    def createBottomFrame(self):
        self.bottomFrame = tk.Frame(self)
        self.bottomFrame.pack(fill="both", expand=True)

        self.imageLabels = []

    def createStatusLabel(self):
        self.lblStatus = tk.Label(self, text="", font=("arial", 10, "bold"))
        self.lblStatus.pack(side="bottom", fill="x", padx=10, pady=5)

    def startGame(self):

        if self.top_frame.btnStart["text"] == "START":
            self.top_frame.btnStart["text"] = "RESTART"
            self.loadImages()
        else:
            self.top_frame.btnStart["text"] = "START"
            
            for label in self.imageLabels:
                label.destroy()
            self.imageLabels = []
    def loadImages(self):
        for widget in self.middleFrame.winfo_children():
            widget.grid_forget()

        with open("txtImages.txt", "r") as file:
            animalNames = file.readlines()

        animalNames = [name.strip('\n') for name in animalNames]

        animalImages = []
        for name in animalNames:
            try:
                image = tk.PhotoImage(file=f"{name}.png")
                animalImages.append(image)
            except tk.TclError:
                print(f"Image file for {name} not found")

        random.shuffle(animalImages)

        for label in self.imageLabels:
            label.destroy()
        self.imageLabels = []
        poppedImages = []
        for i in range(5):
            for j in range(5):

                if animalImages:
                    poppedImages.append(animalImages[-1])
                    selected_image = animalImages.pop()
                    label = tk.Label(self.middleFrame, image=selected_image, relief="groove")
                    label.image = selected_image
                    label.grid(row=i, column=j)
                else:
                    break
        self.lblStatus.config(text=f"Status: {len(animalImages)} left")
        if self.top_frame.btnStart["text"] == "RESTART":
            self.numberOfImage = 150

            animalImages = poppedImages + animalImages
            self.load_images_job = self.after(1000, app.loadImagesInBottomFrame, animalImages)

    def checkIfGameOver(self):
        for i in range(5):
            for j in range(5):
                if self.middleFrame.grid_slaves(row=i, column=j):
                    label_on_board = self.middleFrame.grid_slaves(row=i, column=j)[0]
                    if label_on_board.cget("bg") != "red":
                        return False
        return True

   

class BingoGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bingo Game")

        # Create the top frame
        self.top_frame = TopFrame(self)
        self.top_frame.pack(fill=tk.X)

        self.boards = []
    def loadImagesInBottomFrame(self, animalImages):
        random.shuffle(animalImages)

        for board in self.boards:
            if board.checkIfGameOver():
                board.lblStatus.config(text="Game Over")
                return
            else: 
                selected_image = animalImages.pop(0)
                if len(board.imageLabels) >= 5:
                    label_to_overwrite = board.imageLabels.pop(0)
                    label_to_overwrite.config(image=selected_image)
                    label_to_overwrite.image = selected_image
                    board.imageLabels.append(label_to_overwrite)
                else:
                    label = tk.Label(board.bottomFrame, image=selected_image)
                    label.image = selected_image
                    board.imageLabels.append(label)

                for i, label in enumerate(board.imageLabels):
                    label.grid(row=0, column=i + 2)  
        
                for i in range(5):
                    for j in range(5):
                        if board.middleFrame.grid_slaves(row=i, column=j):
                            label_on_board = board.middleFrame.grid_slaves(row=i, column=j)[0]
                            if str(label_on_board.image) == str(selected_image):
                                label_on_board.config(bg="red")
                board.numberOfImage -= 1
                print()
                board.lblStatus.config(text=f"Status: {board.numberOfImage} left")

                if len(board.imageLabels) < 5:
                    self.reload_images_again = board.after(1000, self.loadImagesInBottomFrame, animalImages)
                else:
                    self.reload_images_again = board.after(1000, self.loadImagesInBottomFrame, animalImages + [selected_image])


    def start_all(self, num_boards):
        # Remove old boards
        for board in self.boards:
            board.pack_forget()
            board.destroy()

        # Create new boards
        self.boards = [BingoBoard(self, self.top_frame) for _ in range(num_boards)]
        for board in self.boards:
            board.pack(side=tk.LEFT, padx=10)
            
        for board in self.boards:
            print("Starting the Game...")
            board.startGame()
app = BingoGame()
app.mainloop()