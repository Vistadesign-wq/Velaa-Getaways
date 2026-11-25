# -*- coding: utf-8 -*-
"""Velaa Getaways — static site generator (v3 design).
Run:  python3 build/build.py   → writes EN pages to ./ and RU pages to ./ru/"""
import json, os, re, html, datetime
from PIL import Image

import icons as _ic
from icons import icon
from brands import brand
from content import *
from countries import COUNTRIES, POPULAR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
C = CONFIG
SITE = C["site_url"].rstrip("/")
E = html.escape
_sz = {}

_ic.ICONS["phone"] = '<path d="M5 3.5h3.2l1.6 4-2 1.3a11 11 0 0 0 5.4 5.4l1.3-2 4 1.6V17a2.5 2.5 0 0 1-2.7 2.5C9.6 19 5 14.4 4.5 6.2A2.5 2.5 0 0 1 5 3.5z"/>'
_ic.ICONS["chevup"] = '<path d="M6 15l6-6 6 6"/>'
_ic.ICONS["chevdown"] = '<path d="M6 9l6 6 6-6"/>'
_ic.ICONS["plus"] = '<path d="M12 5v14M5 12h14"/>'
_ic.ICONS["grid"] = '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>'


def size(name):
    if name not in _sz:
        with Image.open(os.path.join(IMG, name)) as im:
            _sz[name] = im.size
    return _sz[name]


def img(name, alt="", sizes="100vw", eager=False, cls=""):
    big = f"{name}.webp"
    w, h = size(big)
    c = f' class="{cls}"' if cls else ""
    ld = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    if os.path.exists(os.path.join(IMG, f"{name}-sm.webp")):
        return (f'<img{c} src="{{R}}assets/img/{name}-sm.webp" srcset="{{R}}assets/img/{name}-sm.webp 900w, {{R}}assets/img/{big} {w}w" '
                f'sizes="{sizes}" alt="{E(alt)}" width="{w}" height="{h}" decoding="async"{ld}>')
    return f'<img{c} src="{{R}}assets/img/{big}" alt="{E(alt)}" width="{w}" height="{h}" decoding="async"{ld}>'


def url(lang, page):
    return f"{SITE}/{'' if lang == 'en' else 'ru/'}{'' if page == 'index' else page + '.html'}"


def href(lang, page, r):
    f = "index.html" if page == "index" else page + ".html"
    if r == "../":
        return f if lang == "ru" else "../" + f
    return f if lang == "en" else "ru/" + f


EMBLEM = '<span class="emblem"><img src="{R}assets/brand/emblem-256.png" alt="" width="256" height="229" decoding="async"></span>'

# ------------------------------------------------------------------ extra copy for v3 layouts
T3 = {
    "en": {
        "loc": "Thoddoo · Alif Alif Atoll · Maldives", "enquire": "Plan your trip",
        "explore": "Explore packages", "watch": "Plan your trip",
        "slides": ["Sandbank · North Ari Atoll", "Sandbar · Alif Alif", "Arrival by speedboat"],
        "book": {"arr": "Arrival", "dep": "Departure", "guests": "Guests", "pkg": "Package", "any": "Any package", "go": "Check availability"},
        "intro_label": "Welcome to Thoddoo",
        "statement": 'A real Maldivian island where <span class="kw">turtles</span> glide past the reef, <span class="kw">watermelons</span> ripen in the fields, <span class="kw">coconuts</span> hang from the palms&nbsp;— and you are welcomed <em>like&nbsp;a&nbsp;friend.</em>',
        "pillars": [("heart", "Hosted by locals", "Dhaain was born on Thoddoo — you see the island through the people who call it home."),
                    ("turtle", "The reef at your doorstep", "Step off the beach into clear water where turtles and reef fish live."),
                    ("tag", "Honest, clear prices", "All taxes included and every inclusion listed before you book.")],
        "trip": ["House reef", "Bikini beach", "Family guesthouses"],
        "pk_label": "Holiday packages", "pk_title": "Three ways to live <em>island life</em>",
        "pk_facts": [("calendar", "8&nbsp;days · 7&nbsp;nights"), ("bed", "Twin or double sharing"), ("users", "Per person · 2&nbsp;adults"), ("check", "All taxes included")], "pk_season": "Prices by season",
        "pk_lead": "8 days · 7 nights · twin or double sharing. Per person, 2 adults sharing, all taxes included.",
        "view": "View package", "book_now": "Book",
        "xp_label": "Experiences", "xp_title": "Moments made <em>by the ocean</em>",
        "xp_lead": "Swim with turtles, meet manta rays, follow dolphins at sunset — tap any experience for the details.",
        "xp_all": "All experiences",
        "nums": [("7", "", "nights in every package"), ("10", "+", "ocean experiences"), ("2", "", "bikini beaches"), ("28", "°C", "average sea temperature")],
        "why_label": "Why Velaa", "why_title": "Travel with people who <em>call this home</em>",
        "why_badge": ("Velaa — sea turtle", "our name in Dhivehi"),
        "th_label": "The island", "th_title": "Thoddoo, the <em>green side</em> of the Maldives",
        "th_facts": [("leaf", "Papaya & watermelon farms"), ("beach", "Two bikini beaches"), ("turtle", "Reef close to shore"), ("bicycle", "Walk or cycle everywhere")],
        "th_more": "Discover Thoddoo",
        "f_label": "Our story", "story": "Read our story",
        "t_label": "Guest stories", "t_title": "Five-star <em>memories</em>", "t_sub": "average guest rating",
        "strip_label": "Island days", "strip_title": "A week that feels like <em>a lifetime</em>",
        "cta_label": "Your island is waiting",
        "f_news": "Ready for your <em>island escape?</em>", "f_cols": ["Explore", "Help", "Contact"],
        "gal": "Gallery", "cat_all": "All",
        "cats": {"U": "Underwater", "W": "On the water", "I": "Island life", "M": "Special moments"},
        "steps": ["Your escape", "Dates & guests", "Experiences", "Your details"],
        "st_t": ["Which escape speaks to you?", "When are you coming?", "Anything you’d love to add?", "Where should we send your plan?"],
        "st_p": ["Choose a package — or let us suggest one.", "Approximate dates are fine; we’ll confirm availability.",
                 "Select any experiences you’d like included or quoted.", "We reply personally, usually within a few hours."],
        "not_sure": ("Not sure yet", "Advise me"), "exc_only": ("Excursions only", "No package"),
        "adults": "Adults", "children": "Children (2–12)",
        "reply": "Reply by", "next": "Continue", "back": "Back", "send": "Send enquiry", "send_wa": "Send via WhatsApp",
        "consent": "By sending, you agree that we use your details only to reply to this enquiry.",
        "s_dates": "Dates", "s_nights": "Nights", "s_guests": "Guests", "s_xp": "Experiences",
        "s_total": "Estimated total", "s_note": "per person × adults · {season}. Final quote confirmed by our team.",
        "s_quote": "Personal quote", "s_none": "—", "s_kids": "children on request",
        "done_t": "Thank you — your island plan is on its way", "done_p": "We’ve received your enquiry and will reply personally by e-mail or WhatsApp, usually within a few hours.",
        "done_b": "Back to home", "season_low": "April–October", "season_high": "November–March",
    },
    "ru": {
        "loc": "Тодду · атолл Алиф Алиф · Мальдивы", "enquire": "Спланировать поездку",
        "explore": "Смотреть туры", "watch": "Спланировать поездку",
        "slides": ["Песчаная отмель · Северный Ари", "Песчаная коса · Алиф Алиф", "Прибытие на скоростном катере"],
        "book": {"arr": "Прилёт", "dep": "Вылет", "guests": "Гостей", "pkg": "Тур", "any": "Любой тур", "go": "Проверить даты"},
        "intro_label": "Добро пожаловать на Тодду",
        "statement": 'Настоящий мальдивский остров, где у&nbsp;рифа неспешно проплывают <span class="kw">черепахи</span>, на полях зреют <span class="kw">арбузы</span>, на пальмах висят <span class="kw">кокосы</span>, а&nbsp;вас встречают <em>как&nbsp;друга.</em>',
        "pillars": [("heart", "Местные хозяева", "Дхаин родился на Тодду — вы увидите остров глазами тех, для кого он дом."),
                    ("turtle", "Риф у порога", "С пляжа — сразу в прозрачную воду, где живут черепахи и рифовые рыбы."),
                    ("tag", "Честные, понятные цены", "Все налоги включены, а состав тура известен до бронирования.")],
        "trip": ["Домашний риф", "Бикини-пляж", "Семейные гестхаусы"],
        "pk_label": "Туры", "pk_title": "Три способа прожить <em>островную жизнь</em>",
        "pk_facts": [("calendar", "8&nbsp;дней · 7&nbsp;ночей"), ("bed", "Twin или double"), ("users", "За человека · 2&nbsp;взрослых"), ("check", "Все налоги включены")], "pk_season": "Цены по сезонам",
        "pk_lead": "8 дней · 7 ночей · twin или double. Цена за человека при размещении 2 взрослых, все налоги включены.",
        "view": "Подробнее", "book_now": "Забронировать",
        "xp_label": "Впечатления", "xp_title": "Моменты, подаренные <em>океаном</em>",
        "xp_lead": "Плавайте с черепахами, встречайте мант, наблюдайте за дельфинами на закате — нажмите на карточку, чтобы узнать больше.",
        "xp_all": "Все впечатления",
        "nums": [("7", "", "ночей в каждом туре"), ("10", "+", "морских впечатлений"), ("2", "", "бикини-пляжа"), ("28", "°C", "средняя температура воды")],
        "why_label": "Почему Velaa", "why_title": "Путешествуйте с теми, для кого <em>это дом</em>",
        "why_badge": ("Велаа — морская черепаха", "наше имя на языке дивехи"),
        "th_label": "Остров", "th_title": "Тодду — <em>зелёная сторона</em> Мальдив",
        "th_facts": [("leaf", "Фермы папайи и арбузов"), ("beach", "Два бикини-пляжа"), ("turtle", "Риф у самого берега"), ("bicycle", "Пешком или на велосипеде")],
        "th_more": "Открыть Тодду",
        "f_label": "Наша история", "story": "Читать нашу историю",
        "t_label": "Истории гостей", "t_title": "Воспоминания <em>на пять звёзд</em>", "t_sub": "средняя оценка гостей",
        "strip_label": "Островные дни", "strip_title": "Неделя, которая запомнится <em>на всю жизнь</em>",
        "cta_label": "Ваш остров ждёт",
        "f_news": "Готовы к <em>островному отдыху?</em>", "f_cols": ["Разделы", "Помощь", "Контакты"],
        "gal": "Галерея", "cat_all": "Все",
        "cats": {"U": "Под водой", "W": "На воде", "I": "Островная жизнь", "M": "Особые моменты"},
        "steps": ["Ваш отдых", "Даты и гости", "Впечатления", "Контакты"],
        "st_t": ["Какой отдых вам ближе?", "Когда вы приедете?", "Что добавить в поездку?", "Куда отправить ваш план?"],
        "st_p": ["Выберите тур — или мы подскажем.", "Подойдут примерные даты — мы подтвердим наличие.",
                 "Отметьте впечатления, которые хотите добавить или узнать их стоимость.", "Мы отвечаем лично, обычно в течение нескольких часов."],
        "not_sure": ("Пока не знаю", "Посоветуйте"), "exc_only": ("Только экскурсии", "Без тура"),
        "adults": "Взрослые", "children": "Дети (2–12)",
        "reply": "Как ответить", "next": "Далее", "back": "Назад", "send": "Отправить заявку", "send_wa": "Отправить в WhatsApp",
        "consent": "Отправляя заявку, вы соглашаетесь, что мы используем ваши данные только для ответа на неё.",
        "s_dates": "Даты", "s_nights": "Ночей", "s_guests": "Гостей", "s_xp": "Впечатления",
        "s_total": "Ориентировочно", "s_note": "за человека × взрослые · {season}. Точную стоимость подтвердит наша команда.",
        "s_quote": "Индивидуальный расчёт", "s_none": "—", "s_kids": "дети — по запросу",
        "done_t": "Спасибо! Мы уже начали планировать ваш отдых", "done_p": "Мы получили вашу заявку и ответим лично по e-mail или в WhatsApp, обычно в течение нескольких часов.",
        "done_b": "На главную", "season_low": "апрель–октябрь", "season_high": "ноябрь–март",
    },
}
XP_CAT = {"turtle": "U", "reef": "U", "halfday": "U", "fullday": "U", "whaleshark": "U", "fishing": "W", "dolphin": "W",
          "hopping": "W", "octopus": "I", "resort": "I", "more": "I", "photoshoot": "M", "drone": "M", "dinner": "M", "watersports": "M"}
PKG_GALLERY = {"essential": ["thoddoo-beach", "turtle", "palm-road-aerial"], "ocean": ["ocean-jetski", "manta-snorkel", "dolphin"],
               "signature": ["photoshoot", "beach-dinner", "sunset-fishing"]}
