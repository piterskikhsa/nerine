from django.db import models


class Person(models.Model):
    Name = models.CharField(max_length=2048)

    def __str__(self):
        return self.Name


class KeyWord(models.Model):
    Name = models.CharField(max_length=2048)
    PersonID = models.ForeignKey(Person, related_name='key_words')

    def __str__(self):
        return self.Name


class Site(models.Model):
    Name = models.CharField(max_length=2048)

    def __str__(self):
        return self.Name
