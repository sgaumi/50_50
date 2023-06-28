import tkinter as tk
from PIL import Image, ImageTk
import json
import time

BACKGROUND = "#222222"
COUNT_SORT = True

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
        self.delete_mode = False
        self.windowed = False

        #GUI#
        self.master = tk.Tk()
        self.master.configure(background=BACKGROUND)
        self.master.state('zoomed')
        self.master.title("50/50")
        self.master.attributes('-fullscreen', True)

        self.master.columnconfigure(0,weight=3)
        self.master.columnconfigure(1,weight=1)
        self.master.rowconfigure(0,weight=1)

        #############

        self.menubar = tk.Menu(self.master,tearoff=0)
        self.filemenu = tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="mode incrémentation",command=self.switch_to_incr_mode,background=self.filemenu.cget("background") if self.delete_mode else "green")
        self.filemenu.add_command(label="mode décrémentation",command=self.switch_to_delete_mode,background=self.filemenu.cget("background") if not self.delete_mode else "green")
        self.menubar.add_cascade(label="mode",menu=self.filemenu)
        self.filemenu2 = tk.Menu(self.menubar,tearoff=0)
        self.filemenu2.add_command(label="plein écran",command=self.switch_to_fullscreen,background=self.filemenu2.cget("background") if self.windowed else "green")
        self.filemenu2.add_command(label="fenêtré",command=self.switch_to_wdw,background=self.filemenu2.cget("background") if not self.windowed else "green")
        self.menubar.add_cascade(label="écran",menu=self.filemenu2)
        self.menubar.add_command(label="réinitialiser",command=self.reset)
        self.menubar.add_command(label="sortir",command=self.master.destroy)
        self.master.config(menu=self.menubar)

        #############

        self.count = tk.Frame(self.master,background=BACKGROUND)
        self.count.grid(row=0,column=0,sticky="nwes")

        self.nb_col = 4
        self.nb_row = len(self.teams)//self.nb_col + (1 if len(self.teams)%self.nb_col!=0 else 0)
        for c in range(self.nb_col):
            self.count.columnconfigure(c,weight=1)
        for r in range(self.nb_row):
            self.count.rowconfigure(r,weight=1)

        self.bt_count = {}
        func={}
        for i,t in enumerate(self.teams.values()):
            w = int(((self.master.winfo_screenwidth()*3/4)/self.nb_col)-20)
            h = int(((self.master.winfo_screenheight())/self.nb_row)-20)-35 
            img_ = ImageTk.PhotoImage(self.im_resize(t.image,(w,h)))
            self.bt_count[t.name] = tk.Button(self.count,text=f"{t.name} - {t.point}",
                                              image=img_,compound="top",bg=BACKGROUND,relief="flat",fg="#ffffff",font=("Arial",14),
                                              activebackground='black',activeforeground='white',
                                              command=lambda nm=t.name: self.add_point(nm))
            self.bt_count[t.name].image = img_
            self.bt_count[t.name].grid(row=i//self.nb_col,column=i%self.nb_col,sticky='news',padx=10,pady=10)
        
        

        ###########

        self.rank = tk.Frame(self.master,background=BACKGROUND)
        self.rank.grid(row=0,column=1,sticky="news",padx=10)
        
        self.rank.columnconfigure(0,weight=1)
        self.rank.rowconfigure(0,weight=2)
        for r in range(len(self.teams)):
            self.rank.rowconfigure(r+1,weight=1)
        self.rank_title = tk.Label(self.rank,text="Classement",fg="white",font=("Arial",50),bg=BACKGROUND)
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

    def switch_to_incr_mode(self):
        self.delete_mode = False
        self.filemenu.entryconfigure("mode incrémentation", background=self.filemenu.cget("background") if self.delete_mode else "green")
        self.filemenu.entryconfigure("mode décrémentation", background=self.filemenu.cget("background") if not self.delete_mode else "green")

    def switch_to_delete_mode(self):
        self.delete_mode = True
        self.filemenu.entryconfigure("mode incrémentation", background=self.filemenu.cget("background") if self.delete_mode else "green")
        self.filemenu.entryconfigure("mode décrémentation", background=self.filemenu.cget("background") if not self.delete_mode else "green")

    def switch_to_fullscreen(self):
        if self.windowed:
            self.master.attributes('-fullscreen', True)
        self.windowed = False
        self.filemenu2.entryconfigure("plein écran", background=self.filemenu2.cget("background") if self.windowed else "green")
        self.filemenu2.entryconfigure("fenêtré", background=self.filemenu2.cget("background") if not self.windowed else "green")

    def switch_to_wdw(self):
        if not self.windowed:
            self.master.attributes('-fullscreen', False)
        self.windowed = True
        self.filemenu2.entryconfigure("plein écran", background=self.filemenu2.cget("background") if self.windowed else "green")
        self.filemenu2.entryconfigure("fenêtré", background=self.filemenu2.cget("background") if not self.windowed else "green")

    def add_point(self,n):
        if self.delete_mode:
            self.teams[n].point -= 1
        else:
            self.teams[n].point += 1
        self.bt_count[n].config(text=f"{n} - {self.teams[n].point}")
        self.refresh_rank()

    def reset(self):
        for n in self.teams.keys():
            self.teams[n].point = 0
            self.bt_count[n].config(text=f"{n} - {self.teams[n].point}")
        self.refresh_rank()

    def refresh_rank(self):
        self.points = sort_dict(dict([(t.name,t.point) for t in self.teams.values()]))
        i=1
        for k,(n,p) in enumerate(zip(self.points.keys(),self.points.values())):
            self.lb_rank[n] = tk.Label(self.rank,text=f"{k+1} - {n} ({p} {'points' if p>1 else 'point'})",bg=self.teams[n].color,compound="center",fg=self.teams[n].color_text,font=("Arial",24))
            self.lb_rank[n].grid(row=i,column=0,sticky='news',pady=1)
            i+=1

            if COUNT_SORT:
                self.bt_count[n].grid(row=k//self.nb_col,column=k%self.nb_col,sticky='news',padx=10,pady=10)

        

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