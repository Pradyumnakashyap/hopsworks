#!/usr/bin/python



try:
    import sys
    import requests
    import json

except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import requests
    import json	
    import sys

def get_project_id(project_name):

        try:	
		resp = requests.head(r'https://{}/api/v2.0/projects?project_name={}'.format(harbor_host,project_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
		if resp.status_code == 200:
			resp = requests.get(r'https://{}/api/v2.0/projects?name={}'.format(harbor_host,project_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        		if resp.status_code != 200:
                    		print(r'Error fetching project with name "{}"  /api/projects {}'.format(project_name,resp.status_code))
				sys.exit(1)
        		resp_dump = json.dumps(resp.text)
        		resp_str = json.loads(resp_dump)
			return [resp_str[24:35].split(',', 1)[0]]
		else:
			print(r'Project with name {} does not exists!'.format(project_name))
			sys.exit(1)
        	
	except IOError:
		print('Please verify the name of the Harbor registry passed as argument or check if the certificate required to access the Harbor Registry is located in path: "/etc/docker/certs.d/<registryip>/"!')
		sys.exit(1)
	except:
		print('Please verify the registry credentials!')
		sys.exit(1)

def get_member_id(project_id,user_name):
	try:
		resp = requests.get(r'https://{}/api/v2.0/projects/{}/members?entityname={}'.format(harbor_host,project_id,user_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        	if resp.status_code != 200:
        		print('Member is not linked to the project  with name "{}"'.format(user_name,resp.status_code))
			sys.exit(1)
        	resp_dump = json.dumps(resp.text)
        	resp_str = json.loads(resp_dump)
        	return [resp_str[16:22].split(',', 1)[0]]
	except:
		print('Error fetching member in the project  with name "{}"'.format(user_name,resp.status_code))
		sys.exit(1)

def delete_member(project_name,user_name):

        try:
		project_detail = get_project_id(project_name)
		project_id = int(project_detail[0])
		member_detail = get_member_id(project_id,user_name)
		member_id = int(member_detail[0])
        	if member_id > 0:
               		resp = requests.delete(r'https://{}/api/v2.0/projects/{}/members/{}'.format(harbor_host,project_id,member_id),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
               		if resp.status_code != 200:
               			print('Error deleting member from project ! POST error with status code {}'.format(resp.status_code))
				sys.exit(1)
        #print(r'{} Member successfully deleted'.format(user_name))
	except:
		print('Error deleting member from project, please verify if the member is linked to the project!')
                sys.exit(1)

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
	if len(sys.argv)<6:
        	print("Fatal: Please include the required arguments for the script!")
                sys.exit(1)
	harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
        project_name = str(sys.argv[4])
	user_name = str(sys.argv[5])
        delete_member(project_name,user_name)
