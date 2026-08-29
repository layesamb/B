import streamlit as st
import pandas as pd
from datetime import datetime
from modules.stockage import charger_donnees, sauvegarder_donnees, JOURS
from modules.style import appliquer_style, titre_page

st.set_page_config(page_title="Sport Planner", page_icon="💪", layout="wide")
appliquer_style()

donnees = charger_donnees()

st.sidebar.title("💪 Sport Planner")
page = st.sidebar.radio(
    "Navigation",
    ["Planning semaine", "Bibliotheque exercices", "Statistiques"]
)

BIBLIOTHEQUE = {
    "Haut du corps": [
        "Pompes", "Developpe couche", "Tractions", "Rowing barre",
        "Developpe militaire", "Curl biceps", "Extensions triceps"
    ],
    "Bas du corps": [
        "Squat", "Fentes", "Presse a cuisses", "Souleve de terre",
        "Mollets debout", "Hip thrust"
    ],
    "Cardio": [
        "Course a pied", "Velo", "Corde a sauter", "Rameur", "Burpees"
    ],
    "Abdominaux": [
        "Crunchs", "Planche", "Releve de jambes", "Russian twist"
    ],
}


if page == "Planning semaine":
    titre_page("Cette semaine", "Planning d'entrainement")

    jour_selectionne = st.selectbox("Choisis un jour", JOURS)

    with st.expander(f"Ajouter un exercice a {jour_selectionne}"):
        with st.form(f"form_ajout_{jour_selectionne}", clear_on_submit=True):
            nom = st.text_input("Nom de l'exercice")
            col1, col2, col3 = st.columns(3)
            with col1:
                series = st.number_input("Series", min_value=1, value=3)
            with col2:
                repetitions = st.number_input("Repetitions", min_value=1, value=10)
            with col3:
                poids = st.number_input("Poids (kg, 0 si non applicable)", min_value=0.0, value=0.0, step=2.5)

            soumis = st.form_submit_button("Ajouter au planning")

            if soumis and nom:
                donnees["planning"][jour_selectionne].append({
                    "nom": nom,
                    "series": int(series),
                    "repetitions": int(repetitions),
                    "poids": poids if poids > 0 else None,
                    "fait": False
                })
                sauvegarder_donnees(donnees)
                st.success(f"{nom} ajoute a {jour_selectionne} !")
                st.rerun()

    st.divider()

    exercices_jour = donnees["planning"][jour_selectionne]

    if not exercices_jour:
        st.info(f"Aucun exercice prevu pour {jour_selectionne}. Ajoute-en un ci-dessus.")
    else:
        for i, exercice in enumerate(exercices_jour):
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

            texte = f"**{exercice['nom']}** — {exercice['series']} x {exercice['repetitions']}"
            if exercice.get("poids"):
                texte += f" @ {exercice['poids']} kg"

            with col1:
                if exercice.get("fait"):
                    st.markdown(f"~~{texte}~~ ✅")
                else:
                    st.markdown(texte)

            with col2:
                if st.button("Fait" if not exercice.get("fait") else "Annuler", key=f"toggle_{jour_selectionne}_{i}"):
                    exercice["fait"] = not exercice.get("fait", False)
                    if exercice["fait"]:
                        donnees["historique"].append({
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "jour": jour_selectionne,
                            "exercice": exercice["nom"],
                            "series": exercice["series"],
                            "repetitions": exercice["repetitions"],
                            "poids": exercice.get("poids")
                        })
                    sauvegarder_donnees(donnees)
                    st.rerun()

            with col4:
                if st.button("Suppr.", key=f"suppr_{jour_selectionne}_{i}"):
                    donnees["planning"][jour_selectionne].pop(i)
                    sauvegarder_donnees(donnees)
                    st.rerun()


elif page == "Bibliotheque exercices":
    titre_page("Reference", "Bibliotheque d'exercices")
    st.caption("Utilise ces noms quand tu ajoutes un exercice dans ton planning.")

    for categorie, exercices in BIBLIOTHEQUE.items():
        with st.expander(categorie, expanded=True):
            for exercice in exercices:
                st.markdown(f"- {exercice}")


elif page == "Statistiques":
    titre_page("Progression", "Statistiques")

    historique = donnees["historique"]

    if not historique:
        st.info("Aucune seance enregistree pour le moment. Marque des exercices comme 'Fait' dans le planning pour commencer.")
    else:
        df_hist = pd.DataFrame(historique)
        df_hist["date"] = pd.to_datetime(df_hist["date"])

        aujourd_hui = pd.Timestamp(datetime.now())
        il_y_a_7_jours = aujourd_hui - pd.Timedelta(days=7)
        seances_recentes = df_hist[df_hist["date"] >= il_y_a_7_jours]

        col1, col2 = st.columns(2)
        col1.metric("Seances (7 derniers jours)", len(seances_recentes))
        col2.metric("Total seances enregistrees", len(df_hist))

        st.divider()
        st.subheader("Exercices les plus pratiques")
        top_exercices = df_hist["exercice"].value_counts().head(5)
        st.bar_chart(top_exercices)

        exercices_avec_poids = df_hist[df_hist["poids"].notna()]
        if not exercices_avec_poids.empty:
            st.divider()
            st.subheader("Historique des charges (poids)")
            st.dataframe(
                exercices_avec_poids[["date", "exercice", "poids"]].sort_values("date", ascending=False),
                use_container_width=True,
                hide_index=True
            )