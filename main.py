from win32gui import GetWindowText, GetForegroundWindow 
import datetime
import json
from tkinter import *

''' Get current date '''
today = datetime.datetime.now().strftime("%Y-%m-%d")

''' Load data '''
with open('data.json','r') as f:
        data = json.loads(f.read())

''' Load current seconds '''
if today in data:
        seconds = data[today]["total"]
else:
        data[today] = {}
        seconds = 0

''' Initiate window '''
window = Tk()
title  = "Time Tracker"
window.title(title)
WIN_HEIGHT = 700
WIN_WIDTH  = 700
canvas = Canvas(window,height=WIN_HEIGHT,width=WIN_WIDTH)
canvas.pack()
TEXT_RELWIDTH = 0.6
TEXT_RELHEIGHT = 0.2 

''' Update usage history '''
def update_history():
        current_app = GetWindowText(GetForegroundWindow())
        current_app = app_filter(current_app)
        if current_app in data[today]:
                data[today][current_app] += 1
        else:
                data[today][current_app] = 1
        save_data()

''' Convert seconds into text hh/mm/ss '''
def time_to_text(seconds):
        h = seconds // 3600
        m = (seconds - 3600*h) // 60
        s = seconds - 3600*h - 60*m

        h,m,s = map(str,(h,m,s))
        text = "0"*(2 - len(h)) + h + ":" + "0"*(2 - len(m)) + m + ":" + "0"*(2 - len(s)) + s 
        return text

''' Update text every second '''
def update_text():
        var = StringVar()
        label = Label(window, textvariable=var,bg="gray",font="Courier 40 bold")
        var.set(time_to_text(seconds))
        label.place(relwidth=TEXT_RELWIDTH,relheight=TEXT_RELHEIGHT,relx=(1-TEXT_RELWIDTH)/2,rely=0.15)

''' Start a timer '''        
def start_timer():
        global seconds
        global pause
        if pause:
                return
        seconds += 1
        update_text()
        update_history()
        update_leaderboard()
        window.after(1000,start_timer)

''' Pause '''
def pause_timer():
        global pause
        pause = True
        btn.config(text="Continue",command=continue_timer)
        save_data()

''' Continue '''
def continue_timer():
        global pause
        pause = False
        btn.config(text="Pause",command=pause_timer)
        start_timer()

''' Save data '''
def save_data():
        global seconds
        data[today]["total"] = seconds
        with open('data.json','w') as f:
                json.dump(data, f)

''' Update leaderboard every second '''
def update_leaderboard():
        global data
        data[today] = {k: v for k, v in sorted(data[today].items(), key=lambda item: item[1],reverse=True)}
        save_data()
        colors = ["#FAF402","#2BFFF4","#E00022","#7A0871","#294994"]
        for i,v in enumerate(data[today].keys()):
                if i != 0:
                        app = app_filter(v)
                        app  += " " + time_to_text(data[today][v]) 
                        label = Label(window, text=app,bg=colors[i-1],font="Courier 10 bold")
                        label.place(relwidth=0.8,relheight=0.05,relx=0.1,rely=0.45 + 0.07*i)
                        if i == 5:
                                break

''' Filter app name '''
def app_filter(app):
        with open('filter_dict.json','r') as f:
                filter_dict = json.loads(f.read())

        for a,f in filter_dict.items():
                if a in app and a != "":
                        app = f
                if len(app) == 0:
                        app = filter_dict[""]
        if len(app) > 50:
                app = app[:23] + "..." + app[-23:] 
        return app

''' Main loop '''
pause = False
btn = Button(window,text="Pause",command=pause_timer)
btn.place(relx=0.4,rely=0.4,relwidth=0.2)
start_timer()
window.mainloop()