PKG_GAL_CAP = {"en": {"turtle": "Turtle snorkelling", "palm-road": "Palm Road drone video", "dolphin": "Dolphin cruise", "jetski": "Jetski + drone video",
                      "resort": "Resort day visit", "sunset-fishing": "Sunset fishing"},
               "ru": {"turtle": "Снорклинг с черепахами", "palm-road": "Видео с дрона", "dolphin": "Дельфины", "jetski": "Гидроцикл + дрон",
                      "resort": "День на курорте", "sunset-fishing": "Закатная рыбалка"}}
STRIP = {"en": [("turtle", "Turtle mornings"), ("hero-sandbar", "Sandbank afternoons"), ("guesthouse-6", "Island homes"), ("sunset-fishing", "Sunset fishing"),
                ("vaau-magu", "Vaau Magu"), ("whale-shark", "Gentle giants"), ("beach-dinner", "Candlelit dinners"), ("palm-road-aerial", "Palm roads"), ("thoddoo-aerial", "Thoddoo"), ("dolphin", "Dolphin seas"), ("papaya", "Island papaya")],
         "ru": [("turtle", "Утро с черепахами"), ("hero-sandbar", "Песчаные отмели"), ("guesthouse-6", "Островной дом"), ("sunset-fishing", "Закатная рыбалка"),
                ("vaau-magu", "Ваау Магу"), ("whale-shark", "Добрые великаны"), ("beach-dinner", "Ужин при свечах"), ("palm-road-aerial", "Пальмовые аллеи"), ("thoddoo-aerial", "Тодду"), ("dolphin", "Встреча с дельфинами"), ("papaya", "Островная папайя")]}


def socials(light=False):
    out = f'<a data-b="whatsapp" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener" aria-label="WhatsApp">{brand("whatsapp")}</a>'
    for k, lab in (("instagram", "Instagram"), ("facebook", "Facebook"), ("telegram", "Telegram"), ("tiktok", "TikTok"), ("tripadvisor", "Tripadvisor")):
        if C.get(k):
            out += f'<a data-b="{k}" href="{C[k]}" target="_blank" rel="noopener" aria-label="{lab}">{brand(k)}</a>'
    out += f'<a data-b="mail" href="mailto:{C["email"]}" aria-label="E-mail">{icon("mail")}</a>'
    out += f'<a data-b="phone" href="tel:{C["phone_tel"]}" aria-label="Phone">{icon("phone")}</a>'
    return f'<div class="social{" social--light" if light else ""}">{out}</div>'


# ================================================================== chrome
def header(lang, page, r):
    U = UI[lang]; T = T3[lang]
    links = "".join(f'<li><a href="{href(lang, p, r)}"{" aria-current=\"page\"" if p == page else ""}>{U["nav"][p]}</a></li>'
                    for p in ["about", "packages", "thoddoo", "experiences", "guesthouses", "faq"])
    lang_sw = (f'<div class="lang"><a href="{href("en", page, r)}" hreflang="en" lang="en"{" class=\"on\"" if lang == "en" else ""}>EN</a>'
               f'<a href="{href("ru", page, r)}" hreflang="ru" lang="ru"{" class=\"on\"" if lang == "ru" else ""}>RU</a></div>')
    mini = f'<a href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener" aria-label="WhatsApp">{brand("whatsapp")}</a>'
    for k in ("instagram", "facebook", "telegram", "tiktok"):
        if C.get(k):
            mini += f'<a href="{C[k]}" target="_blank" rel="noopener" aria-label="{k}">{brand(k)}</a>'
    brand_html = (f'<a class="brand" href="{href(lang, "index", r)}" aria-label="Velaa Getaways">{EMBLEM}'
                  f'<span class="brand__txt"><span class="brand__name">VELAA</span><span class="brand__sub">Getaways</span><span class="brand__tag">{U["tagline"]}</span></span></a>')
    dl = "".join(f'<a href="{href(lang, p, r)}">{U["nav"][p]}</a>'
                 for i, p in enumerate(["index", "about", "packages", "thoddoo", "experiences", "guesthouses", "faq", "contact"]))
    return f'''<a class="sr-only skip" href="#main">{U["skip"]}</a>
<div class="pre" aria-hidden="true"><div class="pre__in">{EMBLEM}<i></i></div></div>
<div class="progress" aria-hidden="true"></div>
<div class="topbar"><div class="wrap">
    <span class="topbar__l">{icon("pin")}{T["loc"]}</span>
    <div class="topbar__r">
      <a href="tel:{C["phone_tel"]}">{icon("phone")}{C["phone_display"]}</a>
      <a href="mailto:{C["email"]}">{icon("mail")}{C["email"]}</a>
      <span class="mini-social">{mini}</span>
    </div>
  </div></div>
<header class="hdr">
  <div class="nav-row"><div class="wrap">
    {brand_html}
    <nav aria-label="Main"><ul class="menu">{links}</ul></nav>
    <div class="hdr__right">
      {lang_sw}
      <a class="btn btn--gold btn--sm" href="{href(lang, "contact", r)}">{T["enquire"]} {icon("arrow")}</a>
      <button class="burger" data-open aria-label="{U["menu"]}" aria-expanded="false">{icon("menu")}</button>
    </div>
  </div></div>
</header>
<div class="drawer" aria-label="{U["menu"]}">
  <div class="drawer__top">{brand_html}<button class="drawer__close" data-close aria-label="{U["close"]}">{icon("x")}</button></div>
  <nav>{dl}</nav>
  <div class="drawer__foot">{lang_sw}{socials(light=True)}<a class="btn btn--gold btn--block" href="{href(lang, "contact", r)}">{U["plan"]}</a></div>
</div>'''


def footer(lang, page, r):
    U = UI[lang]; T = T3[lang]
    ex = "".join(f'<li><a href="{href(lang, p, r)}">{U["nav"][p]}</a></li>' for p in ["about", "packages", "thoddoo", "experiences", "guesthouses"])
    hp = "".join(f'<li><a href="{href(lang, p, r)}">{U["nav"][p]}</a></li>' for p in ["faq", "contact"])
    other = "ru" if lang == "en" else "en"
    langs = "Languages" if lang == "en" else "Языки"
    reply = "Reply time" if lang == "en" else "Время ответа"
    reply_v = "Usually within a few hours" if lang == "en" else "Обычно в течение нескольких часов"
    tag = U["tagline"]
    cta_p = U["cta_lead"]
    lang_sw = (f'<div class="lang lang--dark"><a href="{href("en", page, r)}" hreflang="en" lang="en"{" class=\"on\"" if lang == "en" else ""}>EN</a>'
               f'<a href="{href("ru", page, r)}" hreflang="ru" lang="ru"{" class=\"on\"" if lang == "ru" else ""}>RU</a></div>')
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr__cta">
      {img("thoddoo-sunset", "", "100vw")}
      <div class="ftr__cta-in"><span class="label"><i></i>{T["cta_label"]}</span><h3>{T["f_news"]}</h3><p>{cta_p}</p></div>
      <div class="ftr__cta-btns"><a class="btn btn--gold" href="{href(lang, "contact", r)}">{U["plan"]} {icon("arrow")}</a>
        <a class="btn btn--glass" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} WhatsApp</a></div>
    </div>
    <div class="ftr__grid">
      <div class="ftr__brand">
        <a class="ftr__mark" href="{href(lang, "index", r)}" aria-label="Velaa Getaways">{EMBLEM}
          <span class="brand__txt"><span class="brand__name">VELAA</span><span class="brand__sub">Getaways</span></span></a>
        <p class="ftr__tag">“{tag}”</p>
        <p>{U["footer_about"]}</p>
        {socials(light=True)}
      </div>
      <nav class="ftr__col" aria-label="{T["f_cols"][0]}"><h4>{T["f_cols"][0]}</h4><ul>{ex}</ul></nav>
      <nav class="ftr__col" aria-label="{T["f_cols"][1]}"><h4>{T["f_cols"][1]}</h4><ul>{hp}</ul></nav>
      <div class="ftr__col ftr__contact"><h4>{T["f_cols"][2]}</h4>
        <a href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener"><span class="fi fi--wa">{brand("whatsapp")}</span><span><small>WhatsApp</small>{C["phone_display"]}</span></a>
        <a href="mailto:{C["email"]}"><span class="fi">{icon("mail")}</span><span><small>E-mail</small>{C["email"]}</span></a>
        <div><span class="fi">{icon("pin")}</span><span><small>{"Location" if lang == "en" else "Где мы"}</small>{U["footer_addr"]}</span></div>
      </div>
    </div>
    <div class="ftr__bot">
      <span>© <span data-year>2026</span> Velaa Getaways · {U["rights"]}</span>
      <span class="ftr__lang"><small>{langs}</small>{lang_sw}</span>
    </div>
  </div>
</footer>
<div class="fab"><span>{U["wa"]}</span><a href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener" aria-label="{U["wa"]}">{brand("whatsapp")}</a></div>
<div class="lhint" role="dialog" aria-live="polite"><span lang="{other}">{UI[other]["lang_hint"]}</span><a href="{href(other, page, r)}" lang="{other}">{UI[other]["lang_hint_go"]} →</a><button aria-label="{U["close"]}">×</button></div>
<div class="modal" id="modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="m-title">
  <div class="modal__bg" data-x></div>
  <div class="modal__p">
    <button class="modal__x" data-x aria-label="{U["close"]}">{icon("x")}</button>
    <div class="modal__m"><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt=""></div>
    <div class="modal__b"><div class="modal__ic"></div><span class="label m-kick"></span><h3 id="m-title"></h3><div class="modal__t"></div>
      <a class="btn btn--ink m-cta" href="#">{U["add"]} {icon("arrow")}</a></div>
  </div>
</div>'''


def label(text, num=None):
    n = f"<b>{num}</b>" if num else ""
    return f'<span class="label">{n}<i></i>{text}</span>'


def head(lbl, title, lead="", side="", center=False, num=None):
    lp = f'<p class="lead">{lead}</p>' if lead else ""
    sidecol = f'<div class="head__side">{lp}{side}</div>' if (lead or side) else ""
    return f'<div class="head{" head--c" if center else ""} rv"><div>{label(lbl, num)}<h2>{title}</h2></div>{sidecol}</div>'


def arrow_link(text, link):
    return f'<a class="arrow-link" href="{link}">{text}<span>{icon("arrow")}</span></a>'


def stars():
    return '<span class="stars" aria-label="5/5">' + icon("star") * 5 + "</span>"


def season_switch(lang):
    U = UI[lang]
    return (f'<div class="season" role="group"><span class="knob"></span><button class="on" data-season="low" aria-pressed="true">{U["season_low"]}</button>'
            f'<button data-season="high" aria-pressed="false">{U["season_high"]}</button></div>')


def xp_card(lang, r, item, extra_cls=""):
    title, short, detail = item[lang]
    T = T3[lang]; cat = XP_CAT.get(item["key"], "I")
    cta = href(lang, "contact", r) + f'?exp={item["key"]}#enquiry'
    return f'''<button class="xp {extra_cls}" data-cat="{cat}" data-modal data-img="{{R}}assets/img/{item["img"]}.webp" data-title="{E(title)}" data-kicker="{E(T["cats"][cat])}" data-cta="{cta}" aria-haspopup="dialog">
  {img(item["img"], title, "(max-width:900px) 50vw, 33vw")}
  <span class="xp__ico">{icon(item["icon"])}</span><span class="xp__plus">{icon("plus")}</span>
  <span class="xp__body"><span class="xp__cat">{T["cats"][cat]}</span><h3>{title}</h3><span class="xp__short">{short}</span></span>
  <span class="xp__detail"><p>{detail}</p></span>
</button>'''


def face(rv, name):
    """Real guest photo if assets/img/guests/<img>.webp exists (use only with the guest's consent);
    otherwise the guest's initials in a gold circle."""
    if os.path.exists(os.path.join(IMG, "guests", rv["img"] + ".webp")):
        return f'<img src="{{R}}assets/img/guests/{rv["img"]}.webp" alt="{E(name)}" width="56" height="56" loading="lazy">'
    return f'<span class="rvw__mono" aria-hidden="true">{"".join(w[0] for w in name.split()[:2])}</span>'


def testimonials(lang, r):
    T = T3[lang]
    cards = ""
    for rv in REVIEWS:
        name, place, text = rv[lang]
        cards += (f'<figure class="rvw">{stars()}<blockquote>{text}</blockquote>'
                  f'<figcaption>{face(rv, name)}'
                  f'<span><strong>{name}</strong><small><i class="flag flag--{rv["flag"]}"></i>{place} · {rv["pkg"]}</small></span></figcaption></figure>')
    return f'''<!-- DRAFT REVIEWS: replace with genuine guest reviews before launch -->
<section class="sec--s sec--ink on-dark tst-sec" aria-labelledby="t-title">
  <div class="wrap">
    <div class="tst__head rv">{label(T["t_label"])}<h2 id="t-title">{T["t_title"]}</h2>
      <span class="tst__badge"><b>5.0</b>{stars()}<small>{T["t_sub"]}</small></span></div>
    {carousel(lang, cards, 2, "car--reviews", auto=True)}
  </div>
