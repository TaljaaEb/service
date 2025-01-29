# service

Release ready:

- run_server_orig.py (Ensure reply)
- service.py         
- mimic_reply.cmd    (Instead of payment success)

Outputs to:
- c_purchase_monitor.log
- reply_events.json

Baseline:
- get_tile (todo)
- get_lines (todo)
- get_reply (working)
- send_data (todo)

What works: 
- delete both c_purchase_monitor.log & reply_events.json
- python.exe run_server_orig.py (in a seperate shell)
- python.exe service.py remove (when applicable)
- python.exe service.py install
- python.exe service.py start (check running with services.msc)
- mimic_reply.cmd
