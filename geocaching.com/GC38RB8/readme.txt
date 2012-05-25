= Workflow =

index.php:
== Vyplnění formuláře ==
pole $U:
- login
- klice (vstup od uzivatele)
- penize
- jidlo
- karma
- keylist - list zadanych klicu, indexovano poradim
- perky - pole perku, vypocitano (fce vyhodnot_klice)

kontrola IP (ip_check)

ohodnot_hrace($U):
- parse_keys (vygeneruje keylist)
- vyhodnot_klice($U) [custom] (vygeneruje perky se zadanych klicu)
- over_platnost($U)
- spocti_skore

zobraz perky

vygeneruj token

vypis odkaz na certifikat

== certifikat ==

