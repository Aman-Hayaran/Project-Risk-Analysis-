#c:\Users\HP\OneDrive\Desktop\payoff final.py
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 10:19:36 2022

@author: prashant
"""

from tkinter import *
import numpy as np

root = Tk()
root.title("PayOff Matrix")
root.geometry("900x900")



    
    



def number():
    

    
    x=int(e.get())
    y=int(e3.get())
    l=Label(root, text = "Enter Decision Alternatives\n(E.g. D1,D2)")
    l.grid(row=5,column=0)
    l=Label(root, text = "Enter States of Nature\n")
    l.grid(row=5,column=1, columnspan=y)
    x1=[]

    def payoff():
        te1=Label(root,text="Results:",font=("Courier",25))
        te1.grid(sticky='w')
        x2=[]
        for i in x1:
            c=i.get()
            x2.append(c)
        arr1=np.array(x2)
        arr_2d = np.reshape(arr1, (x, (y+1)))
        a3=arr_2d.transpose()
        a4=np.delete(a3,0,0)
        a5=a4.transpose()
        a6=a5.astype(int)
        maximin=[]
        for i in range(0,x):
            min=np.min(a6[i])
            maximin.append(min)
            maxi1=np.array(maximin)
        maxiv=np.max(maxi1)
    
             
            
        p1=Label(root, text="Maximin = "+str(maxiv))
        p1.grid()
        
        maximax=[]
        for i in range(0,x):
            max=np.max(a6[i])
            maximax.append(max)
        maxix=np.array(maximax)
        maxixv=np.max(maxix)
        
        p2=Label(root, text="Maximax = "+str(maxixv))
        p2.grid()

        a7=a6.transpose()
        mat = []
        for i in range(0, len(a7)):
            col = []
            xi=np.max(a7[i])
            for j in range(0, len(a7[i])):
                col.append(xi-a7[i][j])
            mat.append(col)
        mat1=np.array(mat)
        mat2=mat1.transpose()
        
        mr=[]
        for i in range(0,len(mat2[0])):
            max3=np.max(mat2[i])
            mr.append(max3)
        mr2=np.array(mr)
        mrv=np.min(mr2)
        p3=Label(root, text="Minimax Regret = "+str(mrv)+"\n")
        p3.grid()
        
        #expected monatory value
        prob1=[]
        
        def emv():
            prob2=[]
            for i in prob1:
                c2=int(i.get())
                prob2.append(c2)
            prob3=np.array(prob2)
            prob4=prob3.astype(int)
            
            em1 = []
            for i in range(0, len(a6)):
                emv1 = 0
                for j in range(0, len(a6[0])):
                    k1 = a6[i][j]
                    emv1 = emv1 + (k1 * (prob3[j]/100))
                em1.append(emv1)
            for i in range(0, len(em1)):
                p5=Label(root, text="EMV for Decision "+str(i+1)+" = "+str(em1[i]))
                p5.grid()
                


        
        p4=Label(root, text="Enter Probabilities of states of nature in %")
        p4.grid(sticky='w')
        for i in range(0,y):
            pr=Entry(root)
            pr.grid()
            prob1.append(pr)
        b2=Button(root, text="Submit", command=emv)
        b2.grid()
            

    for i in range(0,x):
        
        for j in range(0,y+1):
            c=Entry(root)
            c.grid(row=i+7, column =j)
            x1.append(c)
        #x1.append(x2)
    
    b=Button(root, text="Submit", command=payoff)
    b.grid(columnspan=y+1)
    
    l1=Label(root,text='')
    l1.grid()
    
    

k1=Label(root, text="WELCOME TO OUR DECISION MAKING TOOL")
k1.grid(row=0, columnspan=3)
l=Label(root, text = "PayOff Matrix Analysis", font=("Phosphate",50))
l.grid(row=1, columnspan=3, pady=30,padx=50)


e1=Label(root, text = "Enter no. of Decision alternatives")
e1.grid(row=2, sticky='e')
e = Entry(root)
e.grid(row=2,column=1)

e2=Label(root, text = "Enter no. of States of nature")
e2.grid(row=3,sticky='e')
e3 = Entry(root)
e3.grid(row=3,column=1)

b=Button(root, text="Submit", command=number)
b.grid(row=4,column = 1,pady=10)


    


root.mainloop()