#final amazing scaling and zooming with mouse
import tkinter as tk
import random
import numpy
import math
import turtle as tt
import tkinter.font as tf
import os.path
from datetime import datetime
import matplotlib.pyplot as plt
import configparser
import ast
import json
import tkinter.messagebox as tkMessageBox
import sqlite3
from PIL import ImageTk, Image
pressed = False
def tsp(s1,data,starting,ending):
    # build a graph
    G,inn = build_graph(s1,data,starting,ending)
    

    # build a minimum spanning tree
    MSTree = minimum_spanning_tree(G)
    

    # find odd vertexes
    odd_vertexes = find_odd_vertexes(MSTree)
   
    # add minimum weight matching edges to MST
    minimum_weight_matching(MSTree, G, odd_vertexes)
    

    # find an eulerian tour
    eulerian_tour = find_eulerian_tour(MSTree, G)
    
    
    #del(eulerian_tour[-1])
    
    
    p=[]
    for v in eulerian_tour:
        p.append(data[v])

    

   
    
    
    
    
    
    
    return  p,inn
    




def build_graph(grid,data,starting,ending):
    graph = {}
    innerroute={}
    for this in range(len(data)):
        for another_point in range(len(data)):
            if this != another_point:
                if this not in graph:
                        graph[this] = {}
                if(data[this]==("dummy") or data[another_point]==("dummy")):
                    if(data[this]==starting or data[another_point]==starting):
                        graph[this][another_point]=0
                        key1=str([data[this],data[another_point]])
                        innerroute[key1]=[] 
                    elif(data[this]==ending or data[another_point]==ending):
                        graph[this][another_point]=0
                        key1=str([data[this],data[another_point]])
                        innerroute[key1]=[]       
                    else:
                        graph[this][another_point]=math.inf
                        key1=str([data[this],data[another_point]])
                        innerroute[key1]=[]   
                else:
                    
                    ib=breadth_first_search(grid,data[this],data[another_point])
                
                    graph[this][another_point] =len(ib)
                    key1=str([data[this],data[another_point]])
                    innerroute[key1]=ib

    return graph,innerroute


class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def minimum_spanning_tree(G):
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)

    return tree


def find_odd_vertexes(MST):
    tmp_g = {}
    vertexes = []
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes


def minimum_weight_matching(MST, G, odd_vert):
    import random
    random.shuffle(odd_vert)

    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        MST.append((v, closest, length))
        odd_vert.remove(closest)


def find_eulerian_tour(MatchedMSTree, G):
    # find neigbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # print("Neighbours: ", neighbours)

    # finds the hamiltonian circuit
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(MatchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP


def remove_edge_from_matchedMST(MatchedMST, v1, v2):

    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]

    return MatchedMST




def breadth_first_search(grid,start,goal):
    N = len(grid)

    def is_clear(cell):
        return grid[cell[0]][cell[1]] == 0

    def get_neighbours(cell):
        (i, j) = cell
        return (
            (i + a, j + b)
            
            for a in (-1, 0, 1)
            for b in (-1, 0, 1)
            if a != 0 or b != 0
            if 0 <= i + a < N
            if 0 <= j + b < N
            if is_clear( (i + a, j + b) )
        )

   

    queue = []
    if is_clear(start):
        queue.append([start])
    visited = set()
    path_len = {start: 1}
    route=[]
    
    while queue:
        path = queue.pop(0)
        vertex = path[-1]
    
        if vertex == goal:
                return path
        
        elif vertex not in visited: 
            for neighbour in get_neighbours(vertex):
                
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    return new_path
                    
            visited.add(vertex)       
        
           

    return route
class item:
    def __init__(self,itemname,xcor,ycor):
        self.itemname = itemname
        self.xcor = xcor
        self.ycor = ycor
def convert(L):
    C=[]
    for I in L:
        C.append((I.itemname,I.xcor,I.ycor))
    return C
def convertback(L):
    C=[]
    for I in L:
        C.append(item(I[0],I[1],I[2]))        
    return(C)
    
