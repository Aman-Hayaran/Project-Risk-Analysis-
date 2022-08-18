#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import random


# In[2]:


def prob_cost_ana():
    print("\n\n")
    a = int(input("How many work packages : "))
    wp,lp,mlp,hp = [],[],[],[]


    for i in range (0,a):
        str1 = input(f"Enter the work package name {i+1}: ")
        wp.append(str1)
        str2 = int(input(f"Enter the lowest price of work package {i+1}: "))
        lp.append(str2)
        str3 = int(input(f"Enter the most likely price of work package {i+1}: "))
        mlp.append(str3)
        str4 = int(input(f"Enter the high price of work package {i+1}: "))
        hp.append(str4)
        print("\n")

    tp=0
    for i in range(0,a):
        tp=tp+mlp[i]


    mid_pt1, mid_pt2, ta_1, ta_2, prob1, prob2 = [],[],[],[],[],[]
    for i in range(0,a):
        mid_pt1.append((lp[i]+mlp[i])/2)
        mid_pt2.append((mlp[i]+hp[i])/2)
        ta_1.append((mlp[i]-lp[i])/2)
        ta_2.append((hp[i]-mlp[i])/2)
        prob1.append(ta_1[i]/(ta_1[i]+ta_2[i]))
        prob2.append(ta_2[i]/(ta_1[i]+ta_2[i]))


    #CREATING DICTIONARY
    mp={}
    prob={}
    for i in range(0,a):
        mp[wp[i]]=[mid_pt1[i],mid_pt2[i]]
        prob[wp[i]]=[prob1[i],prob2[i]]


    #COMBINATIONS
    wplist=[]
    a9=[]
    l=len(wp)
    for i in wp:
        a9.extend([i+'1',i+'2'])
    wplist=np.array(a9).reshape(len(wp),2).tolist()

    
    mplist, problist = [],[]
    for i in range(0,a):
        mplist.append(mp[wp[i]])
        problist.append(prob[wp[i]])

    acomb = [p for p in itertools.product(*wplist)]
    mlcomb = [p for p in itertools.product(*mplist)]
    plcomb = [p for p in itertools.product(*problist)]



    #ADDING COMBINATIONS VALUES
    mcompl=[]
    pcompl=[]
    for i in range(0,len(mlcomb)):
        kl=mlcomb[i]
        sum=0
        for j in range(0,len(kl)):
            sum=sum+kl[j]
        mcompl.append(sum)
    for i in range(0,len(plcomb)):
        ll=plcomb[i]
        mul=1
        for j in range(0,len(ll)):
            mul=mul*ll[j]
        pcompl.append(mul)




    #COMBINED PROBABILITY
    temp1=0
    temp2=0
    for i in range(0, len(mcompl)):
        for j in range(i+1, len(mcompl)):
            if(mcompl[i] > mcompl[j]):
                temp1 = mcompl[i]
                mcompl[i] = mcompl[j]
                mcompl[j] = temp1
                temp2 = pcompl[i]
                pcompl[i] = pcompl[j]
                pcompl[j] = temp2


    # In[9]:


    table=pd.DataFrame(list(zip(wp,lp,mlp,hp)), columns=['Work Package','Lowest (Optimistic) Price','Most Likely Price','High (Pessimistic) Price'])
    print("\n\n",table.to_string(index=False))
    
    dfdata=pd.DataFrame(list(zip(acomb,mcompl,pcompl)), columns=['Combination of Work Package Zones','Cost based on Mid Point','Probability of Occurence'])
    print("\n\n",dfdata.to_string(index=False))

    
    

    # In[11]:


    #FREQUENCY DISTRIBUTION
    df=pd.DataFrame(list(zip(mcompl,pcompl)), columns=['Project Cost','Joint Prob'])
    df1=df.groupby(['Project Cost']).sum().reset_index()
    df4=pd.crosstab(index=df['Project Cost'], columns='Frequency').reset_index()
    f=df4['Frequency'].values.tolist()
    x=df1['Project Cost'].values.tolist()
    y=df1['Joint Prob'].values.tolist()
    z=[]
    qw=0
    for i in range(0,len(y)):
        qw=qw+y[i]
        z.append(qw)
    df2=pd.DataFrame(list(zip(x,f,y,z)), columns=['Project Cost','Frequency of Occurrence','Joint Probabilities','Cummulative Probability'])
    print("\n\n",df2.to_string(index=False))
    
    for i in range(0,len(z)):
        if tp>=x[i] and tp<=x[i+1]:
            cfi=z[i]+(((z[i+1]-z[i])/(x[i+1]-x[i]))*(tp-x[i]))

    print("\nConfidence level at Taget Price = ",(cfi*100))
    conf=int(input("\n\nEnter the confidence level of contractor in % : "))
    confi=conf/100
        
    maxi=y[0]
    maxipos=0
    for i in range(1,len(y)):
        if y[i]>maxi:
            maxi=y[i]
            maxipos=i
    mlp=x[maxipos]
    for i in range(0,len(z)):
        if confi>=z[i] and confi<=z[i+1]:
            bp=x[i]+(((x[i+1]-x[i])/(z[i+1]-z[i]))*(confi-z[i]))

    
    print("\nBid Price will be = ",bp)


    # In[12]:


    prof=int(input("\nEnter profit for the contractor in %: "))
    prof1=prof/100
    bpwp=bp+(prof1*bp)
    print("\nProfit = ",(prof1*bp))
    print("\nFinal Bid Price with Profit = ",bpwp)


    # In[14]:


    #PLOT GRAPH
    plt.style.use('default')
    plt.plot(x,z, marker='o')
    plt.hlines(y=cfi,xmin=x[0],xmax=tp, color = 'g', linestyles='--', label='Target Price')
    plt.vlines(x=tp,ymin=0,ymax=cfi, color='g', linestyles='--')
    plt.hlines(y=confi,xmin=x[0],xmax=bp, color = 'r', linestyles='--', label='Bid Price')
    plt.vlines(x=bp,ymin=0,ymax=confi, color='r', linestyles='--')

    plt.vlines(x=bpwp, ymin=0, ymax=1.0, color='y', linestyles='--', label='Bid Price with Profit')
    plt.xlabel('Cost in thousands $')
    plt.ylabel('Cummulative Probability')
    plt.title('Cummulative Probability Profile')
    plt.legend()
    plt.show()


    return " ---------------------------"


