import shutil
import os
import threading
import flet as ft

class Backup:
    
    def __init__(self, D1:dict, D2:str):
        self.source = list()
        for i in D1.keys():
            if D1[i] == True:
                self.source.append(i)
        self.destination = D2
        self.files = []
        self.progress = 0
    
    def analyze(self, file:str):
        for drive in self.source:
            R = list(os.walk(f'{drive}:'))
        
            self.files = []
            for r in R:
                for r2 in r[2]:
                    self.files.append(os.path.join(r[0], r2))
            
        self.totalFiles = len(self.files)

        dirsFiles = R[0][1:]
        with open(f'{self.destination}:\\{file}.backup', 'w') as f:
            f.write(str(len(dirsFiles[0])) + '\n')
            for category in dirsFiles:
                for c in category:
                    f.write(c + '\n')

    def get_percentage(self) -> float:
        if self.totalFiles:
            value = self.progress / self.totalFiles
            return round(value, 2)
        return 0

    def move(self, source:str, destination:str):
            destination = destination+':\\' + source[2:]
            done = False
            while not done:
                try:
                    shutil.copyfile(source, destination)
                    done = True
                except:
                    try:
                        os.makedirs(os.path.split(destination)[0])
                    except:
                        break

            self.progress += 1
            
    def run(self, progBar:ft.ProgressBar, progValue:ft.Text, progContainer:ft.Container):
        for file in self.files:
            self.move(file, self.destination)

            n = self.get_percentage()
            progBar.value = n
            if progBar.value == 1:
                progValue.value = 'Backup Successful'
            else:
                progValue.value = f'Progress: {int(n*100)}%'
            progContainer.update()

# todo ====================================================================

class Restore:
    
    def __init__(self, backupFile:str, D2:str):
        with open(backupFile, 'r') as f:
            r = f.readlines()
        self.n = int(r[0])
        self.dir = r[1:self.n+1]
        self.homeFiles = r[self.n+1:]

        self.sourceDrive = backupFile[0]
        self.destinationDrive = D2
        self.progress = 0
    
    def analyze(self):
        R = []
        for dir in self.dir:
            R.extend(list(os.walk(f'{self.sourceDrive}:\\{dir.strip('\n')}')))

        self.totalFiles = []
        for r in R:
            for i in r[2]:
                self.totalFiles.append(os.path.join(r[0], i))
    
    def get_percentage(self) -> float:
        if self.totalFiles:
            value = self.progress / len(self.totalFiles)
            return round(value, 2)
        return 0

    def move(self, source:str, destination:str):
        done = False
        while not done:
            try:
                shutil.copyfile(source, destination)
                done = True
            except:
                try:
                    os.makedirs(os.path.split(destination)[0])
                except:
                    break

        self.progress += 1


    def run(self, progBar2:ft.ProgressBar, progValue2:ft.Text, progContainer2:ft.Container):

        self.totalFiles.extend(self.sourceDrive+':\\'+homeFile.strip('\n') for homeFile in self.homeFiles)

        for file in self.totalFiles:
            self.move(file, self.destinationDrive+file[1:])
        
            n = self.get_percentage()
            progBar2.value = n
            if progBar2.value == 1:
                progValue2.value = 'Backup Successful'
            else:
                progValue2.value = f'Progress: {int(n*100)}%'
            progContainer2.update()
        
        # for file in self.files:


        

# if name == main
if __name__ == "__main__":
    source = {'C': False, 'D': False, 'E': True}
    destination = 'D'
    b = Backup(source, destination)
    # threading.Thread(target=b.get_percentage())
    b.run()
