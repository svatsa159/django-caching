from .models import Variable
from django.conf import settings
from django.core.cache import cache, caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .services import CacheUpdateThread
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
import threading


# @cache_page(CACHE_TTL)
def get_var(request):
	if 'value' in cache:
		print("Used Cache")
		value = cache.get('value')
		
	else:
		value = Variable.objects.get(pk=1)
		cache.set('value',value,timeout=CACHE_TTL)
		print("Cache Set")
	
	return JsonResponse({"value":value.value})
	# {"value": 7}


# @cache_page(CACHE_TTL)
def post_var(request):
	success = 0
	try:
		var = Variable.objects.get(pk=1)
		if (var.value==13):
			var.value=1
		else:
			var.value = 13
		CacheUpdateThread('value',var).start()
		print("out of new thread")
		var.save()
		
		success = 1
	except Exception as e:
		pass

	return JsonResponse({"success":success,"value":var.value})

def get_memcached_var(request):
	if 'value' in caches['memcache']:
		print("Used Cache")
		value = caches['memcache'].get('value')
		
	else:
		value = Variable.objects.get(pk=1).value
		caches['memcache'].set('value',value,timeout=CACHE_TTL)
		print("Cache Set")
	
	return JsonResponse({"value":value})
	