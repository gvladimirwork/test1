from django.shortcuts import render_to_response
from django.http import Http404
from catalog.models import Catalog
from catalog.models import Category
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import redirect
import os
from math import ceil

def admin_main(request):
	try:
		i = Catalog.objects.all()
		c = Category.objects.all()
		leng = len(i)
		onpage = 3
		page = 1
		sort = 'all'
		p = paging(leng,onpage,int(page))
		start = 0
		end = 0
		start = onpage*(int(page)-1)+1
		if leng-start<onpage:
			end = leng
		else:
			end = onpage*(int(page)-1)+onpage
		i = Catalog.objects.all()[start-1:end]
	except:
		i = 'error'
	return render_to_response("ad.html",{'i':i,'c':c,'p':p,'sort':sort})

def admin_catalog(request, sort='all', page='1'):
	try:
		if sort=='all':
			i = Catalog.objects.all()
			c = Category.objects.all()
		else:
			c = Category.objects.get(chpu=sort)
			cid = c.id
			i = Catalog.objects.filter(category_id=cid)
			c = Category.objects.all()
		leng = len(i)
		onpage = 3
		p = paging(leng,onpage,int(page))
		start = 0
		end = 0
		start = onpage*(int(page)-1)+1
		if leng-start<onpage:
			end = leng
		else:
			end = onpage*(int(page)-1)+onpage
		if sort=='all':
			i = Catalog.objects.all()[start-1:end]
		else:
			i = Catalog.objects.filter(category_id=cid)[start-1:end]
	except:
		raise Http404
	return render_to_response("ad.html",{'i':i,'c':c,'p':p,'sort':sort})

@csrf_protect
def admin_edit(request,item):
	try:
		csrfContext = RequestContext(request)
		i = Catalog.objects.get(chpu=item)
		c = Category.objects.all()
		csrfContext = RequestContext(request)
		error = []
		if 'edit' in request.POST:
			values = ['chpu', 'name', 'price', 'url', 'about']
			names = ['Пустое поле ЧПУ.', 'Пустое поле название.', 'Пустое поле цена.', 'Пустое поле сайт производителя.', 'Пустое поле о товаре.']
			for val in values:
				if not request.POST[val]:
					error.append(names[values.index(val)])
			if not error:
				try:
					i.name=request.POST['name']
					i.price=request.POST['price']
					i.category_id=int(request.POST['category'])
					if request.FILES:
						try:
							os.remove('/home/test1/templates/static/'+i.img)
						except:
							pass
						exe = request.FILES['newimg'].name.rfind('.')
						i.img='pic/'+request.POST['chpu']+request.FILES['newimg'].name[exe:]
						with open('/home/test1/templates/static/pic/'+request.POST['chpu']+request.FILES['newimg'].name[exe:], 'wb+') as destination:
							for chunk in request.FILES['newimg'].chunks():
								destination.write(chunk)
					i.chpu=request.POST['chpu']
					i.url=request.POST['url']
					i.about=request.POST['about']
					i.save()
					return redirect('/admin/edit/'+request.POST['chpu'])
				except:
					error.append('Неудалось добавить запись.')
	except:
		raise Http404
	return render_to_response("aded.html",{"i":i,"c":c,"error":error}, csrfContext)

@csrf_protect
def admin_add(request):
	c = Category.objects.all()
	csrfContext = RequestContext(request)
	error = []
	if 'add' in request.POST:
		values = ['chpu', 'name', 'price', 'url', 'about']
		names = ['Пустое поле ЧПУ.', 'Пустое поле название.', 'Пустое поле цена.', 'Пустое поле сайт производителя.', 'Пустое поле о товаре.']
		for val in values:
			if not request.POST[val]:
				error.append(names[values.index(val)])
		if not request.FILES:
			error.append('Незаполнено поле загрузки изображения')
		if not error:
			try:
				exe = request.FILES['newimg'].name.rfind('.')
				i = Catalog.objects.create(name=request.POST['name'], price=request.POST['price'], chpu=request.POST['chpu'],
											 category_id=int(request.POST['category']),	img='pic/'+request.POST['chpu']+request.FILES['newimg'].name[exe:], 
											 url=request.POST['url'], about=request.POST['about'])
				i.save()
				
				with open('/home/test1/templates/static/pic/'+request.POST['chpu']+request.FILES['newimg'].name[exe:], 'wb+') as destination:
					for chunk in request.FILES['newimg'].chunks():
						destination.write(chunk)
				return redirect('/admin/edit/'+request.POST['chpu'])
			except:
				error.append('Неудалось добавить запись.')
	return render_to_response("adad.html",{"c":c,"error":error}, csrfContext)

def admin_delete(request,item):
	i = Catalog.objects.get(chpu=item)
	try:
		os.remove('/home/test1/templates/static/'+i.img)
	except:
		pass
	i.delete()
	
	return redirect('/admin/') 

def paging(amt, onpage, page_need):
	pages = {}
	list1 = []
	list2 = []
	p = {}
	d=1
	c=1
	if amt%onpage>0:
		numpages = (amt/onpage)+1
	else:
		numpages = (amt/onpage)
	if page_need>numpages:
		raise Exception()
	list2.append(page_need)
	while(1):
		if (page_need-d)>0:
			list1.append(page_need-d)
			d=d+1
		if (len(list1)+len(list2))<10:
			if (page_need+c)>numpages:
				if (page_need-d)<1:
					break
				else:
					list1.append(page_need-d)
					d=d+1
			else:
				list2.append(page_need+c)
				c=c+1
		else:
			break
	list1.sort()
	p['list'] = list1+list2
	p['cur'] = page_need
	if page_need==numpages:
		p['next'] = []
	else:
		p['next'] = page_need+1
	if page_need==1:
		p['back'] = []
	else:
		p['back'] = page_need-1
	return p
