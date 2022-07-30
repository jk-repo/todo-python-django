from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
import traceback


class ErrorHandlerMiddleware:

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    if response.status_code == 404:
      return render(request, '404.html')
    return response

  def process_exception(self, request, exception):
    if settings.DEBUG:
      if exception:
        error = {
            'url': request.build_absolute_uri(),
            'message': repr(exception),
            'traceback': traceback.format_exc()
        }

      return render(request, 'error.html', {'error': error, 'showTrace': settings.DEBUG})
