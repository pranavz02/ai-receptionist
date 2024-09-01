import inquirer
import time
import random
import threading
import sys
from pyfiglet import figlet_format
from termcolor import colored
from ai_receptionist.db import query_emergency_db, close_db

class Spinner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.spinner = ['|', '/', '-', '\\']
        self.index = 0

    def run(self):
        while self.running:
            sys.stdout.write(f'\r{self.spinner[self.index]}')
            sys.stdout.flush()
            time.sleep(0.1)
            self.index = (self.index + 1) % len(self.spinner)

    def stop(self):
        self.running = False
        sys.stdout.write('\rDone!        \n')
        sys.stdout.flush()

class Receptionist:
    def __init__(self):
        self.user_location = None
        self.pending_emergency_response = None
        self.is_emergency = False

    def start(self):
        self.show_welcome_message()
        while True:
            self.check_for_emergency_or_message()

    def show_welcome_message(self):
        welcome_text = "Welcome to Dr. Adrin's AI Receptionist"
        ascii_art = figlet_format(welcome_text)
        print(colored(ascii_art, 'cyan'))

    def check_for_emergency_or_message(self):
        questions = [
            inquirer.List(
                'choice',
                message="Is this an emergency or would you like to leave a message?",
                choices=['Emergency', 'Leave a message', 'Exit'],
            ),
        ]
        answers = inquirer.prompt(questions)

        if answers['choice'] == 'Emergency':
            self.is_emergency = True
            self.handle_emergency()
        elif answers['choice'] == 'Leave a message':
            self.handle_message()
        elif answers['choice'] == 'Exit':
            self.display_message("Thank you for using the AI receptionist. Goodbye!", 'green')
            close_db()
            exit()  # Exit the program

    def handle_emergency(self):
        emergency_description = inquirer.text(message="Please describe the emergency:")
        self.display_message("I am checking what you should do immediately. Meanwhile, can you tell me which area you are located in right now?", 'cyan')
        self.user_location = inquirer.text(message="Location:")
        
        # Start the background thread for querying the database
        query_thread = threading.Thread(target=self.query_emergency_db, args=(emergency_description,))
        query_thread.start()
        
        # Start the spinner
        spinner = Spinner()
        spinner.start()

        eta = self.estimate_arrival_time()
        self.display_message(f"Dr. Adrin will be coming to your location immediately. Estimated time of arrival: {eta} minutes.", 'cyan')
        
        if eta > 10:
            self.display_message("I understand that you are worried that Dr. Adrin will arrive too late.", 'yellow')
            if self.pending_emergency_response:
                self.display_message(f"Meanwhile, we suggest you: {self.pending_emergency_response}", 'red')
            else:
                self.display_message("Please hold just a sec...", 'yellow')
                query_thread.join()
                if self.pending_emergency_response:
                    self.display_message(self.pending_emergency_response, 'red')
        else:
            self.display_message("Please hold just a sec...", 'yellow')
            query_thread.join()
            if self.pending_emergency_response:
                self.display_message(self.pending_emergency_response, 'red')
        
        spinner.stop()
        self.display_message("Don't worry, please follow these steps, Dr. Adrin will be with you shortly.", 'green')

    def handle_message(self):
        message = inquirer.text(message="Please leave your message:")
        self.display_message("Thanks for the message, we will forward it to Dr. Adrin.", 'green')

    def query_emergency_db(self, emergency_description):
        """Query the emergency database in a separate thread."""
        time.sleep(15)
        self.pending_emergency_response = query_emergency_db(emergency_description)

    def estimate_arrival_time(self):
        return random.randint(5, 15)

    def display_message(self, message, color='cyan'):
        """Display a colored message."""
        print(colored(message, color))