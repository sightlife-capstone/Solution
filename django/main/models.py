from django.db import models


class Continent(models.Model):
    continent_id = models.AutoField(primary_key=True)
    continent_name = models.CharField(max_length=50)

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    continent_id = models.ForeignKey(Continent, on_delete=models.CASCADE)
    continent_name = models.CharField(max_length=50)

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=50)

class Pam(models.Model):
    pam_id = models.AutoField(primary_key=True)
    pam_first_name = models.CharField(max_length=50)
    pam_last_name = models.CharField(max_length=50)
    pam_email = models.CharField(max_length=100)

class Pam_Region(models.Model):
    pam_region_id = models.AutoField(primary_key=True)
    pam_id = models.ForeignKey(Pam, on_delete=models.CASCADE)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)

class EyeBank(models.Model):
    eyebank_id = models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    eyebank_name = models.CharField(max_length=50, unique=True)
    eyebank_description = models.CharField(max_length=200, blank=True)

class Metric_Type(models.Model):
    metric_type_id = models.AutoField(primary_key=True)
    metric_type_name = models.CharField(max_length=100)

class Metric(models.Model):
    metric_id = models.AutoField(primary_key=True)
    metric_type_id = models.ForeignKey(Metric_Type, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=200)
    metric_description = models.CharField(max_length=200)

class EyeBank_Metric(models.Model):
    eyebank_metric_id = models.AutoField(primary_key=True)
    eyebank_id = models.ForeignKey(EyeBank, on_delete=models.CASCADE)
    metric_id = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()


