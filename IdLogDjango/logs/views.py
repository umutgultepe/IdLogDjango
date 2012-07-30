# Create your views here.
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from logs.models import LogEntry, Category, Relation

def index(request,additionalInfo=None):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    latest_entry_list = LogEntry.objects.filter(activeFlag=True).order_by('-entryDate')[:5]
    return render_to_response('logs/index.html',{'latest_entry_list': latest_entry_list , 'additionalInfo': additionalInfo})

def detail(request,entryID,add=None):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    
    targetEntry = get_object_or_404(LogEntry, id=entryID)
    
    preceeders=Relation.objects.filter(succeeder=targetEntry)
    succeeders=Relation.objects.filter(preceeder=targetEntry)
    
    precList=[]
    
    for prec in preceeders:
        precList.append(prec.preceeder)
    
    succList=[]
    
    for succ in succeeders:
        succList.append(succ.succeeder)
    
    categories=Category.objects.all()
    
    if add is None:
        return render_to_response('logs/detail.html', {'entry': targetEntry, 'preceeders': precList, 'succeeders': succList, 'cats':categories},context_instance=RequestContext(request))
    else:
        return render_to_response('logs/detail.html', {'entry': targetEntry, 'preceeders': precList, 'succeeders': succList, 'cats':categories, 'additionalInfo': add},context_instance=RequestContext(request))
    
def modifyEntry(request,entryID):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    
    targetEntry = get_object_or_404(LogEntry, id=entryID)    
    currUser=get_user(request)
    if currUser != targetEntry.user:
        return detail(request,entryID,"You cannot modify another user's entry")
    
    newContent=request.POST['content']
    categoryID=request.POST['category']
    category=get_object_or_404(Category, id=categoryID)
    active=request.POST.getlist('active')
    
    if len(newContent) is not 0:
        targetEntry.content=newContent
    
    targetEntry.activeFlag=active
    targetEntry.category=category  
    targetEntry.save()   
    
    return detail(request,entryID,"Entry successfully changed!")
        
def deleteEntry(request,entryID):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    
    targetEntry = get_object_or_404(LogEntry, id=entryID)    
    currUser=get_user(request)
    if currUser != targetEntry.user:
        return detail(request,entryID,"You cannot delete another user's entry")
    
    
    targetEntry.activeFlag=False  
    targetEntry.save()   
    return HttpResponseRedirect(reverse('logs.views.index'))
    
def logUser(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    currUser=get_user(request)
    userEntries=LogEntry.objects.filter(user=currUser,activeFlag=True)
    return render_to_response('logs/searchResults.html',{'logList': userEntries})   
    
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
    userID = request.POST['user']
    user=None
    if len(userID) is not 0:
        userList=User.objects.filter(id=userID)
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
        
    query=LogEntry.objects.filter(activeFlag=True)    
    if keyword is not None:        
        keywordList=keyword.split(" ")
        tSum=LogEntry.objects.get_empty_query_set()
        for key in keywordList:
            tempQuery=query.filter(content__icontains=key)
            tSum=tSum | tempQuery
        query=tSum.distinct()
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
    users=User.objects.all()
    categories=Category.objects.all()
    return render_to_response('logs/search.html', {'cats' : categories, 'users' : users}, context_instance=RequestContext(request))

def newEntry(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    
    categories=Category.objects.all()
    logs=LogEntry.objects.filter(activeFlag=True)
    return render_to_response('logs/newEntry.html', {'cats' : categories , 'logs' : logs} , context_instance=RequestContext(request))

def addCategory(name):
    newEntry=Category(categoryName=name)
    newEntry.save(force_insert=True)
    return newEntry

def submitEntry(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    content = request.POST['content']
    #===========================================================================
    # newCategoryList=request.POST.getlist('newCategory')
    # newCategory=""
    # if len(newCategoryList) is not 0:
    #    newCategory=newCategoryList[0]
    #===========================================================================
    newCategory=  request.POST['newCategory']    
    preceedings = request.POST.getlist('preceedings')
    preceedingList=[]
    for item in preceedings:
        preceedingList.append(LogEntry.objects.get(id=item))
    category=None
    if len(newCategory) is not 0:
        category= addCategory(newCategory)
    else:
        category= Category.objects.get(id= request.POST['category'])               
    newEntry=LogEntry(category=category,content=content,user=get_user(request))
    newEntry.save(force_insert=True)
    for prec in preceedingList:
        newRel=Relation(preceeder=prec,succeeder=newEntry)
        newRel.save(force_insert=True)
    return HttpResponseRedirect(reverse('logs.views.categoryEntries',args=(category.categoryName,)))

def submitCategory(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    categoryName = request.POST['categoryName']
    addCategory(categoryName)
    return HttpResponseRedirect(reverse('logs.views.categoryIndex'))

def categoryIndex(request):  
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))  
    category_list=Category.objects.all().order_by('categoryName')
    return render_to_response('logs/categoryIndex.html',{'category_list': category_list})
    # return HttpResponse("You're looking at the category index page." )

def categoryEntries(request,categoryName,additionalInfo=None):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))    
    cat_id=get_object_or_404(Category,categoryName=categoryName).id
    logList=LogEntry.objects.filter(category=cat_id,activeFlag=True).order_by('entryDate')
    return render_to_response('logs/categoryEntries.html',{'logList': logList, 'additionalInfo' : additionalInfo})

def newCategory(request):
    if check_if_anonymous(request):
        return HttpResponseRedirect(reverse('logs.views.anonymous'))
    return render_to_response('logs/newCategory.html',  context_instance=RequestContext(request))
