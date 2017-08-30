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


class Page(models.Model):
    SiteID = models.ForeignKey("Site")
    Url = models.CharField(max_length=2048)
    LastScanDate = models.DateTimeField(auto_now=True)
    FoundDateTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.SiteID) + ' on ' + str(self.LastScanDate)


class PersonPageRank(models.Model):
    PersonID = models.ForeignKey(Person, related_name='ranks_on_pages')
    PageID = models.ForeignKey(Page, related_name='ranks')
    Rank = models.PositiveIntegerField()

    def __str__(self):
        return str(self.PersonID) + ' on ' + str(self.PageID)