# In[3]:


def contingency_fund_allo():
    #  values such as no of workpackages, all cost , confidence limit ,project completion done for each work package taken from user
    #
    a = int(input("Number of workpackages\t "))
    _con = float(input("Confidence limit of the work( in %):\t"))
    profit = float(input("What is the profit percentage you want to add(in %) =\t"))
    cri = float(input("criticality percentage(sugggested value is 0.5%) = \t"))
    list_WP = []
    list_opt_price = []
    list_most_likely_price = []
    list_pes_price = []
    prob_underrun = []
    criti_lis = []
    proj_comp = []
    for i in range(a):
        ch = 0
        while ch== 0 :
            print(f"Name of work package{i + 1} :\t")
            b = input()
            c = float(input(f"Optimistic Price for work package {i + 1}\t"))
            e = float(input(f"Most likely Price for work package {i + 1}\t"))
            d = float(input(f"pessimistic Price for work package {i + 1}\t"))
            f = float(input(f"Probability of **underrun for work package*(in %) {i + 1}\t"))
            g = float(input(f"enter the  **cummulative percentage of project completion{i + 1}*(in percentage)\t"))
            if (c <= e and e <= d):
                proj_comp.append(g)
                list_WP.append(b)
                list_opt_price.append(c)
                list_most_likely_price.append(e)
                list_pes_price.append(d)
                prob_underrun.append(f)
                ch =1
            else:
                print("mostlikely value should be more than optimistic price")
                

    #  Target price
    Target_Price = sum(list_most_likely_price)

    # Applying Criticality Rule :cri% to check
    cri_ = (cri* Target_Price) / 100

    # Overrun and underrun costs calculated , criticality checked
    over_run = []
    underrun = []
    for i in range(a):
        a1 = list_most_likely_price[i] - list_opt_price[i]
        over_run.append(a1)
        b1 = list_pes_price[i] - list_most_likely_price[i]
        underrun.append(b1)
        if ((a1 > cri_) or (b1 > cri_)):
            criti_lis.append('Y')
        else:
            criti_lis.append("N")

    #  A table or data frame of required values  made and shown
    arr = []
    for i in np.arange(0, a):
        arr.append([list_WP[i], list_opt_price[i], list_most_likely_price[i], list_pes_price[i], prob_underrun[i], criti_lis[i],proj_comp[i]])

    df = pd.DataFrame(arr, columns=['Work_Package', 'Low Price', 'Most likely P.', 'High Price', 'Prob_of_underrun','Criticality', 'Project_Completion'])
    print("Entered Values :\n")
    print(df)

    #   100000 monte carlo simulations are done ,slabs  are decided on the basis of probability of
    #  underrun as givn by user. total cost for each simulation is calculated and added in a list (10000 values)
    #centroid of triangular distribution is taken
    val = []
    for i in range(100000):

        cos_t = 0
        for lis in arr:
            ran = random.random()
            if lis[5] == 'Y':
                if (ran >= lis[4]):
                    cos_t = cos_t + (lis[2]+2/3*(lis[3]-lis[2]))
                else:
                    cos_t = cos_t + (lis[3]+1/3*(lis[4]-lis[3]))
            elif lis[5] == 'N':
                cos_t = cos_t + lis[2]
        val.append(cos_t)

    #  dictionary with name 'total_cost_freq' made in which key is total cost and number of occurance in all simulations
    total_cost_freq = dict((i, val.count(i)) for i in val)
    cost_freq = dict(sorted(total_cost_freq.items()))
    # print("dictionary of total value and frequency=\t",cost_freq)
    # pd.DataFrame(MyList, columns=["x"]).groupby('x').size().to_dict()
    print("Cost",'\t', "Frequency")
    for i ,j in cost_freq.items():
        print(i ,'\t' ,j)

    # Cummulative probability has been calculated for each number of total cost
    z = sum(cost_freq.values())
    # print("number of simulations=",z)
    s = list(cost_freq.values())
    # print("frequency of all values =",s)
    s1 = []
    for i, j in enumerate(s):
        if i == 0:
            s1.append(j)
        else:
            k = j + s1[i - 1]
            s1.append(k)
    s2 = []
    for i, j in enumerate(s1):
        k1 = j / z
        s2.append(k1)

    # print("cummulative probability=",s2)


    # Now we are going to Plot the graph between cummulative prob. on x axis and total cost on y axis

    key_ = list(cost_freq.keys())
    plt.plot(key_, s2)  # key_ = total costs and s2 = cummulative probability
    plt.scatter(key_, s2)
    plt.xlabel('Cost')
    # # naming the y axis
    plt.ylabel('Cummulative probability')
    # # giving a title to my graph
    plt.title('Cummulative probability vs Cost Curve')
    plt.grid()
    plt.legend()
    # # function to show the plot
    plt.show()

    # Printing target price , cummulative probability corresponing to it
    target_confidence = (np.interp(Target_Price, key_, s2)) * 100
    print("\n\nTarget_price =", Target_Price)
    print("\n\nCummulative Probability Corresponding to Target price", target_confidence, "%")

    # Bid price  =  “confidence‐limit” price of work packages(in code the variable is bid price (pardon me)) + profit
    # Bid price=target price + contingency fund + profit
    bid_price = np.interp((_con/100), s2, key_)
    print("\n\nConfidence limit Price =", bid_price)
    print("\n\nBid Price for Total project is \t =", bid_price + Target_Price * (profit / 100))

    # Contingency fund = confidence‐limit price− target price


    conti_fun = bid_price - Target_Price
    print("\n\nContingency fund =", conti_fun)

    #  Adding columns (underrun cost,overrun cost , contingency fund allocated ,its use etc) required for draw down curve

    df1 = df.drop(['Criticality'], axis='columns')
    df1["Over run"] = underrun
    df1["Underrun Cost"] = over_run
    df1["prob_Over_run"] = df1["Prob_of_underrun"].apply(lambda x: float(1 - x))
    df1["(O_run-U_run)"] = (df1['Over run'] * df1["prob_Over_run"]) - (df1['Underrun Cost'] * df1['Prob_of_underrun'])


    def zero(a):
        ''' This function checks that if (overrun - underrun) is negative or not '''
        if a < 0:
            return 0
        else:
            return a


    df1["(O_run-U_run)"] = df1["(O_run-U_run)"].apply(zero)



    df1["Allocation"] = (df1["(O_run-U_run)"] / sum(df1["(O_run-U_run)"]))



    df1["Contingency_Fund_Allocation"] = df1["Allocation"] * conti_fun

    def contingency_remaining_funds(list1):
        ''' this function takes Contingency funds allocated and returns a list of the remaining funds  '''
        k1 = []
        k1.append(conti_fun)
        a = conti_fun
        for j in list1:
            a = a - j
            if a < 0: a = 0
            k1.append(a)
        return k1


    list2 = list(df1["Contingency_Fund_Allocation"].copy())
    Cont_Remain_f = contingency_remaining_funds(list2)
    proj_comp_remain = list(df1["Project_Completion"].copy())
    proj_comp_remain.insert(0, 0)
    print("Contingency Fund Allocation Table")
    print(df1)

    # In[5]:


    # At last the graphical representation of utilization of contingency funds is shown against the project completion
    plt.plot(proj_comp_remain, Cont_Remain_f)
    plt.scatter(proj_comp_remain, Cont_Remain_f)
    plt.xlabel("Completion in % ")
    plt.ylabel('Cont_Fund_Alloc_')
    plt.title("Draw Down Curve")
    plt.legend()
    plt.grid()
    plt.show()

    return  None


