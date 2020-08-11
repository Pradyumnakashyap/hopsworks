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

def get_user_id(user_name):

        try:
		resp = requests.get(r'https://{}/api/v2.0/users?username={}'.format(harbor_host,user_name),verify='/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password))
        	if resp.status_code != 200:
                	print('Error fetching username "{}" from Harbor with status code {}'.format(user_name,resp.status_code))
			sys.exit(1)
        	resp_dump = json.dumps(resp.text)
        	resp_str = json.loads(resp_dump)
        	return [resp_str[21:24].split(',', 1)]
	except IOError:
		print('Please verify the name of the Harbor registry passed as argument or check if the certificate required to access the Harbor Registry is located in path: "/etc/docker/certs.d/<registryip>/"!')
		sys.exit(1)
	except:
		print('Please verify the registry credentials!')
		sys.exit(1)
		
def delete_user(user_name):

        try:
		user_detail = get_user_id(user_name)
		user_id = int(user_detail[0][0])
        	if user_id > 2:
                	resp = requests.delete(r'https://{}/api/v2.0/users/{}'.format(harbor_host,user_id),verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
                	if resp.status_code != 200:
                        	print('Error deleting user with status code'.format(resp.status_code))
                        	sys.exit(1)
                #print('User successfully deleted')
      	except ValueError as e:
      		print (r'User with the name {} does not exist!'.format(user_name))
		sys.exit(1)
	except:
		print('User deletion unsuccessfull!')
		sys.exit(1)

if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        if len(sys.argv)<5:
                print("Fatal: Please include the required arguments for the script!")
                sys.exit(1)
	harbor_host= str(sys.argv[1])
	user = str(sys.argv[2])
        password= str(sys.argv[3])
        user_name=str(sys.argv[4])
        delete_user(user_name)
	
