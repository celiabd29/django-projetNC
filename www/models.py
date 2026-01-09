from django.db import models


class Typologie(models.Model):
    label = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.label


class Denomination(models.Model):
    label = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.label


class DateReference(models.Model):
    value = models.CharField(max_length=50, unique=True)  # ex "1886"

    def __str__(self):
        return self.value


class Site(models.Model):
    ndegpoi = models.PositiveIntegerField(unique=True)
    adresse_com = models.CharField(max_length=255, blank=True, null=True)
    site_olympique = models.CharField(max_length=255, blank=True, null=True)

    type_de_reconnaissance_patrimoniale = models.CharField(max_length=255, blank=True, null=True)
    departement = models.PositiveSmallIntegerField(blank=True, null=True)
    commune = models.CharField(max_length=255, blank=True, null=True)
    code_insee = models.IntegerField(blank=True, null=True)

    adresse = models.CharField(max_length=500, blank=True, null=True)
    references_cadastrales = models.CharField(max_length=255, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    informations_d_acces_en_transport_en_commun = models.TextField(blank=True, null=True)

    statut_de_la_propriete_actuelle = models.CharField(max_length=255, blank=True, null=True)
    proprietaire = models.CharField(max_length=255, blank=True, null=True)

    appellation = models.CharField(max_length=255, blank=True, null=True)

    concepteur_s = models.TextField(blank=True, null=True)
    entrepreneur_s = models.TextField(blank=True, null=True)
    autre_s_intervenant_s = models.TextField(blank=True, null=True)
    maitre_s_d_ouvrage = models.TextField(blank=True, null=True)

    datation = models.CharField(max_length=255, blank=True, null=True)
    periode_de_construction = models.CharField(max_length=255, blank=True, null=True)
    historique_et_description = models.TextField(blank=True, null=True)

    protection_ou_label = models.CharField(max_length=255, blank=True, null=True)
    precisions_sur_la_protection = models.TextField(blank=True, null=True)

    sources_d_archives = models.TextField(blank=True, null=True)
    sources_documentaires = models.TextField(blank=True, null=True)
    references_bibliographiques = models.TextField(blank=True, null=True)

    justification = models.CharField(max_length=255, blank=True, null=True)
    credits = models.CharField(max_length=255, blank=True, null=True)

    url_image = models.URLField(blank=True, null=True)

    typologies = models.ManyToManyField(Typologie, blank=True, related_name="sites")
    denominations = models.ManyToManyField(Denomination, blank=True, related_name="sites")
    dates_de_reference = models.ManyToManyField(DateReference, blank=True, related_name="sites")

    def __str__(self):
        return self.appellation or f"Site {self.ndegpoi}"
