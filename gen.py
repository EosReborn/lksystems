# Statikus oldalgenerátor: futtatás -> python3 gen.py
# Minden .html fájlt, a sitemap.xml-t, a robots.txt-t újragenerálja.

import os
OUT = os.path.dirname(os.path.abspath(__file__))  # az oldalak a szkript mellé generálódnak

NAV = [("index.html","Kezdőlap"),("szolgaltatasok.html","Szolgáltatások"),("rolunk.html","Rólunk"),
       ("lakossagi.html","Lakossági"),("szechenyi-2020.html","Széchenyi 2020")]

SITE = "https://lk-systems.hu"
# A közösségi megosztáshoz (og:image) élő, elérhető URL kell. Amíg az oldal a Vercelen fut, ide mutat;
# a lk-systems.hu-ra költözés után állítsd SITE-ra.
OG_HOST = "https://lksystems.vercel.app"
import json
BUSINESS = {
 "@type":"ProfessionalService","@id":SITE+"/#business","name":"LK-SYSTEMS Informatikai, Kereskedelmi és Szolgáltató Bt.",
 "alternateName":"LK-SYSTEMS Bt.","url":SITE+"/","logo":SITE+"/images/logo-lk-systems.png","image":SITE+"/images/og-image.jpg",
 "telephone":"+36704167246","email":"info@lk-systems.hu","foundingDate":"2013",
 "description":"Informatikai rendszerek üzemeltetése, rendszergazda szolgáltatás, hálózatépítés és IT eszközbeszerzés kis- és középvállalkozásoknak Mosonmagyaróváron.",
 "address":{"@type":"PostalAddress","streetAddress":"Palánk utca 1.","postalCode":"9200","addressLocality":"Mosonmagyaróvár","addressCountry":"HU"},
 "areaServed":{"@type":"City","name":"Mosonmagyaróvár"},
 "sameAs":["https://www.facebook.com/lksystemsbt"],
 "taxID":"24357904-2-08",
 "knowsAbout":["Rendszergazda szolgáltatás","IT üzemeltetés","Hálózatépítés","Adatmentés","Vírusvédelem","Informatikai szaktanácsadás"]}
CRUMBS = {"szolgaltatasok.html":"Szolgáltatások","rolunk.html":"Rólunk","lakossagi.html":"Lakossági","szechenyi-2020.html":"Széchenyi 2020","kapcsolat.html":"Kapcsolat","suti.html":"Süti tájékoztató"}

