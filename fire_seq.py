#fireing sequence


import json
import os
os.chdir("%USERPROFILE%\\Desktop\\service")

sequence = []
sequence.append("1") #get_tile
sequence.append("2") #get_lines
sequence.append("3") #ret_reply
sequence.append("4") #send_data

def write_get_reply():
    # Data to be written
    dictionary = {
        "error_code": "",
        "status": "SUCCESS",
        "message": ""
    }
 
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    
    # Writing to sample.json
    with open("reply_events.json", "w") as outfile:
        outfile.write(json_object)

write_get_reply()
