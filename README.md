# Freehold — your business website

Four pages (Home, Work, Pricing, Privacy) plus the three demo sites living inside it under `/demos/`.
No database, no build step, no environment variables. Upload it and it runs.

## Putting it online

1. On GitHub, create a new repo (e.g. `freehold-site`).
2. **Add file → Upload files.** Open this folder, select **everything inside it** (not the folder itself)
   and drag it all in at once. Commit.
3. Check the repo's top level shows `index.html`, `styles.css`, `main.js`, `netlify.toml`,
   and the `assets` and `demos` folders. If you only see one folder, it went in a level too deep.
4. Netlify → **Add new project → Import an existing project → GitHub** → pick the repo → **Deploy**.
   Nothing to fill in; `netlify.toml` handles the settings.

## Changing things

Open `main.js`. Everything you're likely to change is in the `SITE` block at the very top:

| Setting | What it does |
|---|---|
| `phone`, `email` | Used by the menu and quote form (they're also written into the pages) |
| `abn` | Add your ABN and it shows in the footer on every page |
| `formKey` | Free key from web3forms.com. Blank = the quote form opens the visitor's email app instead |
| `pricing` | Every price on the Pricing page and in the estimator comes from here |

Wording on the pages lives in the `.html` files. Easiest route: send me the change and I'll regenerate the pages.
(`build.py` is the generator I use to build them. It's harmless to leave in the repo.)

## Once you have a domain

In each page's `<head>`, change `content="/assets/og.jpg"` to the full address
(e.g. `https://freehold.com.au/assets/og.jpg`) so Facebook shows the preview image.

## About the demos

- Links on the Work page open `/demos/ironbark/`, `/demos/copperline/` and `/demos/hush/`.
- Their booking forms show a success message but don't send anything.
- Prospects can try each editor (passcodes 4060, 4171, 5829). Edits save in their own browser only;
  **Publish** won't work here, on purpose, so nobody can change the demos for everyone.
- `netlify.toml` stops Google listing the demo pages.
- If you still have the demos as separate Netlify projects, you can delete those to save credits.