def page(fname, title, desc, body, hero=None):
    url = SITE + "/" + ("" if fname=="index.html" else fname)
    graph = [BUSINESS, {"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"LK-SYSTEMS Bt.","inLanguage":"hu","publisher":{"@id":SITE+"/#business"}}]
    if fname not in ("index.html","404.html"):
        graph.append({"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Kezdőlap","item":SITE+"/"},
          {"@type":"ListItem","position":2,"name":CRUMBS[fname],"item":url}]})
    extra_head = '\n<link rel="preload" as="image" href="images/slide1.jpg" fetchpriority="high">' if fname=="index.html" else ""
    robots = "noindex, follow" if fname=="404.html" else "index, follow, max-image-preview:large"
    jsonld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h==fname else ""}>{t}</a>' for h,t in NAV)
    kap = ' aria-current="page"' if fname=="kapcsolat.html" else ""
    if hero:
        eyebrow, h1, lead = hero
        hero_html = f'''<section class="page-hero"><div class="wrap"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}</div></section>'''
    else:
        hero_html = ""
    return f'''<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0b2236">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="apple-touch-icon.png">{extra_head}
<meta property="og:type" content="website">
<meta property="og:locale" content="hu_HU">
<meta property="og:site_name" content="LK-SYSTEMS Bt.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_HOST}/images/og-image.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="LK-SYSTEMS Informatika – Saját rendszergazda, nem csak a nagyok kiváltsága">
<meta name="twitter:image" content="{OG_HOST}/images/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.className+=" js"</script>
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<a class="skip" href="#main">Ugrás a tartalomhoz</a>
<header class="nav">
  <div class="wrap nav-in">
    <a href="index.html" class="brand"><img src="images/logo-lk-systems.png" alt="LK-SYSTEMS Informatika" width="205" height="40"></a>
    <button type="button" class="burger" aria-label="Menü megnyitása" aria-expanded="false" aria-controls="main-menu"><span></span></button>
    <nav class="links" id="main-menu" aria-label="Főmenü">
      {nav}
      <a href="kapcsolat.html" class="btn btn-sm"{kap}>Kapcsolat</a>
    </nav>
  </div>
</header>
<main id="main">
{hero_html}{body}
</main>
<footer>
  <div class="wrap foot-in">
    <div>
      <strong>LK-SYSTEMS Informatikai, Kereskedelmi és Szolgáltató Bt.</strong><br>
      9200 Mosonmagyaróvár, Palánk utca 1.<br>
      <a href="tel:+36704167246">+36 70 416 7246</a> · <a href="mailto:info@lk-systems.hu">info@lk-systems.hu</a>
    </div>
    <div>
      Cégjegyzékszám: 08-06-014260<br>Adószám: 24357904-2-08<br>Bankszámlaszám: 1173076-20061193
    </div>
    <div>
      <a href="https://www.facebook.com/lksystemsbt" rel="noopener">Facebook</a> ·
      <a href="szechenyi-2020.html">Széchenyi 2020</a><br>
      <a href="suti.html">Süti tájékoztató</a> · <button type="button" class="linklike" data-cookie-settings>Süti beállítások</button><br>Fotók: <a href="https://www.pexels.com" rel="noopener">Pexels</a> · © 2026 LK-SYSTEMS Bt.
    </div>
  </div>
</footer>
<div class="cookie" id="cookie" role="dialog" aria-modal="false" aria-labelledby="cookie-t" hidden>
  <div class="cookie-in">
    <div><strong id="cookie-t">Sütiket használunk</strong>
    <p>Az oldal működéséhez szükséges sütiket mindig használjuk. Hozzájárulásával statisztikai sütiket is engedélyezhet, amelyek segítenek az oldal fejlesztésében. Részletek: <a href="suti.html">Süti tájékoztató</a>.</p></div>
    <div class="cookie-btns"><button type="button" class="btn" data-cookie="all">Elfogadom</button><button type="button" class="btn btn-ghost" data-cookie="necessary">Csak a szükségesek</button></div>
  </div>
</div>
<script src="script.js" defer></script>
</body>
</html>
'''

def write(name, content):
    with open(os.path.join(OUT, name), "w") as f: f.write(content)

CTA = '''<section class="section cta-band"><div class="wrap cta-in"><div><h2>Beszéljük meg, miben segíthetünk</h2><p>Kérjen ajánlatot, vagy hívjon minket – szívesen áttekintjük az Ön informatikai rendszerét.</p></div><div class="cta"><a href="kapcsolat.html" class="btn">Kapcsolat</a><a href="tel:+36704167246" class="btn btn-ghost-light">+36 70 416 7246</a></div></div></section>'''

STATS = '''<ul class="stats" aria-label="Általunk üzemeltetett géppark">
      <li><b>190</b><span>munkaállomás</span></li>
      <li><b>21</b><span>Windows szerver</span></li>
      <li><b>15</b><span>virtuális szerver</span></li>
      <li><b>63</b><span>aktív hálózati eszköz</span></li>
    </ul>'''

CARDS4 = '''<div class="grid four">
      <article class="card"><img class="media" src="images/stock/uzemeltetes.jpg" alt="Szerverszekrények egy szerverteremben" width="800" height="533" loading="lazy"><h3>IT üzemeltetés</h3><p>A szolgáltatás megrendelése esetén cégünk átveszi az Ön informatikai rendszerének üzemeltetésével kapcsolatos feladatokat.</p></article>
      <article class="card"><img class="media" src="images/stock/beszerzes.jpg" alt="RAM-modulok és hálózati kártyák" width="800" height="533" loading="lazy"><h3>IT beszerzés</h3><p>Szerződéses partnereink számára biztosítjuk a megfelelő hálózati eszközök, hardverek, szoftverek, valamint irodai kellékanyagok beszerzését.</p></article>
      <article class="card"><img class="media" src="images/stock/infrastruktura.jpg" alt="Hálózati patch panel kék kábelekkel" width="800" height="533" loading="lazy"><h3>Infrastruktúra</h3><p>A megbízható és hatékony informatikai rendszer alapja a megfelelő hálózati infrastruktúra megléte.</p></article>
      <article class="card"><img class="media" src="images/stock/tamogatas.jpg" alt="Fejhallgató ügyféltámogatáshoz" width="800" height="533" loading="lazy"><h3>Támogatás</h3><p>Munkatársainak és alkalmazottainak minden technikai segítséget megadunk, amire munkájuk során szükségük lehet.</p></article>
    </div>'''