# LISTBOX
class EditShoppingList(tk.Frame):
    def __init__(self, parent,availableitems,previouslist,*args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        
        self.shoppinglist=availableitems
        self.finallist=previouslist
        self.listboxx=tk.Listbox(parent)
        self.listboxx2=tk.Listbox(parent)
        self.listbox2 = tk.Listbox(self.listboxx2,height=20,width=20)
        self.listbox = tk.Listbox(self.listboxx,height=20,width=20)
        self.chkboxes=[]
        self.chkboxes2=[]
        self.chkstates=[]
        self.chkstates2=[]
        self.search_var =tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        self.entry = tk.Entry(parent, textvariable=self.search_var, width=13)
        self.Tx=tk.Label(parent,text="    Search")
        self.Tx1=tk.Label(parent,text="\n"+"    Available Items in Store"+"\n"+"    (click on item to add)")
        self.Tx2=tk.Label(parent,text="\n"+"    Your shopping List"+"\n"+"(click on item to remove)")
        self.flag=0
        for item in range(len(self.shoppinglist)):
            chk_state9 =tk.BooleanVar()
            if(self.shoppinglist[item] in self.finallist):
                chk_state9.set(True)
            else:        
                chk_state9.set(False)
            self.chkstates.append(chk_state9)
            chk9 = tk.Checkbutton(self.listbox, text=self.shoppinglist[item], var=self.chkstates[-1],bg='white',selectcolor="white",fg="black",command=self.createlist)
            self.chkboxes.append(chk9)
            chk9.pack(fill='both')
        for item1 in range(len(self.finallist)):
            chk_state9 =tk.BooleanVar()
            chk_state9.set(False)
            self.chkstates2.append(chk_state9)
            chk9 = tk.Checkbutton(self.listbox2, text=self.finallist[item1], var=self.chkstates2[-1],bg='white',selectcolor="white",fg="black",command=self.deletelist)
            self.chkboxes2.append(chk9)
            chk9.pack(fill='both')
            
        self.listboxx.grid(column=0, row=2)
        self.listboxx2.grid(column=1, row=2)
        self.listbox.pack(fill='both')
        self.listbox2.pack(fill='both')
        #chk.grid(column=0, row=0)
        self.entry.grid(column=1, row=0)
        self.Tx.grid(column=0, row=0)
        self.Tx1.grid(column=0, row=1)
        self.Tx2.grid(column=1, row=1)
      




            
    def deletelist(self):
        
        if(len(self.chkstates2)==0):
            return(0)
        i=0
        l=len(self.chkstates2)
        while(i<l):
            if(self.chkstates2[i].get()==True):
                for j in range(len(self.chkstates)):
                    if(self.chkboxes2[i].cget('text')==self.chkboxes[j].cget('text') ):   
                        self.chkstates[j].set(False)

                        temp=self.chkboxes2.pop(i)
                        temp.destroy()

                  
                        del self.chkstates2[i]
                        l=l-1
                        self.finallist.remove(self.chkboxes[j].cget('text'))
                        self.flag=1
                        break
            i=i+1        
                   

    def createlist(self):
         

        for i in range(len(self.chkstates)):

            if(self.chkstates[i].get()==True):
                f=0
                for j in range(len(self.chkstates2)):
                    if(self.chkboxes[i].cget('text')==self.chkboxes2[j].cget('text')):
                        f=1
                        break
                if(f==0):
                    chk_state9 =tk.BooleanVar()
                    chk_state9.set(False)
                    self.chkstates2.append(chk_state9)
                    chk9 = tk.Checkbutton(self.listbox2, text=self.shoppinglist[i], var=self.chkstates2[-1],bg='white',selectcolor="white",fg="black",command=self.deletelist)
                    self.chkboxes2.append(chk9)
                    chk9.pack(fill='both')
                    self.finallist.append(self.shoppinglist[i])
                    self.flag=1
            elif(self.chkstates[i].get()==False):
                for k in range(len(self.chkstates2)):
                    if(self.chkboxes2[k].cget('text')==self.chkboxes[i].cget('text') ):   


                        temp=self.chkboxes2.pop(k)
                        temp.destroy()


                        del self.chkstates2[k]
                        self.finallist.remove(self.chkboxes[i].cget('text'))
                        self.flag=1
                        break        
    def update_list(self):

        search_term = self.search_var.get()

            # Just a generic list to populate the self.listbox



        for i in range(len(self.chkboxes)):
            self.chkboxes[i].pack_forget()
        for item in self.shoppinglist:
            if search_term.lower() in item.lower():
                for i in range(len(self.chkboxes)):
                    if(self.chkboxes[i].cget('text')==item):
                        self.chkboxes[i].pack()
                #self.listbox2.insert(END, item)


        allitems=list()
        for i in range(self.listbox.size()):
            allitems.append(self.listbox.get(i))

def convtotuple(L):
        T=[]
        for I in L:
            T.append((I[0],I[1]))
        return T
class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        buttonsframe=tk.Frame(root)
        buttonfont=tf.Font(family="Lucida Grande", size=15,weight="bold")
        b=tk.Button(buttonsframe,text="find path",font=buttonfont,command=self.findroute)
        lm=tk.Label(buttonsframe,text="MAP KEY:",font=buttonfont)
        
        self.maplist=tk.Listbox(buttonsframe,height=10,font=buttonfont)
        buttonsframe.grid(row=1, column=1, sticky="ew",pady=10,padx=50)
        bshop=tk.Button(buttonsframe,text="Create/Edit Shopping List",command=self.createshoplist,font=buttonfont)
        banalaytics=tk.Button(buttonsframe,text="Analytics",font=buttonfont,command=self.showanalytics)
        bsave=tk.Button(buttonsframe,text="SAVE",font=buttonfont,command=self.save)
        
        bshop.pack()
        b.pack(pady=5)
        banalaytics.pack()
        bsave.pack()
        lm.pack()
        self.maplist.pack()
        global size,s1,items,z,rows,columns,myFont,labels,entry,Exit,allitems,analyticlist,userage,user,usergender
        analyticlist=[]
        self.myshoppinglist=[]
        allitems=[]
        entry=[(1,1)]
        Exit=[(1,2)]
        rows = 35
        columns=35
        myFont = tf.Font(family="Lucida Grande", size=15,weight="bold")
        scale=1
        items=[("dummy")]
        labels=[]
        size=40
        
        

        z=[]
        self.item = 0; self.previous = (0, 0)
        self.canvas = tk.Canvas(self, width=1000, height=1000, background="bisque")
        self.screen = tt.TurtleScreen( self.canvas )
        self.xsb = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion = (0,0,rows*size*1.25,columns*size*1.25))
        
        self.xsb.grid(row=0, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        buttons = []
    

        #Plot some rectangles
        l=rows
        b=columns
        s1= numpy.array([[0]*l]*b)
        s1[0]=[1]*l
        s1[-1]=[1]*l
        for i in range(l):
            s1[i][0]=1
            s1[i][-1]=1
        self.load()
        for i in range(0,size*rows,size):
            
            for j in range(0,size*columns,size):
                xr=int(i/size)
                yr=int(j/size)
                t=str(xr)+" "+str(yr)
                t1=str(xr)+", "+str(yr)
                
                f=s1[int(i/size)][int(j/size)]
                if(f==0):
                    c="black"
                elif(f==1):
                    c="#CAC6C5"
                r = self.canvas.create_rectangle(i,j,i+size,j+size,fill=c,outline='grey',tag=t)
                
                
                
                #self.canvas.create_oval(i+size/2-1.5, j+size/2-1.5, i+size/2+1.5, j+size/2+1.5, fill="blue",outline="blue")
         
        for i in range(len(labels)):
            a=(labels[i][0]*size+size/1.6)
            b=(labels[i][1]*size+size/1.6)
            T0=self.canvas.create_text(a,b,fill=labels[i][3],font=myFont,text=labels[i][2],anchor="center",angle=labels[i][4])
        
            
                


        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<ButtonPress-1>", self.clickrectangle)

        self.canvas.bind("<ButtonPress-3>", self.onrightclick)
        self.canvas.bind("<Motion>", self.move_move2)
        
        

        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)
        # Hack to make zoom work on Windows
        root.bind_all("<MouseWheel>",self.zoomer)
        
    def load(self):
        
        global rows,columns,data,s1,allitems,labels,entry,Exit
        if os.path.isfile("file.json"):
        
            with open("file.json", 'r') as f:
                filedata = json.load(f)
            rows=filedata["rows"]
            columns=filedata["columns"]
            data=filedata["data"]
            s1=filedata["s1"]
            allitems=convertback(filedata["allitems"])
            labels=filedata["labels"]
            entry=convtotuple(filedata["entry"])
            Exit=convtotuple(filedata["exit"])
        else:
            self.defaultsettings
    def save(self):
        s2=s1
        if(type(s1)!=type(list())):
            s2=s1.tolist()
        l={"rows":rows,"columns":columns,"data":[],"s1":s2,"allitems":convert(allitems),"labels":labels,"entry":entry,"exit":Exit}    

        
        with open("file.json", 'w') as f:
            # indent=1 is not needed but makes the file more 
            # human-readable for more complicated data
            json.dump(l, f, indent=1) 
        
    
    def defaultsettings(self):
        
        
        rows=35
        columns=35
        a=rows
        b=columns
        s1= numpy.array([[0]*a]*b)
        s1[0]=[1]*a
        s1[-1]=[1]*a
        for i in range(a):
            s1[i][0]=1
            s1[i][-1]=1
         
           
        l={"rows":rows,"columns":columns,"data":[],"s1":s1.tolist(),"allitems":[],"labels":[],"entry":[(1,1)],"exit":[(1,2)]}    

        
        with open("file.json", 'w') as f:
            # indent=1 is not needed but makes the file more 
            # human-readable for more complicated data
            json.dump(l, f, indent=1) 

        
    def showanalytics(self):
        with open("file.json", 'r') as f:
            filedata = json.load(f)
        analyticlist1=filedata["data"]    
        t=[]
        for i in range(len(analyticlist1)):
            for j in range(len(analyticlist1[i][3])):
                t.append(analyticlist1[i][3][j])
       
       

          
        print(t)
        d = {x:t.count(x) for x in t}
    
        keys = d.keys()
        values = d.values()
        plt.clf()
        plt.bar(keys, values)
        
        
        plt.savefig('itemviews.png')
        plt.clf()
        def count_range(li, min, max):
            ctr = 0
            for x in li:
                if min <= x <= max:
                    ctr += 1
            return ctr
        t2=[]
        for i in range(len(analyticlist1)):
            t2.append(int(analyticlist1[i][2]))
        d2={str(x)+"-"+str((x+10)):count_range(t2,x,x+10) for x in range(0,100,10)}  
        keys2 = d2.keys()
        values2 = d2.values()
        plt.bar(keys2, values2)
        
        plt.savefig('age.png')
        plt.clf()
        #pie chart
        t1=[]
        for i in range(len(analyticlist1)):
            t1.append(analyticlist1[i][1])
        d1 = {x:t1.count(x) for x in t1}
        keys1 = d1.keys()
        values1 = d1.values()
        
        fig1, ax1 = plt.subplots()
        ax1.pie(values1, labels=keys1, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
      
        
        plt.savefig('gender.png')
        analyticwin=tk.Toplevel()
        image_window = tk.Toplevel()
        img1 = ImageTk.PhotoImage(Image.open("itemviews.png"))
        T1 = tk.Label(image_window,text="ITEM VIEWS")
        panel1 = tk.Label(image_window, image=img1,text="ITEM VIEWS")
        T1.grid(row=0,column=0)
        panel1.grid(row=1,column=0)
        T2 = tk.Label(image_window,text="Age GROUPS")
        img2 = ImageTk.PhotoImage(Image.open("age.png"))
        panel2 = tk.Label(image_window, image=img2)
        
        T2.grid(row=2,column=0)
        panel2.grid(row=3,column=0)
        T3 = tk.Label(image_window,text="GENDER")
        img3 = ImageTk.PhotoImage(Image.open("gender.png"))
        panel3 = tk.Label(image_window, image=img3)
        T3.grid(row=2,column=1)
        panel3.grid(row=3,column=1)
        
        image_window.mainloop()

        


        
        
    def saveanalytics(self,username,gender,age):
        
        
        #configuration
        
        #analyticlist=list(config.get("analytics","data"))
       
        #analyticaldata=
       
       
       
        
        '''
        for i in range(len(analyticlist)):
            for j in range(len( analyticlist[i][2])):
                t.append(analyticlist[i][2][j])
        '''
        #print(t)
         
        #configuration
        with open("file.json", 'r') as f:
            filedata = json.load(f)
        
        
        
        
        
        dt=[username,gender,age,self.myshoppinglist]
        filedata["data"].append(dt)   
        
       
        
        
        analyticlist1=filedata["data"]
        with open("file.json", 'w') as f:
            # indent=2 is not needed but makes the file more 
            # human-readable for more complicated data
            json.dump(filedata, f, indent=1) 
        '''
        #config.set("analytics","data",str(analyticlist))
        #with open("config.ini", "w") as file:
            #config.write(file)     
        '''
    
    def createshoplist(self):
        listofallitems=[]
        for i in range(len(allitems)):
            listofallitems.append(allitems[i].itemname)
        win = tk.Toplevel()
        self.ESL=EditShoppingList(win,listofallitems,self.myshoppinglist)
        
        win.mainloop()
        
    def findroute(self):
        global scale,rows,columns,entry,Exit,items
        self.myshoppinglist=self.ESL.finallist
        items=[("dummy"),entry[0],Exit[0]]
        
        for i in range(len(self.myshoppinglist)):
            for j in range(len(allitems)):
                if (self.myshoppinglist[i]==allitems[j].itemname):
                    p=(allitems[j].xcor,allitems[j].ycor)
                    items.append(p)
        
       
            

       
        path,fullroute = tsp(s1,items,entry[0],Exit[0])
       
                
        del path[0]
        del path[0]
        
        if(path[-1]==entry[0]):
            path.reverse()
            
        
        for i in range(len(path)-1):
            if(path[i]==Exit[0] and i!=len(path)-1):
                del(path[i])
      
        path = list(dict.fromkeys(path))      
       
        
        

       
        
        
        
        self.canvas.delete("all")
        self.canvas.grid_forget()
        self.canvas.grid(row=0, column=0, sticky="nsew")
       
        for i in range(0,size*rows,size):
            
            for j in range(0,size*columns,size):
                xr=int(math.floor(i/size))
                yr=int(math.floor(j/size))
                f=s1[int(math.floor(i/size))][int(math.floor(j/size))]
                t=str(xr)+" "+str(yr)
                
                
                if(f==0):
                    c="black"
                elif(f==1):
                    c="#CAC6C5"
                r = self.canvas.create_rectangle(i,j,i+size,j+size,fill=c,outline='grey',tag=t)
        
            
        
                
        for i in range(len(path)-1):
            key2=str([path[i],path[i+1]])
            innerroute=fullroute[key2]
            
            for k in range(len(innerroute)-1):
                x1 = (innerroute[k][0]*size)+size/2
                y1 = (innerroute[k][1]*size)+size/2
                x2 = (innerroute[k+1][0]*size) +size/2
                y2 = (innerroute[k+1][1]*size)+size/2
                self.canvas.create_line(x1,y1,x2,y2,fill="red",dash=(1,1),width=3)
            ax=path[i][0]*size
            ay=path[i][1]*size
            bx=path[i+1][0]*size
            by=path[i+1][1]*size
            self.canvas.create_oval(int(ax+size/2-3), int(ay+size/2-3), int(ax+size/2+3), int(ay+size/2+3), fill="blue",outline="white")
            self.canvas.create_oval(int(bx+size/2-3), int(by+size/2-3), int(bx+size/2+3), int(by+size/2+3), fill="blue",outline="white")
            i1=i
            i2=i+1
            if(i==0):
                T1=self.canvas.create_text(ax+size/1.6,ay+size/1.6,fill="white",font=myFont,text="ENTRY",anchor="w")
                T2=self.canvas.create_text(bx+size/1.6,by+size/1.6,fill="white",font=myFont,text="1",anchor="w")
                r1=self.canvas.create_rectangle(self.canvas.bbox(T1),fill="black")
                r2=self.canvas.create_rectangle(self.canvas.bbox(T2),fill="black")
                self.canvas.tag_lower(r1,T1)
                self.canvas.tag_lower(r2,T2)
            elif(i==len(path)-2):    
                T3=self.canvas.create_text(ax+size/1.6,ay+size/1.6,fill="white",font=myFont,text=str(i),anchor="w")
                T4=self.canvas.create_text(bx+size/1.6,by+size/1.6,fill="white",font=myFont,text="EXIT",anchor="w")
                r3=self.canvas.create_rectangle(self.canvas.bbox(T3),fill="black")
                r4=self.canvas.create_rectangle(self.canvas.bbox(T4),fill="black")
                self.canvas.tag_lower(r3,T3)
                self.canvas.tag_lower(r4,T4)
             
            elif(i!=1):
                T5=self.canvas.create_text(ax+size/1.6,ay+size/1.6,fill="white",font=myFont,text=str(i1),anchor="w")
                T6=self.canvas.create_text(bx+size/1.6,by+size/1.6,fill="white",font=myFont,text=str(i2),anchor="w")
                r5=self.canvas.create_rectangle(self.canvas.bbox(T5),fill="black")
                r6=self.canvas.create_rectangle(self.canvas.bbox(T6),fill="black")
                self.canvas.tag_lower(r5,T5)
                self.canvas.tag_lower(r6,T6)
        axe=entry[0][0]*size
        aye=entry[0][1]*size
        self.canvas.create_oval(axe+size/2-3, aye+size/2-3, axe+size/2+3, aye+size/2+3, fill="green",outline="white")
        
        '''
        for i in range(len(entry_path)-1):
            axe1=entry_path[i][0]*size+size/2
            aye1=entry_path[i][1]*size+size/2
            bxe1=entry_path[i+1][0]*size+size/2
            bye1=entry_path[i+1][1]*size+size/2
            self.canvas.create_line(axe1,aye1,bxe1,bye1,fill="green",dash=(1,1),width=3)
            
        axe=Exit[0][0]*size
        aye=Exit[0][1]*size
        self.canvas.create_oval(axe+size/2-3, aye+size/2-3, axe+size/2+3, aye+size/2+3, fill="red",outline="white")
        for i in range(len(exit_path)-1):
            axe1=exit_path[i][0]*size+size/2
            aye1=exit_path[i][1]*size+size/2
            bxe1=exit_path[i+1][0]*size+size/2
            bye1=exit_path[i+1][1]*size+size/2
            self.canvas.create_line(axe1,aye1,bxe1,bye1,fill="blue",dash=(1,1),width=3)     
        '''
        
        #for tx in labels:
            #self.canvas.create_text(tx[0]*size+size/1.6,tx[1]*size+size/1.6,fill="white",font=myFont,text=tx[2],anchor="w")    
            
        
        for i in range(len(labels)):
            a=(labels[i][0]*size+size/1.6)
            b=(labels[i][1]*size+size/1.6)
            T0=self.canvas.create_text(a,b,fill=labels[i][3],font=myFont,text=labels[i][2],anchor="center",angle=labels[i][4])
                    
        for p in z:
            self.canvas.scale("all",p[0],p[1],p[2],p[2]) 
        loc=0
        self.maplist.delete(0, tk.END)
        for i in range(len(path)):
            
            al=[]
            for k in range(len(allitems)):
                if(path[i][0]==allitems[k].xcor and path[i][1]==allitems[k].ycor and (allitems[k].itemname in self.myshoppinglist) ):
                    al.append(allitems[k].itemname)
            
            if(len(al)>0):
                loc=loc+1
                
                self.maplist.insert(tk.END,str(loc)+")"+ ','.join(al))    
   # def createshoppinglist(self,event):
        if(self.ESL.flag==1):
            now = datetime.now()
            username="me"
            
            self.saveanalytics(user,usergender,userage)
            self.ESL.flag=0 
    def clicked(self,x,y):
        J=self.entry.get()
        It=item(J,x,y)
        allitems.append(It)
        
        self.listbox.insert(tk.END,J)
        
    def delete(self,x,y):
        for i in range(len(allitems)):
            if(allitems[i].xcor==x and allitems[i].ycor==y):
                del allitems[i]
        self.listbox.delete(0, tk.END)
       
 
    def delete_selected(self):
        
        for k in range(len(allitems)):
            if(allitems[k].itemname==self.listbox.get(tk.ANCHOR)):
                
                del allitems[k]
        self.listbox.delete(tk.ANCHOR) 
        
            
    
    def additem(self,event):
        
     
    
        
        
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        r = event.widget.find_closest(xc, yc) 
        
        
        
        
        c=list(map(str, self.canvas.itemcget(r,"tag").split()))
        x=int(c[0])
        y=int(c[1])
        cord=self.canvas.coords(r)
        #print(cord)
        sz=cord[2]-cord[0]
        sz1=cord[3]-cord[1]
        
        #print(sz,sz1)
        ax=x*sz
        ay=y*sz
        res=size/sz
        ov=self.canvas.create_oval(cord[0]+sz/1.7, cord[1]+sz/1.7, cord[2]-sz/1.7, cord[3]-sz/1.7, fill="blue",outline="white")
         
        self.master = tk.Toplevel()
        self.master.title("Add an item here")
        self.master.geometry("400x400")
        self.listbox = tk.Listbox(self.master)
        for i in range(len(allitems)):
            if(allitems[i].xcor==x and allitems[i].ycor==y):
                self.listbox.insert(tk.END,allitems[i].itemname)
                
        
        
        self.entry = tk.Entry(self.master )
        self.entry.pack()
        self.button0 = tk.Button(self.master, text="Add Item", command=lambda a=x,b=y:self.clicked(a,b))
        self.button0.pack()
        self.button_delete = tk.Button(self.master,text="Delete", command=lambda a=x,b=y:self.delete(a,b))
        self.button_delete.pack()
        self.button_delete_selected = tk.Button(self.master,text="Delete Selected", command=self.delete_selected)
        
        self.button_delete_selected.pack()
        self.listbox.pack()
        self.master.mainloop() 
        return(0)
    def addlabel(self,event,a,b):    
        global labels
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        r = event.widget.find_closest(xc, yc) 
        
        
        
        c=list(map(str, self.canvas.itemcget(r,"tag").split()))
        x=int(c[0])
        y=int(c[1])
        
        if(self.var0.get()==1):
            ang=0
        else:
            ang=90
        if(self.varc.get()==1):
            col="black"
        elif(self.varc.get()==2):
            col="blue"
        elif(self.varc.get()==3):
            col="white"
        else:
            col="red"
            
        if(str(self.en.get())!=""):
            T0=self.canvas.create_text(a,b,fill=col,font=myFont,text=str(self.en.get()),anchor="center",angle=ang)
            labels.append((x,y,self.en.get(),col,ang))
            #r0=self.canvas.create_rectangle(self.canvas.bbox(T0),fill="black")
        #self.canvas.tag_lower(r0,T0)
    def changelabel(self,event):
        
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        labelwindow=tk.Toplevel()
        labelwindow.title("Your shopping list")
        labelwindow.geometry("400x400")
        self.en=tk.Entry(labelwindow)
        
        self.var0 = tk.IntVar()
        self.varc = tk.IntVar()
        but=tk.Button(labelwindow,text="ok",command=lambda e=event,a=xc,b=yc: self.addlabel(e,a,b))
        lab=tk.Label(labelwindow,text="Select orintation")
        ra1=tk.Radiobutton(labelwindow,text="horizontal",variable=self.var0,value=1)
        ra2=tk.Radiobutton(labelwindow,text="vertical",variable=self.var0,value=2)
        labc=tk.Label(labelwindow,text="Select colour")
        self.en.pack()
        ra3=tk.Radiobutton(labelwindow,text="Black",variable=self.varc,value=1)
        ra4=tk.Radiobutton(labelwindow,text="Blue",variable=self.varc,value=2)
        ra5=tk.Radiobutton(labelwindow,text="white",variable=self.varc,value=3)
        ra6=tk.Radiobutton(labelwindow,text="Red",variable=self.varc,value=4)
        lab.pack()
        ra1.pack()
        ra2.pack()
        labc.pack()
        ra3.pack()
        ra4.pack()
        ra5.pack()
        ra6.pack()
        but.pack()
        
        labelwindow.mainloop()
        
        
    def onrightclick(self,event):
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        r = event.widget.find_closest(xc, yc) 
        
        
        cord=self.canvas.coords(r)
        sz=cord[2]-cord[0]
        menuedit = tk.Menu(root, tearoff=0)
        
        menuedit.add_command(label="Add/Edit item",command=lambda:self.additem(event))
        menuedit.add_command(label="Add/Edit Label",command=lambda:self.changelabel(event))
       

        menuedit.add_command(label="set as entry",command=lambda:self.setentry(event))
        menuedit.add_command(label="set as exit",command=lambda:self.setexit(event))
       

        
        menuedit.post(x=int(event.x),y=int(event.y))
        
        
    def setentry(self,event):
        global entry,labels
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        r = event.widget.find_closest(xc, yc) 
        c=list(map(str, self.canvas.itemcget(r,"tag").split()))
        x=int(c[0])
        y=int(c[1])
        entry[0]=(x,y)
        cord=self.canvas.coords(r)
        #print(cord)
        sz=cord[2]-cord[0]
        sz1=cord[3]-cord[1]
        J="entry"
        
        self.canvas.create_text(cord[0]+sz/1.6,cord[1]+sz/1.6,fill="white",font=myFont,text=J,anchor="w")
        
        #print(sz,sz1)
        ax=x*sz
        ay=y*sz
        res=size/sz
        ov=self.canvas.create_oval(cord[0]+sz/1.7, cord[1]+sz/1.7, cord[2]-sz/1.7, cord[3]-sz/1.7, fill="Green",outline="white")
        items.append(entry[0])
    def setexit(self,event):
        global Exit,labels
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        r = event.widget.find_closest(xc, yc) 
        c=list(map(str, self.canvas.itemcget(r,"tag").split()))
        x=int(c[0])
        y=int(c[1])
        Exit[0]=(x,y)
        cord=self.canvas.coords(r)
        #print(cord)
        sz=cord[2]-cord[0]
        sz1=cord[3]-cord[1]
        J="exit"
        
        self.canvas.create_text(cord[0]+sz/1.6,cord[1]+sz/1.6,fill="white",font=myFont,text=J,anchor="w")
        
        #print(sz,sz1)
        ax=x*sz
        ay=y*sz
        res=size/sz
        ov=self.canvas.create_oval(cord[0]+sz/1.7, cord[1]+sz/1.7, cord[2]-sz/1.7, cord[3]-sz/1.7, fill="red",outline="white")
        items.append(Exit[0])
    def clickrectangle(self,event):
        
        
        xc = self.canvas.canvasx(event.x); 
        yc = self.canvas.canvasy(event.y)
        r = event.widget.find_closest(xc, yc)[0]
        c1=list(map(str, self.canvas.itemcget(r,"tag").split()))
        x=int(c1[0])
        y=int(c1[1])
        
        
            
        
        if(self.canvas.itemcget(r,"fill")=="black"):
            self.canvas.itemconfig( r,fill="#CAC6C5")
            
            s1[x][y]=1
            
            
        elif(self.canvas.itemcget(r,"fill")=="#CAC6C5"):
            self.canvas.itemconfig( r,fill="black")
            
            s1[x][y]=0
    def unzoom(self):
        global scale 
        x0 = self.canvas.canvasx(0) 
        y0 = self.canvas.canvasy(0)
        self.canvas.scale("all", x0, y0, 1/scale, 1/scale)
        
    #move
    
    def move_start(self, event):
        
        
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #move
    def pressed2(self, event):
        global pressed
        pressed = not pressed
        self.canvas.scan_mark(event.x, event.y)
    def move_move2(self, event):
        if pressed:   
            self.canvas.scan_dragto(event.x, event.y, gain=1)        

    #windows zoom
    def zoomer(self,event):
        global scale,z,myFont
        xc = self.canvas.canvasx(event.x)
        yc = self.canvas.canvasy(event.y)
        if (event.delta > 0):
            self.canvas.scale("all", xc, yc, 1.1, 1.1)
            z.append((xc,yc,1.1))
            fontsize = myFont['size']
            if(fontsize<=30): 
                myFont.configure(size=fontsize+1)
             
            
        elif (event.delta < 0):
            
            self.canvas.scale("all", xc,yc, 0.9, 0.9)
            z.append((xc,yc,0.9))
            fontsize = myFont['size']
            if(fontsize>=15): 
                myFont.configure(size=fontsize-1)
            
       
    #linux zoom
    def zoomerP(self,event):
        xc = self.canvas.canvasx(event.x)
        yc = self.canvas.canvasy(event.y)
        self.canvas.scale("all", xc, yc, 1.1, 1.1)
        
    def zoomerM(self,event):
        xc = self.canvas.canvasx(event.x)
        yc = self.canvas.canvasy(event.y)
        self.canvas.scale("all", xc, yc, 0.9, 0.9)
        


root = tk.Tk()
root.title("OneClick Indoor Store Navigation")
root.geometry("500x500") 



#=======================================VARIABLES=====================================
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()
GENDER = tk.StringVar()
AGE = tk.StringVar()

#=======================================METHODS=======================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member1.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, gender TEXT, age TEXT)")


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


def LoginForm():
    global LoginFrame, lbl_result1,userFrame
    userFrame.destroy()
    LoginFrame = tk.Frame(root)
    LoginFrame.pack(side=tk.TOP, pady=80)
    lbl_username = tk.Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = tk.Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = tk.Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = tk.Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = tk.Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = tk.Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = tk.Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=tk.W)
    lbl_register.bind('<Button-1>', ToggleToRegister)
    

