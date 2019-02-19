import settings
import apicem
import command
import json
import pprint

apic =command.Command()
task_id = apic.post_command()
print task_id
file_id =  apic.check_task_status(task_id)
print file_id
output = apic.get_file(file_id)
print '\n\n'
#print json.dumps(output, separators=(',',':'))

pp = pprint.PrettyPrinter(depth=6)
pp.pprint(output)