</section>'''


def cta(lang, r, image="sunset-sea"):
    U = UI[lang]; T = T3[lang]
    return f'''<div class="cta-wrap"><section class="cta rv">{img(image, "", "100vw")}
  <div class="cta__in on-dark">{label(T["cta_label"])}<h2>{U["cta_title"]}</h2><p class="lead">{U["cta_lead"]}</p>
    <div class="cta__btns"><a class="btn btn--gold" href="{href(lang, "contact", r)}">{icon("calendar")} {U["check"]}</a>
    <a class="btn btn--glass" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} {U["wa"]}</a></div></div>
</section></div>'''


def page_hero(lang, r, image, eyebrow, title, lead, page, full=False):
    U = UI[lang]
    alt = re.sub("<[^>]+>", "", title) + (" — Thoddoo, Maldives" if lang == "en" else " — Тодду, Мальдивы")
    return f'''<section class="phero phero--{page}{" phero--full" if full else ""}">{img(image, alt, "100vw", eager=True)}<div class="hero__shade"></div>
  <div class="wrap on-dark"><div><ol class="crumbs"><li><a href="{href(lang, "index", r)}">{U["breadcrumb_home"]}</a></li><li>{U["nav"][page]}</li></ol>
    <h1>{title}</h1></div><div>{label(eyebrow)}{lead if lead.startswith("<ul") else f'<p class="lead" style="margin-top:14px">{lead}</p>'}</div></div>
