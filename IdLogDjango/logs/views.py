# Create your views here.
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from logs.models import LogEntry, Category, Relation

def index(request):
    
    latest_entry_list = LogEntry.objects.all().order_by('-entryDate')[:5]
    return render_to_response('logs/index.html',{'latest_entry_list': latest_entry_list})

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


def search(request):
    return HttpResponse("You're looking at the search page." )
def results(request):
    return HttpResponse("You're looking at the results page." )
def newEntry(request):
    categories=Category.objects.all()
    logs=LogEntry.objects.all()
    return render_to_response('logs/newEntry.html', {'cats' : categories , 'logs' : logs} , context_instance=RequestContext(request))

def submitEntry(request):
    content = request.POST['content']
    category= Category.objects.get(id= request.POST['category'])
    preceedings = request.POST.getlist('preceedings')
    preceedingList=[]
    for item in preceedings:
        preceedingList.append(LogEntry.objects.get(id=item))
    newEntry=LogEntry(category=category,content=content,user=get_user(request))
    newEntry.save(force_insert=True)
    for prec in preceedingList:
        newRel=Relation(preceeder=prec,succeeder=newEntry)
        newRel.save(force_insert=True)
    return HttpResponseRedirect(reverse('logs.views.categoryEntries',args=(category.categoryName,)))

    

def categoryIndex(request):    
    category_list=Category.objects.all().order_by('categoryName')
    return render_to_response('logs/categoryIndex.html',{'category_list': category_list})
    # return HttpResponse("You're looking at the category index page." )

def categoryEntries(request,categoryName):
    cat_id=Category.objects.get(categoryName=categoryName).id
    logList=LogEntry.objects.filter(category=cat_id).order_by('entryDate')
    return render_to_response('logs/categoryEntries.html',{'logList': logList})

def newCategory(request):
    return HttpResponse("You're looking at the new category page." )
