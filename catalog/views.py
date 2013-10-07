from django.shortcuts import render_to_response
from catalog.models import Catalog
from catalog.models import Category
from math import ceil
from django.http import Http404

def main(request):
	try:
		i = Catalog.objects.all()
		c = Category.objects.all()
		leng = len(i)
		onpage = 4
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
	return render_to_response("catalog.html",{'i':i,'c':c,'p':p,'sort':sort})


def catalog(request,sort='all',page='1'):
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
		onpage = 4
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
	return render_to_response("catalog.html",{'i':i,'c':c,'p':p,'sort':sort})

def item(request,item):
	try:
		i = Catalog.objects.get(chpu=item)
		c = Category.objects.all()
	except:
		raise Http404
	return render_to_response("item.html",{"i":i,"c":c})

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
	if numpages==0:
		numpages = 1
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
