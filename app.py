from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF
import io
import os
from datetime import date

app = Flask(__name__)

BAZA_HTML = """
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titlu_pagina }} - DocumenteRapide</title>
    <meta name="description" content="{{ descriere_seo }}">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f8; color: #2d3748; margin: 0; padding: 0; line-height: 1.6; }
        header { background-color: #1a365d; color: white; padding: 15px 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
        .nav-container { max-width: 900px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; }
        .logo { font-size: 22px; font-weight: bold; color: #63b3ed; text-decoration: none; }
        nav a { color: #e2e8f0; text-decoration: none; margin-left: 18px; font-size: 15px; font-weight: 500; }
        nav a:hover { color: #63b3ed; }
        .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 25px; }
        h1 { color: #1a365d; margin-top: 0; font-size: 26px; }
        h2 { color: #2b6cb0; font-size: 20px; }
        label { font-weight: 600; display: block; margin-top: 15px; color: #4a5568; }
        input, textarea, select { width: 100%; padding: 12px; margin-top: 6px; border: 1px solid #cbd5e0; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        button { background-color: #2b6cb0; color: white; padding: 14px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; margin-top: 22px; font-weight: bold; transition: background 0.2s; }
        button:hover { background-color: #1a365d; }
        .grid-tools { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }
        .tool-box { background: #ebf8ff; border: 1px solid #bee3f8; padding: 20px; border-radius: 8px; text-decoration: none; color: #1a365d; transition: transform 0.2s; }
        .tool-box:hover { transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .tool-box h3 { margin-top: 0; color: #2b6cb0; }
        footer { text-align: center; padding: 25px; color: #718096; font-size: 14px; border-top: 1px solid #e2e8f0; margin-top: 40px; }
        footer a { color: #2b6cb0; text-decoration: none; margin: 0 10px; }
    </style>
</head>
<body>
    <header>
        <div class="nav-container">
            <a href="/" class="logo">📄 DocumenteRapide</a>
            <nav>
                <a href="/">Acasă</a>
                <a href="/cerere-demisie">Cerere Demisie</a>
                <a href="/cerere-concediu">Cerere Concediu</a>
                <a href="/declaratie-proprie-raspundere">Declarație</a>
            </nav>
        </div>
    </header>

    <div class="container">
        {{ continut | safe }}
    </div>

    <footer>
        <p>© 2026 DocumenteRapide - Generator Gratuit de Documente PDF Online</p>
        <p>
            <a href="/despre-noi">Despre Noi</a> | 
            <a href="/confidentialitate">Politica de Confidențialitate</a>
        </p>
    </footer>
</body>
</html>
"""