</section>'''


def why_list(lang):
    out = ""
    for i, w in enumerate(WHY):
        t, small, text = w[lang]
        out += (f'<details class="why__item"{" open" if i == 0 else ""}><summary><span class="why__n">0{i + 1}</span><span class="why__i">{icon(w["icon"])}</span>'
                f'<h3><small>{small}</small>{t}</h3><span class="why__t"></span></summary><p>{text}</p></details>')
    return f'<div class="why__list rv d1">{out}</div>'



WHY_IMG = ["couple-beach", "guesthouse-3", "turtle", "beach-dinner", "guesthouse-1"]


def why_cards(lang):
    out = ""
    for i, w in enumerate(WHY):
        t, small, text = w[lang]
        im = WHY_IMG[i]
        out += (f'<button class="wc rv d{i % 4 + 1}" data-modal data-img="{{R}}assets/img/{im}.webp" data-title="{E(t)}" data-kicker="{E(small)}" aria-haspopup="dialog">'
                f'<span class="wc__ring"><span class="wc__img">{img(im, t, "200px")}</span><span class="xp__ico">{icon(w["icon"])}</span></span>'
                f'<span class="wc__n">0{i + 1}</span><small>{small}</small><h3>{t}</h3>'
                f'<span class="wc__more">{UI[lang]["discover"]} {icon("plus")}</span>'
                f'<span class="xp__detail"><p>{text}</p></span></button>')
    return f'<div class="wcs">{out}</div>'


def strip(lang):
    T = T3[lang]
    figs = re.sub(r' srcset="[^"]*"', '', "".join(f'<figure>{img(n, c, "320px")}</figure>' for n, c in STRIP[lang]))
    return (f'<section class="sec--s" aria-label="{T["strip_label"]}"><div class="wrap">{head(T["strip_label"], T["strip_title"], center=True)}</div>'
            f'<div class="strip"><div class="strip__track">{figs}{figs.replace("<figure>", "<figure aria-hidden=\"true\">")}</div></div></section>')


# ------------------------------------------------------------------ carousel (client request: carousel style everywhere)
CAR_UI = {"en": ("Previous", "Next"), "ru": ("Назад", "Вперёд")}


def carousel(lang, items, per=3, cls="", auto=False):
    p, n = CAR_UI[lang]
    if "car--cards" in cls and "car--travel" not in cls:
        cls += " car--stage"
    return (f'<div class="car {cls}" data-car{" data-auto" if auto else ""} style="--per:{per}">'
            f'<div class="car__track" tabindex="0">{items}</div>'
            f'<div class="car__nav"><button class="navb" data-cprev aria-label="{p}">{icon("arrowl")}</button>'
            f'<div class="car__dots"></div><button class="navb" data-cnext aria-label="{n}">{icon("arrow")}</button></div></div>')


def pcard(lang, image, ic, title, short, detail="", kicker="", extra=""):
    """Photo card: picture + round icon badge + title + short text; opens a detail modal when it has detail."""
    more = f'<span class="lm__more">{UI[lang]["discover"]} {icon("arrow")}</span>' if detail else ""
    body = (f'<figure>{img(image, title, "(max-width:760px) 100vw, 820px")}</figure>'
            f'<span class="pc__ic">{icon(ic)}</span>'
            f'<span class="pc__b">{f"<small>{kicker}</small>" if kicker else ""}<h3>{title}</h3><p>{short}</p>{extra}{more}</span>')
    if detail:
        return (f'<button class="pc" data-modal data-img="{{R}}assets/img/{image}.webp" data-title="{E(title)}" data-kicker="{E(kicker)}" aria-haspopup="dialog">'
                f'{body}<span class="xp__detail"><p>{detail}</p></span></button>')
    return f'<div class="pc">{body}</div>'


INTRO_CARDS = [
    ("beach-walk", "heart",
     {"en": ("Hosted by locals", "Dhaain was born on Thoddoo — see the island through the people who call it home.",
             "Velaa is run by Dhaain, who grew up on Thoddoo, and Julia, who fell in love with it. We meet you, look after you and share the places only locals know — the quiet beach at sunrise, the best seafood dinner, the family farm with the sweetest papaya."),
      "ru": ("Местные хозяева", "Дхаин родился на Тодду — вы увидите остров глазами тех, для кого он дом.",
             "Velaa ведут Дхаин, выросший на Тодду, и Юлия, которая влюбилась в этот остров. Мы встречаем вас, заботимся о вас и показываем места, которые знают только местные: тихий пляж на рассвете, лучший ужин из морепродуктов, семейную ферму с самой сладкой папайей.")}),
    ("turtle-reef", "turtle",
     {"en": ("The reef at your doorstep", "Step off the beach into clear water where turtles and reef fish live.",
             "Thoddoo’s house reef lies just off the beach. Green and hawksbill turtles feed here most mornings, along with parrotfish, reef sharks and rays. Bring a mask — or join our guided turtle snorkel."),
      "ru": ("Риф у порога", "С пляжа — сразу в прозрачную воду, где живут черепахи и рифовые рыбы.",
             "Домашний риф Тодду начинается прямо у пляжа. По утрам здесь кормятся зелёные черепахи и черепахи-бисса, рыбы-попугаи, рифовые акулы и скаты. Возьмите маску — или присоединяйтесь к нашему снорклингу с черепахами.")}),
    ("papaya-lush", "leaf",
     {"en": ("The garden island", "Papaya, watermelon and bananas grow beneath the palms.",
             "Thoddoo is famous across the Maldives for its farms. Fresh papaya, watermelon, bananas and passion fruit are grown here and shipped to Malé and the resorts — and you taste them straight from the field at breakfast."),
      "ru": ("Остров-сад", "Под пальмами растут папайя, арбузы и бананы.",
             "Тодду знаменит на всех Мальдивах своими фермами. Здесь выращивают папайю, арбузы, бананы и маракуйю, которые отправляют в Мале и на курорты, — а вы пробуете их прямо с грядки за завтраком.")}),
    ("thoddoo-beach", "beach",
     {"en": ("White-sand beaches", "Two bikini beaches with soft sand and turquoise water.",
             "Thoddoo has two designated bikini beaches where you can swim and sunbathe freely, with palms for shade, a coral reef close to shore and some of the most beautiful sunsets in Ari Atoll."),
      "ru": ("Белоснежные пляжи", "Два бикини-пляжа с мягким песком и бирюзовой водой.",
             "На Тодду два бикини-пляжа, где можно свободно купаться и загорать: пальмы для тени, коралловый риф у самого берега и одни из самых красивых закатов атолла Ари.")}),
    ("seaplane", "plane",
     {"en": ("Easy to reach", "A shared speedboat from the airport — or the new seaplane in about 20 minutes.",
             "Thoddoo lies in North Ari Atoll, about 60–90 minutes from Velana International Airport by shared speedboat. Since February 2026 a scheduled seaplane also flies in about 20 minutes. We book your transfer and meet you on arrival."),
      "ru": ("Легко добраться", "Групповой катер из аэропорта — или новый гидросамолёт примерно за 20 минут.",
             "Тодду находится в атолле Северный Ари — 60–90 минут от аэропорта Велана на групповом скоростном катере. С февраля 2026 года сюда также летает гидросамолёт — около 20 минут. Мы бронируем трансфер и встречаем вас.")}),
    ("hammock-sunset", "tag",
     {"en": ("Honest, clear prices", "All taxes included — every inclusion listed before you book.",
             "Our packages show the full price per person with all Maldivian taxes included. You know exactly what is in your week before you pay — no hidden fees, no surprises on arrival."),
      "ru": ("Честные цены", "Все налоги включены — состав тура известен до бронирования.",
             "В наших турах указана полная цена за человека со всеми мальдивскими налогами. Вы точно знаете, что входит в вашу неделю, ещё до оплаты — без скрытых сборов и сюрпризов.")}),
]
INTRO_FACTS = {"en": [("pin", "fact-location", "Location", "North Ari Atoll"), ("boat", "fact-speedboat", "By speedboat", "60–90 min"), ("plane", "fact-seaplane", "By seaplane", "20 min"), ("sun", "fact-sea", "The sea", "28°C all year")],
               "ru": [("pin", "fact-location", "Где", "Атолл Северный Ари"), ("boat", "fact-speedboat", "На катере", "60–90 минут"), ("plane", "fact-seaplane", "На гидросамолёте", "20 минут"), ("sun", "fact-sea", "Море", "28 °C круглый год")]}
INTRO_LEAD = {"en": "Thoddoo is a small, green, real Maldivian island — farms and palm roads in the middle, white sand and coral reef all around. Here is what makes a week here special.",
              "ru": "Тодду — небольшой зелёный остров, настоящие Мальдивы: фермы и пальмовые аллеи в центре, белый песок и коралловый риф по краям. Вот что делает неделю здесь особенной."}


def intro_cards(lang):
    return "".join(pcard(lang, im, ic, d[lang][0], d[lang][1], d[lang][2], T3[lang]["intro_label"]) for im, ic, d in INTRO_CARDS)


RESTAURANTS = [
    {"img": "food-seafood-platter", "icon": "fish", "ig": "https://www.instagram.com/breezethoddoo/",
     "en": ("Breeze", "Seafood · sunset views", "Fresh seafood, beautiful moments and island atmosphere.",
            "A favourite for seafood platters, the grilled catch of the day and relaxed dinners by the sea as the sun goes down. Groups of five or more can pre-order a seafood feast — tell us and we arrange it."),
     "ru": ("Breeze", "Морепродукты · закаты", "Свежие морепродукты, красивые моменты и островная атмосфера.",
            "Любимое место для сетов из морепродуктов, улова дня на гриле и спокойных ужинов у моря на закате. Для групп от пяти человек можно заранее заказать морской пир — скажите нам, и мы всё организуем.")},
    {"img": "food-seafood-plate", "icon": "dinner",
     "en": ("Fishka", "Café · seafood", "Cosy, clean and loved for its grilled shrimps.",
            "A cosy, spotless café with a short, well-made menu: grilled shrimps, seafood fried rice, Maldivian rice and a fresh tuna tartare. Good coffee and friendly service."),
     "ru": ("Fishka", "Кафе · морепродукты", "Уютно, чисто и очень вкусные креветки на гриле.",
            "Уютное и чистое кафе с небольшим продуманным меню: креветки на гриле, жареный рис с морепродуктами, мальдивский рис и свежий тартар из тунца. Хороший кофе и приветливый сервис.")},
    {"img": "food-tuna-steak", "icon": "anchor",
     "en": ("Black Anchor", "Seafood · Mediterranean", "Tuna steaks, grilled reef fish and generous portions.",
            "Known for perfectly seared tuna steak, grilled reef fish and big Mediterranean-style plates. There is a kids’ menu, and the fresh mango drinks are a must."),
     "ru": ("Black Anchor", "Морепродукты · средиземноморская", "Стейки из тунца, рифовая рыба на гриле и большие порции.",
            "Славится идеально обжаренным стейком из тунца, рифовой рыбой на гриле и щедрыми средиземноморскими блюдами. Есть детское меню, а свежие манговые напитки — обязательно попробуйте.")},
    {"img": "food-curry-spread", "icon": "dinner",
     "en": ("Sun Sky", "Maldivian · Indian", "Fresh BBQ dinners and family-friendly prices.",
            "Home-style Maldivian and Indian cooking: fish curries, rice and roshi, plus a fresh barbecue in the evening. Relaxed, good value and popular with families."),
     "ru": ("Sun Sky", "Мальдивская · индийская", "Свежее барбекю на ужин и доступные цены.",
            "Домашняя мальдивская и индийская кухня: рыбные карри, рис и роши, а вечером — свежее барбекю. Спокойно, недорого и любимо семьями.")},
    {"img": "food-smoothies", "icon": "coffee",
     "en": ("Food Land", "Bakery · café", "Own bakery, coffee, cakes, juices and smoothies.",
            "Their own bakery means fresh bread and cakes every day, with good coffee, big portions and fresh fruit juices and smoothies made from Thoddoo’s farms."),
     "ru": ("Food Land", "Пекарня · кафе", "Своя пекарня, кофе, торты, соки и смузи.",
            "Собственная пекарня — свежий хлеб и выпечка каждый день, хороший кофе, большие порции, свежевыжатые соки и смузи из фруктов с ферм Тодду.")},
    {"img": "food-curry-roti", "icon": "leaf",
     "en": ("Taste real Maldivian food", "Local cuisine", "Garudhiya, mas huni with roshi and hedhikaa.",
            "Start the day like a local with mas huni — tuna, coconut and onion with warm roshi flatbread. Try garudhiya, the clear fish broth eaten with rice, lime and chilli, and hedhikaa, the island’s tea-time snacks. Sun Sky serves Maldivian curries, and many guesthouse hosts will cook a home-style Maldivian dinner on request — just ask us."),
     "ru": ("Настоящая мальдивская кухня", "Местная кухня", "Гарудия, мас хуни с роши и хедика.",
            "Начните день по-местному с мас хуни — тунец, кокос и лук с тёплой лепёшкой роши. Попробуйте гарудию — прозрачный рыбный бульон с рисом, лаймом и чили, и хедику — островные закуски к чаю. В Sun Sky готовят мальдивские карри, а многие хозяева гестхаусов по просьбе приготовят домашний мальдивский ужин — просто скажите нам.")},
]
REST_HEAD = {"en": ("Where to eat", "Thoddoo’s <em>favourite tables</em>", "Fresh seafood, island fruit and real Maldivian cooking — our guests’ favourite places to eat.",
                    "Photos show typical dishes, not the restaurants’ own. Opening times vary — ask us for today’s recommendations."),
             "ru": ("Где поесть", "Любимые <em>рестораны Тодду</em>", "Свежие морепродукты, островные фрукты и настоящая мальдивская кухня — любимые места наших гостей.",
                    "На фото — типичные блюда, а не фотографии ресторанов. Часы работы меняются — спросите нас о рекомендациях на сегодня.")}


def restaurants(lang):
    h = REST_HEAD[lang]
    cards = ""
    for x in RESTAURANTS:
        name, kick, short, det = x[lang]
        if x.get("ig"):
            det += f' <a href="{x["ig"]}" target="_blank" rel="noopener">Instagram @breezethoddoo</a>'
        cards += pcard(lang, x["img"], x["icon"], name, short, det, kick)
    return (f'<section class="sec" id="restaurants"><div class="wrap">{head(h[0], h[1], h[2])}'
            f'{carousel(lang, cards, 3, "car--cards")}<p class="note car__note">{h[3]}</p></div></section>')


TRAVEL = {
    "en": {"label": "Getting to Thoddoo", "title": "Three ways to <em>reach the island</em>",
           "lead": "Thoddoo lies in North Ari Atoll, west of Malé. Choose the journey that suits your time and budget — we book it and meet you on arrival.",
           "modes": [("seaplane", "plane", "Seaplane", "New · fastest", "~20 minutes",
                      [("Operator", "Maldivian (national airline)"), ("Departs", "Seaplane terminal, Velana Airport"), ("Arrives", "Thoddoo seaplane platform — a short ride to your guesthouse")]),
                     ("speedboat", "boat", "Shared speedboat", "Most popular", "60–90 minutes",
                      [("Malé airport → Thoddoo", '<span class="tchip">10:00</span><span class="tchip">16:00</span>'), ("Thoddoo → Malé airport", '<span class="tchip">06:45</span><span class="tchip">13:00</span>'), ("Departs", "Airport jetty, opposite arrivals · arrives Thoddoo harbour")]),
                     ("ferry", "anchor", "Public ferry", "Budget", "4–5 hours",
                      [("Departs", "Malé ferry terminal"), ("When", "Set days of the week"), ("Good for", "Slow travel and tight budgets")])],
           "notes": ["", "Daily departures. Times can change with weather and season — we confirm your boat when you book.", "Depends on sea conditions; we help with connections from the airport."],
           "tt_label": "Seaplane", "tt_title": "Timetable &amp; fares",
           "tt": [("clock", "Schedule", ["Thursdays &amp; Saturdays", "Malé → Thoddoo · 15:45–16:15", "Thoddoo → Malé · 16:30–17:00"]),
                  ("money", "One-way fare", ["Foreign guests · US$131", "Work-permit holders · MVR 866", "Maldivian locals · MVR 799"]),
                  ("passport", "Baggage", ["Tourists · 20 kg", "Residents · 15 kg", "Excess from US$3.5 per kg, subject to availability"])],
           "tt_note": "Fares include taxes and are non-refundable. Schedules can change — we confirm the latest timetable when we book your seats.",
           "cta": "Arrange my transfer"},
    "ru": {"label": "Как добраться до Тодду", "title": "Три способа <em>добраться до острова</em>",
           "lead": "Тодду находится в атолле Северный Ари, к западу от Мале. Выберите путь по времени и бюджету — мы всё забронируем и встретим вас.",
           "modes": [("seaplane", "plane", "Гидросамолёт", "Новинка · быстрее всего", "~20 минут",
                      [("Перевозчик", "Maldivian (национальная авиакомпания)"), ("Отправление", "Терминал гидросамолётов, аэропорт Велана"), ("Прибытие", "Платформа гидросамолётов Тодду — рядом с гестхаусом")]),
                     ("speedboat", "boat", "Групповой скоростной катер", "Самый популярный", "60–90 минут",
                      [("Аэропорт Мале → Тодду", '<span class="tchip">10:00</span><span class="tchip">16:00</span>'), ("Тодду → аэропорт Мале", '<span class="tchip">06:45</span><span class="tchip">13:00</span>'), ("Отправление", "Причал аэропорта напротив зоны прилёта · прибытие в гавань Тодду")]),
                     ("ferry", "anchor", "Общественный паром", "Бюджетно", "4–5 часов",
                      [("Отправление", "Паромный терминал Мале"), ("Когда", "По определённым дням недели"), ("Подходит", "Для неспешных путешествий и экономии")])],
           "notes": ["", "Ежедневно. Время может меняться из-за погоды и сезона — мы подтверждаем рейс при бронировании.", "Зависит от погоды на море; мы поможем со стыковкой из аэропорта."],
           "tt_label": "Гидросамолёт", "tt_title": "Расписание и тарифы",
           "tt": [("clock", "Расписание", ["По четвергам и субботам", "Мале → Тодду · 15:45–16:15", "Тодду → Мале · 16:30–17:00"]),
                  ("money", "Билет в одну сторону", ["Иностранные гости · 131 $", "С рабочей визой · 866 MVR", "Граждане Мальдив · 799 MVR"]),
                  ("passport", "Багаж", ["Туристы · 20 кг", "Резиденты · 15 кг", "Сверх нормы — от 3,5 $ за кг, при наличии места"])],
           "tt_note": "Тарифы включают налоги и не возвращаются. Расписание может меняться — мы уточняем актуальное время при бронировании мест.",
           "cta": "Заказать трансфер"},
}


def getting_there(lang, r):
    T = TRAVEL[lang]
    cards = ""
    for i, (im, ic, name, tag, dur, rows) in enumerate(T["modes"]):
        dl = "".join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in rows)
        note = f'<p class="tv__note">{T["notes"][i]}</p>' if T["notes"][i] else ""
        cards += (f'<article class="tv{" tv--new" if i == 0 else ""}"><figure>{img(im, name, "(max-width:640px) 86vw, 30vw")}<span class="tv__tag">{tag}</span></figure>'
                  f'<div class="tv__b"><span class="pc__ic">{icon(ic)}</span><h3>{name}</h3><p class="tv__dur">{icon("clock")}{dur}</p><dl>{dl}</dl>{note}</div></article>')
    tt = "".join(f'<div class="tt__c"><span class="why__i">{icon(ic)}</span><h4>{h}</h4><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></div>' for ic, h, xs in T["tt"])
    return f"""<section class="sec sec--white" id="getting-here"><div class="wrap">
  {head(T["label"], T["title"], T["lead"])}
  {carousel(lang, cards, 3, "car--cards car--travel")}
  <div class="tt rv"><div class="tt__h">{label(T["tt_label"])}<h3>{T["tt_title"]}</h3><p>{T["tt_note"]}</p>
    <a class="btn btn--gold" href="{href(lang, "contact", r)}#enquiry">{T["cta"]} {icon("arrow")}</a></div><div class="tt__g">{tt}</div></div>
</div></section>"""


STAY_GAL = ["gh-room-haisha", "guesthouse-6", "gh-clean", "guesthouse-5", "gh-garden", "guesthouse-1",
            "gh-breakfast", "guesthouse-7", "gh-comfort", "guesthouse-4", "gh-room-garden"]
STAY_CARDS = [
    ("gh-comfort", "bed", {"en": ("Comfort", "Calm rooms, good beds and air-conditioning.", "Every room we book has air-conditioning, a private bathroom with hot water, good beds and Wi-Fi — so you rest well between island days."),
                                   "ru": ("Комфорт", "Спокойные номера, удобные кровати и кондиционер.", "В каждом номере, который мы бронируем, — кондиционер, собственная ванная с горячей водой, удобные кровати и Wi-Fi, чтобы вы хорошо отдыхали между островными днями.")}),
    ("gh-clean", "sparkle", {"en": ("Cleanliness", "We visit and check every guesthouse we work with.", "We personally visit every guesthouse we partner with and keep checking — fresh linen, spotless bathrooms and daily housekeeping are a must for us."),
                                   "ru": ("Чистота", "Мы лично проверяем каждый гестхаус.", "Мы лично посещаем каждый гестхаус-партнёр и регулярно проверяем его: свежее бельё, чистые ванные и ежедневная уборка — обязательны.")}),
    ("gh-breakfast", "coffee", {"en": ("Breakfast included", "Island fruit, eggs, fresh bread and good coffee.", "Breakfast is included in all our packages — tropical fruit from Thoddoo’s farms, eggs your way, fresh bread, Maldivian mas huni on request and good coffee."),
                                  "ru": ("Завтрак включён", "Островные фрукты, яйца, свежий хлеб и кофе.", "Завтрак входит во все наши туры: тропические фрукты с ферм Тодду, яйца на ваш вкус, свежий хлеб, мальдивский мас хуни по желанию и хороший кофе.")}),
    ("gh-garden", "palm", {"en": ("Gardens &amp; terraces", "Shady tropical gardens to relax in after the beach.", "Our partner guesthouses have shaded gardens, terraces and sandy courtyards — perfect for a slow afternoon with a fresh coconut."),
                             "ru": ("Сады и террасы", "Тенистые тропические сады для отдыха после пляжа.", "У наших гестхаусов-партнёров тенистые сады, террасы и песчаные дворики — идеально для неспешного дня со свежим кокосом.")}),
    ("guesthouse-6", "heart", {"en": ("Island hospitality", "Family-run hosts who treat you like a guest of the house.", "Thoddoo’s guesthouses are run by local families. Expect warm welcomes, local tips and help with anything you need during your stay."),
                               "ru": ("Гостеприимство", "Семейные хозяева, которые принимают вас как дорогих гостей.", "Гестхаусы Тодду ведут местные семьи. Вас ждут тёплый приём, советы от местных и помощь во всём, что нужно во время отдыха.")}),
    ("bikini-beach", "beach", {"en": ("Close to the beach", "A short walk to the bikini beach and the reef.", "Everything on Thoddoo is close: from your guesthouse it is a short walk or bicycle ride to the bikini beach, the house reef and the island’s cafés."),
                               "ru": ("Рядом с пляжем", "Несколько минут пешком до бикини-пляжа и рифа.", "На Тодду всё рядом: от гестхауса — короткая прогулка или поездка на велосипеде до бикини-пляжа, домашнего рифа и кафе острова.")}),
]
STAY_TXT = {"en": ("Why our stays", "Comfort, care &amp; <em>island warmth</em>", "Rooms &amp; spaces", "Rooms, terraces &amp; <em>island breakfasts</em>",
                   "Photos show the style of rooms and spaces we book; your exact guesthouse and room are confirmed with your package."),
            "ru": ("Почему у нас уютно", "Комфорт, забота и <em>островное тепло</em>", "Номера и пространства", "Номера, террасы и <em>островные завтраки</em>",
                   "На фото — стиль номеров и пространств, которые мы бронируем; конкретный гестхаус и номер подтверждаются вместе с туром.")}


TH_GAL = [("watermelon", "Island watermelon", "Островной арбуз"), ("coconut", "Fresh coconuts", "Свежие кокосы"),
          ("breadfruit", "Breadfruit", "Хлебное дерево"),
          ("th-beach-long", "White-sand beach", "Белоснежный пляж"), ("th-palm-avenue", "Palm avenue", "Пальмовая аллея"),
          ("th-turtle", "Turtles on the reef", "Черепахи на рифе"), ("th-farm-road", "Farm roads", "Дороги между фермами"),
          ("th-sunset-palm", "Sunset palms", "Пальмы на закате"), ("coconut-palm", "Coconut palms", "Кокосовые пальмы"),
          ("th-beach-palms", "Bikini beach", "Бикини-пляж"), ("watermelon-field", "Watermelon fields", "Арбузные поля"),
          ("th-palm-shore", "Palm on the shore", "Пальма у берега"), ("th-coast", "Thoddoo coastline", "Побережье Тодду"),
          ("papaya-lush", "Papaya", "Папайя"), ("th-sunset-sky", "Evening sky", "Вечернее небо")]

BEACHES = [
    ("th-beach-palms", "beach", {"en": ("Bikini beach", "Thoddoo’s main tourist beach — soft sand, shady palms and calm water.", "The designated bikini beach is where most guests spend their days: soft white sand, palms for shade, sunbeds and calm, clear water for swimming. Swimwear is fine here; please cover up when you walk back into the village."),
                                 "ru": ("Бикини-пляж", "Главный туристический пляж Тодду — мягкий песок, пальмы и спокойная вода.", "На бикини-пляже гости проводят большую часть дня: мягкий белый песок, пальмы для тени, лежаки и спокойная прозрачная вода. Здесь можно в купальнике; возвращаясь в деревню, пожалуйста, накиньте одежду.")}),
    ("th-beach-long", "sun", {"en": ("Long white beach", "Kilometres of quiet white sand for walks and swims.", "Follow the shoreline and you find long, empty stretches of white sand and turquoise shallows — perfect for a morning walk, a swim or simply time to yourself."),
                              "ru": ("Длинный белый пляж", "Километры тихого белого песка для прогулок и купания.", "Идите вдоль берега — и вы найдёте длинные пустые полосы белого песка и бирюзовое мелководье: идеально для утренней прогулки, купания или времени наедине с собой.")}),
    ("th-turtle", "turtle", {"en": ("Snorkel from the beach", "The reef starts a few metres out — turtles included.", "One of Thoddoo’s specialities: you can snorkel straight from the beach. Turtles, reef fish and rays feed along the reef edge — ask us for the best entry point and tide times."),
                             "ru": ("Снорклинг с пляжа", "Риф в нескольких метрах от берега — и черепахи тоже.", "Особенность Тодду — снорклинг прямо с пляжа. Черепахи, рифовые рыбы и скаты кормятся у края рифа — спросите нас о лучшем месте входа и времени прилива.")}),
    ("th-sunset-palm", "sun", {"en": ("Sunset side", "The west coast glows gold every evening.", "Thoddoo’s western shore faces the sunset. Bring a fresh coconut, find a palm and watch the sky turn gold, pink and violet over the Indian Ocean."),
                               "ru": ("Закатная сторона", "Западный берег каждый вечер сияет золотом.", "Западный берег Тодду смотрит на закат. Возьмите свежий кокос, найдите пальму и смотрите, как небо становится золотым, розовым и фиолетовым над Индийским океаном.")}),
    ("th-palm-shore", "palm", {"en": ("Palms by the sea", "Leaning palms and swings — Thoddoo’s classic photo.", "Leaning coconut palms and beach swings over the sand make Thoddoo’s beaches some of the most photogenic in Ari Atoll — come at golden hour for the best light."),
                               "ru": ("Пальмы у моря", "Наклонённые пальмы и качели — классическое фото Тодду.", "Наклонённые кокосовые пальмы и качели над песком делают пляжи Тодду одними из самых фотогеничных в атолле Ари — приходите в золотой час.")}),
    ("th-couple-beach", "heart", {"en": ("Romantic moments", "Private beach set-ups for couples and celebrations.", "Honeymoon, anniversary or proposal? We arrange candlelit beach dinners, flower set-ups and photo sessions on the quietest stretch of sand."),
                                  "ru": ("Романтические моменты", "Приватные сервировки на пляже для пар и праздников.", "Медовый месяц, годовщина или предложение? Мы организуем ужин при свечах на пляже, цветочное оформление и фотосессию на самом тихом участке берега.")}),
]
SPECIAL = [
    ("watermelon", "leaf", {"en": ("Watermelons", "Thoddoo is the Maldives’ watermelon island.", "Thoddoo grows more watermelon than almost anywhere in the Maldives — the fruit is shipped to Malé and the resorts. Taste it fresh from the field, especially sweet in the dry season."),
                                  "ru": ("Арбузы", "Тодду — арбузный остров Мальдив.", "На Тодду выращивают больше арбузов, чем почти где-либо на Мальдивах, — их отправляют в Мале и на курорты. Попробуйте прямо с поля — особенно сладкие в сухой сезон.")}),
    ("coconut", "palm", {"en": ("King coconuts", "Fresh coconut water straight from the palm.", "Coconut palms grow all over the island. Ask your hosts for a freshly cut king coconut — the most refreshing drink after the beach."),
                         "ru": ("Кокосы", "Свежая кокосовая вода прямо с пальмы.", "Кокосовые пальмы растут по всему острову. Попросите хозяев срезать свежий кокос — лучший напиток после пляжа.")}),
    ("papaya-lush", "leaf", {"en": ("Papaya &amp; tropical fruit", "Papaya, bananas and passion fruit from the farms.", "Alongside watermelon, Thoddoo’s farms grow papaya, bananas, passion fruit and chillies — you will find them at breakfast and in fresh juices all over the island."),
                             "ru": ("Папайя и фрукты", "Папайя, бананы и маракуйя с ферм.", "Кроме арбузов, на фермах Тодду растут папайя, бананы, маракуйя и чили — вы встретите их за завтраком и в свежих соках по всему острову.")}),
    ("th-field-palm", "bicycle", {"en": ("Green farm fields", "The green heart of the island, best by bicycle.", "The centre of Thoddoo is a patchwork of green fields and palm-lined sandy roads — rent a bicycle and explore the farms in the quiet morning light."),
                                 "ru": ("Зелёные поля", "Зелёное сердце острова — лучше на велосипеде.", "Центр Тодду — лоскутное одеяло зелёных полей и песчаных дорог с пальмами. Возьмите велосипед и исследуйте фермы в тихом утреннем свете.")}),
    ("food-curry-roti", "dinner", {"en": ("Island cooking", "Fresh tuna, curries and roshi, Maldivian-style.", "Fresh reef fish and tuna, mild curries, mas huni and roshi flatbread — home-style Maldivian cooking is a speciality of local islands like Thoddoo."),
                                   "ru": ("Островная кухня", "Свежий тунец, карри и роши по-мальдивски.", "Свежая рифовая рыба и тунец, мягкие карри, мас хуни и лепёшки роши: домашняя мальдивская кухня — одна из радостей местных островов вроде Тодду.")}),
]
BS_HEAD = {"en": (("Tourist beaches", "Thoddoo’s <em>beaches</em>", "White sand, palms and a reef just off the shore — each beach has its own mood."),
                  ("Island specialities", "What Thoddoo is <em>famous for</em>", "The farming island of the Maldives — fresh fruit, green fields and real island cooking.")),
           "ru": (("Пляжи для туристов", "Пляжи <em>Тодду</em>", "Белый песок, пальмы и риф у самого берега — у каждого пляжа своё настроение."),
                  ("Особенности острова", "Чем <em>славится</em> Тодду", "Сельскохозяйственный остров Мальдив — свежие фрукты, зелёные поля и настоящая островная кухня."))}


def beaches_specials(lang):
    out = ""
    for i, (items, white) in enumerate(((BEACHES, True), (SPECIAL, False))):
        h = BS_HEAD[lang][i]
        cards = "".join(pcard(lang, im, ic, d[lang][0], d[lang][1], d[lang][2], h[0]) for im, ic, d in items)
        out += (f'<section class="sec{" sec--white" if white else ""}" id="{"beaches" if i == 0 else "specialities"}"><div class="wrap">{head(h[0], h[1], h[2])}'
                f'{carousel(lang, cards, 3, "car--cards")}</div></section>')
    return out


LANDMARKS = [
    {"key": "vaau", "icon": "palm", "img": "vaau-magu",
     "en": ("Vaau Magu", "Thoddoo’s famous palm road — a sandy avenue lined with tall coconut palms running between the green farms. Walk or cycle it in the soft morning light; it is the island’s favourite spot for photos and our drone videos."),
     "ru": ("Ваау Магу", "Знаменитая пальмовая аллея Тодду — песчаная дорога между зелёными фермами, обрамлённая высокими кокосовыми пальмами. Прогуляйтесь или проедьтесь на велосипеде в мягком утреннем свете — это любимое место для фото и наших видео с дрона.")},
    {"key": "mosque", "icon": "compass", "img": ("aisha-mosque" if os.path.exists(os.path.join(IMG, "aisha-mosque.webp")) else "mosque"),
     "en": ("Aisha Mosque", "Masjidhul Aisha stands in the heart of Thoddoo on Valhu Magu. Opened in 2016, it is one of the largest mosques in Ari Atoll and a striking piece of island architecture. Visitors are welcome to admire it from outside — please dress modestly (shoulders and knees covered) and be mindful of prayer times."),
     "ru": ("Мечеть Аиша", "Мечеть Масджидул Аиша стоит в самом центре Тодду, на улице Валху Магу. Открытая в 2016 году, она — одна из крупнейших мечетей атолла Ари и яркий образец островной архитектуры. Гости могут полюбоваться ею снаружи — пожалуйста, одевайтесь скромно (плечи и колени закрыты) и уважайте время молитвы.")},
    {"key": "farms", "icon": "leaf", "img": "th-farm-road",
     "en": ("Fruit farms", "Thoddoo is one of the Maldives’ farming islands: papaya, watermelon, bananas and passion fruit grow in neat fields beneath the palms. Among the fields lie the remains of an ancient Buddhist temple — a reminder of the island’s long history."),
     "ru": ("Фруктовые фермы", "Тодду — один из сельскохозяйственных островов Мальдив: на аккуратных полях под пальмами растут папайя, арбузы, бананы и маракуйя. Среди полей сохранились руины древнего буддийского храма — напоминание о долгой истории острова.")},
    {"key": "beach", "icon": "beach", "img": "bikini-beach",
     "en": ("Bikini beaches", "Two designated bikini beaches with soft white sand, palms and clear turquoise water — and a coral reef close to shore for snorkelling."),
     "ru": ("Бикини-пляжи", "Два бикини-пляжа с мягким белым песком, пальмами и прозрачной бирюзовой водой — а коралловый риф совсем рядом с берегом.")},
    {"key": "reef", "icon": "turtle", "img": "turtle-reef",
     "en": ("House reef &amp; turtles", "Thoddoo’s reef starts a few metres from the beach. Turtles feed here most mornings — swim out with a mask, or join our guided snorkel for the best spots."),
     "ru": ("Домашний риф и черепахи", "Риф Тодду начинается в нескольких метрах от пляжа. По утрам здесь кормятся черепахи — возьмите маску или присоединяйтесь к снорклингу с гидом.")},
    {"key": "swing", "icon": "sun", "img": "beach-swing",
     "en": ("Beach swings", "Palm-tree swings over the sand are Thoddoo’s favourite photo spot — come at golden hour for the softest light."),
     "ru": ("Качели на пляже", "Качели на пальмах над песком — любимое фото-место Тодду. Приходите в золотой час, когда свет самый мягкий.")},
    {"key": "cycle", "icon": "bicycle", "img": "cycling",
     "en": ("Cycling the farm roads", "There are almost no cars on Thoddoo. Rent a bicycle and ride the quiet sandy roads between farms, palms and beaches — the whole island in an afternoon."),
     "ru": ("На велосипеде по фермам", "Машин на Тодду почти нет. Возьмите велосипед и катайтесь по тихим песчаным дорогам между фермами, пальмами и пляжами — весь остров за полдня.")},
    {"key": "sandbank", "icon": "island", "img": "hero-sandbank",
     "en": ("Sandbank day trips", "A short boat ride takes you to a sandbank in the middle of the lagoon — pure white sand, turquoise water and nobody else around."),
     "ru": ("Поездка на песчаную отмель", "Короткая прогулка на лодке — и вы на песчаной отмели посреди лагуны: белый песок, бирюзовая вода и никого вокруг.")},
    {"key": "harbour", "icon": "boat", "img": "harbour-arrival",
     "en": ("Arrival by speedboat", "Your holiday begins on the water: the shared speedboat from Malé glides across the atoll to Thoddoo, where your island stay begins."),
     "ru": ("Прибытие на катере", "Отпуск начинается на воде: групповой скоростной катер из Мале скользит по атоллу к Тодду, где начинается ваш островной отдых.")},
    {"key": "sunset", "icon": "sun", "img": "thoddoo-sunset",
     "en": ("Sunset beach", "Evenings on Thoddoo end with golden sunsets over the Indian Ocean — find a quiet spot on the sand and watch the sky change colour."),
     "ru": ("Закаты на пляже", "Вечера на Тодду заканчиваются золотыми закатами над Индийским океаном — найдите тихое место на песке и наблюдайте, как меняется небо.")},
]
LM_HEAD = {"en": ("Island highlights", "The places that make <em>Thoddoo</em>", "Tap a place to read more."),
           "ru": ("Достопримечательности", "Места, которые делают <em>Тодду</em> особенным", "Нажмите, чтобы узнать больше.")}


def landmarks(lang, white=True):
    h = LM_HEAD[lang]
    cards = ""
    for l in LANDMARKS:
        t, d = l[lang]
        short = d.split(". ")[0].split(" — ")[0].rstrip(".") + "."
        cards += pcard(lang, l["img"], l["icon"], t, short, d, h[0])
    return (f'<section class="sec{" sec--white" if white else ""}" id="highlights"><div class="wrap">{head(h[0], h[1], h[2], center=True)}'
            f'{carousel(lang, cards, 3, "car--cards")}</div></section>')

# ================================================================== pages
def p_index(lang, r):
    U = UI[lang]; T = T3[lang]; H = HERO[lang]; A = ABOUT[lang]; TH = THODDOO[lang]
    figs = ('<figure class="on"><video autoplay muted loop playsinline preload="auto" poster="{R}assets/img/hero-video-poster.webp" aria-hidden="true">'
            '<source src="{R}assets/video/hero-1080.mp4" type="video/mp4" media="(min-width: 901px)">'
            '<source src="{R}assets/video/hero-720.mp4" type="video/mp4"></video></figure>')
    B = T["book"]
    popts = f'<option value="">{B["any"]}</option>' + "".join(f'<option value="{p["key"]}">{p[lang]["name"]}</option>' for p in PACKAGES)
    gopts = "".join(f"<option{' selected' if n == 2 else ''}>{n}</option>" for n in range(1, 11))
    stmt = T["statement"]
    pillars = "".join(f'<div class="pillar rv d{i + 1}"><span class="pillar__i">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(T["pillars"]))
    ifacts = "".join(f'<div class="ifact"><span class="ifact__ph"><span class="ifact__img">{img(im, "", "120px")}</span><span class="ifact__i">{icon(ic)}</span></span><small>{l}</small><strong>{t}</strong></div>' for ic, im, l, t in INTRO_FACTS[lang])
    pk = ""
    for i, p in enumerate(PACKAGES):
        P = p[lang]
        hl = "".join(f'<li>{icon("check")}<span>{x}</span></li>' for x in P["incl"][-4:])
        pk += f'''<article class="pk rv d{i + 1}{" pk--feat" if p.get("featured") else ""}">{img(p["img"], P["name"], "(max-width:1000px) 100vw, 33vw")}
  <div class="pk__top"><span class="pk__num">{p["num"]}</span><span class="pk__tag">{P["tag"]}</span></div>
  <div class="pk__body"><span class="pk__kick">{P["kicker"]}</span><h3>{P["name"]}</h3>
    <div class="pk__more"><div><ul>{hl}</ul></div></div>
    <div class="pk__price"><small>{U["from"]}</small><strong data-low="{p["low"]}" data-high="{p["high"]}">{p["low"]}</strong><span>{U["per_guest"]}</span></div>
    <div class="pk__btns"><a class="btn btn--line" href="{href(lang, "packages", r)}#{p["key"]}">{T["view"]}</a><a class="btn btn--gold" href="{href(lang, "contact", r)}?package={p["key"]}#enquiry">{T["book_now"]}</a></div>
  </div></article>'''
    bento = "".join(xp_card(lang, r, e, "rv") for k in ["turtle", "whaleshark", "dolphin", "halfday", "fishing"] for e in EXPERIENCES if e["key"] == k)
    nums = "".join(f'<div class="rv d{i + 1}"><strong><span data-count="{a}">{a}</span><sup>{s}</sup></strong><span>{b}</span></div>' for i, (a, s, b) in enumerate(T["nums"]))
    facts = "".join(f'<div><span>{icon(ic)}</span>{t}</div>' for ic, t in T["th_facts"])
    rib_img = ["th-turtle", "th-palm-avenue", "hero-sandbank", "sunset-fishing", "dolphin", "watermelon", "beach-dinner"]
    ribbon = "".join(f'<span class="rchip"><i>{img(p, "", "64px")}</i>{m}</span>' for p, m in list(zip(rib_img, MARQUEE[lang])) * 2)
    return f'''
