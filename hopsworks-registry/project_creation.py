#!/usr/bin/python

try:
    import requests
    import sys
except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import requests
    import sys

def create_project(project_name):
        try: 
		create_project = {
  "count_limit": -1,
  "project_name": project_name,
  "storage_limit": -1
  
}

        	resp = requests.post(r'https://{}/api/v2.0/projects'.format(harbor_host), json=create_project,verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        	if resp.status_code != 201:
                	print('Error creating project ! POST error with status code /api/projects {}'.format(resp.status_code))
                	sys.exit(1)
        #print(r'{} project successfully created'.format(project_name))
	except IOError:
		print('Please verify the name of the Harbor registry passed as argument or check if the certificate required to access the Harbor Registry is located in path: "/etc/docker/certs.d/<registryip>/"! ')
		sys.exit(1)
	except:
		print('Please verify the registry credentials!')
		sys.exit(1)
		
if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        if len(sys.argv)<5:
                print("Fatal: Please include the required arguments for the script!")
                sys.exit(1)
	harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
        project_name = str(sys.argv[4])
        create_project(project_name)
       	 

