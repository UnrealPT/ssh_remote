import datetime
import json
import paramiko


def create_logfile(name, txt):
    """Writes data into a datestamped .txt file (will append if file already exists). E.g: 2020-04-20_Filename.txt
      
    Parameters:
      name(str): name of the file to be created
      txt: data to be written / appended to the file """
    
    dateStamp = datetime.datetime.now().strftime("%Y-%m-%d")
    fileName = '{}_{}.txt'.format(dateStamp, name)
    fHandle = open(fileName, "a+")
    fHandle.write(txt)
    print('Saving to log file...')
    fHandle.close()


def parse_json(fName):
    """Parses the JSON data from a file and populates a Python dict with the data and returns it.
    If the json cannot be parsed an exception will be raised.
    
    Parameters:
      fName(str): Name of the JSON file(already formated with .json), to be parsed.
    
    Returns:
      data(dict): dictionary populated from the json file."""
    try:
        with open('{}.json'.format(fName)) as jsonFile:
            data = json.load(jsonFile)
            return data
    except Exception as e:
        print('Unable to parse', fName)
        print(e)


cmdDict = parse_json('health_check')
hostDict = parse_json('hosts_info')


def open_ssh(hostname, username, password, commands):
    """Uses Paramiko interface to open an SSH session, through port 22, with the specified host address, username / password and returns the established connection. Known ssh host keys are loaded, if the key is new, the policy is set to add that key.
    
    Parameters:
      hostname(str): host IP address
      username(str): user name 
      password(str): user password
    
    Returns:
      client(class): Established SSH session """
    port = 22
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Connecting to', hostname)
        client.connect(
            hostname, port=port, username=username, password=password)
        print('Connection successful')
        return client
    except Exception as e:
        print('Connection Failed')
        print(e)


def exec_cmd():
    try:
        for host in hostDict:
            output = ''
            connection = open_ssh(**hostDict[host])
            for cmd in hostDict[host]['commands']:
                stdin, stdout, stderr = connection.exec_command(cmdDict[cmd])
                output += stdout.read().decode('utf-8')
            create_logfile(host, output)
            connection.close()
    except Exception as e:
        print(e)


exec_cmd()