<section class="hero">
  <div class="hero__slides">{figs}</div><div class="hero__shade"></div>
  <div class="wrap hero__inner on-dark">
    {label(H["eyebrow"])}
    <h1>{H["title"]}</h1>
    <p class="lead">{H["lead"]}</p>
    <div class="hero__cta"><a class="btn btn--gold" href="{href(lang, "packages", r)}">{T["explore"]} {icon("arrow")}</a>
      <a class="btn btn--glass" href="{href(lang, "contact", r)}">{T["watch"]}</a></div>
  </div>
</section>
<div class="book"><div class="wrap"><form class="book__card" data-book action="{href(lang, "contact", r)}" method="get">
  <label class="book__f"><small>{icon("calendar")}{B["arr"]}</small><input type="date" name="arrival"></label>
  <label class="book__f"><small>{icon("calendar")}{B["dep"]}</small><input type="date" name="departure"></label>
  <div class="book__f book__f--g"><small id="bk-gl">{icon("users")}{B["guests"]}</small><div class="gstep"><input id="bk-guests" aria-labelledby="bk-gl" type="number" name="adults" value="1" min="1" max="50" step="1" inputmode="numeric">
    <span class="gstep__btns"><button type="button" data-g="1" aria-label="{"More guests" if lang == "en" else "Больше гостей"}">{icon("chevup")}</button><button type="button" data-g="-1" aria-label="{"Fewer guests" if lang == "en" else "Меньше гостей"}">{icon("chevdown")}</button></span></div></div>
  <label class="book__f"><small>{icon("island")}{B["pkg"]}</small><select name="package">{popts}</select></label>
  <button class="btn btn--gold" type="submit">{B["go"]} {icon("arrow")}</button>
