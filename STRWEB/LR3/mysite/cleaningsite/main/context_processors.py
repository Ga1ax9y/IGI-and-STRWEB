from .models import Partner

def partners_processor(request):
    partners = Partner.objects.all()
    return {
        'partners': partners,
    }
