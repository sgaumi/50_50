import tkinter as tk
from PIL import Image, ImageTk
import json
import time


class team:
    def __init__(self,name,points,imagepath,color):
        self.name = name
        self.point = points
        self.color = color
        self.image = Image.open(imagepath)
        # self.image = ImageTk.PhotoImage(pilim)

class gui:
    def __init__(self,config_file):
        #INIT#
        self.teams = self.teams_from_json(config_file)

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
        for i,t in enumerate(self.teams):
            w = int(((self.master.winfo_screenwidth()*3/4)/nb_col)-20)
            h = int(((self.master.winfo_screenheight())/nb_row)-20) 
            img_ = ImageTk.PhotoImage(self.im_resize(t.image,(w,h)))
            self.bt_count[t.name] = tk.Button(self.count,text=t.name,image=img_,compound="center",bg="black",relief="flat")
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
        for i,t in enumerate(self.teams):
            w = int(((self.master.winfo_screenwidth()*1/4)/1))
            h = int(((self.master.winfo_screenheight()*len(self.teams)/(len(self.teams)+2))/len(self.teams))-2)
            print(w,h) 
            img_ = ImageTk.PhotoImage(self.im_resize(t.image,(w,h)))
            self.lb_rank[t.name] = tk.Label(self.rank,text=t.name,image=img_,bg="black",compound="center")
            self.lb_rank[t.name].image = img_
            self.lb_rank[t.name].grid(row=i+1,column=0,sticky='news',pady=1)

        ############
        # self.master.update_idletasks()
        # for i,t in enumerate(self.teams):
        #     img_ = ImageTk.PhotoImage(self.im_resize(t.image,(100,100)))
        #     self.bt_count[t.name].configure(image=img_)
        #     self.bt_count[t.name].image=img_
        # self.master.update_idletasks()

        # self.bt1 = tk.Button(self.count,text="cnt")
        # self.bt1.grid(row=0,column=2,sticky="nwes",padx=10,pady=10)
        # self.bt12 = tk.Button(self.count,text="cnt")
        # self.bt12.grid(row=0,column=3,sticky="nwes")
        # self.bt13 = tk.Button(self.count,text="cnt")
        # self.bt13.grid(row=1,column=2,sticky="nwes")
        
        # self.bt2 = tk.Button(self.rank,text="rank")
        # self.bt2.pack()

        self.master.mainloop()

        

    def teams_from_json(self,config):
        with open(config,'r') as f:
            dic_ = json.loads(f.read())

        dicteams = dic_["teams"]
        teams = []
        for t in dicteams:
            tx = team(t['name'],t['point'],t['image'],t['color'])
            teams.append(tx)
        return teams
    
    def im_resize(self,img,size):
        # width = tkobj.winfo_width()
        # height = tkobj.winfo_height()
        # print(width,height)
        return img.resize(size)


if __name__ == "__main__":
    gui("config.json")