import tkinter as tk
import random


class BingoGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.title("Bingo Game")
        self.geometry("355x490")
        self.loadImages()
        self.numberOfImage = 51

    def createWidgets(self):
        self.createTopFrame()
        self.createBottomFrame()
        self.createStatusLabel()

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

        if self.btnStart["text"] == "START":
            self.btnStart["text"] = "RESTART"
            self.loadImages()
        else:
            self.btnStart["text"] = "START"
            self.after_cancel(self.reload_images_again)
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
        if self.btnStart["text"] == "RESTART":
            self.numberOfImage = 25

            animalImages = poppedImages + animalImages
            self.load_images_job = self.after(1000, self.loadImagesInBottomFrame, animalImages)

    def checkIfGameOver(self):
        for i in range(5):
            for j in range(5):
                if self.middleFrame.grid_slaves(row=i, column=j):
                    label_on_board = self.middleFrame.grid_slaves(row=i, column=j)[0]
                    if label_on_board.cget("bg") != "red":
                        return False
        return True

    def loadImagesInBottomFrame(self, animalImages):
        random.shuffle(animalImages)

        if self.checkIfGameOver():
            self.lblStatus.config(text="Game Over")
            self.after_cancel(self.reload_images_again)
            return

        if not animalImages:
            return
        if self.numberOfImage == 0:
            return
        selected_image = animalImages.pop(0)
        if len(self.imageLabels) >= 5:
            label_to_overwrite = self.imageLabels.pop(0)
            label_to_overwrite.config(image=selected_image)
            label_to_overwrite.image = selected_image
            self.imageLabels.append(label_to_overwrite)
        else:
            label = tk.Label(self.bottomFrame, image=selected_image)
            label.image = selected_image
            self.imageLabels.append(label)

        for i, label in enumerate(self.imageLabels):
            label.grid(row=0, column=i + 2)  
  
        for i in range(5):
            for j in range(5):
                if self.middleFrame.grid_slaves(row=i, column=j):
                    label_on_board = self.middleFrame.grid_slaves(row=i, column=j)[0]
                    if str(label_on_board.image) == str(selected_image):
                        label_on_board.config(bg="red")
        self.numberOfImage -= 1
        print()
        self.lblStatus.config(text=f"Status: {self.numberOfImage} left")

        if len(self.imageLabels) < 5:
            self.reload_images_again = self.after(1000, self.loadImagesInBottomFrame, animalImages)
        else:
            self.reload_images_again = self.after(1000, self.loadImagesInBottomFrame, animalImages + [selected_image])


app = BingoGame()
app.mainloop()