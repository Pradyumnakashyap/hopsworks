#!/usr/bin/python

try:
    import docker
    import sys
    import subprocess
    import datetime
    import requests

except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker
    import sys
    import subprocess
    import datetime
    import requests

def run_command(command):
    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        raise Exception('Error: Exited with error code: {}. Output:{}'.format(e.returncode, e.output))

def docker_login(harbor_host, user, password):
        try:
		command = ["sudo", "docker", "login", harbor_host, "-u", user, "-p", password]
        	run_command(command)
	except:
		print('Docker daemon is not able login to the Harbor Registry, please verify the hostname, username and password !') 
		sys.exit(1)
def docker_image_tag(image, tag):
        try: 
		command = ["sudo", "docker", "tag", image , tag]
        	run_command(command)
        except:
		print('Docker image not found on local machine, please provide a valid image name in the format "dockerimage:tag"!')
		sys.exit(1)
def add_dockerImage(image,project_name):

        try:
		resp = requests.get(r'https://{}/api/v2.0/projects?project_name={}'.format(harbor_host,project_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        	if resp.status_code != 200:
    			print('Docker image not added to the repository, Please verify if the project exists in Harbor and re-try!')
			sys.exit(1)
		client = docker.from_env()
        	cli = docker.APIClient(base_url='unix://var/run/docker.sock')
        	for line in cli.push(image, stream=True, decode=True):
			line              
		command = ["sudo", "docker", "rmi", tag]
        	run_command(command) 					#Delete local image upon push
		#print("Image added successfully")
	except:
		print('Docker image not added to the repository, Please verify if the project exists in Harbor and re-try!')
		sys.exit(1)

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        if len(sys.argv)<6:
                print("Fatal: Please include the required arguments for the script!")
                sys.exit(1)
	harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
	project_name= str(sys.argv[4])
        docker_image = str(sys.argv[5])
	now = datetime.datetime.now()
	dt_string = now.strftime("%d%m%Y%H%M")
        tag = r'{}/{}/{}:{}'.format(harbor_host, project_name, 'conda-image',dt_string)
        docker_login(harbor_host, user, password)
        docker_image_tag(docker_image,tag)
        add_dockerImage(tag,project_name)
 
        
       	 

