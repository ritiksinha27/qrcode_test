from django.shortcuts import render,redirect
from django import forms
from django.views import View
# Create your views here.
from django.forms import modelformset_factory
  # Replace with your actual form and model names
from django.http import QueryDict
from .models import *
class kycForm(forms.ModelForm):
    class Meta:
        model = KycUser
        fields = '__all__'
        widgets = {
            'doc_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-control'}),
            'user_id': forms.Select(attrs={'class': 'form-control'}),
        }
from django.shortcuts import render
from django.views import View


class KYCViews(View):
    def get(self, request):
        form = kycForm()
        return render(request, 'kyc.html', {'form': form})

    # def post(self, request):
    #     forms = []
    #     data = request.POST
    #     files = request.FILES.getlist('doc_img')  # Adjust 'doc_img' to match your actual file input field name

    #     print(data, len(files))
        
    #     for i in range(len(files)):
    #         file_data = {key: value for key, value in data.items()}
    #         file_data['doc_img'] = files[i]
            
    #         form = kycForm(file_data, {'doc_img': files[i]})
    #         # print('ritik', form)            
    #         if form.is_valid():
    #             print('valid')
    #             print(form.cleaned_data)
    #             form.save()
    #         else:
    #             print('invalid', form.errors)
            
    #         forms.append(form)
    #         print(forms)
        
    #     return render(request, 'kyc.html', {'forms': forms})
    # from django.shortcuts import render, redirect


    def post(self, request):
        KYCFormSet = modelformset_factory(KycUser, form=kycForm, extra=2)

        if request.method == 'POST':
            doc_types = request.POST.getlist('doc_type')
            user_ids = request.POST.getlist('user_id')
            doc_imgs = request.FILES.getlist('doc_img')  # Get list of uploaded files

            # Create separate form instances for each set of data
            forms = []
            for i in range(len(doc_types)):
                form_data = {
                    'doc_type': doc_types[i],
                    'user_id': user_ids[i],
                    'doc_img': doc_imgs[i]  # Assign corresponding file
                }
                form = kycForm(data=form_data, files={'doc_img': doc_imgs[i]})
                forms.append(form)

            # Validate each form
            if all(form.is_valid() for form in forms):
                for form in forms:
                    form.save()
                return redirect('kyc')
            else:
                for form in forms:
                    print(form.errors)  # Print form errors for debugging
                return render(request, 'kyc.html', {'forms': forms})

        else:
            forms = KYCFormSet(queryset=KycUser.objects.none())
            return render(request, 'kyc.html', {'forms': forms})