# https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import logging, queue

logger = logging.getLogger(__name__)

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

class Console(tk.Frame):
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.text = tk.Text(self, state='disabled')
        vertical_scroll_bar = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=vertical_scroll_bar.set)
        vertical_scroll_bar.pack(side="right", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.tag_config('INFO', foreground='black')
        self.text.tag_config('DEBUG', foreground='gray')
        self.text.tag_config('WARNING', foreground='orange')
        self.text.tag_config('ERROR', foreground='red')
        self.text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logging.getLogger('').addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.text.configure(state='normal')
        self.text.insert(tk.END, msg + '\n', record.levelname)
        self.text.configure(state='disabled')
        # Autoscroll to the bottom
        self.text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.after(100, self.poll_log_queue)
