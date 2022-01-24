from django.db import models

# Create your models here.
class Update(models.Model):
    # fields of the model
    length = models.IntegerField()
    to_update=models.BooleanField()
    

class India_data(models.Model):
  date=models.CharField(max_length=50)
  total_cases= models.IntegerField()
  total_deceased= models.IntegerField()
  total_recovered= models.IntegerField()