</form></div></div>

<section class="sec">
  <div class="wrap">
    <div style="text-align:center;margin-bottom:34px">{label(T["intro_label"])}</div>
    <p class="statement rv">{stmt}</p>
    <div class="orn rv" aria-hidden="true"><i></i><b></b><i></i></div>
    <p class="intro__lead rv">{INTRO_LEAD[lang]}</p>
    <div class="ifacts rv">{ifacts}</div>
    {carousel(lang, intro_cards(lang), 3, "car--cards car--intro")}
  </div>
</section>

<section class="sec sec--white" id="packages">
  <div class="wrap">
    <div class="pkh rv"><div class="head head--c">{label(T["pk_label"], "01")}<h2>{T["pk_title"]}</h2></div>
      <ul class="pkh__facts">{"".join(f'<li>{icon(ic)}<span>{t}</span></li>' for ic, t in T["pk_facts"])}</ul>
      <div class="pkh__season"><small>{T["pk_season"]}</small>{season_switch(lang)}</div></div>
    <div class="pk-grid">{pk}</div>
  </div>
</section>

<div class="ribbon" aria-hidden="true"><div class="ribbon__t">{ribbon}</div></div>

<section class="sec">
  <div class="wrap">
    <div class="pkh pkh--xp rv"><div class="head head--c">{label(T["xp_label"], "02")}<h2>{T["xp_title"]}</h2></div>
      <p class="pkh__lead">{T["xp_lead"]}</p>{arrow_link(T["xp_all"], href(lang, "experiences", r))}</div>
    <div class="bento">{bento}</div>
  </div>
</section>

<section class="sec--s sec--ink"><div class="wrap numbers">{nums}</div></section>

<section class="sec">
  <div class="wrap">
    {head(T["why_label"], T["why_title"], WHY_HEAD[lang][2], center=True, num="03")}
    {why_cards(lang)}
  </div>
</section>

<section class="sec--s"><div class="wrap">
  <div class="banner rv">{img("thoddoo-aerial", "Thoddoo island", "100vw")}
    <div class="banner__in on-dark">{label(T["th_label"], "04")}<h2>{T["th_title"]}</h2><p>{TH["p"][0]}</p><div class="facts">{facts}</div>{arrow_link(T["th_more"], href(lang, "thoddoo", r))}</div>
  </div>
</div></section>
{landmarks(lang)}
<section class="sec">
  <div class="wrap founders">
    <div class="f-media rv"><div class="a img-rv">{img("beach-walk", "", "40vw")}</div><div class="b">{img("guesthouse-2", "", "20vw")}</div></div>
    <div class="f-body rv d1">{label(T["f_label"], "05")}<h2>{A["title"]}</h2><p>{A["together"]}</p><p class="quote">{A["quote"]}</p>
      <div class="sign"><div class="monos"><span>D</span><span>J</span></div><div><strong>Dhaain &amp; Julia</strong><small>{A["role"]}</small></div></div>
      {arrow_link(T["story"], href(lang, "about", r))}</div>
  </div>
</section>
{testimonials(lang, r)}
{strip(lang)}
'''


def p_about(lang, r):
    A = ABOUT[lang]; T = T3[lang]
    return f'''{page_hero(lang, r, "about-hero", A["eyebrow"], A["title"], A["lead"], "about", full=True)}
<section class="sec">
  <div class="wrap founders">
    <div class="f-media rv"><div class="a img-rv">{img("beach-walk", "", "40vw")}</div><div class="b">{img("turtle", "", "20vw")}</div></div>
    <div class="f-body rv d1">{label(T["f_label"])}<h2>{A["hello"]}</h2>
      <div class="duo"><div><small>{A["d_role"]}</small><h3>{A["d_title"]}</h3><p>{A["dhaain"]}</p></div><div><small>{A["j_role"]}</small><h3>{A["j_title"]}</h3><p>{A["julia"]}</p></div></div>
      <p>{A["together"]}</p><p class="quote">{A["quote"]}</p>
      <div class="sign"><div class="monos"><span>D</span><span>J</span></div><div><strong>Dhaain &amp; Julia</strong><small>{A["role"]}</small></div></div></div>
  </div>
</section>
<section class="sec sec--white">
  <div class="wrap">
    {head(T["why_label"], T["why_title"], WHY_HEAD[lang][2], center=True)}
    {why_cards(lang)}
  </div>
</section>
{testimonials(lang, r)}
'''


def p_packages(lang, r):
    P = PKG_PAGE[lang]; U = UI[lang]; T = T3[lang]
    blocks = ""
    for i, p in enumerate(PACKAGES):
        X = p[lang]
        gal = PKG_GALLERY[p["key"]]
        media = f'<figure class="img-rv">{img(gal[0], X["name"], "50vw")}</figure>' + "".join(
            f'<figure>{img(g, PKG_GAL_CAP[lang].get(g, ""), "25vw")}</figure>' for g in gal[1:])
        incl = "".join(f'<li>{icon("check")}<span>{x}</span></li>' for x in X["incl"])
        days = "".join(f'<div class="day"><b>{d}</b><span>{t}</span></div>' for d, t in X["week"])
        blocks += f'''<article class="pkx{" pkx--rev" if i % 2 else ""}" id="{p["key"]}">
  <div class="pkx__media">{media}</div>
  <div class="pkx__body rv">
    <span class="pkx__no">{p["num"]}</span>{label(X["kicker"])}<h2>{X["name"]}</h2><p class="lead">{X["lead"]}</p>
    <div class="prices"><div class="cur"><small>{U["season_low"]}</small><strong>{p["low"]}</strong><span>{U["per_guest"]}</span></div>
      <div><small>{U["season_high"]}</small><strong>{p["high"]}</strong><span>{U["per_guest"]}</span></div></div>
    <h4 class="sub-h">{U["tab_incl"]}</h4><ul class="incl">{incl}</ul>
    <h4 class="sub-h">{U["tab_week"]}</h4><div class="days">{days}</div>
    <div class="best">{icon("users")}<p><small>{U["tab_best"]}</small>{X["best"]}<br><span class="note">{X["note"]}</span></p></div>
    <div class="pkx__btns"><a class="btn btn--ink" href="{href(lang, "contact", r)}?package={p["key"]}#enquiry">{U["book"]} {icon("arrow")}</a>
      <a class="btn btn--wa" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} WhatsApp</a></div>
  </div>
</article>'''
    y = icon("check")
    rows = ""
    for nm, a, b, c in P["rows"]:
        cells = ""
        for i, v in enumerate((a, b, c)):
            cls = ("y" if v else "n") + (" col-feat" if i == 1 else "")
            cells += f'<td class="{cls}">{y if v else "—"}</td>'
        rows += f"<tr><td>{nm}</td>{cells}</tr>"
    th = "".join(f'<th{" class=\"col-feat\"" if i == 1 else ""}><small>{p["num"]}</small>{p[lang]["name"]}</th>' for i, p in enumerate(PACKAGES))
    foot = "".join(f'<td{" class=\"col-feat\"" if i == 1 else ""}>{p["low"]} <small class="note">/ {p["high"]}</small></td>' for i, p in enumerate(PACKAGES))
    nots = "".join(f'<li class="x">{icon("x")}<span>{x}</span></li>' for x in P["not"])
    terms = "".join(f'<li>{icon("check")}<span>{x}</span></li>' for x in P["terms"])
    facts = [("calendar", P["hf"][0]), ("bed", P["hf"][1]), ("users", P["hf"][2]), ("check", P["hf"][3])]
    hfacts = '<ul class="hfacts">' + "".join(f'<li><span class="hfacts__i">{icon(ic)}</span><span>{t}</span></li>' for ic, t in facts) + '</ul>'
    return f'''{page_hero(lang, r, "aerial-lagoon", P["eyebrow"], P["title"], hfacts, "packages", full=True)}
