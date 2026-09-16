# Translation notes for human review

French strings below are ones I'm not fully confident about, or made a
deliberate judgment call on, and want a native fr-CA speaker (or OQLF
reference) to check. None of these are part of the seeded defect
catalog — they're all meant to be correct in every build; flag anything
here that reads wrong.

## Gender-neutral phrasing

- `apply.consent_label`: "J'accepte d'être contacté par la Banque
  Northstar au sujet de cette demande." Uses the generic masculine
  "contacté". A more inclusive phrasing would be "contacté(e)" or a
  reworded sentence avoiding the agreement entirely (e.g. "J'accepte que
  la Banque Northstar me contacte au sujet de cette demande."). Left as
  generic masculine for now — flag if you'd rather standardize on
  something else app-wide.
- `landing.banner_alt`: "Un conseiller de la Banque Northstar aidant un
  client à planifier un prêt." Same generic-masculine pattern
  ("conseiller", "client"). This is alt text (not visible copy), so
  lower priority, but consistency with the above may matter.

## Typography

- Question marks (`calculator.how_calculated_link` /
  `calculator.modal_title`: "Comment ce montant est-il calculé?") use a
  plain space-less "?" per common Quebec web-copy practice. Formal French
  typographic convention (also taught and used in Quebec) would put a
  non-breaking space before `?`/`!`/`:`/`;`. I simplified to no NBSP here
  to avoid an extra invisible-character footgun in a demo app that
  already carries real, load-bearing NBSPs from Babel's number
  formatting. Flag if you want strict typographic NBSP usage instead.

## Marketing / non-literal copy

These are deliberately not literal translations — flagging so you can
confirm the tone and register read right, not because I think they're
wrong:

- `landing.hero_title`: "Un financement qui vous ressemble" (en: "Financing
  that moves with you").
- Banner subtitle (baked into `static/img/banner-fr.png` pixels, not in
  translations/): "Taux compétitifs. Conditions claires. Aucune
  surprise." (en: "Competitive rates. Clear terms. No surprises.")
- `calculator.apply_now`: "Faites votre demande dès maintenant" (en:
  "Apply now") — this one is in the ground-truth catalog as control C01,
  intentionally non-literal but correct; noted here too since it's the
  same pattern as the two above.

## Recently changed

- `apply.submit_button`: changed from "Soumettre la demande" to
  "Soumettre ma demande de prêt" (en unchanged: "Submit application").
  The longer form was needed so the D04 CSS-clip defect (fixed-width
  submit button) actually clips the French label under a real bundled
  font/size/weight rather than relying on unverified assumptions about
  rendered text width. Reads naturally in fr-CA and keeps "vous"/formal
  register consistent with the rest of the form (the possessive "ma" is
  first person, matching "J'accepte..." on the same page — not a
  register shift). Flag if you'd prefer the shorter original wording and
  a different mechanism for the D04 defect instead.

## Terminology double-checks

- `calculator.modal_body`: "...ni l'assurance facultative" for "...or
  optional insurance." Used "facultative" rather than "optionnelle" —
  both are used in Quebec financial copy; "facultative" is the more
  traditional/formal choice. Flag if "optionnelle" is preferred house
  style.
- `dashboard.txn_deposit`: "Dépôt direct" for "Direct deposit." Standard
  fr-CA banking term (used by e.g. Desjardins, Banque Nationale); fairly
  confident, but flagging since deposit/transfer terminology varies
  slightly by institution ("virement" is used for other transfer types).
- `header.sign_in`: "Ouvrir une session" for "Sign in." Chosen over the
  more generic "Se connecter" to match the specific phrasing used by
  major Quebec banks' sign-in flows. Confident in this one but noting the
  rationale in case you'd rather standardize differently.
