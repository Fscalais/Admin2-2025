# floephec.cloud – DNS autoritatif + DNSSEC (TP04)
- Bind9 en Docker (image ISC)
- Zone non signée : state/db.floephec.cloud
- DNSSEC : inline-signing + dnssec-policy default
- Ne pas publier keys/, *.jnl, *.signed
