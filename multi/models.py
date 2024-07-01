from django.db import models

# Create your models here.
class KycUser(models.Model):
    doc_type=models.CharField(max_length=50,choices=[('aadhar','aadhar'),('pan','pan')])
    doc_img=models.FileField(upload_to='kyc_docs')
    user_id=models.ForeignKey('auth.User',on_delete=models.CASCADE)