import sparkmessages
import settings
import apicem
import host
import device
import path
import servicenow
import template

#spark = sparkmessages.Message()
#message = spark.get_message('Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTUxOGQ3MzAtZmNlZC0xMWU1LWIxOGUtODM1ZmRhNjExN2U5')
#print message

def select_test(project_data):
    testinfo = {}
    num = 0
    print('List of Chaos test: ')
    print project_data
    for i in project_data['templates']:
        num += 1
        #print i
        #testinfo = testinfo.append({str(num): i['id']})
        print('{}. {}'.format(str(num), i['name']))

    testnum = input('Please choose your favorite Chaos test: ')
    testnum = testnum - 1
    count = 0

    for i in project_data['templates']:
        if testnum == count:
            test_id = i['id']
        count = count + 1

    #print(testinfo[name])
    print(test_id)
    #return testinfo[testnum]
    return test_id

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
device_id = apic.get_random_device_id_host()
print device_id

'''
print "******\nAll device name"
print apic.list_all_devices()
print "******\nresolve device name"
print apic.resolve_device_name('floor-rtr.domain.net')
print "******\nRandom Device ID and Hostname"
print apic.get_random_device_id_host()
'''
'''
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
'''


templates1 = {'composite': False,
  'containingTemplates': [],
  'description': '',
  'deviceTypes': [{'productFamily': 'Switches and Hubs'},
                  {'productFamily': 'Routers'}],
  'name': 'Device_Reload_Test',
  'projectId': 'ed14efb5-f68d-4f86-b7b2-818978fde6a3',
  'projectName': 'test',
  'softwareType': 'IOS-XE',
  'softwareVariant': 'XE',
  'templateContent': 'copy run flash://pre-chaos-test_reload.cfg\n'
                     'reload\n'
                     'no\n',
  'templateParams': []
    }

templates2 = {'composite': False,
 'containingTemplates': [],
 'description': '',
 'deviceTypes': [{'productFamily': 'Switches and Hubs'},
                 {'productFamily': 'Routers'}],
 'name': 'CPU_Spike_Test',
 'projectId': 'ed14efb5-f68d-4f86-b7b2-818978fde6a3',
 'projectName': 'Chaos_Project',
 'softwareType': 'IOS-XE',
 'softwareVariant': 'XE',
 'templateContent': 'copy run flash://pre-chaos-test_reload.cfg\n'
                    'show tech\n',
 'templateParams': []
  }

apict = template.Template()
print apict.get_project('ChaosMonkey')
project_data = apict.get_project('ChaosMonkey')


if not project_data:
    print('Creating Project and Templates ...')
    project_name = 'ChaosMonkey'
    apict.create_project(project_name)
    project_data = get_project(project_name)
    create_template(project_data['projectID'], templates1)
    create_template(project_data['projectID'], templates2)
else:
    print('Project {}, already Exist!'.format(project_data['projectName']))
    print('Associated templates: ')
    for i in project_data['templates']:
        print(i['name'])

test_id = select_test(project_data)
template_id = apict.get_template_id(test_id)

print 'Test ID = ' + test_id
print  device_id
apict.deploy_chaos_test(template_id, device_id)

#apict.create_project('Edders')