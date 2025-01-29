def notify_host():
    cstring = None
    area_ip = get_ip("A")  # same as send_data, service.py
    host_ip = get_ip("B")  # sql + fork daemon

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((str(host_ip), 8910)) # chosen
    #
    #opt cstring = cstring + str(area_ip) + str(ino) + str(desc) + str(qty) + str(hrs) + str(val)
    cstring = '1100	51231	2022	AA	0,00	30.06.2021	05.07.2021	REF: 2633107	05.07.2021' + area_ip
  
  try:
        sock.send(ctring.encode())
    except socket.error:
        pass
    finally:
        sock.close()

