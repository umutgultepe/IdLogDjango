# Create your views here.
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from logs.models import LogEntry, Category, Relation
def index(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    latest_entry_list = LogEntry.objects.all().order_by('-entryDate')[:5]
    return render_to_response('logs/index.html',{'latest_entry_list': latest_entry_list})

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user

def check_if_anonymous(request):
    d_user=get_user(request)
    return  not d_user.is_authenticated()


def anonymous(request):
    return render_to_response('logs/anonymous.html', context_instance=RequestContext(request))

def submitSearch(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    keyword = request.POST['keyword']
    categories = request.POST.getlist('category')
    username = request.POST['user']
    user=None
    if len(username) is not 0:
        userList=User.objects.filter(username=username)
        if len(userList) is 0:
            return render_to_response('logs/searchResults.html',{'logList': None})
        else:
            user=userList[0] 
    beforeDateString=request.POST['beforeDate']
    afterDateString=request.POST['afterDate']
    beforeDate=None
    afterDate=None
    if len(beforeDateString) is not 0:
        beforeDate=datetime.strptime(beforeDateString,"%d/%m/%Y")
    if len(afterDateString) is not 0:
        afterDate=datetime.strptime(afterDateString,"%d/%m/%Y")
        
    query=LogEntry.objects.all()
    
    if keyword is not None:
        query=query.filter(content__icontains=keyword)
    if user is not None:
        query=query.filter(user=user)
    if len(categories) is not 0:
        cats=Category.objects.filter(id__in = categories)      
        query=query.filter(category__in=cats)
    if beforeDate is not None:
        query=query.filter(entryDate__lte=beforeDate)
    if afterDate is not None:
        query=query.filter(entryDate__gte=afterDate)
     
    return render_to_response('logs/searchResults.html',{'logList': query})   
    #return HttpResponseRedirect(reverse('logs.views.results',args=(query,)))
    
        
    
def search(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    
    categories=Category.objects.all()
    return render_to_response('logs/search.html', {'cats' : categories}, context_instance=RequestContext(request))


def newEntry(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    
    categories=Category.objects.all()
    logs=LogEntry.objects.all()
    return render_to_response('logs/newEntry.html', {'cats' : categories , 'logs' : logs} , context_instance=RequestContext(request))

def submitEntry(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
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
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))  
    category_list=Category.objects.all().order_by('categoryName')
    return render_to_response('logs/categoryIndex.html',{'category_list': category_list})
    # return HttpResponse("You're looking at the category index page." )

def categoryEntries(request,categoryName):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    cat_id=Category.objects.get(categoryName=categoryName).id
    logList=LogEntry.objects.filter(category=cat_id).order_by('entryDate')
    return render_to_response('logs/categoryEntries.html',{'logList': logList})

def newCategory(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    return HttpResponse("You're looking at the new category page." )
