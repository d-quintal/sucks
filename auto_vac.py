from sucks import *
from time import localtime, strftime

def printHeader():
    print()
    print('TIME     VAC       BTY  CHARGER   FAN     MAIN   SIDE   FILTER ')
    print('======== ========= ==== ========= ======= ====== ====== ====== ')

def printStatus():

    try:
        vac = vacbot.vacuum_status.ljust(10)
    except:
        vac = ''.ljust(11)

    try:
        charge = vacbot.charge_status.ljust(10)
    except:
        charge = ''.ljust(10)

    try:
        bty = "{:.0%}".format(vacbot.battery_status).rjust(4) + ' '
    except:
        bty = ''.ljust(5)

    try:
        fan = vacbot.fan_speed.ljust(8)
    except:
        fan = ''.ljust(8)

    try:
        main = vacbot.components['main_brush'].ljust(7)
        side = vacbot.components['side_brush'].ljust(7)
        filter = vacbot.components['filter'].ljust(7)
    except:
        main = ''.ljust(7)
        side = ''.ljust(7)
        filter = ''.ljust(7)

    time_formatted = strftime('%X', localtime()).ljust(9)

    print(time_formatted + vac + bty + charge + fan + main + side + filter)

def clean_exit(err=0):
    print()
    print('Disconnecting...', end='')
    vacbot.disconnect()
    print(' completed.')
    print()
    exit(err)

def run_clean():
    if vacbot.vacuum_status != 'auto':
        try:
            vacbot.run(Clean())
        except:
            pass
    time.sleep(5)
    printStatus()

def run_edge_seek():

    try:
        vacbot.run(Edge())
    except:
        pass

    for i in range(1, 60):
        time.sleep(5)
        printStatus()

    try:
        vacbot.run(Charge())
    except:
        pass

    for i in range(1, 24):
        time.sleep(5)
        printStatus()

def run_charge():
    if vacbot.vacuum_status != 'charging' or 'returning':
        try:
            vacbot.run(Charge())
        except:
            pass
    time.sleep(5)
    printStatus()


''' log in '''

password_hash = '04e6e3eda0e4988398fa76bf2263b57d'
    # password_hash = hashlib.md5(bytes(str('password'), 'utf8')).hexdigest()
device_id = EcoVacsAPI.md5(str(time.time()))
email = 'ecovacs@quintal.org'
country_code = 'us'
continent_code = 'na'

print()
print('Logging in to EcoVacs...')
api = EcoVacsAPI(device_id, email, password_hash, country_code, continent_code)
vacuum = api.devices()[0]
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, vacuum, continent_code, monitor=True)

print('Connecting to vacuum...')
vacbot.connect_and_wait_until_ready()


''' loop through clean/charge cycles '''


while 1 == 1:

    printHeader()

    while vacbot.battery_status is None or vacbot.battery_status < .99:
        run_charge()

    printHeader()

    while vacbot.battery_status >= .5:
        run_clean()

    printHeader()

    while vacbot.charge_status != 'charging':
        run_edge_seek()

clean_exit()

'''
Stats!
=================

E R TIME  BTY
= = ===== ===
2 2 17:35 17%
1 1 OVER
3 1 OVER


















'''
