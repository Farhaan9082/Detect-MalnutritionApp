from tkinter import *
from tkinter.ttk import Combobox
import sqlite3

window= Tk()
window.title("NutriDec")

conn = sqlite3.connect('Malnutrition_book.db')

c = conn.cursor()

'''
c.execute("""CREATE TABLE malnutrition (
        gender text,
        age integer,
        feet integer,
        inches integer,
        kg integer,
        weightloss integer,
        accute text
        )""")
'''

gender=StringVar()
age=IntVar()
feet=IntVar()
inches=IntVar()
kg=IntVar()
Weightloss=IntVar()
accute=StringVar()
score=0
bmi_round=0.00
percentage=0

label_1= Label(window, text="1.What is the gender of your child?", font="ArialBlack 12 bold").grid(row=0,column=0,columnspan=3)

v=["Male","Female"]
Mycombo=Combobox(window, values=v,textvariable=gender).grid(row=1,column=0,columnspan=3)
acc=["Yes","No"]

label_2= Label(window, text="2.What is the age of your child?", font="ArialBlack 12 bold").grid(row=3,column=0,columnspan=3)

label_3= Label(window, text="Age").grid(row=4,column=0,columnspan=2)
spin1= Spinbox(window, from_=0, to=20, width=6,textvariable=age).grid(row=4,column=1)

label_5= Label(window, text="3.How tall is your child?", font="ArialBlack 12 bold").grid(row=6,column=0,columnspan=3)
label_6= Label(window, text="Feet").grid(row=7,column=0,columnspan=2)
entry_1= Entry(window, width=8, borderwidth=2, textvariable=feet).grid(row=7,column=1)
label_7= Label(window, text="Inches").grid(row=8,column=0,columnspan=2)
entry_2= Entry(window, width=8, borderwidth=2, textvariable=inches).grid(row=8,column=1)
label_8= Label(window, text="4.How much does your child weigh?", font="ArialBlack 12 bold").grid(row=9,column=0,columnspan=3)
label_9= Label(window, text="Kg").grid(row=10,column=0,columnspan=2)
entry_3= Entry(window, width=11, borderwidth=2, textvariable=kg).grid(row=10,column=1)

label_10= Label(window, text="5.Unplanned weight loss in past 3-6 months", font="ArialBlack 12 bold").grid(row=11,column=0,columnspan=3)
entry_4= Entry(window, width=11, borderwidth=2, textvariable=Weightloss).grid(row=12,column=1)

label_11= Label(window, text="6.If child has been accutely ill and there has been no intake of nutrition for >5 days", font="ArialBlack 12 bold").grid(row=13,column=0,columnspan=3)
Mycombo1=Combobox(window, values=acc,textvariable=accute).grid(row=14,column=0,columnspan=3)

def submit():
    global score
    global bmi_round
    global percentage
    conn = sqlite3.connect('Malnutrition_book.db')

    c = conn.cursor()

    c.execute("INSERT INTO malnutrition VALUES (:gender, :age, :feet, :inches, :kg, :weightloss, :accute)",
            {
                'gender': gender.get(),
                'age': age.get(),
                'feet': feet.get(),
                'inches': inches.get(),
                'kg': kg.get(),
                'weightloss': Weightloss.get(),
                'accute': accute.get()
            })

    conn.commit()

    conn.close()

    height_meter=(feet.get()*0.3048)+(inches.get()*0.0254)
    bmi=((kg.get())/(height_meter*height_meter))
    bmi_round=round(bmi,2)
    print("your bmi is",bmi_round)

    if bmi_round>20:
        score=0
    elif bmi_round>=18.5:
        score=1
    else:
        score=2

    percentage=(Weightloss.get()/kg.get())*100
    print("Your weight loss is",percentage,"percent")

    if percentage>10:
        score=score+2
    elif percentage>5:
        score=score+1
    else:
        score=score+0
    
    if accute.get()=='Yes':
        score=score+2
    else:
        score=score+0

    print("Your score is",score)


def report():
    
    window2=Toplevel(window)
    window2.title("Report")
    window2.geometry("350x350")
    label_main=Label(window2, text="*Health Report*", font="ArialBlack 12 bold").grid(row=0,column=0,columnspan=3)
    label_w1=Label(window2, text=("Your BMI is",bmi_round)).grid(row=1,column=0,columnspan=3)
    label_w2=Label(window2, text=("Your weight loss is",percentage,"percent")).grid(row=2,column=0,columnspan=3)
    label_w3=Label(window2, text=("Your health score is",score)).grid(row=3,column=0,columnspan=3)
    
    if score>=2:
        label_w4=Label(window2, text="High Risk Of MALNUTRITION", font="ArialBlack 12 bold").grid(row=4,column=0,columnspan=3)
        label_w8=Label(window2, text="TIPS:\n1.Go and check your nearest Doctor immediately.\n2.Contact with Health and Care services.", font="ArialBlack 12 ").grid(row=5,column=0,columnspan=3)
    elif score==1:
        label_w5=Label(window2, text="Medium Risk Of MALNUTRITION", font="ArialBlack 12 bold").grid(row=4,column=0,columnspan=3)
        label_w7=Label(window2, text="TIPS:\n1.Have a healthier and more balanced diet.\n2.Having drinks that contains lots of calories.", font="ArialBlack 12 ").grid(row=5,column=0,columnspan=3)
    else:
        label_w6=Label(window2, text="Low Risk Of MALNUTRITION", font="ArialBlack 12 bold").grid(row=4,column=0,columnspan=3)

btn3= Button(window, text="Submit", width=15, command=submit).grid(row=15,column=0,columnspan=3)
btn4= Button(window, text="Check Report", width=15, command=report).grid(row=16,column=0,columnspan=3)

conn.commit()

conn.close()

window.mainloop()
