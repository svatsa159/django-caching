from .models import Variable
from django.conf import settings
from django.core.cache import cache, caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .services import CacheUpdateThread, MemCacheUpdateThread
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
import threading
from .models import DataMongo


# @cache_page(CACHE_TTL)
def get_var(request):
	fe = []
	if 'value' in cache:
		print("Used Cache")
		fe.append("Used Cache")
		value = cache.get('value')
		
	else:
		print("Set Cache")
		fe.append("Set Cache")
		value = DataMongo.objects(cached=78)
		cache.set('value',value,timeout=CACHE_TTL)
	
	data = value.to_json()
	for c in range(0,10000):
		fe.append(data)
	
	return JsonResponse({"value":fe})

	
def get_no_var(request):
	value = DataMongo.objects(cached=78)
	fe=[]
	fe.append("No Cache")
	data = value.to_json()
	for c in range(0,10000):
		fe.append(data)
	return JsonResponse({"value":fe})

# @cache_page(CACHE_TTL)
def get_post_var(request):
	frrr = request.POST.get("fre")
	print(frrr)
	success = 0
	try:
		var = DataMongo.objects(cached=78)[0]
		if (var.name=="javascript redis"):
			var.name="django redis"
		else:
			var.name = "javascript redis"
		CacheUpdateThread('value',var).start()
		print("out of new thread")
		var.save()
		
		success = 1
	except Exception as e:
		print(e)
		pass

	return JsonResponse({"success":success,"value":var.to_json()})
def get_post_mem_var(request):
	success = 0
	try:
		var = Variable.objects.get(pk=1)
		if (var.value==13):
			var.value=1
		else:
			var.value = 13
		MemCacheUpdateThread('value',var.value).start()
		print("out of new thread")
		var.save()
		
		success = 1
	except Exception as e:
		pass

	return JsonResponse({"success":success,"value":var.value})
def get_mem_var(request):
	if 'value' in caches['memcache']:
		print("Used Cache")
		value = caches['memcache'].get('value')
		
	else:
		value = Variable.objects.get(pk=1)
		caches['memcache'].set('value',value,timeout=CACHE_TTL)
		print("Cache Set for Objects")
	
	return JsonResponse({"value":value.value})
	