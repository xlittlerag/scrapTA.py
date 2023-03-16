import requests
import json
import time

FECHA="17/03/2023"
HORARIOS=["01:22", "06:03", "14:02", "20:00", "XX:XX", "XX:XX"]

def check_availables():
    availables = []

    url = "https://webventas.sofse.gob.ar/ajax/servicio/obtener_servicios.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': 'G_ENABLED_IDPS=google; PHPSESSID=ped5qsk0ehv8d1kj5vuh0lps53'
    }
    params = {"fecha_seleccionada": FECHA, "sentido": 1}
    resp = requests.post(url, headers=headers, data=params)

    servicios = json.loads(resp.text)["servicios"]

    i = 0
    for s in servicios:
        for _s in servicios[s]["servicios"].values():
           pullman = _s["web"]["400"]["disponibilidad"]
           primera = _s["web"]["500"]["disponibilidad"]

           availables.append((pullman, primera))
        i += 1


    with open("service.log", "a") as f:
        i = 0
        for d in availables:
            f.write("[% s] Pull: % s, Pri: % s\n" % (HORARIOS[i], d[0], d[1]))
            i+=1
        f.write("================\n")

while(True):
    check_availables()
    time.sleep(30)