<section class="sec"><div class="wrap">{blocks}<p class="note" style="text-align:center">{P["single"]}</p></div></section>
<section class="sec sec--white"><div class="wrap">
  {head(P["compare_eyebrow"], P["compare_title"], center=True)}
  <p class="swipe-hint">{"Swipe to compare" if lang == "en" else "Листайте, чтобы сравнить"} {icon("arrow")}</p><div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>{P["compare_cols"][0]}</th>{th}</tr></thead><tbody>{rows}</tbody>
    <tfoot><tr><td><small class="note">{T["season_low"]} / {T["season_high"]}</small></td>{foot}</tr></tfoot></table></div>
  <div class="cards-2" style="margin-top:40px">
    <div class="icard rv"><h3><span>{icon("info")}</span>{P["not_title"]}</h3><ul>{nots}</ul></div>
    <div class="icard rv d1"><h3><span>{icon("calendar")}</span>{P["terms_title"]}</h3><ul>{terms}</ul></div>
  </div>
  <p class="note" style="text-align:center;margin-top:30px">{U["wildlife"]}</p>
</div></section>
{testimonials(lang, r)}
'''


def p_experiences(lang, r):
    X = EXP_PAGE[lang]; T = T3[lang]; U = UI[lang]
    items = "".join(xp_card(lang, r, e, "rv") for e in EXPERIENCES + MOMENTS)
    ficons = {"U": "fish", "W": "boat", "I": "palm", "M": "sparkle"}
    filters = f'<button class="on" data-f="*">{icon("grid")}{T["cat_all"]}</button>' + "".join(f'<button data-f="{k}">{icon(ficons[k])}{v}</button>' for k, v in T["cats"].items())
    return f'''{page_hero(lang, r, "dolphin-hero", X["eyebrow"], X["title"], X["lead"], "experiences", full=True)}
<section class="sec"><div class="wrap">
  <div class="filters rv" role="group">{filters}</div>
  <div class="xgrid">{items}</div>
  <p class="note" style="text-align:center;margin-top:36px">{U["wildlife"]} · {X["else"]}</p>
</div></section>
{testimonials(lang, r)}
'''


def p_thoddoo(lang, r):
    TH = THODDOO[lang]; U = UI[lang]; T = T3[lang]
    rfy = "".join(f'<article class="rv d{i + 1}"><figure>{img(f["img"], f[lang][0], "25vw")}<span class="xp__ico">{icon(f["icon"])}</span></figure><div><h3>{f[lang][0]}</h3><p>{f[lang][1]}</p></div></article>'
                  for i, f in enumerate(RIGHT_FOR_YOU))
    gtk = "".join(f'<button class="t8" data-modal data-title="{E(g[lang][0])}" data-kicker="{E(TH["gtk_eyebrow"])}"><span class="why__i">{icon(g["icon"])}</span><h3>{g[lang][0]}</h3>'
                  f'<p>{g[lang][1]}</p><span class="more">{U["discover"]} {icon("arrow")}</span><span class="xp__detail"><p>{g[lang][1]}</p></span></button>' for g in GOOD_TO_KNOW)
    gal = "".join(f'<button class="gcard" data-lb="{{R}}assets/img/{n}.webp" aria-label="{E(en if lang == "en" else ru)}">{img(n, en if lang == "en" else ru, "(max-width:640px) 86vw, 25vw")}<span class="gcap">{en if lang == "en" else ru}</span><span class="zoom">{icon("zoom")}</span></button>' for n, en, ru in TH_GAL)
    sea = "sea ~28°C" if lang == "en" else "вода ~28°C"
    return f'''{page_hero(lang, r, "thoddoo-hero", TH["eyebrow"], TH["title"], TH["lead"], "thoddoo", full=True)}
<section class="sec"><div class="wrap split">
  <div class="split__media rv"><div class="m1 img-rv">{img("papaya-lush", "Papaya growing on Thoddoo", "50vw")}</div><div class="m2">{img("turtle-reef", "", "25vw")}</div>
</div>
  <div class="split__body rv d1">{label(TH["eyebrow"])}<h2>{TH["title"]}</h2>{"".join(f"<p>{p}</p>" for p in TH["p"])}<p class="note">{U["wildlife"]}</p></div>
</div></section>
{landmarks(lang)}
{beaches_specials(lang)}
{restaurants(lang)}
{getting_there(lang, r)}
<section class="sec"><div class="wrap">{head(TH["right_eyebrow"], TH["right_title"])}<div class="rfy">{rfy}</div></div></section>
<section class="sec sec--white"><div class="wrap">{head(TH["gtk_eyebrow"], TH["gtk_title"], TH["gtk_lead"])}<div class="tiles8 rv">{gtk}</div></div></section>
<section class="sec--s"><div class="wrap">{head(T["gal"], TH["gallery_title"])}{carousel(lang, gal, 4, "car--gal")}</div></section>
{testimonials(lang, r)}
'''


def p_guesthouses(lang, r):
    G = GUEST[lang]; S = STAY_TXT[lang]
    prom = "".join(pcard(lang, im, ic, d[lang][0], d[lang][1], d[lang][2], S[0]) for im, ic, d in STAY_CARDS)
    gal = "".join(f'<button class="gcard" data-lb="{{R}}assets/img/{n}.webp" aria-label="{S[2]}">{img(n, S[2], "(max-width:640px) 86vw, 33vw")}<span class="zoom">{icon("zoom")}</span></button>' for n in STAY_GAL)
    return f'''{page_hero(lang, r, "guesthouse-hero", G["eyebrow"], G["title"], G["lead"], "guesthouses", full=True)}
<section class="sec"><div class="wrap split">
  <div class="split__media rv"><div class="m1 img-rv">{img("guesthouse-6", S[2], "50vw")}</div><div class="m2">{img("gh-breakfast", "", "25vw")}</div></div>
  <div class="split__body rv d1">{label(G["eyebrow"])}<h2>{G["title"]}</h2>{"".join(f"<p>{p}</p>" for p in G["p"])}<p>{G["help"]}</p>
    <a class="btn btn--wa" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} WhatsApp</a></div>
</div></section>
<section class="sec sec--white"><div class="wrap">{head(S[0], S[1])}{carousel(lang, prom, 3, "car--cards")}</div></section>
<section class="sec"><div class="wrap">{head(S[2], S[3])}{carousel(lang, gal, 3, "car--gal")}<p class="note car__note">{S[4]}</p></div></section>
{testimonials(lang, r)}
'''


def p_faq(lang, r):
    F = FAQ_HEAD[lang]; U = UI[lang]
    qa = "".join(f'<details class="qa"{" open" if i == 0 else ""}><summary><span class="why__i">{icon(q["icon"])}</span>{q[lang][0]}<span class="why__t"></span></summary><div class="qa__a">{q[lang][1]}</div></details>' for i, q in enumerate(FAQ))
    return f'''{page_hero(lang, r, "vaau-magu", F["eyebrow"], F["title"], F["lead"], "faq", full=True)}
<section class="sec"><div class="wrap faq">
  <aside class="faq__side rv"><div class="helpcard on-dark">{label(U["nav"]["contact"])}<h3>{F["aside_t"]}</h3><p>{F["aside_p"]}</p>
    <a class="btn btn--wa" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} WhatsApp</a>
    <a class="btn btn--glass" href="mailto:{C["email"]}">{icon("mail")} E-mail</a></div></aside>
  <div class="rv d1">{qa}</div>
</div></section>
'''


CTRY_T = {"en": ("Country", "Select your country", "Country code", "Phone number", "Popular", "All countries"),
          "ru": ("Страна", "Выберите страну", "Код страны", "Номер телефона", "Популярные", "Все страны")}


def _cname(lang, row):
    return row[1] if lang == "en" else row[2]


def country_opts(lang):
    t = CTRY_T[lang]
    by = {r[0]: r for r in COUNTRIES}
    rows = sorted(COUNTRIES, key=lambda r: _cname(lang, r))
    pop = "".join(f'<option value="{E(_cname(lang, by[k]))}" data-iso="{k}" data-dial="{by[k][3]}">{E(_cname(lang, by[k]))}</option>' for k in POPULAR)
    allc = "".join(f'<option value="{E(_cname(lang, r))}" data-iso="{r[0]}" data-dial="{r[3]}">{E(_cname(lang, r))}</option>' for r in rows)
    return f'<option value="">{t[1]}</option><optgroup label="{t[4]}">{pop}</optgroup><optgroup label="{t[5]}">{allc}</optgroup>'


def code_opts(lang):
    rows = sorted(COUNTRIES, key=lambda r: _cname(lang, r))
    default = "RU" if lang == "ru" else ""
    first = '' if default else f'<option value="">+ …</option>'
    return first + "".join(f'<option value="+{r[3]}" data-iso="{r[0]}"{" selected" if r[0] == default else ""}>{r[0]} +{r[3]}</option>' for r in rows)


def p_contact(lang, r):
    K = CONTACT[lang]; F = K["f"]; T = T3[lang]; U = UI[lang]; P = PKG_PAGE[lang]
    opts = ""
    for p in PACKAGES:
        X = p[lang]
        opts += (f'<label class="opt"><input type="radio" name="package" value="{p["key"]}" data-name="{E(X["name"])}" data-low="{p["low"]}" data-high="{p["high"]}" data-img="{{R}}assets/img/{p["img"]}-sm.webp">'
                 f'<figure>{img(p["img"], X["name"], "300px")}</figure><span class="opt__check">{icon("check")}</span>'
                 f'<span class="opt__b"><strong>{X["name"]}</strong><span>{U["from"]} {p["low"]} · {X["kicker"]}</span></span></label>')
    for val, (a, b), ic, im in (("", T["not_sure"], "question", "hero-sandbank"), ("excursions", T["exc_only"], "compass", "dolphin")):
        opts += (f'<label class="opt opt--plain"><input type="radio" name="package" value="{val}" data-name="{E(a)}" data-img="{{R}}assets/img/{im}-sm.webp"{" checked" if not val else ""}>'
                 f'<span class="opt__check">{icon("check")}</span><span class="opt__b"><span class="ico">{icon(ic)}</span><strong>{a}</strong><span>{b}</span></span></label>')
    xo = "".join(f'<label class="opt"><input type="checkbox" name="extras" value="{e["key"]}" data-label="{E(e[lang][0])}"><figure>{img(e["img"], e[lang][0], "160px")}</figure>'
                 f'<span class="opt__check">{icon("check")}</span><span class="opt__b"><strong>{e[lang][0]}</strong></span></label>' for e in EXPERIENCES[:-1] + MOMENTS)
    steps_btns = "".join(f'<button type="button" data-go="{i}"{" class=\"on\"" if i == 0 else ""}><i>{i + 1}</i><span>{s}</span></button>' for i, s in enumerate(T["steps"]))
    data = " ".join(f'data-{k}="{E(F[k])}"' for k in ["sending", "err", "hello", "subject"])
    data += " " + " ".join(f'data-l-{k[1:].lower()}="{E(F[k])}"' for k in ["lName", "lDates", "lGuests", "lPackage", "lExtras", "lMsg"])
    data += (f' data-season-low="{E(T["season_low"])}" data-season-high="{E(T["season_high"])}" data-note="{E(T["s_note"])}"'
             f' data-quote="{E(T["s_quote"])}" data-kids="{E(T["s_kids"])}" data-none="{E(T["s_none"])}"')

    def nav(i):
        back = f'<button type="button" class="btn btn--line" data-prev-step>{T["back"]}</button>' if i else "<span></span>"
        return f'<div class="step__nav">{back}<div class="r"><button type="button" class="btn btn--ink" data-next-step>{T["next"]} {icon("arrow")}</button></div></div>'

    lbl = 'style="font-size:.66rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-2)"'
    stepper = lambda name, v, t: (f'<div class="fld"><span {lbl}>{t}</span><div class="stepper" data-stepper="{name}"><button type="button" data-d="-1" aria-label="−">−</button>'
                                  f'<output>{v}</output><button type="button" data-d="1" aria-label="+">+</button></div><input type="hidden" name="{name}" value="{v}"></div>')
    return f'''{page_hero(lang, r, "contact-hero", K["eyebrow"], K["title"], K["lead"], "contact", full=True)}
