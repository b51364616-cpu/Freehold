# Freehold — your business website

Four pages (Home, Work, Pricing, Privacy) plus the Hush demo living inside it under `/demos/hush/`.
The Kingpin and Tessera demos run on their own Netlify sites, and the Work page links straight to them.
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
| `pricing.freehold` | The one-off price and its deposit percentage. The deposit and balance are worked out from these |
| `pricing.managed` | The subscription's startup fee, its deposit percentage, the monthly fee and the small changes included each month. The deposit, the balance and the first-year total are worked out from these |
| `pricing` (the rest) | Pages included, the price of an extra page, and the hourly rate |
| `phone`, `email` | Used by the mobile menu and the quote form (they're also written into the pages) |

The pages also have the prices written into them, so they show correctly before the script runs.
If you change a price, change it in `PRICE` at the top of `build.py` as well and run `python3 build.py`,
or send me the change and I'll regenerate the pages.

Wording on the pages lives in the `.html` files, which `build.py` generates.
(`build.py` is the generator I use to build them. It's harmless to leave in the repo.)

## The quote form

Quote requests go through **Netlify Forms**, which is free and needs no other account.

1. After the first deploy, open the project in Netlify → **Forms**. If it asks you to enable form detection,
   do it, then **Deploys → Trigger deploy**. A form called **quote** should appear.
2. **Project configuration → Notifications → Form submission notifications → Add notification → Email notification.**
   Pick the **quote** form and enter connor@freeholdweb.com.au.
3. Send yourself a test from the live site with realistic details (Netlify quietly drops obvious test data as spam).
   The email's subject names the business, a one-line summary comes first, and **Reply** goes to the customer.

## The demos

- **Kingpin Automotive** (mechanic) → https://kingpinauto.netlify.app/
- **Tessera Tiling Co.** (tiler) → https://tesseratiling.netlify.app/
- **Hush Home Cleaning** (cleaner) → `/demos/hush/`, with its practice editor (passcode 5829).
  Edits save in the visitor's own browser only; **Publish** won't work there, on purpose.

Kingpin's and Tessera's editors are locked to the owner's passphrase, so the Work page says you'll walk
people through them rather than giving out a passcode.

The old Ironbark and Copperline demos are gone from this folder. `netlify.toml` sends anyone with an old
`/demos/ironbark/` or `/demos/copperline/` link to the new mechanic or tiler demo. If those two folders are
still in your GitHub repo, you can delete them there (open the folder → the **⋯** menu → **Delete directory**),
along with the old `ironbark-*` and `copperline-*` files in `assets`. Leaving them does no harm either.

`netlify.toml` also stops Google listing the demo pages.

## Updating the live site

On GitHub, **Add file → Upload files**, drag in everything from this folder again and commit.
Files with the same name are replaced, and Netlify redeploys on its own within a minute.

## Animations on calm devices

If a visitor's device has "reduce motion" switched on, the site starts calm and shows a small
"Show them" prompt. Anyone can switch animations on or off from the link in the footer.
In calm mode the home page scene doesn't build itself or move with the scroll; it just shows each layer.
