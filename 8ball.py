import random

class Ball():
    def __init__(self, pytanie=0):
        self.pytanie = pytanie

    def convo(self):
        self.pytanie = input("\nWhat is it you seek?\n")
        response = ['\nYes\n', '\nNo\n', '\nPlease try agian later.\n']
        print(random.choice(response))

def ask():
    ball8 = Ball()
    while True:
        start = input("\nWould you like to ask me a question?\n\tPlease enter 'yes' or 'no':  \n")
        if start.lower() == 'yes':
            ball8.convo()
        elif start.lower() == 'no':
            break
        else:
            print('I do not understand')

ask()
