# Velaa Getaways: website (English + Russian)

This is a fast static website. It runs on any web host (Netlify, Vercel, Cloudflare Pages, cPanel hosting or GitHub Pages) and needs no database.

```
index.html … contact.html      English pages (site root)
ru/*.html                      Russian pages (same layout)
assets/css/site.css, fonts.css   Design system (v3) and self-hosted fonts
assets/js/app.js               All interactions (slideshow, modals, filters, multi-step enquiry)
assets/img                     Optimised WebP photos (+ guests/ portraits)
assets/brand                   Client logo: emblem.png / emblem-256.png (round mark), logo-full.png (+ -web), favicons
assets/fonts                   Self-hosted Cormorant Garamond + Manrope (Latin + Cyrillic)
sitemap.xml, robots.txt        For SEO (with EN/RU hreflang)
build/                         Generator: edit content here, then rebuild
```

## Editing text, prices or contacts
1. Edit `build/content.py`. It holds all English and Russian copy, prices, reviews and the `CONFIG` block (domain, e-mail, WhatsApp, Instagram, hero video, verification codes).
2. Run `python3 build/build.py` (needs Python 3 and Pillow: `pip install pillow`).
3. Upload the whole folder, except `build/`, to your host.

## Before going live: checklist
- [ ] **Domain**: set `site_url` in `CONFIG` if it is not `https://www.velaagetaways.com`, then rebuild.
- [ ] **Activate the enquiry form.** The form posts to FormSubmit (formsubmit.co), which forwards it to **sales@velaagetaways.com**. FormSubmit sends a one-time *activation e-mail* to that inbox after the first submission. Click the link in it. Until then, enquiries are not delivered.
- [ ] **Replace the draft reviews.** The 10 reviews in `REVIEWS` and their portraits (randomuser.me placeholders) are drafts for layout only. Publishing invented reviews breaks consumer-protection law in the EU, UK and Russia, and Google and Yandex policies. Swap in real guest reviews, with their permission, before launch.
- [ ] **Founders photo.** The About section shows "D / J" monograms over a beach photo. Add a real photo of Dhaain & Julia when available.
- [ ] **Estimated price in the enquiry form** uses package price × adults by season (Apr–Oct / Nov–Mar from the arrival date). Children show as "on request".
- [ ] **Hero video (optional).** Put an aerial clip at `assets/video/hero.mp4`, keep it short (15–30 s, under 8 MB, muted), then set `hero_video` in `CONFIG`.
- [ ] **Search engines.** Add the site to Google Search Console and **Yandex Webmaster** (important for Russia). Paste the verification codes into `CONFIG`, rebuild, and submit `sitemap.xml` in both.
- [ ] **Social media**: add Instagram / Facebook / Telegram / TikTok / Tripadvisor URLs in `CONFIG` — each icon appears automatically (header, menu, footer) once its link is set. WhatsApp, e-mail and phone are already live.

## Content points to confirm with the client
- **Seasonal prices.** The brochure lists November–March prices as **€** in the summary table but **$** on the package pages. The site shows **$** everywhere ($690 / $990 / $1,550).
- **Comparison table.** It now follows the detailed inclusion lists. Ocean Explorer *includes* the dolphin cruise and jetski, as its own list says, although the brochure table showed "—". "Group photography" and "+ lunch" appeared only in the brochure table, so they were left out.
- **Signature meals.** Described as **half board** (breakfast and dinner), as in its inclusion list. The brochure footnote said "full-board".

## SEO built in
- Separate EN and RU pages, each with its own keyword-focused `<title>` and meta description, canonical URL and `hreflang` (en / ru / x-default).
- Structured data (JSON-LD): TravelAgency, WebSite, BreadcrumbList, TouristTrip offers with seasonal prices, FAQPage, TouristDestination and TouristAttraction list.
- Open Graph and Twitter cards with a 1200×630 share image.
- `sitemap.xml` with language alternates, `robots.txt` and a web manifest.
- Speed: WebP images with responsive `srcset`, lazy loading, fixed image sizes (no layout shift), self-hosted fonts (no Google Fonts dependency, which can be unreliable from Russia), and no frameworks.
- When a visitor's browser language is Russian, Ukrainian, Belarusian or Kazakh, a small banner suggests the Russian version. It does not auto-redirect, which is better for SEO.

## Photo credits
The scenery photos are from Unsplash (free for commercial use, no attribution required). The guesthouse photos come from the client's concept document.
