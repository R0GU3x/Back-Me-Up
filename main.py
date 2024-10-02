import flet as ft
import os
import backup
import threading

p = ft.Page

# ================= CLASSES =========================

D1 = {}
class ChckBox(ft.UserControl):

    def __init__(self, drive:str):
        super().__init__()
        self.drive = drive[0]
        D1[self.drive] = False
    
    @staticmethod
    def change(e):
        D1[e.control.data] = e.control.value

    def build(self):
        return ft.Checkbox(label=f'Drive {self.drive}',
                           value=self.drive,
                           active_color=ft.colors.TRANSPARENT,
                           check_color='#00ffff',
                           on_change=ChckBox.change,
                           data=self.drive)
    
# D2 = ''
class RadBut(ft.UserControl):

    def __init__(self, drives:list):
        super().__init__()
        self.drives = drives
        self.D2 = ''
    
    def change(self, e):
        self.D2 = e.control.value

    def build(self):
        radios = [ft.Radio(label=f'Drive {drive[0]}', 
                           value=drive[0],
                           active_color='#ffa44a') 
                    for drive in self.drives]
        return ft.RadioGroup(ft.Column(controls=radios), on_change=self.change)

class Head(ft.UserControl):

    def __init__(self, s:str):
        super().__init__()
        self.s = s.split()
    
    def build(self):
        controls = []
        for i in self.s:
            color = 'red' if i == 'Me' else 'white'
            controls.append(ft.Text(value=i,font_family=0,size=80, color=color))
        return ft.Row(controls=controls,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20)

# ================= HEAD SECTION ====================

headRow = Head('Back Me Up')

# ================== BODY ======================

backupHead = ft.Text(value='Backup Source', 
                     font_family=1, 
                     size=15,
                     color='#1971C2')

d = os.listdrives()
drives = {i+1: ChckBox(d[i]) for i in range(0, len(d))}

sourceDrives = ft.Column(controls=list(drives.values()))
sourceSection = ft.Container(
    ft.Column(controls=[backupHead, sourceDrives]))

destinationHead = ft.Text(value='Backup Destination',
                          font_family=1,
                          size=15,
                          color='#ff8000')
destinationDrives = RadBut(os.listdrives())
destinationSection = ft.Container(
    ft.Column(controls=[destinationHead,destinationDrives]))

body = ft.Row(controls=[sourceSection,destinationSection],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=50)

# ========================= SUBMIT =======================

def run(e):

    file = fileNameField.value
    if not file:
        fileNameField.error_text = 'Name your Backup to proceed'
        fileNameField.update()
        return None

    p.close(filePrompt)
    progContainer.visible = True
    progContainer.update()

    b = backup.Backup(D1, destinationDrives.D2)
    b.analyze(file)
    b.run(progBar, progValue, progContainer)

def start(e):

    global fileNameField, filePrompt
    fileNameField = ft.TextField(
        hint_text='File Name',
        autofocus=True,
        on_submit=run
    )

    filePrompt = ft.AlertDialog(open=True, modal=True,
                        title=ft.Text(value='Backup Name'),
                        content=fileNameField,
                        actions=[ft.Column(controls=[
                            ft.ElevatedButton(
                                text='Begin Backup',
                                on_click=run)
                        ])],
                        shadow_color=ft.colors.BLACK)
    p.open(filePrompt)

submitText = ft.Text(
                value='Create Backup',
                color='Yellow',
                size=20,
                italic=True)
submit = ft.Container(ft.ElevatedButton(content=submitText,
                           color='Yellow',
                           bgcolor='#10ffff00',
                           on_click=start),
                        margin=ft.margin.only(top=20, bottom=5))

# ====================== PROGRESSBAR ======================

progBar = ft.ProgressBar(width=500, 
                         color='#1cff1c', 
                         border_radius=5)
progValue = ft.Text(value='Analyzing...', 
                    visible=True, 
                    color='#1cff1c')

progContainer = ft.Column(
        controls=[progBar, progValue],
        spacing=2,
        visible=False)

# TODO ======================= Head 2 =============================

headRow2 = Head('Revive Me')

# ================== BODY ======================

backupHead2 = ft.Text(value='Backup Location', 
                     font_family=1, 
                     size=15,
                     color='#1971C2')
# backupScanButton = ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
#                                  icon_color='#00ffff',
#                                  on_click=scan)
# backupHead2Container = ft.Row(controls=[backupHead2, backupScanButton])

# d = os.listdrives()
# drives = {i+1: ChckBox(d[i]) for i in range(0, len(d))}

def pick_files2(e:ft.FilePickerResultEvent):
    global backupFile
    backupFile = (e.files)[0].path
    filePicker.text = os.path.split(backupFile)[-1]
    filePicker.update()
# sourceDrives2 = ft.Column(controls=list(drives.values()))

filePickerDialog = ft.FilePicker(on_result=pick_files2)
filePicker = ft.TextButton(
    text='Choose your Backup File',
    style=ft.ButtonStyle(color='#00ff9d'),
    icon=ft.icons.UPLOAD_FILE_ROUNDED,
    # icon_color='#00ffff',
    on_click=lambda _:filePickerDialog.pick_files(allowed_extensions=['backup']))

sourceSection2 = ft.Container(
    ft.Column(controls=[backupHead2, filePicker]))

destinationHead2 = ft.Text(value='Restore Location',
                          font_family=1,
                          size=15,
                          color='#ff8000')
destinationDrives2 = RadBut(os.listdrives())
destinationSection2 = ft.Container(
    ft.Column(controls=[destinationHead2,destinationDrives2]))

body2 = ft.Row(controls=[sourceSection2,destinationSection2],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=50)

# ========================= SUBMIT =======================

def run2(e):

    progContainer2.visible = True
    progContainer2.update()

    r = backup.Restore(backupFile, destinationDrives2.D2)
    r.analyze()
    r.run(progBar2, progValue2, progContainer2)

submitText2 = ft.Text(
                value='Restore Backup',
                color='Yellow',
                size=20,
                italic=True)
submit2 = ft.Container(ft.ElevatedButton(content=submitText2,
                           color='Yellow',
                           bgcolor='#10ffff00',
                           on_click=run2),
                        margin=ft.margin.only(top=20, bottom=5))

# ====================== PROGRESSBAR ======================

progBar2 = ft.ProgressBar(width=500, 
                         color='#1cff1c', 
                         border_radius=5)
progValue2 = ft.Text(value='Analyzing...', 
                    visible=True, 
                    color='#1cff1c')

progContainer2 = ft.Column(
        controls=[progBar2, progValue2],
        spacing=2,
        visible=False)


def main(page: ft.Page):
    page.title = 'Backup System'
    page.fonts = {0: 'fonts/INFECTED.ttf', 1:'fonts/Akira Expanded Demo.otf'}
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width, page.window.height = 555, 830
    page.window.resizable = False
    page.scroll = ft.ScrollMode.ALWAYS

    global p
    p = page

    page.add(ft.Column(controls=[headRow, body, submit, progContainer,
                                 headRow2, body2, submit2, progContainer2,
                                 filePickerDialog], 
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER))


ft.app(main)