PARTNERS = '''<section class="section alt"><div class="wrap">
    <p class="eyebrow">Partnereink</p><h2>Akik bíznak bennünk</h2>
    <ul class="logos">
      <li><a href="https://ambroziaetterem.hu" rel="noopener" aria-label="Ambrózia Étterem"><img src="images/partners/ambrozia.jpg" alt="Ambrózia Étterem" width="65" height="60" loading="lazy"></a></li>
      <li><a href="http://www.legjobbalkusz.hu" rel="noopener" aria-label="Global Alkusz"><img src="images/partners/globalalkusz.png" alt="Global Alkusz" width="275" height="60" loading="lazy"></a></li>
      <li><a href="https://movarprint.hu/" rel="noopener" aria-label="Movar Print"><img src="images/partners/movar_print_logo.png" alt="Movar Print" width="271" height="60" loading="lazy"></a></li>
      <li><a href="https://mptt.hu/" rel="noopener" aria-label="MPTT"><img src="images/partners/mptt_logo.png" alt="MPTT" width="146" height="60" loading="lazy"></a></li>
      <li><span class="nolink"><img src="images/partners/notefix.png" alt="Notefix" width="177" height="60" loading="lazy"></span></li>
      <li><a href="http://preinerbau.hu" rel="noopener" aria-label="Preiner Bau"><img src="images/partners/preinerlogo.png" alt="Preiner Bau" width="61" height="60" loading="lazy"></a></li>
    </ul></div></section>'''

# ---------- index
write("index.html", page("index.html",
 "Vállalati és lakossági informatika Mosonmagyaróvár – LK-SYSTEMS Bt.",
 "Rendszergazda szolgáltatás, informatikai üzemeltetés, hálózatépítés és eszközbeszerzés kis- és középvállalkozásoknak Mosonmagyaróváron.",
 f'''<section class="hero"><div class="wrap hero-in">
    <div>
      <p class="eyebrow">IT üzemeltetés · Mosonmagyaróvár</p>
      <h1>Saját rendszergazda.<br><span>Nem csak a nagyok kiváltsága.</span></h1>
      <p class="lead">Kis- és középvállalkozások, intézmények informatikai rendszereinek teljes körű üzemeltetése fix havidíjért – hogy Ön az alaptevékenységére koncentrálhasson.</p>
      <div class="cta"><a href="kapcsolat.html" class="btn">Kérjen ajánlatot</a><a href="tel:+36704167246" class="btn btn-ghost">+36 70 416 7246</a></div>
    </div>
    {STATS}
  </div></section>

<section class="section"><div class="wrap">
    <p class="eyebrow">Mit csinálunk</p>
    <h2>Minden, ami a megbízható informatikai működéshez kell</h2>
    {CARDS4}
    <p class="more"><a href="szolgaltatasok.html">Összes szolgáltatásunk →</a></p>
</div></section>

<section class="section dark"><div class="wrap split">
    <div>
      <p class="eyebrow">Kik vagyunk</p>
      <h2>2006 óta informatikusként, 2013 óta saját cégként</h2>
      <p>Mosonmagyaróváron és vonzáskörzetében segítjük a kis- és középvállalatokat, hogy hatékonyabbak és versenyképesebbek legyenek. Értékrendünk alapja a fedhetetlenség és az alázat ügyfeleink felé.</p>
      <p class="more"><a href="rolunk.html">Tudjon meg többet rólunk →</a></p>
    </div>
    <div class="panel-dark"><h3>Lakossági ügyfeleknek is</h3><p>Internet beállítás, szoftveres karbantartás, alkatrészek és perifériák – gyorsan és véglegesen.</p><p class="more"><a href="lakossagi.html">Lakossági szolgáltatások →</a></p></div>
</div></section>

{PARTNERS}
{CTA}''', None))