<section class="sec" id="enquiry"><div class="wrap conc">
  <form class="conc__main rv" id="enquiry-form" action="https://formsubmit.co/ajax/{C["email"]}" method="POST" data-wa="{C["whatsapp"]}" {data} novalidate>
    <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="steps">{steps_btns}</div>
    <div class="step on" data-step="0"><h3>{T["st_t"][0]}</h3><p>{T["st_p"][0]}</p><div class="opt-grid">{opts}</div>{nav(0)}</div>
    <div class="step" data-step="1"><h3>{T["st_t"][1]}</h3><p>{T["st_p"][1]}</p>
      <div class="frow"><div class="fld"><label for="f-arr">{F["arrival"]}</label><input id="f-arr" name="arrival" type="date"></div>
        <div class="fld"><label for="f-dep">{F["departure"]}</label><input id="f-dep" name="departure" type="date"></div></div>
      <div class="frow">{stepper("adults", 1, T["adults"])}{stepper("children", 0, T["children"])}</div>
      {nav(1)}</div>
    <div class="step" data-step="2"><h3>{T["st_t"][2]}</h3><p>{T["st_p"][2]}</p><div class="xopts">{xo}</div>{nav(2)}</div>
    <div class="step" data-step="3"><h3>{T["st_t"][3]}</h3><p>{T["st_p"][3]}</p>
      <div class="frow"><div class="fld"><label for="f-name">{F["name"]}</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div class="fld"><label for="f-email">{F["email"]}</label><input id="f-email" name="email" type="email" required autocomplete="email"></div></div>
      <div class="frow"><div class="fld"><label for="f-country">{CTRY_T[lang][0]}</label><select id="f-country" name="country" autocomplete="country">{country_opts(lang)}</select></div>
        <div class="fld"><label for="f-phone">{F["phone"]}</label><div class="tel"><select id="f-code" name="code" aria-label="{CTRY_T[lang][2]}">{code_opts(lang)}</select><input id="f-phone" name="phone" type="tel" autocomplete="tel-national" inputmode="tel" placeholder="{CTRY_T[lang][3]}"></div></div></div>
      <div class="frow">
        <fieldset class="fld"><legend>{T["reply"]}</legend><div class="seg"><label><input type="radio" name="reply" value="E-mail" checked><span>{icon("mail")}E-mail</span></label><label><input type="radio" name="reply" value="WhatsApp"><span>{brand("whatsapp")}WhatsApp</span></label></div></fieldset><div></div></div>
      <div class="fld"><label for="f-msg">{F["message"]}</label><textarea id="f-msg" name="message"></textarea></div>
      <p class="consent">{T["consent"]}</p>
      <div class="status" role="status" aria-live="polite"></div>
      <div class="step__nav"><button type="button" class="btn btn--line" data-prev-step>{T["back"]}</button>
        <div class="r"><button type="button" class="btn btn--wa" data-send-wa>{brand("whatsapp")} {T["send_wa"]}</button><button type="submit" class="btn btn--gold">{icon("mail")} {T["send"]}</button></div></div>
    </div>
    <div class="sent"><span class="sent__ic">{icon("check")}</span><h3>{T["done_t"]}</h3><p>{T["done_p"]}</p><a class="btn btn--ink" href="{href(lang, "index", r)}">{T["done_b"]}</a></div>
  </form>
  <aside class="sum">
    <div class="sum__card" aria-live="polite" hidden data-sum-card>
      <div class="sum__img"><small class="sum__kick">{"Your booking summary" if lang == "en" else "Ваше бронирование"}</small><img data-sum-img src="{{R}}assets/img/hero-sandbank-sm.webp" alt="" width="900" height="600"><strong data-sum="pkg">{T["not_sure"][0]}</strong></div>
      <div class="sum__rows">
        <div><span>{icon("calendar")}{T["s_dates"]}</span><span data-sum="dates">{T["s_none"]}</span></div>
        <div><span>{icon("clock")}{T["s_nights"]}</span><span data-sum="nights">{T["s_none"]}</span></div>
        <div><span>{icon("users")}{T["s_guests"]}</span><span data-sum="guests">{T["s_none"]}</span></div>
        <div><span>{icon("sparkle")}{T["s_xp"]}</span><span data-sum="xp">{T["s_none"]}</span></div>
      </div>
      <div class="sum__total"><small>{T["s_total"]}</small><strong data-sum="total">{T["s_quote"]}</strong><span data-sum="note"></span></div>
    </div>
    <div class="contact-list">
      <a href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener"><span class="ci wa">{brand("whatsapp")}</span><span><small>WhatsApp</small><strong>{C["phone_display"]}</strong></span></a>
      <a href="mailto:{C["email"]}"><span class="ci">{icon("mail")}</span><span><small>E-mail</small><strong>{C["email"]}</strong></span></a>
      <div><span class="ci">{icon("pin")}</span><span><small>{K["cards"][2][1]}</small><strong>{K["cards"][2][2]}</strong></span></div>
      <div><span class="ci">{icon("clock")}</span><span><small>{K["cards"][3][1]}</small><strong>{K["cards"][3][2]}</strong></span></div>
    </div>
    <div class="icard"><h3><span>{icon("calendar")}</span>{P["terms_title"]}</h3><ul>{"".join(f"<li>{icon('check')}<span>{t}</span></li>" for t in P["terms"][:2])}</ul></div>
  </aside>
</div></section>'''


BUILDERS = {"index": p_index, "about": p_about, "packages": p_packages, "thoddoo": p_thoddoo,
            "experiences": p_experiences, "guesthouses": p_guesthouses, "faq": p_faq, "contact": p_contact}


# ================================================================== structured data
def jsonld(lang, page):
    U = UI[lang]
    same = [C[k] for k in ("instagram", "facebook", "telegram", "tiktok", "tripadvisor") if C.get(k)]
    org = {"@context": "https://schema.org", "@type": "TravelAgency", "@id": SITE + "/#agency", "name": "Velaa Getaways",
           "slogan": U["tagline"], "url": SITE + "/", "logo": SITE + "/assets/brand/logo-512.png", "image": SITE + "/assets/img/og-image.jpg",
           "description": SEO["index"][lang][1], "email": C["email"], "telephone": C["phone_tel"],
           "address": {"@type": "PostalAddress", "addressLocality": "Thoddoo", "addressRegion": "Alif Alif Atoll", "addressCountry": "MV"},
           "geo": {"@type": "GeoCoordinates", "latitude": 4.4381, "longitude": 72.9586},
           "areaServed": ["Maldives", "Russia", "Europe"], "knowsLanguage": ["en", "ru"], "priceRange": "$600 – $1,550",
           "contactPoint": {"@type": "ContactPoint", "telephone": C["phone_tel"], "email": C["email"], "contactType": "sales", "availableLanguage": ["English", "Russian"]}}
    if same:
        org["sameAs"] = same
    out = [org, {"@context": "https://schema.org", "@type": "WebSite", "name": "Velaa Getaways", "url": SITE + "/", "inLanguage": lang}]
    if page != "index":
        out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": U["breadcrumb_home"], "item": url(lang, "index")},
            {"@type": "ListItem", "position": 2, "name": U["nav"][page], "item": url(lang, page)}]})
    if page in ("packages", "index"):
        trips = [{"@type": "TouristTrip", "name": f'{p[lang]["name"]} — 7 nights on Thoddoo', "description": p[lang]["lead"], "touristType": p[lang]["best"],
                  "itinerary": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"{d}: {t}"} for i, (d, t) in enumerate(p[lang]["week"])]},
                  "provider": {"@id": SITE + "/#agency"},
                  "offers": [{"@type": "Offer", "price": p[s].strip("$").replace(",", ""), "priceCurrency": "USD", "description": U["season_" + s],
                              "url": url(lang, "packages") + "#" + p["key"], "availability": "https://schema.org/InStock"} for s in ("low", "high")]} for p in PACKAGES]
        out.append({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": t} for i, t in enumerate(trips)]})
    if page == "faq":
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q[lang][0], "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", " ", q[lang][1]).strip()}} for q in FAQ]})
    if page == "thoddoo":
        out.append({"@context": "https://schema.org", "@type": "TouristDestination", "name": "Thoddoo", "description": THODDOO[lang]["lead"],
                    "containedInPlace": {"@type": "Country", "name": "Maldives"}, "geo": {"@type": "GeoCoordinates", "latitude": 4.4381, "longitude": 72.9586},
                    "touristType": ["Beach holidays", "Snorkelling", "Families", "Couples"] if lang == "en" else ["Пляжный отдых", "Снорклинг", "Семьи", "Пары"],
                    "includesAttraction": [{"@type": "TouristAttraction", "name": re.sub("<[^>]+>|&amp;", lambda m: "&" if m.group(0) == "&amp;" else "", l[lang][0]),
                                            "description": l[lang][1], "image": f'{SITE}/assets/img/{l["img"]}.webp'} for l in LANDMARKS]
                                          + [{"@type": "Beach", "name": d[lang][0], "description": d[lang][2], "image": f"{SITE}/assets/img/{im}.webp"} for im, ic, d in BEACHES]})
        out.append({"@context": "https://schema.org", "@type": "ItemList", "name": "Where to eat on Thoddoo" if lang == "en" else "Где поесть на Тодду",
                    "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Restaurant", "name": x[lang][0], "servesCuisine": x[lang][1],
                                         "address": {"@type": "PostalAddress", "addressLocality": "Thoddoo", "addressCountry": "MV"}}}
                                        for i, x in enumerate(RESTAURANTS[:5])]})
    if page == "experiences":
        out.append({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "TouristAttraction", "name": e[lang][0], "description": e[lang][2]}} for i, e in enumerate(EXPERIENCES + MOMENTS)]})
    return "\n".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)


import hashlib
V = {f: hashlib.md5(open(os.path.join(ROOT, f), "rb").read()).hexdigest()[:8] for f in ("assets/css/fonts.css", "assets/css/site.css", "assets/js/app.js")}


def render(lang, page):
    r = "" if lang == "en" else "../"
    title, desc = SEO[page][lang]
    verif = ""
    if C["yandex_verification"]:
        verif += f'<meta name="yandex-verification" content="{C["yandex_verification"]}">'
    if C["google_verification"]:
        verif += f'<meta name="google-site-verification" content="{C["google_verification"]}">'
    sub = "latin" if lang == "en" else "cyrillic"
    doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url(lang, page)}">
<link rel="alternate" hreflang="en" href="{url("en", page)}">
<link rel="alternate" hreflang="ru" href="{url("ru", page)}">
<link rel="alternate" hreflang="x-default" href="{url("en", page)}">
<meta name="theme-color" content="#0c2a34">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website"><meta property="og:site_name" content="Velaa Getaways">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url(lang, page)}"><meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{"en_GB" if lang == "en" else "ru_RU"}"><meta property="og:locale:alternate" content="{"ru_RU" if lang == "en" else "en_GB"}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{SITE}/assets/img/og-image.jpg">
<meta name="geo.region" content="MV"><meta name="geo.placename" content="Thoddoo">
{verif}
<link rel="icon" href="{{R}}assets/brand/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{{R}}assets/brand/apple-touch-icon.png">
<link rel="manifest" href="{{R}}site.webmanifest">
<link rel="preload" href="{{R}}assets/fonts/cormorant-garamond-{sub}-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{R}}assets/fonts/manrope-{sub}-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{R}}assets/css/fonts.css?v={V["assets/css/fonts.css"]}">
<link rel="stylesheet" href="{{R}}assets/css/site.css?v={V["assets/css/site.css"]}">
{jsonld(lang, page)}
</head>
<body>
{header(lang, page, r)}
<main id="main">
{BUILDERS[page](lang, r)}
</main>
{footer(lang, page, r)}
<script src="{{R}}assets/js/app.js?v={V["assets/js/app.js"]}" defer></script>
</body>
</html>
'''
    return doc.replace("{R}", r)


def main():
    os.makedirs(os.path.join(ROOT, "ru"), exist_ok=True)
    for lang in ("en", "ru"):
        for page in PAGES:
            with open(os.path.join(ROOT, "" if lang == "en" else "ru", f"{page}.html"), "w", encoding="utf-8") as f:
                f.write(render(lang, page))
    from urllib.parse import urlparse
    base = urlparse(SITE).path.rstrip("/") + "/"
    h = render("en", "index").replace('"assets/', '"' + base + 'assets/').replace(' assets/', ' ' + base + 'assets/').replace('"site.webmanifest', '"' + base + 'site.webmanifest')
    h = re.sub(r'href="(ru/)?([a-z0-9]+)\.html', lambda m: 'href="' + base + (m.group(1) or "") + m.group(2) + '.html', h)
    h = h.replace("<title>", "<title>Page not found · ", 1).replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(h)
    today = datetime.date.today().isoformat()
    prio = {"index": "1.0", "packages": "0.9", "experiences": "0.8", "thoddoo": "0.8", "contact": "0.8"}
    urls = ""
    for lang in ("en", "ru"):
        for page in PAGES:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, page)}"/>' for l in ("en", "ru"))
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en", page)}"/>'
            html_ = open(os.path.join(ROOT, "" if lang == "en" else "ru", f"{page}.html"), encoding="utf-8").read()
            pics = []
            for m in re.findall(r'assets/img/([a-z0-9-]+)\.webp', html_):
                if not m.endswith("-sm") and m not in pics:
                    pics.append(m)
            ims = "".join(f"<image:image><image:loc>{SITE}/assets/img/{p}.webp</image:loc></image:image>" for p in pics[:40])
            urls += f"<url><loc>{url(lang, page)}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{prio.get(page, '0.6')}</priority>{alts}{ims}</url>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + urls + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    json.dump({"name": "Velaa Getaways", "short_name": "Velaa", "start_url": "./", "display": "standalone", "background_color": "#f7f4ef",
               "theme_color": "#0c2a34", "icons": [{"src": "assets/brand/logo-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(ROOT, "site.webmanifest"), "w"))
    print("Built", len(PAGES) * 2, "pages")


if __name__ == "__main__":
    main()
