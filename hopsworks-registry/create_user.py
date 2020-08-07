#!/usr/bin/python

try:
    import requests
    import sys
except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import requests
    import sys
    

def create_user(user_name,user_password,email):
	try: 
		user_details = {
  "username": user_name,
  "realname": user_name,
  "password": user_password,
  "email": email
}

		resp = requests.post(r'https://{}/api/v2.0/users'.format(harbor_host), json=user_details,verify=r'/etc/docker/certs.d/{}/ca.crt'.format(harbor_host),auth=(user,password),headers={'Content-Type':'application/json'})
        	if resp.status_code != 201:
                	print('Error creating a user in Harbor ! POST error with status code {}'.format(resp.status_code))
                	sys.exit(1)
        #print(r'{} created user successfully'.format(user_name))
	except IOError:
		print('Please verify the name of the Harbor registry passed as argument or check if the certificate required to access the Harbor Registry is located in path: "/etc/docker/certs.d/<registryip>/"!')
		sys.exit(1)
	except:
		print('Please verify the registry credentials!')
		sys.exit(1)
if __name__ == '__main__':

        #Inputs to be obtained from Hopsworks
        if len(sys.argv)<7:
                print("Fatal: Please include the required arguments for the script!")
                sys.exit(1)
	harbor_host= str(sys.argv[1])
        user= str(sys.argv[2])
        password= str(sys.argv[3])
	user_name = str(sys.argv[4])
	user_password = str(sys.argv[5])
	email = str(sys.argv[6])
        create_user(user_name,user_password,email)