# ---------- szolgaltatasok
write("szolgaltatasok.html", page("szolgaltatasok.html",
 "Szolgáltatások – LK-SYSTEMS Bt. Mosonmagyaróvár",
 "Átalánydíjas rendszerfelügyelet, felhasználó támogatás, adatmentés, hálózatépítés, hardver- és szoftverértékesítés Mosonmagyaróváron.",
 f'''<section class="section"><div class="wrap">
    <h2 class="sr-only">Szolgáltatásaink</h2>
    {CARDS4}
    <div class="split">
      <div>
        <h2 class="h2s">Rendszergazda szolgáltatás</h2>
        <p>Vállalkozásunk fő tevékenysége <strong>informatikai rendszerek üzemeltetése kis és középvállalatoknak, intézményeknek.</strong></p>
        <p>A jelenlegi gazdasági helyzetben a pénzügyi és emberi erőforrások apadása elengedhetetlenné teszi a működési struktúra és a kiadások ésszerűsítését. Ilyen lépés lehet külső informatikai szolgáltató alkalmazása, hiszen az informatikai tevékenység kiszervezése már rövid távon költségcsökkenést és növekvő hatékonyságot eredményez.</p>
        <p>Az informatikai rendszer külső szolgáltató általi üzemeltetése olcsóbb, mint saját munkatárssal, a költségek pedig jól tervezhetők és ellenőrizhetők. Ma már a kis és középvállalatok több mint 50%-a külső informatikai szolgáltatót bíz meg az IT rendszereinek üzemeltetésével.</p>
        <p>Szolgáltatásainkat fix havidíjas rendszerben ajánljuk, de eseti jelleggel, óradíjas formában is állunk ügyfeleink rendelkezésére.</p>
      </div>
      <div class="panel"><h3>Akiknek ajánljuk</h3>
        <ul class="ticks">
          <li>Vállalkozásuk alaptevékenységére szeretnének koncentrálni.</li>
          <li>Javítani szeretnék meglévő informatikai rendszerük színvonalát, hogy az magas szinten szolgálja az üzleti folyamataikat.</li>
          <li>Nem akarnak saját IT-szakembert alkalmazni, de szeretnék egy kézben tartani az informatikai rendszert.</li>
        </ul></div>
    </div>
    <h2 class="h2s sub">Szolgáltatási portfólió</h2>
    <ul class="chips">
      <li>Átalánydíjas rendszerfelügyelet</li><li>Helyszíni és telefonos felhasználó támogatás</li><li>Kaspersky vírusvédelmi megoldások</li>
      <li>Ütemezett adatmentés</li><li>Hardver és szoftver leltár készítése</li><li>Hálózatépítés</li>
      <li>Hardver és szoftver értékesítés</li><li>Informatikai szaktanácsadás</li><li>Nyomtató kellékanyagok beszerzése</li><li>Nyomtató bérbeadás</li>
    </ul>
    <h2 class="h2s sub">Általunk üzemeltetett géppark</h2>
    {STATS}
    <p class="note">A jelenleg szerződéses ügyfeleinknél, cégünk által felügyelt munkaállomások és szerverek aktuális száma.</p>
</div></section>
{CTA}''',
 ("Szolgáltatások","Teljes körű IT üzemeltetés","Fix havidíjas rendszerfelügyelet, felhasználó támogatás, hálózatépítés és eszközbeszerzés egy kézből.")))

