from django.db import models

# Create your models here.
class Persons(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2048, unique=True)
    def __str__(self):
        return self.name
    
class Sites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    def __str__(self):
        return self.name

class Keywords(models.Model):
    id = models.AutoField(primary_key=True)
    personId = models.ForeignKey("Persons")
    name = models.CharField(max_length=2048, unique=True)
    def __str__(self):
        return self.name

class Pages(models.Model):
    siteId = models.ForeignKey("Sites")
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2048)
    lastScanDate = models.DateField(auto_now_add=True)
    FoundDateTime = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.siteId) + ' on ' + str(self.lastScanDate)

class PersonPageRank(models.Model):
    personId = models.ForeignKey(Persons, related_name='person')
    pageId = models.ForeignKey(Pages, related_name='page')
    rank = models.PositiveIntegerField()

    def __str__(self):
        return str(self.personId) + ' on ' + str(self.pageId)

