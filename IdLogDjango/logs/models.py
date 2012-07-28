from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    categoryName=models.CharField(max_length=200)
    creationDate=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.categoryName
    def getEntries(self):
        ents= LogEntry.objects.filter(category=self.id)
        entList=[]
        for ent in ents:
            entList.append(ent.content)
        return "\n;\n".join(entList)
    getEntries.short_description = 'Category Entries'


class LogEntry(models.Model):
    content=models.CharField(max_length=2048)
    user=models.ForeignKey(User, related_name='created_by')
    category=models.ForeignKey(Category)
    entryDate=models.DateTimeField(auto_now_add=True)
    lastModified=models.DateTimeField(auto_now=True)
    activeFlag=models.BooleanField(default=True)


    def __unicode__(self):
        return self.entryDate.strftime("%d-%m-%Y %H:%M") + self.content
    def getPreceeders(self):
        rels=Relation.objects.filter(succeeder=self.id)
        relList=[]
        for rel in rels:
            relList.append(rel.preceeder.content)
        return "\n;\n".join(relList)
    getPreceeders.short_description = 'Preceeding Entries'
    def getSucceeders(self):
        rels=Relation.objects.filter(preceeder=self.id)
        relList=[]
        for rel in rels:
            relList.append(rel.succeeder.content)
        
        return "\n;\n".join(relList)
    getSucceeders.short_description = 'Successor Entries'
   
class Relation(models.Model):
    preceeder=models.ForeignKey(LogEntry, related_name='Preceeding Entry')
    succeeder=models.ForeignKey(LogEntry, related_name='Succeeding Entry')
    def clean(self):
        from django.core.exceptions import ValidationError
        # Don't allow an entry to succeed itself
        if self.preceeder == self.succeeder :
            raise ValidationError('An entry cannot succeed itself.')
        tempRelation=Relation.objects.filter(succeeder=self.preceeder,preceeder=self.succeeder)
        if len(tempRelation) > 0:
            raise ValidationError('A succeeding entry cannot also be a preceeding entry.')
        
    def __unicode__(self):
        return "%s to %s" % (self.preceeder,self.succeeder)