import tkinter as tk

class AddressWindow:


 def __init__(self):
  self.frame = tk.Tk()
  self.frame.title("Addresses")
  self.frame.geometry('400x200')
  self.input = tk.Text(self.frame, height = 5, width = 20)
  self.input.pack()
  
  self.list = tk.Listbox(self.frame, name = 'listbox')
  self.list.insert(1, 'One')
  self.list.insert(2, 'Two')
  self.list.insert(3, 'Three')
  self.list.pack()
  self.list.bind('<<ListboxSelect>>', self.on_select)
  
  self.button = tk.Button(self.frame, text = "Print", command = self.print_input)
  self.button.pack()
  self.label = tk.Label(self.frame, text = "")
  self.label.pack()
  self.frame.mainloop()

  
 def print_input(self):
  text = self.input.get(1.0, "end-1c")
  self.label.config(text = "Provided Input: " + text)

  
 def on_select(self, event):
  w = event.widget
  index = int(w.curselection()[0])
  value = w.get(index)
  print('You selected item {}: "{}"'.format(index, value))


def main():
 AddressWindow()

 
if __name__ == '__main__':
 main()
