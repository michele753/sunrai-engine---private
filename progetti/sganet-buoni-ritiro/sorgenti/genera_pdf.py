import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, KeepTogether

out = sys.argv[1]
ACC = colors.HexColor("#1F4E79"); LIGHT = colors.HexColor("#EAF1F8"); GREY = colors.HexColor("#555555")
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontSize=20, textColor=ACC, alignment=0, spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontSize=10, textColor=GREY, spaceAfter=14)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=13.5, textColor=ACC, spaceBefore=14, spaceAfter=6)
B = ParagraphStyle("B", parent=ss["Normal"], fontSize=10.5, leading=15)
BS = ParagraphStyle("BS", parent=B, fontSize=9.5, leading=13)
BOX = ParagraphStyle("BOX", parent=B, backColor=LIGHT, borderPadding=8, borderColor=ACC, borderWidth=0.6, spaceBefore=4, spaceAfter=10)

def bullets(items):
    return ListFlowable([ListItem(Paragraph(t, B), leftIndent=12) for t in items], bulletType="bullet", start="•", leftIndent=14, bulletColor=ACC)

s = []
s.append(Paragraph("Automazione buoni di ritiro con Sganet", H1))
s.append(Paragraph("Studio di fattibilità preliminare &nbsp;·&nbsp; 15 novembre 2026", SUB))
s.append(Paragraph("<b>In sintesi:</b> il flusso è quasi certamente automatizzabile. Quanto sarà semplice e robusto "
    "dipende da come si riescono a estrarre i dati da Sganet. Sganet non ha documentazione tecnica pubblica: "
    "il primo passo è chiedere al fornitore quali canali di integrazione mette a disposizione.", BOX))

s.append(Paragraph("1. Come collegarsi a Sganet", H2))
s.append(Paragraph("Le opzioni sono in ordine dalla più solida alla meno solida.", B)); s.append(Spacer(1,6))
rows = [["#", "Modalità", "Come funziona", "Affidabilità"],
 ["1", "API / web service", "Lettura dei nuovi ritiri in tempo reale tramite REST o SOAP", "Ottima"],
 ["2", "Accesso al database", "Sola lettura, con il consenso del fornitore; rischio di rotture dopo gli aggiornamenti", "Buona"],
 ["3", "Export automatico", "File CSV, XML o Excel su cartella o email, letti a intervalli (es. ogni 5 minuti)", "Buona"],
 ["4", "PDF già generati", "Intercettare i buoni prodotti da Sganet (cartella o casella email), leggerli e smistarli", "Discreta"],
 ["5", "Automazione interfaccia (RPA)", "Un robot usa il gestionale al posto dell'operatore; ultima risorsa", "Fragile"]]
data = [[Paragraph(f"<b>{c}</b>" if i==0 else c, BS) for c in r] for i, r in enumerate(rows)]
t = Table(data, colWidths=[0.8*cm, 3.8*cm, 9.2*cm, 2.4*cm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),LIGHT),("LINEBELOW",(0,0),(-1,0),0.8,ACC),
    ("LINEBELOW",(0,1),(-1,-1),0.3,colors.HexColor("#CCCCCC")),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
s.append(t)

s.append(Paragraph("2. Il flusso automatizzato", H2))
steps = [("Nuovo ritiro in Sganet", "Viene inserito un ordine o un ritiro nel gestionale."),
 ("Lettura dati", "Mittente, indirizzo, data e fascia oraria, colli, peso, note, vettore assegnato."),
 ("Generazione buono", "PDF con il modello aziendale ed eventuale QR code o codice a barre."),
 ("Invio al trasportatore", "Email, WhatsApp Business oppure SMS con link."),
 ("Tracciamento", "Consegnato, letto, confermato dal vettore."),
 ("Ritorno (opzionale)", "Aggiornamento dello stato in Sganet, solleciti automatici, riepilogo giornaliero.")]
sd = [[Paragraph(f"<font color='white'><b>{i+1}</b></font>", ParagraphStyle("n", parent=B, alignment=1)), Paragraph(f"<b>{a}</b><br/>{b}", BS)] for i,(a,b) in enumerate(steps)]
st = Table(sd, colWidths=[1*cm, 15.2*cm])
st.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),ACC),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("LINEBELOW",(0,0),(-1,-2),2,colors.white),("BACKGROUND",(1,0),(1,-1),LIGHT),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(1,0),(1,-1),8)]))
s.append(st)
s.append(Spacer(1,8))
s.append(Paragraph("<b>Possibili aggiunte:</b>", B))
s.append(bullets(["Conferma di presa in carico da parte del vettore con un click sul link.",
    "Piccolo portale web dove ogni vettore vede i propri ritiri.",
    "Registro completo di tutti gli invii, utile anche in caso di contestazioni."]))

s.append(KeepTogether([Paragraph("3. Informazioni da chiedere all'azienda", H2), bullets([
    "Versione di Sganet: è in cloud o installato sui loro server?",
    "Il fornitore mette a disposizione API, export schedulati o accesso al database?",
    "Un esempio di buono di ritiro attuale e i campi indispensabili.",
    "Come viene scelto il vettore: è già indicato in Sganet o decide un operatore?",
    "Canale preferito dai trasportatori (email, WhatsApp o altro) e numero di ritiri al giorno.",
    "Lo stato deve tornare dentro Sganet o basta l'invio?"])]))

s.append(Paragraph("4. Prossimi passi", H2))
s.append(bullets(["Raccolta delle risposte e contatto con il fornitore di Sganet per le modalità di integrazione.",
    "Definizione dell'architettura in base al canale disponibile.",
    "Prototipo su un caso reale (pochi ritiri e un vettore pilota), poi estensione a tutti i vettori."]))

def foot(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(GREY)
    c.drawString(2*cm, 1.2*cm, "Automazione buoni di ritiro con Sganet - studio di fattibilità")
    c.drawRightString(A4[0]-2*cm, 1.2*cm, f"Pagina {d.page}"); c.restoreState()

SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
    title="Automazione buoni di ritiro con Sganet", author="").build(s, onFirstPage=foot, onLaterPages=foot)
