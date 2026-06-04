import google.generativeai as genai
from django.conf import settings
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from hospital.models import Bills, DetailsBills
from decouple import config as env
import json
genai.configure(api_key=env('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-2.5-flash")  # gratuit

# liste exacte des modèles accessibles avec votre clé.
# for model in genai.list_models():
#     if "generateContent" in model.supported_generation_methods:
#         print(model.name)

def extraire_periode_par_ia(phrase_gerant: str) -> dict:
    """
    Analyse la phrase du gérant avec un prompt système complet
    et retourne un dictionnaire contenant les dates nettoyées.
    """
    aujourd_hui = timezone.now().date()
    
    # Injection dynamique des repères temporels du jour exact de l'appel
    prompt_systeme = f"""
    Tu es un agent d'analyse de texte et de traitement temporel strict. Ton unique rôle est de lire une demande utilisateur en langage naturel, d'identifier la période temporelle demandée et de la convertir en deux dates exactes au format "YYYY-MM-DD".

    CONTEXTE TEMPOREL DE RÉFÉRENCE (AUJOURD'HUI) :
    - Date courante : {aujourd_hui}
    - Jour de la semaine : {aujourd_hui.strftime('%A')}
    - Mois courant : {aujourd_hui.strftime('%B %Y')}

    RÈGLES STRICTES DE CALCUL DE LA PÉRIODE :
    1. LE JOUR COURANT (Aujourd'hui, ce jour, le bilan du jour) :
       - date_debut = {aujourd_hui} | date_fin = {aujourd_hui}
    2. HIER :
       - date_debut = date_fin = {aujourd_hui - timedelta(days=1)}
    3. CETTE SEMAINE :
       - date_debut = Date du lundi de cette semaine.
       - date_fin = {aujourd_hui}
    4. LE MOIS EN COURS :
       - date_debut = {aujourd_hui.strftime('%Y-%m-01')}
       - date_fin = {aujourd_hui}
    5. PÉRIODES INCONNUES / VAGUES :
       - Si la phrase ne contient aucune notion claire, utilise le jour courant ({aujourd_hui}).

    CONSIGNES DE SORTIE :
    - Réponds UNIQUEMENT avec un objet JSON brut, sans balises ```json.
    
    Format :
    {{"date_debut": "YYYY-MM-DD", "date_fin": "YYYY-MM-DD", "description_fr": "texte"}}

    PHRASE DE L'UTILISATEUR À ANALYSER :
    "{phrase_gerant}"
    """

    try:
        response = model.generate_content(prompt_systeme)
        # Nettoyage des espaces blancs et conversion en dictionnaire Python
        donnees_temps = json.loads(response.text.strip())
        return donnees_temps
    except Exception as e:
        # Fallback de secours en cas de bug : on renvoie la journée d'aujourd'hui
        return {
            "date_debut": str(aujourd_hui),
            "date_fin": str(aujourd_hui),
            "description_fr": "Aujourd'hui (par défaut)"
        }

def get_restaurant_context(question):
    """
    Extrait les données clés du restaurant depuis la base de données
    et les formate pour l'IA.
    """

    period = extraire_periode_par_ia(question)
    print(period)
    date_debut = period['date_debut']
    date_fin = period['date_fin']
    # Chiffre d'affaires sur la période
    ca_periode = Bills.objects.filter(
        createdAt__date__range=[date_debut, date_fin]
    ).exclude(status__isnull=True).aggregate(total=Sum("amount_paid"))["total"] or 0

    # Nombre de commandes sur la période
    nb_commandes = Bills.objects.filter(
        createdAt__date__range=[date_debut, date_fin]
    ).count()

    # Ticket moyen sur la période
    ticket_moyen = Bills.objects.filter(
        createdAt__date__range=[date_debut, date_fin]
    ).exclude(status__isnull=True).aggregate(moy=Avg("amount_paid"))["moy"] or 0

    # Top 5 produits sur la période
    top_produits = (
        DetailsBills.objects.filter(createdAt__date__range=[date_debut, date_fin])
        .exclude(bills__status__isnull=True, cash_id__isnull=True, hospital_id__isnull=True)
        .values("dish__translations__name")
        .annotate(total_vendu=Sum("quantity_served"))
        .order_by("-total_vendu")[:5]
    )

    # Flop 5 produits sur la période (Corrigé avec le tri croissant)
    flop_produits = (
        DetailsBills.objects.filter(createdAt__date__range=[date_debut, date_fin])
        .exclude(bills__status__isnull=True)
        .values("dish__translations__name")
        .annotate(total_vendu=Sum("quantity_served"))
        .order_by("total_vendu")[:5]
    )

    # Commandes actuellement en attente (temps réel global)
    en_attente = Bills.objects.filter(status__isnull=True).count()

    # Formatage du contexte pour l'IA
    context = f"""
    Données du restaurant pour la période du {date_debut} au {date_fin} :

    CHIFFRE D'AFFAIRES :
    - Total sur la période : {ca_periode:,.0f} FCFA

    COMMANDES :
    - Nombre de commandes : {nb_commandes}
    - Ticket moyen sur la période : {ticket_moyen:,.0f} FCFA
    - Commandes actuellement en attente (en ce moment) : {en_attente}

    TOP 5 PRODUITS SUR LA PÉRIODE :
    {chr(10).join([f"  - {p['dish__translations__name']} : {p['total_vendu']} unités" for p in top_produits])}

    FLOP 5 PRODUITS SUR LA PÉRIODE :
    {chr(10).join([f"  - {p['dish__translations__name']} : {p['total_vendu']} unités" for p in flop_produits])}
    """

    return context


def ask_assistant(question: str) -> str:
    """
    Envoie la question du gérant + le contexte des données à Gemini
    et retourne la réponse en langage naturel.
    """
    context = get_restaurant_context(question)

    prompt = f"""
    Tu es l'assistant intelligent du restaurant. Tu analyses les données 
    en temps réel et tu réponds de façon claire, concise et utile au gérant.
    Réponds toujours en français. Sois direct et actionnable.
    Si tu identifies un problème ou une opportunité dans les données, signale-le.

    DONNÉES ACTUELLES DU RESTAURANT :
    {context}

    QUESTION DU GÉRANT :
    {question}

    Réponds de façon structurée avec des chiffres précis quand c'est pertinent.
    """

    response = model.generate_content(prompt)
    return response.text