# ---------- rolunk
write("rolunk.html", page("rolunk.html",
 "Rólunk – LK-SYSTEMS Bt. Mosonmagyaróvár",
 "Az LK-SYSTEMS Bt. 2013 óta nyújt informatikai szolgáltatásokat Mosonmagyaróváron és vonzáskörzetében. 2006 óta dolgozunk informatikusként.",
 f'''<section class="section"><div class="wrap split">
    <div>
      <p>Az LK-SYSTEMS Informatikai, Kereskedelmi és Szolgáltató Bt.-t 2013-ban hoztuk létre azzal a céllal, hogy Mosonmagyaróváron és vonzáskörzetében működő kis- és középvállalatok számára nyújtsunk olyan informatikai szolgáltatásokat, melyekkel növelhetik hatékonyságukat és versenyképességüket.</p>
      <p>2006 óta dolgozunk informatikusként, és ez idő alatt számtalan problémát oldottunk meg, a legkülönbözőbb kihívásokat küzdöttük le, így ezen a területen rendkívül nagy tapasztalatra tettünk szert.</p>
      <p>Arra törekszünk, hogy szakmai tudásunk napra készen tartásával mindig minőségi, az aktuális informatikai trendeknek megfelelő megoldásokat szállítsunk.</p>
      <p>Igyekszünk ügyfeleink részére minden az informatikához szorosan kapcsolódó területen is megoldásokat találni, mint pl. üzleti telekommunikáció vagy biztonságtechnika. Ezeket a szolgáltatásokat helyi partnereinkkel együttműködve nyújtjuk.</p>
      <p>Tisztában vagyunk vele, hogy a piacon egyre több cég nyújt hasonló szolgáltatásokat, ezért felkészültségünkkel és hozzáállásunkkal próbálunk kitűnni közülük. Cégünk előre lefektetett értékrend alapján működik, és üzleti döntéseinket is ezen értékekkel összhangban hozzuk meg. Ezek közül a legfontosabbak a <strong>fedhetetlenség</strong> és az <strong>alázat</strong> ügyfeleink felé.</p>
    </div>
    <ul class="stats one" aria-label="Rövid számok"><li><b>2006</b><span>óta dolgozunk informatikusként</span></li><li><b>2013</b><span>óta működik a cégünk</span></li></ul>
</div></section>

<section class="section dark"><div class="wrap">
    <p class="eyebrow">Válasszanak minket, mert…</p>
    <h2>Öt ok, amiért ügyfeleink velünk maradnak</h2>
    <ol class="why">
      <li><b>Szeretjük, amit csinálunk.</b> Meggyőződésünk, hogy az ember csak akkor lehet kiemelkedő és sikeres valamiben, ha szereti azt, amit csinál.</li>
      <li><b>Mindenki egyformán fontos.</b> Nem teszünk különbséget egy két fős vállalkozás és egy több száz embert foglalkoztató vállalat között.</li>
      <li><b>100%-os elégedettség.</b> A mindennapi munkák eredményeit ügyfeleink visszajelzései alapján értékeljük, és csak a 100%-os elégedettséggel érjük be.</li>
      <li><b>Hosszú távú együttműködés.</b> Legfőbb célunk a hosszú távú, sikeres és eredményes együttműködés, nem a gyors pénzszerzés.</li>
      <li><b>Legjobb árak.</b> Számos helyi partnerrel és az ország legnagyobb beszállítóival állunk szerződéses kapcsolatban, hogy Önnek a legjobb árakat és szolgáltatásokat tudjuk nyújtani.</li>
    </ol>
</div></section>
{PARTNERS}
{CTA}''',
 ("Kik vagyunk","Helyi csapat, országos beszállítók","Több mint másfél évtizede dolgozunk informatikusként Mosonmagyaróváron.")))

# ---------- lakossagi
write("lakossagi.html", page("lakossagi.html",
 "Lakossági informatika – LK-SYSTEMS Bt. Mosonmagyaróvár",
 "Otthoni internet beállítás, számítógép szoftveres karbantartás, alkatrészek és perifériák Mosonmagyaróváron.",
 f'''<section class="section"><div class="wrap">
    <h2 class="sr-only">Lakossági szolgáltatásaink</h2>
    <div class="grid three">
      <article class="card"><img class="media" src="images/stock/internet.jpg" alt="Wifi router" width="800" height="533" loading="lazy"><h3>Internet beállítás</h3><p>Segítünk az otthoni vezetékes vagy vezeték nélküli hálózat beállításában, hogy kényelmesen használhassa számítógépét, okostelefonját, tabletjét, TV-jét.</p></article>
      <article class="card"><img class="media" src="images/stock/szoftver.jpg" alt="Programkód a képernyőn" width="800" height="533" loading="lazy"><h3>Szoftveres karbantartás</h3><p>Lassabbnak tűnik a számítógépe, mint korábban? Nem azt a teljesítményt nyújtja, amit megszokott? Gyorsan és véglegesen orvosoljuk a problémát!</p></article>
      <article class="card"><img class="media" src="images/stock/periferia.jpg" alt="Monitor, billentyűzet és egér az asztalon" width="800" height="533" loading="lazy"><h3>Alkatrészek, perifériák</h3><p>Bővítené számítógépét? Tönkrement egy alkatrész? Egyszerűen csak szüksége van egy új monitorra vagy nyomtatóra? Megtaláljuk a legjobb megoldást!</p></article>
    </div>
</div></section>
{CTA}''',
 ("Lakossági ügyfeleknek","Otthoni gépek, hálózatok, eszközök","Gyors, megbízható segítség otthonra is.")))

