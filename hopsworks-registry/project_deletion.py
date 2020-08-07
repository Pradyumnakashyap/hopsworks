#!/usr/bin/python

try:
    import sys
    import requests
    import json

except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import sys
    import requests
    import json

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
			project_id =  int(resp_str[24:35].split(',', 1)[0][0])
			repo_count =  int(resp_str[298:308].split(',', 1)[0])
			return project_id, repo_count
		else:
			print(r'Project with name {} does not exists!'.format(project_name))
			sys.exit(1)
        	
	except IOError:
		print('Please verify the name of the Harbor registry passed as argument or check if the certificate required to access the Harbor Registry is located in path: "/etc/docker/certs.d/<registryip>/"!')
		sys.exit(1)
	#except:
	#	print('Please verify the registry credentials!')
def delete_repo(project_name):

        repo_name="conda-image"
        resp = requests.delete(r'https://{}/api/v2.0/projects/{}/repositories/{}'.format(harbor_host,project_name,repo_name),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        if resp.status_code != 200:
                print('Error deleting the repository with status code /api/projects {}'.format(resp.status_code))
                return 0
        return 1

def delete_project(project_name):

        try:
		repo_flag = 1
        	project_id, repo_count = get_project_id(project_name)
	      	if repo_count > 0:
                	repo_flag = delete_repo(project_name)
        	if repo_flag :
                	resp = requests.delete(r'https://{}/api/v2.0/projects/{}'.format(harbor_host,project_id),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
                	if resp.status_code != 200:
                        	print('Error deleting project with status code {}'.format(resp.status_code))
                        	sys.exit(1)
                #print('Project successfully deleted')
       	 	else:
                	print('Error deleting project {}'.format(project_name))
	except ValueError as e:
      		print (r'Project with the name {} does not exist!'.format(project_name))
	except:
		print('Project deletion unsuccessful!')

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        if len(sys.argv)<5:
                print("Fatal: Please include the required arguments for the script!")
                sys.exit(1)
	harbor_host= str(sys.argv[1])
	user = str(sys.argv[2])
        password= str(sys.argv[3])
        project_name=str(sys.argv[4])
        delete_project(project_name)

