import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("FOOTBALL_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ BOT PRONOSTICS\n\n"
        "/pronostics - Matchs du jour\n"
        "/scores - Analyse des scores exacts\n"
        "/combi10 - Recherche de combinés cote 10+\n"
        "/bilan - Bilan des pronostics\n\n"
        "Les analyses sont des estimations, pas des garanties."
    )

async def pronostics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not API_KEY:
        await update.message.reply_text(
            "⚠️ API sportive non configurée. Configuration en cours."
        )
        return

    try:
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers={"x-apisports-key": API_KEY},
            params={"date": __import__("datetime").date.today().isoformat(),
                    "timezone": "Africa/Porto-Novo"},
            timeout=20
        )
        response.raise_for_status()
        matchs = response.json().get("response", [])

        if not matchs:
            await update.message.reply_text("Aucun match trouvé pour aujourd'hui.")
            return

        texte = "⚽ MATCHS DU JOUR\n\n"
        for match in matchs[:15]:
            domicile = match["teams"]["home"]["name"]
            exterieur = match["teams"]["away"]["name"]
            heure = match["fixture"]["date"][11:16]
            texte += f"🕒 {heure} — {domicile} vs {exterieur}\n"

        await update.message.reply_text(texte)

    except Exception:
        await update.message.reply_text(
            "Impossible de récupérer les matchs. Réessaie plus tard."
        )

async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 Le module de calcul des scores exacts sera ajouté après "
        "la connexion des données statistiques."
    )

async def combi10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ Le module combiné 10+ sera activé après vérification "
        "des probabilités et des cotes réelles."
    )

async def bilan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Le suivi des résultats sera ajouté dans la prochaine version."
    )

def main():
    if not TOKEN:
        raise RuntimeError("Variable TELEGRAM_BOT_TOKEN manquante")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pronostics", pronostics))
    app.add_handler(CommandHandler("scores", scores))
    app.add_handler(CommandHandler("combi10", combi10))
    app.add_handler(CommandHandler("bilan", bilan))
    app.run_polling()

if __name__ == "__main__":
    main()
