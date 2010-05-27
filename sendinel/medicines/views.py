from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.translation import ugettext as _

from sendinel.backend.models import Hospital
from sendinel.backend.authhelper import redirect_to_authentication_or
from sendinel.infoservices.forms import InfoServiceValidationForm 
from sendinel.infoservices.models import InfoService
from sendinel.infoservices.utils import create_messages_for_infoservice, \
                                        set_session_variables_for_register, \
                                        subscription_save
from sendinel.logger import logger, log_request
from sendinel.medicines.forms import MedicineMessageValidationForm, \
                                     RegisterPatientForMedicineForm
from sendinel.settings import AUTH_NUMBER, MEDICINE_MESSAGE_TEMPLATE
from sendinel.web.utils import fill_authentication_session_variable, \
                               get_ways_of_communication



@log_request
def register_save(request, medicine_id):
    '''
        Save the subscription of the patient to the medicine waiting list.
        Display the success message.
    '''
    subscription = subscription_save(request, medicine_id)
    
    backurl = reverse('medicines_register')        
    nexturl = reverse('web_index')
    title = _("Registration successful")
    message = _("The patient will receive a message once the medicine "
                " \"%s\" is available in the clinic again.") \
                % subscription.infoservice.name
    new_button_label = _("Register another patient")
    success = True
    
    return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))

@log_request                              
def register(request):
    '''
    Register a patient to the waitinglist of a medicine, i.e.
    a new subscription of the infoservice is created.
    '''
    ajax_url= reverse('web_check_call_received')
    medicines = InfoService.objects.all().filter(type='medicine')
    
    ways_of_communication = get_ways_of_communication(immediate = True)
    
    if request.method == "POST":
        set_session_variables_for_register(request)
        
        infoservice = None
        form = None

        form = RegisterPatientForMedicineForm(request.POST)
        request.session['medicine'] = request.POST.get('medicine', '')
                
        if form.is_valid():
            number = fill_authentication_session_variable(request) 
            auth_number = AUTH_NUMBER
            backurl = reverse('web_index')

            return redirect_to_authentication_or(
                            reverse('medicines_register_save',
                                 kwargs = {'medicine_id': 
                                            request.session['medicine']}))
        else:
            logger.info("register patient for medicine: Invalid form.")
       
    backurl = reverse("web_index")
    
    return render_to_response('medicine/register.html', 
                              locals(),
                              context_instance = RequestContext(request))

def create_medicine(request):
    data = {'name': request.POST['name'],
            'type': 'medicine'}
    form = InfoServiceValidationForm(data)
    
    response = {}
    if form.is_valid():
        form.save()
        infoservice = form.instance
        response['id'] = infoservice.id
        response['name'] = infoservice.name
    else:
        response['errors'] = form.errors
    
    return HttpResponse(content = simplejson.dumps(response),
                        content_type = "application/json")

@log_request
def send_message(request):
    '''
        Display the form and send a message to all 
        patients waiting for the medicine. 
        Afterwards, the medicine information group is deleted.
    '''
    if request.method == 'POST':
        form = MedicineMessageValidationForm(request.POST)
        
        if form.is_valid():
            med_id = form.cleaned_data['medicine'].pk
            medicine = get_object_or_404(InfoService, pk = med_id)
            create_messages_for_infoservice(medicine, form.cleaned_data['text'])
                
            medicine.delete()
            
            backurl = reverse('medicines_send_message')
            nexturl = reverse('web_index')
            title = _("Message created")
            message = _("All patients who were waiting for the medicine "
                        "\"%s\" will be informed. The waiting list"
                        " will also be removed.") % medicine.name
            new_button_label = _("Send another message")
            success = True

            return render_to_response('web/status_message.html', 
                          locals(),
                          context_instance = RequestContext(request))
                                      
    medicines = []
    for medicine in InfoService.objects.all().filter(type='medicine'):
        if medicine.members.count() > 0:
            medicines.append(medicine)
    
    current_hospital = Hospital.get_current_hospital()
    template_text = MEDICINE_MESSAGE_TEMPLATE
    template_text = template_text.replace("$hospital", current_hospital.name)
    return render_to_response('medicine/message_create.html',
                              locals(),
                              context_instance = RequestContext(request))