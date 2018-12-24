# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    username = models.CharField(primary_key=True, max_length=25)
    password = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Admin'


class CaseType(models.Model):
    case_type_id = models.IntegerField(primary_key=True)
    case_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'case_type'


class Court(models.Model):
    court_id = models.IntegerField(primary_key=True)
    court_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'court'


class Lawer(models.Model):
    lawer_id = models.IntegerField(primary_key=True)
    lawer_name = models.CharField(max_length=255, blank=True, null=True)
    office = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lawer'


class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    case_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class Paper(models.Model):
    id = models.IntegerField(primary_key=True)
    court = models.ForeignKey(Court, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    case_id = models.CharField(max_length=255, blank=True, null=True)
    case_type = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    plaintiff = models.CharField(max_length=255, blank=True, null=True)
    defendant = models.CharField(max_length=255, blank=True, null=True)
    paper_type = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=20000, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'paper'
'''
    def __init__(self, id, time, court, title, case_type, plaintiff, defendant, paper_type, term, content):
        self.id, self.time, self.court, self.title, self.case_type, self.plaintiff, self.defendant, self.paper_type, self.term, self.content = id, time, court, title, case_type, plaintiff, defendant, paper_type, term, content
    '''