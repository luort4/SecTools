from Ops.Dejavoo import PD
from Ops.Dejavoo import Spin
from Ops.Dejavoo import Steam
from Ops.NMI import nmi_fm
from Ops.NMI import PD_nmi
from Ops.Swipe import PD_SS
from Ops.Swipe import Stax_SS
from Ops.Mxconnect import MxCon
import os

def ask_user():
    user_input = input('''
Which Platform do the users need access to? Enter a number from the list below, press q to quit:
    1.) Dejavoo
    2.) NMI
    3.) Swipe
    4.) MxConnect\n
number:''')
    if user_input == "1":
        PD.main()
        Spin.main()
        Steam.main()
    elif user_input == "2":
        nmi_fm.main()
        PD_nmi.main()
    elif user_input == "3":
        PD_SS.main()
        Stax_SS.main()
    elif user_input == "4":
        MxCon.main()
    else:
        print("Good Bye")
        exit()

    loop = input("\nBegin again for another account? Y/n: \n")

    if loop == "Y" or loop == "":
        ask_user()
    else:
        pass

def main():
    print(os.listdir())
    ask_user()

    # removes any stored copy information.
    os.system("rm temp/*")

main()
