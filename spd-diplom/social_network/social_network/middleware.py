import os
import sys
import codecs

class EncodingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['LANG'] = 'ru_RU.UTF-8'
        os.environ['LC_ALL'] = 'ru_RU.UTF-8'
        
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

    def __call__(self, request):
        if request.method == 'POST':
            if hasattr(request, 'POST') and request.POST:
                for key, value in request.POST.items():
                    if isinstance(value, bytes):
                        request.POST._mutable = True
                        request.POST[key] = value.decode('utf-8')
                        request.POST._mutable = False
            
            if hasattr(request, 'data') and request.data:
                if isinstance(request.data, dict):
                    for key, value in request.data.items():
                        if isinstance(value, bytes):
                            request.data[key] = value.decode('utf-8')
        
        response = self.get_response(request)
        return response 