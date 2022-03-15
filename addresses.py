import tkinter as tk
import requests
import threading
import time


def read_allowed_zips():
 f = open('allowed_zips.txt', 'r')
 lines = f.readlines() 
 f.close()
 lines2 = []
 for line in lines:
  lines2.append(line.strip())
 return lines2


class GoogleAPI:


 def __init__(self):
  self.read_api_key()
  
  
 def read_api_key(self):
  api_file = open('api-key.txt', 'r')
  self.api_key = api_file.read()
  api_file.close()
  
  
 def call_autocomplete(self, input_text):
  url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&key={}".format(input_text, self.api_key)
  payload={}
  headers = {}
  response = requests.request("GET", url, headers = headers, data = payload)
  return response.json()
  
 def call_place_details(self, place_id):
  url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}".format(place_id, self.api_key)
  payload={}
  headers = {}
  response = requests.request("GET", url, headers = headers, data = payload)
  return response.json()


class AddressWindow:

 def __init__(self):
  self.allowed_zips = read_allowed_zips()
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
  self.list.pack()
  self.list.bind('<<ListboxSelect>>', self.on_select)
  
  self.label2 = tk.Label(self.frame, text = "Your saved addresses:")
  self.label2.pack()
  
  self.list2 = tk.Listbox(self.frame, name = 'listbox2')
  self.list2.pack()
  self.list2.bind('<<ListboxSelect>>', self.on_select2)
  
  self.maps = GoogleAPI()

  self.thread = threading.Thread(target = self.counter_thread)
  self.thread.start()

  self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
  self.frame.mainloop()
  
 
 def on_closing(self):
  self.stop_thread = True
  self.frame.destroy()
  
  
 def center_window(self):
  self.frame.resizable(False, False)
  window_width = 400
  window_height = 200
  screen_width = self.frame.winfo_screenwidth()
  screen_height = self.frame.winfo_screenheight()
  x_cordinate = int((screen_width - window_width) / 2)
  y_cordinate = int((screen_height - window_height) / 2)
  self.frame.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

  
 def on_select(self, event):
  widget = event.widget
  if len(widget.curselection()) == 0: return
  index = int(widget.curselection()[0])
  value = widget.get(index)
  place_id = self.predictions[index]['place_id']
  json = self.maps.call_place_details(place_id)
  components = json['result']['address_components']
  postal_code = None
  for component in components:
   if component['types'][0] == 'postal_code':
    postal_code = component['short_name']
    #postal_code = component['long_name']    
  allowed_zip = postal_code in self.allowed_zips
  allowed_string = 'ALLOWED' if allowed_zip else 'NOT ALLOWED'
  print('postal_code={} ({})'.format(postal_code, allowed_string))
  
  
 def on_select2(self, event):
  widget = event.widget
  if len(widget.curselection()) == 0: return
  index = int(widget.curselection()[0])
  value = widget.get(index)
  print('index={}, value={}'.format(index, value))
  
 
 def entry_modified(self, sv):
  self.input_text = sv.get()
  self.last_modification = time.time()
  self.count_time = True
  
 
 def counter_thread(self):
  self.last_modification = time.time()
  self.count_time = False
  self.stop_thread = False
  while not self.stop_thread:
   time.sleep(0.1)
   if self.count_time:
    dt = time.time() - self.last_modification
    if dt > 3:
     self.count_time = False
     self.call_google_maps()
     
 def call_google_maps(self):
  self.list.delete(0, tk.END)  
  json = self.maps.call_autocomplete(self.input_text)
  self.predictions = json['predictions']
  n = len(self.predictions)
  for i in range(n):
   prediction = self.predictions[i]
   self.list.insert(i, prediction['description'])


def main():
 AddressWindow()

 
if __name__ == '__main__':
 main()
