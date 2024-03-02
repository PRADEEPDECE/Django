from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from .forms import Step1Form, Step2Form, Step3Form

class MyWizard(SessionWizardView):
    form_list = [Step1Form, Step2Form, Step3Form]
    template_name = "wizard_app/step1.html"

    def done(self, form_list, **kwargs):
        # Process the form data
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        
        # Do something with the collected data
        print(data)
        
        # Redirect to a success page
        return HttpResponseRedirect(reverse('success'))

def success(request):
    return render(request, 'wizard_app/success.html')