def RegisterForm():
    global RegisterFrame, lbl_result2
    
    RegisterFrame = tk.Frame(root)
    RegisterFrame.pack(side=tk.TOP, pady=40)
    lbl_username = tk.Label(RegisterFrame, text="Username:", bd=18)
    lbl_username.grid(row=1)
    lbl_password = tk.Label(RegisterFrame, text="Password:", bd=18)
    lbl_password.grid(row=2)
    lbl_gender = tk.Label(RegisterFrame, text="Gender:", bd=18)
    lbl_gender.grid(row=3)
    lbl_age = tk.Label(RegisterFrame, text="Age:", bd=18)
    lbl_age.grid(row=4)
    lbl_result2 = tk.Label(RegisterFrame, text="" )
    lbl_result2.grid(row=5, columnspan=2)
    username = tk.Entry(RegisterFrame, textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = tk.Entry(RegisterFrame, textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    gender = tk.Entry(RegisterFrame, textvariable=GENDER, width=15)
    gender.grid(row=3, column=1)
    age = tk.Entry(RegisterFrame, textvariable=AGE, width=15)
    age.grid(row=4, column=1)
    btn_login = tk.Button(RegisterFrame, text="Register", width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = tk.Label(RegisterFrame, text="Login", fg="Blue")
    lbl_login.grid(row=0, sticky=tk.W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()
def chooseuser(event=None):
    global userFrame 
    userFrame = tk.Frame(root)
    userFrame.pack(side=tk.TOP, pady=150)
    b1=tk.Button(userFrame,text="Store Manager Login",command=LoginForm)
    #b2=tk.Button(userFrame,text="Store Manager Login")
    b1.pack()    
    #b2.pack(pady=10)
    
def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or GENDER.get() == "" or AGE.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, gender, age) VALUES(?, ?, ?, ?)", (str(USERNAME.get()), str(PASSWORD.get()), str(GENDER.get()), str(AGE.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            GENDER.set("")
            AGE.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()
def Login():
    Database()
    global userage,usergender,user
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
            cursor.execute("SELECT gender FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
            for record in cursor:
                usergender=('{0}'.format(record[0]))
            cursor.execute("SELECT age FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
            for record in cursor:
                userage=('{0}'.format(record[0]))
            user=USERNAME.get()
           
            
            LoginFrame.destroy()
            E=Example(root)
            E.grid( row=1,column=0)
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
#LoginForm()

#========================================MENUBAR WIDGETS==================================
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)



   

        
if __name__ == "__main__":
    #root = tk.Tk()
    chooseuser()
    #E=Example(root)
    
    
    #E.grid( row=1,column=0)
    
    
    #f.pack(fill="both", expand=True)

    root.mainloop()