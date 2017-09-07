from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    #ID = models.AutoField(primary_key=True, db_column='ID')
    Name = models.CharField(max_length=2048)
    #Owner = models.ForeignKey('auth.User', related_name='persons')

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "Persons"


class KeyWord(models.Model):
    Name = models.CharField(max_length=2048)
    PersonID = models.ForeignKey(Person, related_name='key_words', db_column='PersonID')

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "Keywords"


class Site(models.Model):
    Name = models.CharField(max_length=2048)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = "Sites"


class Page(models.Model):
    SiteID = models.ForeignKey("Site", db_column='SiteID')
    Url = models.CharField(max_length=2048)
    LastScanDate = models.DateTimeField(auto_now=True, null=True, blank=True)
    FoundDateTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.SiteID) + ' on ' + str(self.LastScanDate)

    class Meta:
        db_table = "Pages"


class PersonPageRank(models.Model):
    PersonID = models.ForeignKey(Person, related_name='person', db_column='PersonID')
    PageID = models.ForeignKey(Page, related_name='page', db_column='PageID')
    Rank = models.PositiveIntegerField()

    def __str__(self):
        return str(self.PersonID) + ' on ' + str(self.PageID)

    class Meta:
        db_table = "PersonPageRank"


class UserSite(models.Model):
    UserID = models.ForeignKey(User, related_name='root_api_user_id', db_column='UserID')
    SiteID = models.ForeignKey(Site, related_name='root_api_site_id', db_column='SiteID')

    def __str__(self):
        return '{} on {}'.format(self.UserID, self.SiteID)

    class Meta:
        db_table = "UserSite"
