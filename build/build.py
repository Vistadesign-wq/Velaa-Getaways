# -*- coding: utf-8 -*-
"""Velaa Getaways — static site generator (v3 design).
Run:  python3 build/build.py   → writes EN pages to ./ and RU pages to ./ru/"""
import json, os, re, html, datetime
from PIL import Image

import icons as _ic
from icons import icon
from brands import brand
from content import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
C = CONFIG
SITE = C["site_url"].rstrip("/")
E = html.escape
_sz = {}

_ic.ICONS["phone"] = '<path d="M5 3.5h3.2l1.6 4-2 1.3a11 11 0 0 0 5.4 5.4l1.3-2 4 1.6V17a2.5 2.5 0 0 1-2.7 2.5C9.6 19 5 14.4 4.5 6.2A2.5 2.5 0 0 1 5 3.5z"/>'
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
        "loc": "Thoddoo · Alif Alif Atoll · Maldives", "enquire": "Enquire",
        "explore": "Explore packages", "watch": "Plan my trip",
        "slides": ["Sandbank · North Ari Atoll", "Sandbar · Alif Alif", "Arrival by speedboat"],
        "book": {"arr": "Arrival", "dep": "Departure", "guests": "Guests", "pkg": "Package", "any": "Any package", "go": "Check availability"},
        "intro_label": "Welcome to Thoddoo",
        "statement": 'A real Maldivian island <span class="inline-img">{I1}</span> where turtles glide past the reef, papaya grows beneath the palms <span class="inline-img">{I2}</span> and you are welcomed <em>like a friend.</em>',
        "pillars": [("heart", "Hosted by locals", "Dhaain was born on Thoddoo — you see the island through the people who call it home."),
                    ("turtle", "The reef at your doorstep", "Step off the beach into clear water where turtles and reef fish live."),
                    ("tag", "Honest, clear prices", "All taxes included and every inclusion listed before you book.")],
        "trip": ["House reef", "Bikini beach", "Family guesthouses"],
        "pk_label": "Holiday packages", "pk_title": "Three ways to live <em>island life</em>",
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
        "loc": "Тодду · атолл Алиф Алиф · Мальдивы", "enquire": "Заявка",
        "explore": "Смотреть туры", "watch": "Спланировать поездку",
        "slides": ["Песчаная отмель · Северный Ари", "Песчаная коса · Алиф Алиф", "Прибытие на скоростном катере"],
        "book": {"arr": "Прилёт", "dep": "Вылет", "guests": "Гостей", "pkg": "Тур", "any": "Любой тур", "go": "Проверить даты"},
        "intro_label": "Добро пожаловать на Тодду",
        "statement": 'Настоящий мальдивский остров <span class="inline-img">{I1}</span>, где черепахи скользят вдоль рифа, папайя растёт под пальмами <span class="inline-img">{I2}</span>, а вас встречают <em>как друга.</em>',
        "pillars": [("heart", "Местные хозяева", "Дхаин родился на Тодду — вы увидите остров глазами тех, для кого он дом."),
                    ("turtle", "Риф у порога", "С пляжа — сразу в прозрачную воду, где живут черепахи и рифовые рыбы."),
                    ("tag", "Честные, понятные цены", "Все налоги включены, а состав тура известен до бронирования.")],
        "trip": ["Домашний риф", "Бикини-пляж", "Семейные гестхаусы"],
        "pk_label": "Туры", "pk_title": "Три способа прожить <em>островную жизнь</em>",
        "pk_lead": "8 дней · 7 ночей · twin или double. Цена за человека при размещении 2 взрослых, все налоги включены.",
        "view": "Подробнее", "book_now": "Бронь",
        "xp_label": "Впечатления", "xp_title": "Моменты, подаренные <em>океаном</em>",
        "xp_lead": "Плавайте с черепахами, встречайте мант, следуйте за дельфинами на закате — нажмите на впечатление, чтобы узнать больше.",
        "xp_all": "Все впечатления",
        "nums": [("7", "", "ночей в каждом туре"), ("10", "+", "морских впечатлений"), ("2", "", "бикини-пляжа"), ("28", "°C", "средняя температура воды")],
        "why_label": "Почему Velaa", "why_title": "Путешествуйте с теми, для кого <em>это дом</em>",
        "why_badge": ("Велаа — морская черепаха", "наше имя на языке дивехи"),
        "th_label": "Остров", "th_title": "Тодду — <em>зелёная сторона</em> Мальдив",
        "th_facts": [("leaf", "Фермы папайи и арбузов"), ("beach", "Два бикини-пляжа"), ("turtle", "Риф у самого берега"), ("bicycle", "Пешком или на велосипеде")],
        "th_more": "Открыть Тодду",
        "f_label": "Наша история", "story": "Читать нашу историю",
        "t_label": "Истории гостей", "t_title": "Воспоминания <em>на пять звёзд</em>", "t_sub": "средняя оценка гостей",
        "strip_label": "Островные дни", "strip_title": "Неделя, которая ощущается <em>как целая жизнь</em>",
        "cta_label": "Ваш остров ждёт",
        "f_news": "Готовы к <em>островному отдыху?</em>", "f_cols": ["Разделы", "Помощь", "Контакты"],
        "gal": "Галерея", "cat_all": "Все",
        "cats": {"U": "Под водой", "W": "На воде", "I": "Островная жизнь", "M": "Особые моменты"},
        "steps": ["Ваш отдых", "Даты и гости", "Впечатления", "Контакты"],
        "st_t": ["Какой отдых вам ближе?", "Когда вы приедете?", "Что добавить в поездку?", "Куда отправить ваш план?"],
        "st_p": ["Выберите тур — или мы подскажем.", "Подойдут примерные даты — мы подтвердим наличие.",
                 "Отметьте впечатления, которые хотите включить или узнать цену.", "Мы отвечаем лично, обычно в течение нескольких часов."],
        "not_sure": ("Пока не знаю", "Посоветуйте"), "exc_only": ("Только экскурсии", "Без тура"),
        "adults": "Взрослые", "children": "Дети (2–12)",
        "reply": "Как ответить", "next": "Далее", "back": "Назад", "send": "Отправить заявку", "send_wa": "Отправить в WhatsApp",
        "consent": "Отправляя заявку, вы соглашаетесь, что мы используем ваши данные только для ответа на неё.",
        "s_dates": "Даты", "s_nights": "Ночей", "s_guests": "Гостей", "s_xp": "Впечатления",
        "s_total": "Ориентировочно", "s_note": "за человека × взрослые · {season}. Точную стоимость подтвердит наша команда.",
        "s_quote": "Индивидуальный расчёт", "s_none": "—", "s_kids": "дети — по запросу",
        "done_t": "Спасибо — ваш островной план уже в пути", "done_p": "Мы получили вашу заявку и ответим лично по e-mail или в WhatsApp, обычно в течение нескольких часов.",
        "done_b": "На главную", "season_low": "апрель–октябрь", "season_high": "ноябрь–март",
    },
}
XP_CAT = {"turtle": "U", "reef": "U", "halfday": "U", "fullday": "U", "whaleshark": "U", "fishing": "W", "dolphin": "W",
          "hopping": "W", "octopus": "I", "resort": "I", "more": "I", "photoshoot": "M", "drone": "M", "dinner": "M", "watersports": "M"}
