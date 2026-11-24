# Automazione buoni di ritiro con Sganet

Progetto per un'azienda di trasporti che usa il gestionale Sganet: generare in automatico i buoni di ritiro e inviarli agli autotrasportatori.

**Stato:** studio di fattibilità preliminare. In attesa delle risposte dell'azienda e del fornitore di Sganet sui canali di integrazione (API, export, database).

## Contenuto

| Cartella | File | Descrizione |
|---|---|---|
| `documenti/` | `Sganet_fattibilita_buoni_ritiro.pdf` | Studio di fattibilità (2 pagine) |
| `audio/` | `sganet_sintesi_vocale.mp3` | Sintesi vocale della fattibilità (circa 1 min 40 s) |
| `audio/` | `testo_sintesi_vocale.txt` | Testo letto nell'audio |
| `sorgenti/` | `genera_pdf.py` | Script che genera il PDF (reportlab) |

Per rigenerare il PDF:

```bash
python3 sorgenti/genera_pdf.py documenti/Sganet_fattibilita_buoni_ritiro.pdf
```

## Domande aperte per l'azienda

- Versione di Sganet: è in cloud o installato sui loro server?
- Il fornitore mette a disposizione API, export schedulati o accesso al database?
- Un esempio di buono di ritiro attuale e i campi indispensabili.
- Come viene scelto il vettore: è già indicato in Sganet o decide un operatore?
- Canale preferito dai trasportatori e numero di ritiri al giorno.
- Lo stato deve tornare dentro Sganet o basta l'invio?
