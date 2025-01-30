# service

Release ready:

- python -m http.server 81 (ensure http://localhost:81/cart_trolley_checkout.html)
- run_server_orig.py (Ensure reply)
- service.py         
- mimic_reply.cmd    (Instead of payment success)

Outputs to:
- c_purchase_monitor.log
- tile_events.json  (procrun)
- line_events.json
- reply_events.json

Baseline:
- get_tile (working)
- get_lines (working)
- get_reply (working)
- send_data (todo)

What works: 
- delete both c_purchase_monitor.log & reply_events.json
- python.exe -m http.server 81
- python.exe run_server_orig.py (in a seperate shell)
- python.exe service.py remove (when applicable)
- python.exe service.py install
- python.exe service.py start (check running with services.msc)
- mimic_reply.cmd