# In[4]:


def payoff_mat():

    n = int(input("Enter no. of decision alternatives: "))
    m = int(input("Enter state of nature: "))
    x = []
    for i in range(0, n):
        y = []
        print(f"Enter all state of nature for decision{i + 1} : ")
        for j in range(0, m):
            y.append(int(input()))
        x.append(y)

        # In[121]:

    def myMax(list1):
        max = list1[0]
        for x in list1:
            if x > max:
                max = x
        return max

    def myMin(list1):
        min = list1[0]
        for x in list1:
            if x < min:
                min = x
        return min

    # In[120]:


    # maximin

    a = []
    for i in range(0, n):
        a.append(min(x[i]))



    maximin = myMax(a)
    print("Maximin = ", maximin)

    # In[122]:


    # maximax
    b = []
    for i in range(0, n):
        b.append(myMax(x[i]))
    maximax = myMax(b)
    print("Maximax = ", maximax)


    # minimax regret
    p = []
    for i in range(0, m):
        q = []
        for j in range(0, n):
            q.append(x[j][i])
        p.append(q)

    # In[125]:


    mat = []
    for i in range(0, len(p)):
        col = []
        ma = myMax(p[i])
        for j in range(0, len(p[i])):
            col.append(ma - p[i][j])
        mat.append(col)


    row = []
    for i in range(0, n):
        r1 = []
        for j in range(0, m):
            r1.append(mat[j][i])
        row.append(r1)


    mat1 = []
    for i in range(0, n):
        m2 = myMax(row[i])
        mat1.append(m2)

    # In[128]:


    minreg = myMin(mat1)
    print("Minimax Regret= ", minreg)

    # In[129]:


    # expected monetary value
    prob = []
    for i in range(0, m):
        n3 = int(input(f"Enter probability of state of nature {i + 1} in % = "))
        prob.append(n3 / 100)

    # In[130]:


    em1 = []
    for i in range(0, len(x)):
        emv1 = 0
        for j in range(0, len(x[0])):
            k1 = x[i][j]
            emv1 = emv1 + (k1 * prob[j])
        em1.append(emv1)
    for i in range(0, len(em1)):
        print(f"EMV for decision {i + 1} = ", em1[i])
    return " ---------------------------"


# In[ ]:


if __name__ == '__main__':
    print("\n\n\t\t\tWELCOME")
    print("\t\t-----------------------\n")
    print("\tThis is a Decision Making Program for Bidders")
    print("\t---------------------------------------------\n")
    print("What do you want to access ?")
    cont = 'Y'
    while (cont == 'Y' or cont == 'y'):
        try:
            choice = int(input("Press 1 for Probabilistic cost analysis\nPress 2 for Contingency Analysis and Allocation\nPress 3 for Payoff Matrix\n"))

            if(choice==1):
                prob_cost_ana()
            elif choice== 2:
                contingency_fund_allo()
            elif choice ==3:
                payoff_mat()
        except :
            print("please enter a valid number :")

        cont = input("Do you want to continue.\n If yes press Y or y if not press n or N")

