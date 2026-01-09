from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Site, Typologie, Denomination, DateReference

def site_list(request):
    qs = (
        Site.objects.all()
        .prefetch_related("typologies", "denominations", "dates_de_reference")
        .order_by("ndegpoi")
    )

    # (Phase 3.3) on branchera la recherche ici (je te la mets déjà prête)
    q = (request.GET.get("q") or "").strip()
    typ = request.GET.getlist("typologie")
    den = request.GET.getlist("denomination")
    dref = request.GET.getlist("date_ref")

    if q:
        qs = qs.filter(
            Q(appellation__icontains=q)
            | Q(commune__icontains=q)
            | Q(adresse__icontains=q)
            | Q(historique_et_description__icontains=q)
            | Q(type_de_reconnaissance_patrimoniale__icontains=q)
        )

    if typ and "all" not in typ:
        qs = qs.filter(typologies__id__in=typ).distinct()

    if den and "all" not in den:
        qs = qs.filter(denominations__id__in=den).distinct()

    if dref and "all" not in dref:
        qs = qs.filter(dates_de_reference__id__in=dref).distinct()

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "q": q,
        "typologies": Typologie.objects.order_by("label"),
        "denominations": Denomination.objects.order_by("label"),
        "dates_ref": DateReference.objects.order_by("value"),
        "selected_typ": typ,
        "selected_den": den,
        "selected_dref": dref,
    }
    return render(request, "www/site_list.html", context)

def site_detail(request, ndegpoi):
    site = (
        Site.objects
        .prefetch_related("typologies", "denominations", "dates_de_reference")
        .get(ndegpoi=ndegpoi)
    )
    return render(request, "www/site_detail.html", {"site": site})