def genereaza_pdf_bytes(titlu, corp_text):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("C:/Windows/Fonts/arial.ttf"):
        pdf.add_font("ArialUnicode", "", "C:/Windows/Fonts/arial.ttf")
        pdf.set_font("ArialUnicode", size=14)
    else:
        pdf.set_font("Helvetica", size=14)

    pdf.cell(0, 10, text=titlu, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    pdf.set_font_size(12)
    pdf.multi_cell(0, 8, text=corp_text)

    pdf_output = io.BytesIO(pdf.output())
    pdf_output.seek(0)
    return pdf_output

@app.route("/")
def acasa():
    continut = """
    <div class="card">
        <h1>Generează Gratuit Cereri și Declarații în Format PDF</h1>
        <p>Alege documentul de care ai nevoie, completează datele în 30 de secunde și descarcă fișierul PDF gata formatat pentru printare sau trimitere pe e-mail.</p>
        <div class="grid-tools">
            <a href="/cerere-demisie" class="tool-box">
                <h3>📝 Cerere de Demisie</h3>
                <p>Model oficial cu preaviz sau cu acordul părților, conform Codului Muncii.</p>
            </a>
            <a href="/cerere-concediu" class="tool-box">
                <h3>🏖️ Cerere Concediu</h3>
                <p>Generează rapid cererea pentru concediul de odihnă sau fără plată.</p>
            </a>
            <a href="/declaratie-proprie-raspundere" class="tool-box">
                <h3>✍️ Declarație Proprie Răspundere</h3>
                <p>Utilă pentru primărie, instituții publice, școli sau furnizori.</p>
            </a>
            <a href="/cerere-generala" class="tool-box">
                <h3>📩 Cerere / Reclamație Generală</h3>
                <p>Formular flexibil pentru orice solicitare către o firmă sau instituție.</p>
            </a>
        </div>
    </div>
    <div class="card">
        <h2>De ce să folosești acest generator online?</h2>
        <p>Nu mai pierzi timp formatând margini în Word. Toate documentele respectă structura standard cerută de angajatori și instituțiile din România, iar datele tale nu sunt stocate pe serverele noastre.</p>
    </div>
    """
    return render_template_string(BAZA_HTML, titlu_pagina="Acasă - Modele Cereri PDF", descriere_seo="Genereaza gratuit cereri de demisie, concediu si declaratii in format PDF.", continut=continut)

@app.route("/cerere-demisie", methods=["GET", "POST"])
def demisie():
    if request.method == "POST":
        nume = request.form.get("nume", "")
        functie = request.form.get("functie", "")
        firma = request.form.get("firma", "")
        tip = request.form.get("tip", "")
        data_incetare = request.form.get("data_incetare", "")
        azi = date.today().strftime("%d.%m.%Y")

        text = (
            f"Către conducerea {firma},\n\n"
            f"Subsemnatul(a) {nume}, având funcția de {functie} în cadrul societății dumneavoastră, "
            f"vă aduc la cunoștință hotărârea mea de a înceta contractul individual de muncă prin {tip}, "
            f"începând cu data de {data_incetare}.\n\n"
            f"Vă mulțumesc pentru colaborare.\n\n"
            f"Data: {azi}                                        Semnătura: ____________"
        )
        pdf_file = genereaza_pdf_bytes("CERERE DE DEMISIE", text)
        return send_file(pdf_file, as_attachment=True, download_name="cerere_demisie.pdf", mimetype="application/pdf")

    continut = """
    <div class="card">
        <h1>Generator Cerere de Demisie (PDF)</h1>
        <form method="POST">
            <label>Numele și Prenumele tău:</label>
            <input type="text" name="nume" required placeholder="Ex: Popescu Andrei">
            <label>Funcția ocupată:</label>
            <input type="text" name="functie" required placeholder="Ex: Operator calculator / Vânzător">
            <label>Numele firmei (Angajator):</label>
            <input type="text" name="firma" required placeholder="Ex: SC Exemplu SRL">
            <label>Modalitatea de încetare:</label>
            <select name="tip">
                <option value="acordul părților (art. 55 lit. b din Codul Muncii)">Cu acordul părților (fără preaviz)</option>
                <option value="demisie cu respectarea termenului de preaviz (art. 81 din Codul Muncii)">Demisie cu preaviz (20 zile lucrătoare)</option>
            </select>
            <label>Data de la care dorești încetarea:</label>
            <input type="text" name="data_incetare" required placeholder="Ex: 01.12.2026">
            <button type="submit">Descarcă Cererea de Demisie (PDF)</button>
        </form>
    </div>
    <div class="card">
        <h2>Informații utile despre depunerea demisiei</h2>
        <p>Conform Codului Muncii din România, angajatul are dreptul să nu își motiveze demisia. Dacă optezi pentru încetarea cu acordul părților, contractul se poate încheia chiar a doua zi, dacă angajatorul este de acord.</p>
    </div>
    """
    return render_template_string(BAZA_HTML, titlu_pagina="Generator Cerere de Demisie PDF", descriere_seo="Completeaza online si descarca gratuit model cerere de demisie PDF.", continut=continut)

@app.route("/cerere-concediu", methods=["GET", "POST"])
def concediu():
    if request.method == "POST":
        nume = request.form.get("nume", "")
        functie = request.form.get("functie", "")
        firma = request.form.get("firma", "")
        zile = request.form.get("zile", "")
        perioada = request.form.get("perioada", "")
        azi = date.today().strftime("%d.%m.%Y")

        text = (
            f"Către conducerea {firma},\n\n"
            f"Subsemnatul(a) {nume}, angajat(ă) în funcția de {functie}, vă rog să binevoiți a-mi aproba "
            f"efectuarea a {zile} zile de concediu de odihnă în perioada {perioada}.\n\n"
            f"Vă mulțumesc,\n\n"
            f"Data: {azi}                                        Semnătura: ____________"
        )
        pdf_file = genereaza_pdf_bytes("CERERE DE CONCEDIU DE ODIHNĂ", text)
        return send_file(pdf_file, as_attachment=True, download_name="cerere_concediu.pdf", mimetype="application/pdf")

    continut = """
    <div class="card">
        <h1>Generator Cerere Concediu de Odihnă (PDF)</h1>
        <form method="POST">
            <label>Numele și Prenumele tău:</label>
            <input type="text" name="nume" required placeholder="Ex: Ionescu Maria">
            <label>Funcția ocupată:</label>
            <input type="text" name="functie" required placeholder="Ex: Contabil / Asistent">
            <label>Numele firmei:</label>