# ---------- szechenyi
write("szechenyi-2020.html", page("szechenyi-2020.html",
 "Széchenyi 2020 – GINOP-5.2.4-16 program – LK-SYSTEMS Bt.",
 "GINOP-5.2.4-16 Gyakornoki program pályakezdők támogatására – a program megvalósulása az LK-SYSTEMS Bt.-nél.",
 '''<section class="section"><div class="wrap split">
    <div>
      <h2 class="h2s">A program megvalósulása az LK-SYSTEMS Bt.-nél</h2>
      <dl class="facts">
        <div><dt>A kedvezményezett neve</dt><dd>LK-SYSTEMS Bt.</dd></div>
        <div><dt>A projekt címe</dt><dd>Gyakornoki program az LK-SYSTEMS Betéti társaságnál</dd></div>
        <div><dt>Szerződés száma</dt><dd>GINOP-5.2.4-16-2017-02008</dd></div>
        <div><dt>Támogatás összege</dt><dd>3 589 975 Ft</dd></div>
        <div><dt>Támogatás mértéke</dt><dd>100%</dd></div>
        <div><dt>Pályázat záró dátuma</dt><dd>2018. november 30.</dd></div>
      </dl>
      <p>Az LK-SYSTEMS Bt. 2013-ban jött létre azzal a céllal, hogy Mosonmagyaróváron és környékén működő kkv-k számára nyújtson olyan informatikai szolgáltatásokat, melyek növelhetik hatékonyságukat és versenyképességüket. A társaság a kezdetektől IT rendszerek üzemeltetésével, hálózatépítéssel, hibaelhárítással, informatikai eszközök karbantartásával, kereskedelmével és egyéb felhő (Cloud) szolgáltatások nyújtásával foglalkozik. Folyamatosan bővülő ügyfélkörükben megtalálható az 1-2 fős mikrovállalkozásoktól a több száz főt foglalkoztató kis- és középvállalkozás is.</p>
      <p>A program elsődleges célja a közvetlen munkahelyteremtés elősegítésén túl az iskolai rendszerű képzésben megszerzett szakképesítés hasznosulásának elősegítése, a fiatalok korai munkahelyi tapasztalathoz segítése, ezzel a későbbi foglalkoztathatóságuk és cégünk versenyképességének növelése. Ennek keretében az LK-SYSTEMS Bt. 13 és fél hónapon keresztül foglalkoztat egy fő rendszergazda gyakornokot, akinek fejlődését a munkahelyi mentor, valamint újonnan beszerzett IT berendezések, eszközök segítik.</p>
      <p>A programmal kapcsolatos további információ: <a href="mailto:balazs@lk-systems.hu">balazs@lk-systems.hu</a></p>
    </div>
    <figure class="sz"><img src="images/szechenyi-2020.jpg" alt="Magyarország Kormánya, Európai Unió – Európai Szociális Alap, Befektetés a jövőbe, Széchenyi 2020" width="434" height="300"></figure>
</div></section>''',
 ("Széchenyi 2020","GINOP&#8209;5.2.4&#8209;16 Gyakornoki program pályakezdők támogatására",None)))

# ---------- kapcsolat
write("kapcsolat.html", page("kapcsolat.html",
 "Kapcsolat – LK-SYSTEMS Bt. Mosonmagyaróvár",
 "LK-SYSTEMS Bt., 9200 Mosonmagyaróvár, Palánk utca 1. Telefon: +36 70 416 7246, e-mail: info@lk-systems.hu",
 '''<section class="section"><div class="wrap">
    <h2 class="sr-only">Elérhetőségeink</h2>
    <div class="grid three contact">
      <a class="card link" href="tel:+36704167246"><span class="ico" aria-hidden="true">📞</span><h3>Telefon</h3><p>+36 70 416 7246</p></a>
      <a class="card link" href="mailto:info@lk-systems.hu"><span class="ico" aria-hidden="true">✉️</span><h3>E-mail</h3><p>info@lk-systems.hu</p></a>
      <a class="card link" href="https://www.google.com/maps/search/?api=1&amp;query=9200+Mosonmagyar%C3%B3v%C3%A1r,+Pal%C3%A1nk+utca+1." target="_blank" rel="noopener"><span class="ico" aria-hidden="true">📍</span><h3>Cím</h3><p>9200 Mosonmagyaróvár,<br>Palánk utca 1.</p></a>
    </div>
    <div class="panel info">
      <h3>További információk</h3>
      <dl class="facts">
        <div><dt>Cégnév</dt><dd>LK-SYSTEMS Informatikai, Kereskedelmi és Szolgáltató Bt.</dd></div>
        <div><dt>Cégjegyzékszám</dt><dd>08-06-014260</dd></div>
        <div><dt>Adószám</dt><dd>24357904-2-08</dd></div>
        <div><dt>Bankszámlaszám</dt><dd>1173076-20061193</dd></div>
      </dl>
    </div>
</div></section>''',
 ("Kapcsolat","Beszéljük meg, miben segíthetünk","Hívjon, írjon, vagy keressen fel minket Mosonmagyaróváron.")))

