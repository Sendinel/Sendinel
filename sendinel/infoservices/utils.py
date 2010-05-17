from datetime import datetime

from sendinel.backend.models import Patient
from sendinel.infoservices.models import InfoMessage, \
                                         InfoService, \
                                         Subscription
from sendinel.logger import logger


def subscription_save(request, id):
    patient = request.session['patient']
    patient.save()
    way_of_communication = request.session['way_of_communication']
    infoservice = InfoService.objects.filter(pk = id)[0]
    subscription = Subscription(patient = patient,
                                way_of_communication = way_of_communication,
                                infoservice = infoservice)
    subscription.save()
    logger.info("Saved subscription %s of type %s.", 
                (unicode(subscription), 
                 unicode(subscription.infoservice.type)))
    return subscription
    
def create_messages_for_infoservice(infoservice, text):
    '''
        Put together all information for an infomessage and
        calls InfoService.create_scheduled_event
    '''
    
    for patient in infoservice.members.all():
        info_message = InfoMessage()
        info_message.text = text
        subscription = Subscription.objects.filter(patient = patient,
                                            infoservice = infoservice)[0]
        info_message.recipient = patient
        info_message.send_time = datetime.now()
        info_message.way_of_communication = \
                        subscription.way_of_communication
        info_message.save()        
        info_message.create_scheduled_event(datetime.now())
        logger.info("Created %s", str(info_message))
        
def set_session_variables_for_register(request):
    request.session['way_of_communication'] = \
                                    request.POST['way_of_communication']
    patient = Patient()
    patient.phone_number = request.POST['phone_number']
    request.session['patient'] = patient  
    