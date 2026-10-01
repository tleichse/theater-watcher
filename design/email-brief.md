# Design brief: the theater-watcher weekly email

Paste everything below the line into a new Claude Design chat. You can also attach this
week's preview, `data/digests/issue-1-2026-10-05.html`, as a reference for structure (not for
style). Background on why: [T-011](../tasks/T-011-email-design-brief.md).

<!-- Format: one section per topic, ending with "Sample content" and "What to deliver". Keep the
fixed structure in sync with tasks/T-003 step 3 and the constraints in sync with
digest/email/issue.html. Refresh the sample content from a recent issue before each design
round. -->

**Decide before you paste** (edit the line in the brief that says "My answers"):
1. **Name** readers see: keep "theater-watcher", or a pt-PT name?
2. **Tone:** playful and colourful, editorial and elegant, or bold and poster-like?
3. **References:** 3–5 things you like (programmes, posters, newsletters). Attach or link
   them.

---

## Who this is for
I'm designing a **weekly email** that lists open opportunities for **professional actors in
Portugal**: castings, auditions, training (workshops, courses), grants and residencies, and
early signs of new productions. It goes out every Monday morning. Readers scan it quickly,
**mostly on their phones**, to see what's open, who's behind each call, and when it closes.
Every word readers see is in **European Portuguese (pt-PT)**.

It should feel like it belongs to the **theatre and film world**: artistic, colourful, with
personality. It also has to be **trustworthy and easy to scan**: this is a working tool, not a
magazine.

My answers: name = ____ · tone = ____ · references = ____

## The structure is fixed: please design it, don't change it
From top to bottom:
1. **Header:** name, issue number and date ("N.º 1 · 5 out 2026"), and one line such as "Esta
   semana: 10 novas, 2 a fechar".
2. **Últimos dias:** opportunities that close within 7 days (any pillar).
3. **Five pillar sections, always present, in this order:** Teatro, Cinema, Televisão,
   Publicidade, Dobragem. An empty one shows "Sem novidades esta semana".
4. **Formação** (training), **Apoios e oportunidades** (grants), and **No radar** (news of
   upcoming productions). These appear only when they have items.
5. **Candidaturas permanentes:** a compact list of links (not cards) to always-open sign-up
   forms.
6. **Footer:** a short note on how we pick and summarise opportunities, and the list of
   sources.

**Card anatomy** (Últimos dias, pillar sections, Formação, Apoios, No radar):
- Badges: **pillar** (Teatro / Cinema / Televisão / Publicidade / Dobragem), **Novo** (first
  time shown), **region** (Norte / Centro / Sul / Ilhas / Nacional)
- **Title** (up to about 90 characters)
- **Organisation**: who posted it. Always shown, because it's what makes a call trustworthy.
- **Summary**: 1–2 sentences
- **Key facts** line: place · pay or price · ages (e.g. "Lisboa · 90 € · 18–35 anos")
- **Deadline chip**: "Fecha em 3 dias" (urgent), "Candidaturas até 15 out", or "Começa a 16 out"
- **Button**: "Ver e candidatar" (or "Ler a notícia" in No radar). It goes to the original page.

Each of the five pillars needs **its own colour**, used consistently: pillar badge, section
heading, and the colour strip. Colour must never be the only cue, because the label text is
always there. Formação, Apoios, No radar, and Últimos dias need accents too.

## Hard constraints (email clients, not the web)
Designs must survive Gmail (web, Android, iOS), Apple Mail, and Outlook:
- **Width:** 600–640 px on desktop, a single column that works at **375 px** on phones.
- **Layout with tables only:** no flexbox, no grid, no absolute positioning, no overlapping
  elements.
- **No CSS variables, no gradients you can't do without, no `background-image` the content
  depends on.** Flat colours only, as fixed hex values.
- **Fonts:** web fonts are often ignored. Every font needs a web-safe fallback (Georgia,
  Times New Roman, Arial, Helvetica, Verdana, Trebuchet MS), and the design must still look
  right in that fallback. A custom typeface is only safe inside a logo image.
- **Images:** optional. A small logo or wordmark image is fine (with alt text). Don't rely on
  images for any text or for the layout, because many clients block them by default.
- **Dark mode:** clients may invert colours. Avoid thin light-on-light details that vanish,
  and keep contrast at **WCAG AA** (4.5:1 for body text) in both modes.
- **Buttons:** solid colour blocks with text, at least 44 px tall for thumbs.
- **Weight:** keep it lean. Gmail cuts emails above about 100 KB, and an issue can have 30+
  cards.

## Explore three directions
Show each as a **full mockup of the sample issue below**, at desktop and phone width:
- **A, "Cartaz":** like a theatre poster. Bold display type, big flat colour blocks, strong
  pillar colours, energetic.
- **B, "Folha de sala":** like a printed programme. Editorial serif, warm paper tone,
  generous spacing, restrained colour accents.
- **C, "Bilhete":** like tickets. Each opportunity is a ticket stub (a perforated edge drawn
  with dashed borders, a "stub" holding the deadline), playful and colourful.

I'll choose one (or mix), then we refine it.

## Sample content (this week's real issue)
Use this exact content, so the mockups show real lengths and real pt-PT.