write("suti.html", page("suti.html",
 "Süti tájékoztató – LK-SYSTEMS Bt.",
 "Tájékoztató arról, hogy a lk-systems.hu milyen sütiket használ, és hogyan módosíthatja a hozzájárulását.",
 '''<section class="section"><div class="wrap prose">
    <h2 class="h2s">Mik azok a sütik?</h2>
    <p>A sütik (cookie-k) kis szöveges fájlok, amelyeket a weboldal az Ön böngészőjében tárol. Segítségükkel az oldal megjegyzi a beállításait, illetve ismeri fel a visszatérő látogatót.</p>
    <h2 class="h2s">Milyen sütiket használunk?</h2>
    <dl class="facts">
      <div><dt>Szükséges</dt><dd>Az oldal alapműködéséhez, és a süti-hozzájárulás megjegyzéséhez kell (böngészőtárhely: <code>lk_cookie_consent</code>, 12 hónapig). Nem kér hozzájárulást.</dd></div>
      <div><dt>Statisztikai</dt><dd>Csak az Ön hozzájárulásával kapcsolható be. Jelenleg nem használunk ilyen szolgáltatást; ha bevezetjük, ez a tájékoztató frissül.</dd></div>
    </dl>
    <h2 class="h2s">Hozzájárulás módosítása</h2>
    <p>A választását bármikor módosíthatja: <button type="button" class="btn btn-sm" data-cookie-settings>Süti beállítások megnyitása</button></p>
    <p>A sütiket a böngészője beállításaiban is törölheti vagy letilthatja.</p>
    <h2 class="h2s">Az adatkezelő</h2>
    <p>LK-SYSTEMS Informatikai, Kereskedelmi és Szolgáltató Bt., 9200 Mosonmagyaróvár, Palánk utca 1., <a href="mailto:info@lk-systems.hu">info@lk-systems.hu</a>.</p>
  </div></section>''',
 ("Jogi tájékoztató","Süti tájékoztató",None)))

write("404.html", page("404.html",
 "Az oldal nem található – LK-SYSTEMS Bt.",
 "A keresett oldal nem található. Térjen vissza a kezdőlapra, vagy vegye fel velünk a kapcsolatot.",
 '''<section class="section"><div class="wrap prose">
    <p>Az oldal, amit keres, nem létezik vagy áthelyeztük. Az alábbi linkeken találhat tovább:</p>
    <p class="cta"><a href="index.html" class="btn">Vissza a kezdőlapra</a><a href="kapcsolat.html" class="btn btn-ghost">Kapcsolat</a></p>
  </div></section>''',
 ("404-es hiba","Az oldal nem található",None)))

# sitemap + robots
import datetime
today = datetime.date.today().isoformat()
pages = ["index.html","szolgaltatasok.html","rolunk.html","lakossagi.html","szechenyi-2020.html","kapcsolat.html","suti.html"]
prio = {"index.html":"1.0","szolgaltatasok.html":"0.9","kapcsolat.html":"0.8","rolunk.html":"0.7","lakossagi.html":"0.7","szechenyi-2020.html":"0.4","suti.html":"0.2"}
urls = "".join(f"  <url><loc>{SITE}/{'' if p=='index.html' else p}</loc><lastmod>{today}</lastmod><priority>{prio[p]}</priority></url>\n" for p in pages)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("ok")
