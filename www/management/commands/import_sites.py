import json
from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from www.models import Site, Typologie, Denomination, DateReference


IGNORE_FIELDS = {"image"}  # on ignore l'objet image, on garde url_image


def to_decimal(x):
    if x is None or x == "":
        return None
    try:
        return Decimal(str(x))
    except (InvalidOperation, ValueError):
        return None


def get_or_create_labels(Model, values, field_name="label"):
    """values: liste de strings"""
    objs = []

    if not values:
        return objs

    for v in values:
        if v is None:
            continue

        s = str(v).strip()
        if not s:
            continue

        kwargs = {field_name: s}
        obj, _ = Model.objects.get_or_create(**kwargs)
        objs.append(obj)

    return objs


class Command(BaseCommand):
    help = "Importe les sites depuis data/sites.json"

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str)

    @transaction.atomic
    def handle(self, *args, **opts):
        path = opts["json_path"]

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f"Fichier introuvable: {path}")

        # Racine: liste ou objet contenant une liste
        if isinstance(data, dict):
            data = data.get("results") or data.get("items") or data.get("data")

        if not isinstance(data, list):
            raise CommandError(
                "Structure JSON inattendue: attendu une liste d'objets."
            )

        created = 0
        updated = 0

        for row in data:
            if not isinstance(row, dict):
                continue

            ndegpoi = row.get("ndegpoi")
            if ndegpoi is None:
                continue

            geo = row.get("geo") or {}
            lon = geo.get("lon", row.get("longitude"))
            lat = geo.get("lat", row.get("latitude"))

            defaults = {
                "type_de_reconnaissance_patrimoniale": row.get(
                    "type_de_reconnaissance_patrimoniale"
                ),
                "departement": row.get("departement"),
                "commune": row.get("commune"),
                "code_insee": row.get("code_insee"),
                "adresse": row.get("adresse"),
                "references_cadastrales": row.get("references_cadastrales"),
                "code_postal": row.get("code_postal"),
                "longitude": to_decimal(lon),
                "latitude": to_decimal(lat),
                "informations_d_acces_en_transport_en_commun": row.get(
                    "informations_d_acces_en_transport_en_commun"
                ),
                "statut_de_la_propriete_actuelle": row.get(
                    "statut_de_la_propriete_actuelle"
                ),
                "proprietaire": row.get("proprietaire"),
                "appellation": row.get("appellation"),
                "concepteur_s": row.get("concepteur_s"),
                "entrepreneur_s": row.get("entrepreneur_s"),
                "autre_s_intervenant_s": row.get("autre_s_intervenant_s"),
                "maitre_s_d_ouvrage": row.get("maitre_s_d_ouvrage"),
                "datation": row.get("datation"),
                "periode_de_construction": row.get("periode_de_construction"),
                "historique_et_description": row.get(
                    "historique_et_description"
                ),
                "protection_ou_label": row.get("protection_ou_label"),
                "precisions_sur_la_protection": row.get(
                    "precisions_sur_la_protection"
                ),
                "sources_d_archives": row.get("sources_d_archives"),
                "sources_documentaires": row.get("sources_documentaires"),
                "references_bibliographiques": row.get(
                    "references_bibliographiques"
                ),
                "justification": row.get("justification"),
                "credits": row.get("credits"),
                "adresse_com": row.get("adresse_com"),
                "site_olympique": row.get("site_olympique"),
                "url_image": row.get("url_image"),
            }

            site, was_created = Site.objects.update_or_create(
                ndegpoi=int(ndegpoi),
                defaults=defaults,
            )

            created += int(was_created)
            updated += int(not was_created)

            # ManyToMany
            typologies = row.get("typologie") or []
            denominations = row.get("denomination") or []
            dates_ref = row.get("date_s_de_reference") or []

            site.typologies.set(
                get_or_create_labels(Typologie, typologies, "label")
            )
            site.denominations.set(
                get_or_create_labels(Denomination, denominations, "label")
            )
            site.dates_de_reference.set(
                get_or_create_labels(DateReference, dates_ref, "value")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé ✅ created={created} updated={updated}"
            )
        )
