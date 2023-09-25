import spacy
from datetime import datetime, timedelta
import time
import pygame
import threading
import queue

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

message_queue = queue.Queue()

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("/media/amey/New Volume/pythonproject/file_example_MP3_700KB.wav")
    pygame.mixer.music.play()
    time.sleep(10)  # Let the music play for 10 seconds
    pygame.mixer.music.stop()  # Stop the music after 10 seconds

def handle_alarm(task):
    doc = nlp(task)
    now = datetime.now()
    
    # Extracting time and setting an alarm
    for ent in doc.ents:
        if ent.label_ == 'TIME':
            task_time = ent.text
            if 'hour' in task_time or 'hr' in task_time:
                delta = int(task_time.split()[0])
                alarm_time = now + timedelta(hours=delta)
            elif 'minute' in task_time or 'min' in task_time:
                delta = int(task_time.split()[0])
                alarm_time = now + timedelta(minutes=delta)
            elif 'second' in task_time or 'sec' in task_time:
                delta = int(task_time.split()[0])
                alarm_time = now + timedelta(seconds=delta)
            else:
                message_queue.put("Time format not recognized.")
                return

            while datetime.now() < alarm_time:
                time.sleep(5)  # Check every 5 seconds to reduce the waiting time

            message_queue.put(f"ALARM: Time to {task}")
            threading.Thread(target=play_sound).start()  # Play sound in a separate thread
            return

    message_queue.put("Couldn't find a time in the task.")

if __name__ == "__main__":
    num_tasks = int(input("How many tasks do you want to schedule?\n"))
    
    for _ in range(num_tasks):
        task = input("What task do you want to schedule? (e.g., 'Wash dishes in 1 hour')\n")
        
        # Start a new thread for each task's alarm process
        alarm_thread = threading.Thread(target=handle_alarm, args=(task,))
        alarm_thread.start()
        
        # Display messages from the queue
        while not message_queue.empty():
            print(message_queue.get())
