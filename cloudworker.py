
import logging
from queues import gcppubsub
from queues import gcprun
from datetime import date, datetime

def execute( message ):        
    start =  datetime.now().strftime("%d%m%Y %H:%M:%S")    
    process = gcprun.Process(message.data)    
    message.ack()

    try:
        if process.Run():
            logging.info( "executed the command:", process.command )
        else:
            logging.error( "Not able to run the payload", message.data )
    except Exception as e:
        print( e )
    
    end =  datetime.now().strftime("%d%m%Y %H:%M:%S")

    if process.result is not None:
        print( process.result['returncode'], start, end, process.result['runtime'], process.command, *process.arguments )
        if process.result['returncode'] != 0:
            print( process.stdout )
            print( process.stderr )
    

print( "Cloud worker started")

consumer = gcppubsub.Consumer()
consumer.Consume( execute )

