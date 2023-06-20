import tkinter as tk
from PIL import Image, ImageTk
import json
import time


class team:
    def __init__(self,name,points,imagepath,color,color_text):
        self.name = name
        self.point = points
        self.color = color
        self.color_text = color_text
        self.image = Image.open(imagepath)
        # self.image = ImageTk.PhotoImage(pilim)

def sort_dict(x):
    return dict(sorted(x.items(), key=lambda item: item[1], reverse=True))

def add_point(n):
    print(n)

class gui:
    def __init__(self,config_file):
        #INIT#
        self.teams = self.teams_from_json(config_file)
        self.points = sort_dict(dict([(t.name,t.point) for t in self.teams.values()]))

        #GUI#
        self.master = tk.Tk()
        self.master.configure(background="black")
        self.master.state('zoomed')
        self.master.title("50/50")

        self.master.columnconfigure(0,weight=3)
        self.master.columnconfigure(1,weight=1)
        self.master.rowconfigure(0,weight=1)

        #############

        self.count = tk.Frame(self.master,background='black')
        self.count.grid(row=0,column=0,sticky="nwes")

        nb_col = 4
        nb_row = len(self.teams)//nb_col + (1 if len(self.teams)%nb_col!=0 else 0)
        for c in range(nb_col):
            self.count.columnconfigure(c,weight=1)
        for r in range(nb_row):
            self.count.rowconfigure(r,weight=1)

        self.bt_count = {}
        func={}
        for i,t in enumerate(self.teams.values()):
            w = int(((self.master.winfo_screenwidth()*3/4)/nb_col)-20)
            h = int(((self.master.winfo_screenheight())/nb_row)-20)-35 
            img_ = ImageTk.PhotoImage(self.im_resize(t.image,(w,h)))
            self.bt_count[t.name] = tk.Button(self.count,text=f"{t.name} - {t.point}",image=img_,compound="top",bg="black",relief="flat",fg="#ffffff",font=("Arial",14),command=lambda nm=t.name: self.add_point(nm))
            self.bt_count[t.name].image = img_
            self.bt_count[t.name].grid(row=i//nb_col,column=i%nb_col,sticky='news',padx=10,pady=10)
        
        

        ###########

        self.rank = tk.Frame(self.master,background='black')
        self.rank.grid(row=0,column=1,sticky="news",padx=10)
        
        self.rank.columnconfigure(0,weight=1)
        self.rank.rowconfigure(0,weight=2)
        for r in range(len(self.teams)):
            self.rank.rowconfigure(r+1,weight=1)
        self.rank_title = tk.Label(self.rank,text="Classement",fg="white",font=("Arial",50),bg="black")
        self.rank_title.grid(row=0,column=0,sticky='news')
        self.lb_rank={}
        for i,t in enumerate(self.teams.values()):
            w = int(((self.master.winfo_screenwidth()*1/4)/1))
            h = int(((self.master.winfo_screenheight()*len(self.teams)/(len(self.teams)+2))/len(self.teams))-2)
            # img_ = ImageTk.PhotoImage(self.im_resize(t.image,(w,h)))
            self.lb_rank[t.name] = tk.Label(self.rank,text=t.name,bg=t.color,compound="center",fg=t.color_text)
            # self.lb_rank[t.name].image = img_
            self.lb_rank[t.name].grid(row=i+1,column=0,sticky='news',pady=1)
        self.refresh_rank()

        ############

        self.master.mainloop()

    def add_point(self,n):
        self.teams[n].point += 1
        self.bt_count[n].config(text=f"{n} - {self.teams[n].point}")
        self.refresh_rank()

    def refresh_rank(self):
        self.points = sort_dict(dict([(t.name,t.point) for t in self.teams.values()]))
        i=1
        for k,(n,p) in enumerate(zip(self.points.keys(),self.points.values())):
            self.lb_rank[n] = tk.Label(self.rank,text=f"{k+1} - {n} ({p} {'points' if p>1 else 'point'})",bg=self.teams[n].color,compound="center",fg=self.teams[n].color_text,font=("Arial",12))
            self.lb_rank[n].grid(row=i,column=0,sticky='news',pady=1)
            i+=1
        

    def teams_from_json(self,config):
        with open(config,'r') as f:
            dic_ = json.loads(f.read())

        dicteams = dic_["teams"]
        teams = {}
        for t in dicteams:
            tx = team(t['name'],t['point'],t['image'],t['color'],t["color_text"])
            teams[t['name']] = tx
        return teams
    
    def im_resize(self,img,size):
        # width = tkobj.winfo_width()
        # height = tkobj.winfo_height()
        # print(width,height)
        return img.resize(size)


if __name__ == "__main__":
    gui("config.json")