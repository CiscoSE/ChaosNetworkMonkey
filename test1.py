import sparkmessages
import settings
import apicem
import host
import device
import path
import servicenow

#spark = sparkmessages.Message()
#message = spark.get_message('Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTUxOGQ3MzAtZmNlZC0xMWU1LWIxOGUtODM1ZmRhNjExN2U5')
#print message

"""
room_id = settings.roomId
person_id = settings.apic_person_id
person_email = settings.apic_person_email
text = 'Hello World'
response = spark.post_message(person_id, person_email, room_id, text)
print response


apic = host.Host()
apic_url = 'https://10.52.208.57/api/v1/host'
apic_response = apic.get_api(apic_url)
apic_response2 = apic.get_all_hosts()
print apic_response
print apic_response2
"""
print "******\n"
print "DNAC API Test Framework"
print "******\n"
apic = device.Device()
print "******\nAll device name"
print apic.list_all_devices()
print "******\nresolve device name"
print apic.resolve_device_name('floor-rtr.domain.net')
print "******\nRandom Device ID and Hostname"
print apic.get_random_device_id_host()


print "\n******\nresolve device id \n"
print apic.resolve_device_id('3a909883-948f-47c2-8e34-65a740ab423e')

print "\n******\nget Heal all \n"
print apic.get_health_all()


"""
print "\n******\nget check locations \n"
print apic.get_devices_location('china')
del apic
"""

apich = host.Host()

print "******\nConnected host"
print apich.get_connected_host('floor-rtr.domain.net')
print "******\nConnected host individual"
print apich.get_individual_host('bob')
del apich


apicp = path.Path()
print "******\nTracing Path"
print apicp.path_trace('GET PATH alice bob')


#print "\n ******\n raising case"
#servicenow.raise_case("raise alan@example.com 3 networking issues")