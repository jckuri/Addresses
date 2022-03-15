import tkinter as tk
import requests

class AddressWindow:


 def __init__(self):
  self.frame = tk.Tk()
  self.frame.title("Addresses")
  self.center_window()
  
  self.label = tk.Label(self.frame, text = "Where are you located?\nSo, we know where to drop off the stuff")
  self.label.pack()
  
  sv = tk.StringVar()
  sv.trace("w", lambda name, index, mode, sv = sv: self.entry_modified(sv))
  self.input = tk.Entry(self.frame, textvariable = sv)
  self.input.pack()
  
  self.list = tk.Listbox(self.frame, name = 'listbox')
  self.list.insert(1, 'One')
  self.list.insert(2, 'Two')
  self.list.insert(3, 'Three')
  self.list.pack()
  self.list.bind('<<ListboxSelect>>', self.on_select)
  
  self.frame.mainloop()

 
 def center_window(self):
  self.frame.resizable(False, False)
  window_width = 500
  window_height = 300
  screen_width = self.frame.winfo_screenwidth()
  screen_height = self.frame.winfo_screenheight()
  x_cordinate = int((screen_width - window_width) / 2)
  y_cordinate = int((screen_height - window_height) / 2)
  self.frame.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

  
 def on_select(self, event):
  widget = event.widget
  index = int(widget.curselection()[0])
  value = widget.get(index)
  print('You selected item {}: "{}"'.format(index, value))
  
 
 def entry_modified(self, sv):
  text = sv.get()
  self.label.config(text = "Modified entry: " + text)


def main():
 AddressWindow()

 
if __name__ == '__main__':
 main()
