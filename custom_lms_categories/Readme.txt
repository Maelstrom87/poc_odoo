Custom Module | LMS CATEGORIES | MINDLE ON DEMAND 
Autore: Maurizio Mattioli


Note:
Questo modulo è in fase prototipale.
Richiede Odoo 18.0 Community Edition.

TODO
refactor naming module > CUSTOM_LMS_CATEGORIES or CUSTOM_LMS_MOD (mindle on demand)

=============================================================
Versione: 1.14.0
Data: Maggio 2025
=============================================================
- Slider categorie (basato  su Owl) 
 > suddivisione in comp. (slider, card, modale)
- applicazione palette grafica cliente
- Protoipo modale
- Test - PoC CTAs dinamiche 


=============================================================
Versione: 1.15.0
Data: Giugno 2025
=============================================================

Funzionalità:
- Gestione badge (model, backoffice view, frontend view, permission ACL)

Evoluzioni Model
> aggiunti a Corso (Slide_channel) attributi : teaser_video_url, landing_url, # Relazione badge > badge_ids = fields.One2many(
> aggiunto oggetto Badge      



=============================================================
Versione: 1.16.0 | 05/06/2025
=============================================================
>uso Swipe come Slider (piu avanzato/performante)
>helper per DataLoding Corso 



=============================================================
Versione: 2 | 05/06/2025
=============================================================
>uso Swipe come Slider come pagina odoo/Slide
>helper per DataLoding Corso / 
> attività modale su slider swipe
> layout modale evoluto
> nuovo xml di caricaemnto dati di test compatibile a nuovo model
TODO
>da sistemare relazione categorie corsi > corso categorie

=============================================================
Versione: 2.1 | 06/06/2025
=============================================================
mappato tutta la home page (card corso)
badge dinamici
cta dinamiche