PKG_GALLERY = {"essential": ["thoddoo-beach", "turtle", "palm-road-aerial"], "ocean": ["jetski", "manta-snorkel", "dolphin"],
               "signature": ["resort", "beach-dinner", "sunset-fishing"]}
PKG_GAL_CAP = {"en": {"turtle": "Turtle snorkelling", "palm-road": "Palm Road drone video", "dolphin": "Dolphin cruise", "jetski": "Jetski + drone video",
                      "resort": "Resort day visit", "sunset-fishing": "Sunset fishing"},
               "ru": {"turtle": "Снорклинг с черепахами", "palm-road": "Видео с дрона", "dolphin": "Дельфины", "jetski": "Гидроцикл + дрон",
                      "resort": "День на курорте", "sunset-fishing": "Закатная рыбалка"}}
STRIP = {"en": [("turtle", "Turtle mornings"), ("hero-sandbar", "Sandbank afternoons"), ("guesthouse-6", "Island homes"), ("sunset-fishing", "Sunset fishing"),
                ("vaau-magu", "Vaau Magu"), ("whale-shark", "Gentle giants"), ("beach-dinner", "Candlelit dinners"), ("palm-road-aerial", "Palm roads"), ("thoddoo-aerial", "Thoddoo"), ("dolphin", "Dolphin seas"), ("papaya", "Island papaya")],
         "ru": [("turtle", "Утро с черепахами"), ("hero-sandbar", "Песчаные отмели"), ("guesthouse-6", "Островной дом"), ("sunset-fishing", "Закатная рыбалка"),
                ("vaau-magu", "Ваау Магу"), ("whale-shark", "Добрые великаны"), ("beach-dinner", "Ужин при свечах"), ("palm-road-aerial", "Пальмовые аллеи"), ("thoddoo-aerial", "Тодду"), ("dolphin", "Море дельфинов"), ("papaya", "Островная папайя")]}


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
                  f'<span class="brand__txt"><small class="brand__top">{"Thoddoo · Maldives" if lang == "en" else "Тодду · Мальдивы"}</small>'
                  f'<span class="brand__name">VELAA</span><span class="brand__sub">Getaways</span><span class="brand__tag">{U["tagline"]}</span></span></a>')
    dl = "".join(f'<a href="{href(lang, p, r)}"><small>0{i + 1}</small>{U["nav"][p]}</a>'
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
          <span class="brand__txt"><small class="brand__top">{"Thoddoo · Maldives" if lang == "en" else "Тодду · Мальдивы"}</small><span class="brand__name">VELAA</span><span class="brand__sub">Getaways</span></span></a>
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
        <div><span class="fi">{icon("clock")}</span><span><small>{reply}</small>{reply_v}</span></div>
      </div>
    </div>
    <div class="ftr__bot">
      <span>© <span data-year>2026</span> Velaa Getaways · {U["rights"]}</span>
      <span class="ftr__note">{U["privacy_note"]}</span>
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
    <div class="modal__m"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt=""></div>
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


def testimonials(lang, r):
    T = T3[lang]; U = UI[lang]
    quotes = faces = ""
    for i, rv in enumerate(REVIEWS):
        name, place, text = rv[lang]
        on = " on" if i == 0 else ""
        quotes += (f'<figure class="tq{on}" data-i="{i}"><blockquote>{text}</blockquote>'
                   f'<figcaption class="tq__who"><img src="{{R}}assets/img/guests/{rv["img"]}.webp" alt="{E(name)}" width="48" height="48" loading="lazy">'
                   f'<div><strong>{name}</strong><span><i class="flag flag--{rv["flag"]}"></i>{place} · {rv["pkg"]}</span></div></figcaption></figure>')
        faces += f'<button class="face{on}" data-i="{i}" aria-label="{E(name)}"><img src="{{R}}assets/img/guests/{rv["img"]}.webp" alt="" width="40" height="40" loading="lazy"></button>'
    return f'''<!-- DRAFT REVIEWS: replace with genuine guest reviews before launch -->
<section class="sec--s sec--ink on-dark tst-sec" aria-labelledby="t-title">
  <div class="wrap tst" data-tst>
    <div class="tst__head rv">{label(T["t_label"])}<h2 id="t-title">{T["t_title"]}</h2>
      <span class="tst__badge"><b>5.0</b>{stars()}<small>{T["t_sub"]}</small></span></div>
    <div class="tst__body rv d1">
      <div class="tst__stage">{quotes}</div>
      <div class="rail"><button class="navb" data-prev aria-label="{U["prev"]}">{icon("arrowl")}</button>
        <div class="faces">{faces}</div>
        <button class="navb" data-next aria-label="{U["next"]}">{icon("arrow")}</button></div>
      <div class="tbar"><span></span></div>
    </div>
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
    return f'''<section class="phero{" phero--full" if full else ""}">{img(image, "", "100vw", eager=True)}<div class="hero__shade"></div>
  <div class="wrap on-dark"><div><ol class="crumbs"><li><a href="{href(lang, "index", r)}">{U["breadcrumb_home"]}</a></li><li>{U["nav"][page]}</li></ol>
    <h1>{title}</h1></div><div>{label(eyebrow)}<p class="lead" style="margin-top:14px">{lead}</p></div></div>
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
    figs = "".join(f'<figure>{img(n, c, "320px")}</figure>' for n, c in STRIP[lang])
    return (f'<section class="sec--s" aria-label="{T["strip_label"]}"><div class="wrap">{head(T["strip_label"], T["strip_title"])}</div>'
            f'<div class="strip"><div class="strip__track">{figs}{figs.replace("<figure>", "<figure aria-hidden=\"true\">")}</div></div></section>')



LANDMARKS = [
    {"key": "vaau", "icon": "palm", "img": "vaau-magu",
     "en": ("Vaau Magu", "Thoddoo’s famous palm road — a sandy avenue lined with tall coconut palms running between the green farms. Walk or cycle it in the soft morning light; it is the island’s favourite spot for photos and our drone videos."),
     "ru": ("Ваау Магу", "Знаменитая пальмовая аллея Тодду — песчаная дорога между зелёными фермами, обрамлённая высокими кокосовыми пальмами. Прогуляйтесь или проедьтесь на велосипеде в мягком утреннем свете — это любимое место для фото и наших видео с дрона.")},
    {"key": "mosque", "icon": "compass", "img": ("aisha-mosque" if os.path.exists(os.path.join(IMG, "aisha-mosque.webp")) else "mosque"),
     "en": ("Aisha Mosque", "Masjidhul Aisha stands in the heart of Thoddoo on Valhu Magu. Opened in 2016, it is one of the largest mosques in Ari Atoll and a striking piece of island architecture. Visitors are welcome to admire it from outside — please dress modestly (shoulders and knees covered) and be mindful of prayer times."),
     "ru": ("Мечеть Аиша", "Мечеть Масджидул Аиша стоит в самом центре Тодду, на улице Валху Магу. Открытая в 2016 году, она — одна из крупнейших мечетей атолла Ари и яркий образец островной архитектуры. Гости могут полюбоваться ею снаружи — пожалуйста, одевайтесь скромно (плечи и колени закрыты) и уважайте время молитвы.")},
    {"key": "farms", "icon": "leaf", "img": "thoddoo-aerial",
     "en": ("Fruit farms", "Thoddoo is one of the Maldives’ agricultural islands. From above you see its patchwork of fields, with papaya, watermelon and other local produce growing beneath the palms."),
     "ru": ("Фруктовые фермы", "Тодду — один из сельскохозяйственных островов Мальдив. Сверху видно лоскутное одеяло полей: под пальмами растут папайя, арбузы и другие местные продукты.")},
    {"key": "beach", "icon": "beach", "img": "bikini-beach",
     "en": ("Bikini beaches", "Two designated bikini beaches with soft white sand, palms and clear turquoise water — and a coral reef close to shore for snorkelling."),
     "ru": ("Бикини-пляжи", "Два бикини-пляжа с мягким белым песком, пальмами и прозрачной бирюзовой водой — а коралловый риф совсем рядом с берегом.")},
    {"key": "harbour", "icon": "boat", "img": "harbour-arrival",
     "en": ("Arrival by speedboat", "Your holiday begins on the water: the shared speedboat from Malé glides across the atoll to Thoddoo, where your island stay begins."),
     "ru": ("Прибытие на катере", "Отпуск начинается на воде: групповой скоростной катер из Мале скользит по атоллу к Тодду, где начинается ваш островной отдых.")},
    {"key": "sunset", "icon": "sun", "img": "thoddoo-sunset",
     "en": ("Sunset beach", "Evenings on Thoddoo end with golden sunsets over the Indian Ocean — find a quiet spot on the sand and watch the sky change colour."),
     "ru": ("Закаты на пляже", "Вечера на Тодду заканчиваются золотыми закатами над Индийским океаном — найдите тихое место на песке и наблюдайте, как меняется небо.")},
]
LM_HEAD = {"en": ("Island highlights", "The places that make <em>Thoddoo</em>", "Tap a place to read more."),
           "ru": ("Достопримечательности", "Места, которые делают <em>Тодду</em> особенным", "Нажмите, чтобы узнать больше.")}


def landmarks(lang):
    out = ""
    for i, l in enumerate(LANDMARKS):
        t, d = l[lang]
        out += (f'<button class="lm rv d{i % 3 + 1}" data-modal data-img="{{R}}assets/img/{l["img"]}.webp" data-title="{E(t)}" data-kicker="{E(LM_HEAD[lang][0])}" aria-haspopup="dialog">'
                f'<figure>{img(l["img"], t, "(max-width:760px) 100vw, 33vw")}</figure><span class="xp__ico">{icon(l["icon"])}</span>'
                f'<span class="lm__b"><h3>{t}</h3><span class="lm__more">{UI[lang]["discover"]} {icon("arrow")}</span></span>'
                f'<span class="xp__detail"><p>{d}</p></span></button>')
    h = LM_HEAD[lang]
    return f'<section class="sec sec--white"><div class="wrap">{head(h[0], h[1], h[2])}<div class="lm-grid">{out}</div></div></section>'

# ================================================================== pages
def p_index(lang, r):
    U = UI[lang]; T = T3[lang]; H = HERO[lang]; A = ABOUT[lang]; TH = THODDOO[lang]
    figs = ('<figure class="on"><video autoplay muted loop playsinline preload="auto" poster="{R}assets/img/hero-video-poster.webp" aria-hidden="true">'
            '<source src="{R}assets/video/hero-1080.mp4" type="video/mp4" media="(min-width: 901px)">'
            '<source src="{R}assets/video/hero-720.mp4" type="video/mp4"></video></figure>')
    B = T["book"]
    popts = f'<option value="">{B["any"]}</option>' + "".join(f'<option value="{p["key"]}">{p[lang]["name"]}</option>' for p in PACKAGES)
    gopts = "".join(f"<option{' selected' if n == 2 else ''}>{n}</option>" for n in range(1, 11))
    stmt = T["statement"].replace("{I1}", img("turtle", "", "120px")).replace("{I2}", img("papaya", "", "120px"))
    pillars = "".join(f'<div class="pillar rv d{i + 1}"><span class="pillar__i">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(T["pillars"]))
    trip = "".join(f'<figure class="img-rv">{img(n, c, "33vw")}</figure>' for n, c in zip(["turtle-reef", "bikini-beach", "guesthouse-4"], T["trip"]))
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
    ribbon = "".join(f"<span>{icon(ic)}{m}</span>" for ic, m in list(zip(["turtle", "drone", "island", "fishing", "dolphin", "leaf", "dinner"], MARQUEE[lang])) * 2)
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
  <label class="book__f"><small>{icon("users")}{B["guests"]}</small><select name="adults">{gopts}</select></label>
  <label class="book__f"><small>{icon("island")}{B["pkg"]}</small><select name="package">{popts}</select></label>
  <button class="btn btn--gold" type="submit">{B["go"]} {icon("arrow")}</button>
</form></div></div>

<section class="sec">
  <div class="wrap">
    <div style="text-align:center;margin-bottom:34px">{label(T["intro_label"])}</div>
    <p class="statement rv">{stmt}</p>
    <div class="pillars">{pillars}</div>
    <div class="triptych">{trip}</div>
  </div>
</section>

<section class="sec sec--white" id="packages">
  <div class="wrap">
    {head(T["pk_label"], T["pk_title"], T["pk_lead"], season_switch(lang), num="01")}
    <div class="pk-grid">{pk}</div>
  </div>
</section>

<div class="ribbon" aria-hidden="true"><div class="ribbon__t">{ribbon}</div></div>

<section class="sec">
  <div class="wrap">
    {head(T["xp_label"], T["xp_title"], T["xp_lead"], arrow_link(T["xp_all"], href(lang, "experiences", r)), num="02")}
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
    return f'''{page_hero(lang, r, "aerial-lagoon", P["eyebrow"], P["title"], P["lead"], "packages", full=True)}
<section class="sec"><div class="wrap">{blocks}<p class="note" style="text-align:center">{P["single"]}</p></div></section>
<section class="sec sec--white"><div class="wrap">
  {head(P["compare_eyebrow"], P["compare_title"], center=True)}
  <div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>{P["compare_cols"][0]}</th>{th}</tr></thead><tbody>{rows}</tbody>
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
    return f'''{page_hero(lang, r, "dolphin", X["eyebrow"], X["title"], X["lead"], "experiences")}
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
    gal_items = [("g1", "thoddoo-beach"), ("g2", "palm-road-aerial"), ("g3", "papaya"), ("g4", "vaau-magu"), ("g5", "turtle"), ("g6", "thoddoo-sunset")]
    gal = "".join(f'<button class="{c}" data-lb="{{R}}assets/img/{n}.webp" aria-label="{n.replace("-", " ")}">{img(n, n.replace("-", " "), "50vw")}<span class="zoom">{icon("zoom")}</span></button>' for c, n in gal_items)
    sea = "sea ~28°C" if lang == "en" else "вода ~28°C"
    return f'''{page_hero(lang, r, "thoddoo-aerial", TH["eyebrow"], TH["title"], TH["lead"], "thoddoo")}
<section class="sec"><div class="wrap split">
  <div class="split__media rv"><div class="m1 img-rv">{img("papaya-lush", "Papaya growing on Thoddoo", "50vw")}</div><div class="m2">{img("turtle-reef", "", "25vw")}</div>
</div>
  <div class="split__body rv d1">{label(TH["eyebrow"])}<h2>{TH["title"]}</h2>{"".join(f"<p>{p}</p>" for p in TH["p"])}<p class="note">{U["wildlife"]}</p></div>
</div></section>
{landmarks(lang)}
<section class="sec"><div class="wrap">{head(TH["right_eyebrow"], TH["right_title"])}<div class="rfy">{rfy}</div></div></section>
<section class="sec sec--white"><div class="wrap">{head(TH["gtk_eyebrow"], TH["gtk_title"], TH["gtk_lead"])}<div class="tiles8 rv">{gtk}</div></div></section>
<section class="sec--s"><div class="wrap">{head(T["gal"], TH["gallery_title"])}<div class="gal rv">{gal}</div></div></section>
{testimonials(lang, r)}
'''


def p_guesthouses(lang, r):
    G = GUEST[lang]; T = T3[lang]
    prom = "".join(f'<div class="rv d{i + 1}"><span class="why__i">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(G["promise"]))
    items = [("g1", 3), ("g2", 4), ("g3", 2), ("g4", 5), ("g5", 6), ("g6", 7)]
    gal = "".join(f'<button class="{c}" data-lb="{{R}}assets/img/guesthouse-{n}.webp" aria-label="Guesthouse {n}">{img(f"guesthouse-{n}", f"Thoddoo guesthouse {n}", "50vw")}<span class="zoom">{icon("zoom")}</span></button>' for c, n in items)
    return f'''{page_hero(lang, r, "guesthouse-5", G["eyebrow"], G["title"], G["lead"], "guesthouses")}
<section class="sec"><div class="wrap split">
  <div class="split__media rv"><div class="m1 img-rv">{img("guesthouse-1", "Double room in a Thoddoo guesthouse", "50vw")}</div><div class="m2">{img("guesthouse-2", "", "25vw")}</div></div>
  <div class="split__body rv d1">{label(G["eyebrow"])}<h2>{G["title"]}</h2>{"".join(f"<p>{p}</p>" for p in G["p"])}<p>{G["help"]}</p>
    <a class="btn btn--wa" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} WhatsApp</a></div>
</div></section>
<section class="sec--s sec--white"><div class="wrap promise">{prom}</div></section>
<section class="sec"><div class="wrap">{head(T["gal"], G["gallery"])}<div class="gal rv">{gal}</div></div></section>
{testimonials(lang, r)}
'''


def p_faq(lang, r):
    F = FAQ_HEAD[lang]; U = UI[lang]
    qa = "".join(f'<details class="qa"{" open" if i == 0 else ""}><summary><span class="why__i">{icon(q["icon"])}</span>{q[lang][0]}<span class="why__t"></span></summary><div class="qa__a">{q[lang][1]}</div></details>' for i, q in enumerate(FAQ))
    return f'''{page_hero(lang, r, "lagoon-boat", F["eyebrow"], F["title"], F["lead"], "faq")}
<section class="sec"><div class="wrap faq">
  <aside class="faq__side rv"><div class="helpcard on-dark">{label(U["nav"]["contact"])}<h3>{F["aside_t"]}</h3><p>{F["aside_p"]}</p>
    <a class="btn btn--wa" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{brand("whatsapp")} WhatsApp</a>
    <a class="btn btn--glass" href="mailto:{C["email"]}">{icon("mail")} E-mail</a></div></aside>
  <div class="rv d1">{qa}</div>
</div></section>
'''


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
    return f'''{page_hero(lang, r, "hero-sandbar", K["eyebrow"], K["title"], K["lead"], "contact")}
<section class="sec" id="enquiry"><div class="wrap conc">
  <form class="conc__main rv" id="enquiry-form" action="https://formsubmit.co/ajax/{C["email"]}" method="POST" data-wa="{C["whatsapp"]}" {data} novalidate>
    <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="steps">{steps_btns}</div>
    <div class="step on" data-step="0"><h3>{T["st_t"][0]}</h3><p>{T["st_p"][0]}</p><div class="opt-grid">{opts}</div>{nav(0)}</div>
    <div class="step" data-step="1"><h3>{T["st_t"][1]}</h3><p>{T["st_p"][1]}</p>
      <div class="frow"><div class="fld"><label for="f-arr">{F["arrival"]}</label><input id="f-arr" name="arrival" type="date"></div>
        <div class="fld"><label for="f-dep">{F["departure"]}</label><input id="f-dep" name="departure" type="date"></div></div>
      <div class="frow">{stepper("adults", 2, T["adults"])}{stepper("children", 0, T["children"])}</div>
      {nav(1)}</div>
    <div class="step" data-step="2"><h3>{T["st_t"][2]}</h3><p>{T["st_p"][2]}</p><div class="xopts">{xo}</div>{nav(2)}</div>
    <div class="step" data-step="3"><h3>{T["st_t"][3]}</h3><p>{T["st_p"][3]}</p>
      <div class="frow"><div class="fld"><label for="f-name">{F["name"]}</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div class="fld"><label for="f-email">{F["email"]}</label><input id="f-email" name="email" type="email" required autocomplete="email"></div></div>
      <div class="frow"><div class="fld"><label for="f-phone">{F["phone"]}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="{"+7 …" if lang == "ru" else "+44 …"}"></div>
        <fieldset class="fld"><legend>{T["reply"]}</legend><div class="seg"><label><input type="radio" name="reply" value="E-mail" checked><span>{icon("mail")}E-mail</span></label><label><input type="radio" name="reply" value="WhatsApp"><span>{brand("whatsapp")}WhatsApp</span></label></div></fieldset></div>
      <div class="fld"><label for="f-msg">{F["message"]}</label><textarea id="f-msg" name="message"></textarea></div>
      <p class="consent">{T["consent"]}</p>
      <div class="status" role="status" aria-live="polite"></div>
      <div class="step__nav"><button type="button" class="btn btn--line" data-prev-step>{T["back"]}</button>
        <div class="r"><button type="button" class="btn btn--wa" data-send-wa>{brand("whatsapp")} {T["send_wa"]}</button><button type="submit" class="btn btn--gold">{icon("mail")} {T["send"]}</button></div></div>
    </div>
    <div class="sent"><span class="sent__ic">{icon("check")}</span><h3>{T["done_t"]}</h3><p>{T["done_p"]}</p><a class="btn btn--ink" href="{href(lang, "index", r)}">{T["done_b"]}</a></div>
  </form>
  <aside class="sum">
    <div class="sum__card" aria-live="polite">
      <div class="sum__img"><img data-sum-img src="{{R}}assets/img/hero-sandbank-sm.webp" alt="" width="900" height="600"><strong data-sum="pkg">{T["not_sure"][0]}</strong></div>
      <div class="sum__rows">
        <div><span>{icon("calendar")}{T["s_dates"]}</span><span data-sum="dates">{T["s_none"]}</span></div>
        <div><span>{icon("clock")}{T["s_nights"]}</span><span data-sum="nights">{T["s_none"]}</span></div>
        <div><span>{icon("users")}{T["s_guests"]}</span><span data-sum="guests">2</span></div>
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
                    "containedInPlace": {"@type": "Country", "name": "Maldives"}, "geo": {"@type": "GeoCoordinates", "latitude": 4.4381, "longitude": 72.9586}})
    if page == "experiences":
        out.append({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "TouristAttraction", "name": e[lang][0], "description": e[lang][2]}} for i, e in enumerate(EXPERIENCES + MOMENTS)]})
    return "\n".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)


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
<link rel="stylesheet" href="{{R}}assets/css/fonts.css">
<link rel="stylesheet" href="{{R}}assets/css/site.css">
{jsonld(lang, page)}
</head>
<body>
{header(lang, page, r)}
<main id="main">
{BUILDERS[page](lang, r)}
</main>
{footer(lang, page, r)}
<script src="{{R}}assets/js/app.js" defer></script>
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
            urls += f"<url><loc>{url(lang, page)}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{prio.get(page, '0.6')}</priority>{alts}</url>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    json.dump({"name": "Velaa Getaways", "short_name": "Velaa", "start_url": "./", "display": "standalone", "background_color": "#f7f4ef",
               "theme_color": "#0c2a34", "icons": [{"src": "assets/brand/logo-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(ROOT, "site.webmanifest"), "w"))
    print("Built", len(PAGES) * 2, "pages")


if __name__ == "__main__":
    main()
