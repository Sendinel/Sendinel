from copy import deepcopy

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from sendinel.backend.models import Hospital
from sendinel.groups.models import InfoService
from sendinel.groups.forms import MedicineMessageValidationForm, \
                                  RegisterPatientForMedicineForm
from sendinel.groups.views import create_messages_for_group, \
                                  set_session_variables_for_register, \
                                  subscription_save
from sendinel.logger import logger, log_request
from sendinel.settings import AUTHENTICATION_ENABLED, AUTH_NUMBER, MEDICINE_MESSAGE_TEMPLATE
from sendinel.web.views import fill_authentication_session_variable, \
                               render_status_success



@log_request
def register_patient_save(request, id):
    backurl = reverse('medicine_register_patient')        
    nexturl = reverse('web_index')
    
    subscription = subscription_save(request, id)
    
    success = True
    title = _("Registration successful")
    message = _("The patient will receive a messages once the medicine "
                " \"%s\" is available in the clinic again.") \
                % subscription.infoservice.name
    
    return render_to_response('web/status_message.html', 
                              locals(),
                              context_instance = RequestContext(request))

@log_request                              
def register_patient(request):
    '''
    Register a patient to the waitinglist of a medicine, i.e.
    a new subscription to the infoservice is created.
    '''
    ajax_url= reverse('web_check_call_received')
    medicines = InfoService.objects.all().filter(type='medicine')
     
    if request.method == "POST":
        set_session_variables_for_register(request)
        request.session['medicine'] = request.POST.get('medicine', '')
        
        data = deepcopy(request.POST)
        form = RegisterPatientForMedicineForm(data)
        
        if form.is_valid():
            number = fill_authentication_session_variable(request) 
            auth_number = AUTH_NUMBER
            backurl = reverse('web_index')
            
            if AUTHENTICATION_ENABLED:
                return HttpResponseRedirect(
                        reverse('web_authenticate_phonenumber') \
                        + "?next=" + \
                        reverse('medicine_register_patient_save', \
                        kwargs= {'id': request.session['medicine']}))

            return HttpResponseRedirect( \
                            reverse('medicine_register_patient_save',
                                kwargs = {'id': request.session['medicine']}))
        else:
            logger.info("register_infoservice: Invalid form.")
       
    backurl = reverse("web_index")
    
    return render_to_response('medicine/medicine_register.html', 
                              locals(),
                              context_instance = RequestContext(request))

                              
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
            create_messages_for_group(medicine, form.cleaned_data['text'])
                
            medicine.delete()
            
            nexturl = reverse('web_index')
            title = _("Message created")
            message = _("All patients who were waiting for the medicine " +
                        "\"%s\" will be informed") % medicine.name

            render_status_success(request, title, message, nexturl = nexturl)
                                      
    medicines = InfoService.objects.all().filter(type='medicine')
    
    current_hospital = Hospital.objects.all().filter(current_hospital = True)[0]
    template_text = MEDICINE_MESSAGE_TEMPLATE
    template_text = template_text.replace("$hospital", current_hospital.name)
    return render_to_response('medicine/message_create.html',
                              locals(),
                              context_instance = RequestContext(request))