**Header:** N.º 1 · 5 out 2026 · "Oportunidades para atores em Portugal. Esta semana: 10 novas,
2 a fechar."

**Últimos dias**
- *Publicidade · Novo · Norte*: **Locução para rádio e publicidade (nível I) — Conservatório
  Vocare** · Conservatório Vocare · "Curso certificado de 16 horas sobre locução de rádio,
  comercial e institucional, com gravação final, no Porto." · Porto · chip: "Começa a 10 out"
- *Teatro · Novo · Nacional*: **Prática somática para intérpretes — workshop online (10
  sessões)** · Teresa Prima · "Percurso de 10 sessões online de movimento somático e prática
  expressiva para artistas e intérpretes residentes em Portugal, às segundas à noite." ·
  Online · 102 € · chip: "Começa a 12 out"

**Teatro · Cinema · Televisão · Publicidade:** "Sem novidades esta semana."

**Dobragem**
- *Dobragem · Novo · Nacional*: **Vozes em português europeu — gravação para curso online de
  língua** · Quinza · "Procuram-se vozes masculinas e femininas com dicção clara para gravar
  cerca de mil frases curtas para um curso de português para estrangeiros, em Lisboa ou em
  casa." · Lisboa ou à distância · Cerca de 4–6 € por minuto de áudio final · chip:
  "Candidaturas até 23 out"

**Formação**
- *Teatro · Novo · Centro*: **Oficina de teatro documental — Lisboa** · Razões Pessoais ·
  "Oficina intensiva de cinco dias sobre teatro documental, devising, improvisação e
  autobiografia, aberta a profissionais e não profissionais, em Lisboa." · Lisboa · 55 € ·
  chip: "Candidaturas até 14 out"
- *Teatro · Novo · Centro*: **Workshop de Practical Aesthetics — ACT Escola de Actores** · ACT
  Escola de Actores · "Introdução à técnica de representação Practical Aesthetics, em três
  sessões (12 h) para atores maiores de 17 anos, em Lisboa." · Lisboa · 90 € · chip: "Começa
  a 16 out"
- *Teatro · Novo · Norte*: **O Ator Imaginário — oficina intensiva de 15 horas em Gaia** ·
  Aurora Criativa · "Oficina intensiva de representação de 15 horas num fim de semana, em Vila
  Nova de Gaia, limitada a 20 participantes." · Vila Nova de Gaia · 200 € · chip: "Candidaturas
  até 4 nov"

**Apoios e oportunidades**
- *Teatro · Novo · Nacional*: **Programa IETM Global Connect 2027 para profissionais das artes
  performativas** · IETM · "Seleção de 10 profissionais das artes performativas com mais de
  cinco anos de experiência: adesão ao IETM por cinco anos, sessões online e apoio para ir à
  Assembleia Geral de 2027." · Online e Chipre · Só despesas · chip: "Candidaturas até 15 out"
- *Teatro · Novo · Nacional*: **Festival Teatri Riflessi 2027 — open call para peças curtas** ·
  Festival Teatri Riflessi · "Open call para obras ao vivo até 15 minutos a apresentar na
  Sicília em julho de 2027, com prémios entre 500 e 1 200 €." · Zafferana Etnea, Itália ·
  chip: "Candidaturas até 15 out"
- *Teatro · Novo · Nacional*: **Fundo Europeu de Festivais para Artistas Emergentes (EFFEA
  #5)** · European Festivals Association · "Apoio a projetos de residência de artistas
  emergentes em festivais europeus, incluindo teatro, circo e teatro musical." · Europa ·
  chip: "Candidaturas até 3 nov"

**Candidaturas permanentes** (compact list)
- Candidatura espontânea a elencos — Plural Entertainment

**Footer:** "Cada oportunidade é resumida por nós e revista antes de seguir. Os detalhes, as
condições e a candidatura estão sempre na página original." Sources: A Televisão, ACT Escola
de Actores, Coffeepaste, Conservatório Vocare, DGArtes, Fundação GDA, enCAST.pro, Plural
Entertainment, Portugal Film Commission, Teatro Nacional D. Maria II, Teatro Nacional São
João, Teatro São Luiz, Zapping-TV, MAGG.

Also show **one dense case**: a pillar section with 6 cards, to check how a long issue reads.

## What to deliver
**Round 1:** the three directions as full mockups (desktop and phone).

**After I choose:** a small **email design system** for that direction:
1. **Colour tokens** as hex values: the 5 pillars, plus Últimos dias, Formação, Apoios, No
   radar, text, muted text, background, card, and border. Include the contrast ratio for each
   text-on-background pair.
2. **Typography:** the font stack for headings and body (with fallbacks), sizes and line
   heights for each text style, desktop and phone.
3. **Spacing and shape:** paddings, card radius, border widths, button size.
4. **Components**, each as a **table-based HTML snippet with inline styles**: header, section
   title, empty-section line, card (with every badge type and each chip state), button, link
   list, and footer.
5. A **dark-mode note:** what changes or must be avoided.

Those snippets will be dropped into a Jinja template, so please keep repeated values
identical (same hex, same sizes) and avoid one-off tweaks.
