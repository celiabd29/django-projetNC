from django.http import JsonResponse, Http404
from .models import Site

def site_list(request):
    sites = Site.objects.all().values(
        "ndegpoi",
        "appellation",
        "commune",
        "departement",
        "url_image",
    )
    return JsonResponse(list(sites), safe=False)

def site_detail(request, ndegpoi):
    try:
        site = Site.objects.values().get(ndegpoi=ndegpoi)
    except Site.DoesNotExist:
        raise Http404("Site non trouvé")
    return JsonResponse(site)
