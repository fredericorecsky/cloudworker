from datetime import date
import json
import logging
import subprocess
import sys
import re
import time

allow_list = [
    'gcloud',
    'gsutil',
]

functions = {
    'TODAY': lambda : date.today().strftime("%d%m%Y"),    
}

class Process(object):
    payload = ""
    command = ""
    arguments = []    
    stdout = ""
    stderr = ""
    result = None
   
    def __init__( object, payload):
        object.payload = payload  
        
        try:
            decoded_payload = json.loads( payload )    

            object.command = decoded_payload['command']
            object.arguments = decoded_payload['arguments']
            
            for idx, argument in enumerate(object.arguments):
                matchvar = re.search( "(\$\=(\w+))", object.arguments[idx] )
                
                while matchvar:                    
                    to_change, token = matchvar.groups()
                    if token in functions:                        
                        replace = functions[token]()                                               
                        object.arguments[idx] = object.arguments[idx].replace( to_change, replace ) 
                    else:
                        logging.info( token + " does not exists")        
                    
                    # bug for not valid tokens
                    matchvar = re.search( "(\$\=(\w+))", object.arguments[idx] )
        except Exception as e:            
            logging.warn( payload )
            logging.error( e )

            

    def Run(object):     
        if len(object.command) > 0:
            if object.command in allow_list:
                runtime = time.perf_counter()
                process = subprocess.Popen([ object.command,  *object.arguments], 
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                object.stdout, object.stderr = process.communicate()
                runtime = time.perf_counter() - runtime

                
                object.result = {
                    'returncode':process.returncode,
                    'stdout':object.stdout,
                    'stderr':object.stderr,
                    'runtime':runtime
                }                
                return 1
            else:
                logging.error( "Command not allowed")
                return 0
                
        else:            
            logging.error( "Error command is empty")
            return 0
