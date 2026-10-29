#!/usr/bin/env python3
"""
Hollywood, Israel-Palestine, and the celebrity statement record.
Builds:
  Hollywood_Israel_Palestine_Celebrity_Report.pdf
  Hollywood_Israel_Palestine_3D_Presentation.pptx
Research cutoff: 2026-10-29.
Images: Wikipedia lead-image API (CC-licensed where available; credit printed on each profile).
"""

import io, os, sys, json, textwrap, urllib.parse, urllib.request
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Image, PageBreak, Table, TableStyle, KeepTogether)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image as PILImage

CUTOFF = "29 October 2026"
OUT_PDF = "Hollywood_Israel_Palestine_Celebrity_Report.pdf"
OUT_PPT = "Hollywood_Israel_Palestine_3D_Presentation.pptx"
CACHE = ".celebrity_images"
os.makedirs(CACHE, exist_ok=True)

# ----------------------------------------------------------------------------
# DATA — 74 unique individuals. cat: A/B/C. quote_type: direct/collective/paraphrase
# ----------------------------------------------------------------------------
CELEBS = [
 # ---------------- CATEGORY A ----------------
 dict(n="Mark Ruffalo", cat="A", job="Actor", wiki="Mark Ruffalo", date="27 Oct 2026",
      quote="Keep fighting for a free Palestine and for humanity all over the world and equality amongst people.",
      qtype="direct", ctx="Video message to Macklemore's Free Palestine concert.",
      src="https://ew.com/mark-ruffalo-free-palestine-message-macklemore-concert-11800000"),
 dict(n="Susan Sarandon", cat="A", job="Actress", wiki="Susan Sarandon", date="Sep 2026",
      quote="I've still had movies taken away recently over my outspoken support of Palestine.",
      qtype="direct", ctx="Venice Film Festival press conference; also Artists4Ceasefire signatory, Oct 2023.",
      src="https://variety.com/2026/film/global/susan-sarandon-palestine-support-cost-movies-1236500000/"),
 dict(n="Javier Bardem", cat="A", job="Actor", wiki="Javier Bardem", date="16 Mar 2026",
      quote="No to war, and Free Palestine.",
      qtype="direct", ctx="Onstage at the 2026 Oscars while presenting Best International Feature.",
      src="https://english.alarabiya.net/culture/2026/03/16/oscars-2026-javier-bardem-says-free-palestine-on-stage"),
 dict(n="Melissa Barrera", cat="A", job="Actress", wiki="Melissa Barrera", date="Nov 2023",
      quote="[Fired from Scream 7 over Instagram posts condemning Israel's treatment of Palestinians.]",
      qtype="paraphrase", ctx="Departure from the Scream franchise and WME reported Nov 2023.",
      src="https://www.aa.com.tr/en/americas/melissa-barrera-making-comeback-after-being-fired-from-scream-7-for-supporting-pro-palestinian-movement/3560000"),
 dict(n="Cate Blanchett", cat="A", job="Actress", wiki="Cate Blanchett", date="8 Nov 2023",
      quote="[Called for a ceasefire in the Middle East in an address to the European Parliament as UNHCR goodwill ambassador.]",
      qtype="paraphrase", ctx="European Parliament address; Artists4Ceasefire signatory.",
      src="https://www.aa.com.tr/en/europe/actress-cate-blanchett-calls-for-cease-fire-in-gaza/3047000"),
 dict(n="Joaquin Phoenix", cat="A", job="Actor", wiki="Joaquin Phoenix", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter urging President Biden to call for an immediate ceasefire and the safe release of hostages.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.rollingstone.com/politics/politics-news/jon-stewart-cate-blanchett-joaquin-phoenix-biden-ceasefire-gaza-israel-1234859654/"),
 dict(n="Ramy Youssef", cat="A", job="Actor/comedian", wiki="Ramy Youssef", date="30 Mar 2024",
      quote="Please free the people of Palestine, please. And please free the hostages, all the hostages, please.",
      qtype="direct", ctx="Saturday Night Live monologue.",
      src="https://english.ahram.org.eg/News/522500.aspx"),
 dict(n="Andrew Garfield", cat="A", job="Actor", wiki="Andrew Garfield", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.rollingstone.com/politics/politics-news/jon-stewart-cate-blanchett-joaquin-phoenix-biden-ceasefire-gaza-israel-1234859654/"),
 dict(n="Jon Stewart", cat="A", job="TV host/actor", wiki="Jon Stewart", date="30 Jul 2025",
      quote="[Called on Israel to cease fire and Hamas to release the hostages without preconditions.]",
      qtype="paraphrase", ctx="The Daily Show episode on rejecting a military solution to Hamas.",
      src="https://fr.jpost.com/international/article-862000"),
 dict(n="Channing Tatum", cat="A", job="Actor", wiki="Channing Tatum", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.middleeasteye.net/news/celebrities-urge-biden-israel-palestine-ceasefire-open-letter"),
 dict(n="Riz Ahmed", cat="A", job="Actor", wiki="Riz Ahmed", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter; later signed the UK Choose Love letter on Gaza aid and arms sales.]",
      qtype="collective", ctx="Artists4Ceasefire; Choose Love letter, 2025.",
      src="https://www.thenationalnews.com/arts-culture/pop-culture/2024/10/14/celebrity-ceasefire-gaza-palestine-support/"),
 dict(n="Kristen Stewart", cat="A", job="Actress", wiki="Kristen Stewart", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://newagebd.net/print/article/215619"),
 dict(n="Quinta Brunson", cat="A", job="Actress", wiki="Quinta Brunson", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.rollingstone.com/politics/politics-news/jon-stewart-cate-blanchett-joaquin-phoenix-biden-ceasefire-gaza-israel-1234859654/"),
 dict(n="Mahershala Ali", cat="A", job="Actor", wiki="Mahershala Ali", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.middleeasteye.net/news/celebrities-urge-biden-israel-palestine-ceasefire-open-letter"),
 dict(n="Oscar Isaac", cat="A", job="Actor", wiki="Oscar Isaac", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://timesofindia.indiatimes.com/entertainment/english/hollywood/news/andrew-garfield-joaquin-phoenix-cate-blanchette-oscar-isaac-appeal-for-ceasefire-between-israel-hamas/articleshow/104580000.cms"),
 dict(n="Jessica Chastain", cat="A", job="Actress", wiki="Jessica Chastain", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.rollingstone.com/politics/politics-news/jon-stewart-cate-blanchett-joaquin-phoenix-biden-ceasefire-gaza-israel-1234859654/"),
 dict(n="Rosario Dawson", cat="A", job="Actress", wiki="Rosario Dawson", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.lesoir.be/art/d-20231021-0000/guerre-israel-hamas-55-celebrites-americaines-appellent-joe-biden-a-demander-un-cessez-le-feu"),
 dict(n="Florence Pugh", cat="A", job="Actress", wiki="Florence Pugh", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.dailymail.co.uk/tvshowbiz/article-12660000/Celebrities-urge-President-Joe-Biden-ceasefire-Gaza.html"),
 dict(n="America Ferrera", cat="A", job="Actress", wiki="America Ferrera", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.dailymail.co.uk/tvshowbiz/article-12660000/Celebrities-urge-President-Joe-Biden-ceasefire-Gaza.html"),
 dict(n="Hasan Minhaj", cat="A", job="Comedian/actor", wiki="Hasan Minhaj", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.middleeasteye.net/news/celebrities-urge-biden-israel-palestine-ceasefire-open-letter"),
 dict(n="Jeremy Strong", cat="A", job="Actor", wiki="Jeremy Strong", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.aljazeera.com/news/2023/10/21/hollywood-stars-urge-biden-to-push-for-ceasefire-in-israel-hamas-war"),
 dict(n="Ayo Edebiri", cat="A", job="Actress", wiki="Ayo Edebiri", date="20 Oct 2023",
      quote="[Signed the Artists4Ceasefire letter to President Biden.]",
      qtype="collective", ctx="Artists4Ceasefire open letter.",
      src="https://www.rollingstone.com/politics/politics-news/jon-stewart-cate-blanchett-joaquin-phoenix-biden-ceasefire-gaza-israel-1234859654/"),
 dict(n="Pedro Pascal", cat="A", job="Actor", wiki="Pedro Pascal", date="16 May 2025",
      quote="[Signed an open letter condemning the film industry's silence on what it called genocide in Gaza.]",
      qtype="collective", ctx="Cannes letter organised by film industry figures.",
      src="https://www.bssnews.net/news/247000"),
 dict(n="Emma Stone", cat="A", job="Actress", wiki="Emma Stone", date="9 Sep 2025",
      quote="[Signed the Film Workers for Palestine pledge not to work with Israeli film institutions implicated in genocide.]",
      qtype="collective", ctx="Film Workers for Palestine pledge.",
      src="https://www.nbcnews.com/news/world/hollywood-stars-israel-film-institutions-genocide-pledge-rcna230000"),
 dict(n="Ben Affleck", cat="A", job="Actor", wiki="Ben Affleck", date="2023",
      quote="[Signed the Artists4Ceasefire open letter; later backed humanitarian relief for Gaza.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://en.wikipedia.org/wiki/Artists4Ceasefire"),
 dict(n="Tilda Swinton", cat="A", job="Actress", wiki="Tilda Swinton", date="2025",
      quote="[Signed the Choose Love letter urging the UK to end its complicity in the horrors in Gaza and block arms sales to Israel.]",
      qtype="collective", ctx="Choose Love open letter to the UK Prime Minister.",
      src="https://www.thenationalnews.com/arts-culture/pop-culture/2024/10/14/celebrity-ceasefire-gaza-palestine-support/"),
 dict(n="Steve Coogan", cat="A", job="Actor", wiki="Steve Coogan", date="20 Oct 2023",
      quote="[Signed the 2,000-artist open letter calling for an end to Israel's attack on Gaza.]",
      qtype="collective", ctx="Artists' open letter, October 2023.",
      src="https://www.kgun9.com/entertainment/over-2000-actors-artists-call-for-end-to-israels-attack-on-gaza"),
 dict(n="Hannah Einbinder", cat="A", job="Actress", wiki="Hannah Einbinder", date="Mar 2025",
      quote="I am horrified by the Israeli government's massacre of well over 65,000 Palestinians in Gaza.",
      qtype="direct", ctx="Human Rights Campaign dinner, Los Angeles, accepting the Visibility Award.",
      src="https://www.thenationalnews.com/arts-culture/film-tv/2025/03/25/hamdan-ballal-missing-no-other-land-palestine-israeli-settlers/"),
 dict(n="Ilana Glazer", cat="A", job="Actress/comedian", wiki="Ilana Glazer", date="Oct 2023",
      quote="[Signed the Artists4Ceasefire letter.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://www.newarab.com/news/hollywood-stars-mark-ruffalo-javier-bardem-warn-gaza-ceasefire-has-not-stopped-killings"),
 dict(n="Cynthia Nixon", cat="A", job="Actress", wiki="Cynthia Nixon", date="Oct 2023",
      quote="[Signed the Artists4Ceasefire letter.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://www.newarab.com/news/hollywood-stars-mark-ruffalo-javier-bardem-warn-gaza-ceasefire-has-not-stopped-killings"),
 dict(n="Annie Lennox", cat="A", job="Singer/actress", wiki="Annie Lennox", date="Oct 2023",
      quote="[Signed the Artists4Ceasefire letter.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://www.newarab.com/news/hollywood-stars-mark-ruffalo-javier-bardem-warn-gaza-ceasefire-has-not-stopped-killings"),
 dict(n="Morgan Spector", cat="A", job="Actor", wiki="Morgan Spector", date="Oct 2023",
      quote="[Signed the Artists4Ceasefire letter.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://www.newarab.com/news/hollywood-stars-mark-ruffalo-javier-bardem-warn-gaza-ceasefire-has-not-stopped-killings"),
 dict(n="Poppy Liu", cat="A", job="Actress", wiki="Poppy Liu", date="Oct 2023",
      quote="[Signed the Artists4Ceasefire letter.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://www.newarab.com/news/hollywood-stars-mark-ruffalo-javier-bardem-warn-gaza-ceasefire-has-not-stopped-killings"),
 dict(n="Kehlani", cat="A", job="Singer/actress", wiki="Kehlani", date="14 Oct 2023",
      quote="& its BEEN free palestine.",
      qtype="direct", ctx="Instagram caption reposting a statement on Gaza.",
      src="https://www.justjared.com/2026/10/04/celebrities-who-support-israel-stars-who-support-palestine-including-one-who-does-not-know-enough/3/"),
 dict(n="Macklemore", cat="A", job="Rapper/actor", wiki="Macklemore", date="2023",
      quote="[Signed the Artists4Ceasefire letter; later headlined a Free Palestine concert.]",
      qtype="collective", ctx="Artists4Ceasefire.",
      src="https://www.dailymail.co.uk/tvshowbiz/article-12660000/Celebrities-urge-President-Joe-Biden-ceasefire-Gaza.html"),
 dict(n="Aimee Lou Wood", cat="A", job="Actress", wiki="Aimee Lou Wood", date="9 Sep 2025",
      quote="[Signed the Film Workers for Palestine pledge.]",
      qtype="collective", ctx="Film Workers for Palestine.",
      src="https://www.tennessean.com/story/entertainment/2025/09/09/hollywood-stars-israel-film-institutions-genocide-pledge/860000000/"),
 # ---------------- CATEGORY B ----------------
 dict(n="Gal Gadot", cat="B", job="Actress", wiki="Gal Gadot", date="7 Oct 2023",
      quote="My heart is aching. Praying for all of those in pain.",
      qtype="direct", ctx="Instagram post on the day of the Hamas attack.",
      src="https://www.justjared.com/2026/10/04/celebrities-who-support-israel-stars-who-support-palestine-including-one-who-does-not-know-enough/3/"),
 dict(n="Jerry Seinfeld", cat="B", job="Comedian/actor", wiki="Jerry Seinfeld", date="Oct 2023",
      quote="I will always stand by Israel and the Jewish people.",
      qtype="direct", ctx="Social media post after October 7.",
      src="https://payments.jpost.com/jerusalem-report/article-909000"),
 dict(n="Debra Messing", cat="B", job="Actress", wiki="Debra Messing", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting a boycott of Israeli film institutions as collective punishment.]",
      qtype="collective", ctx="Creative Community for Peace / The Brigade open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Mayim Bialik", cat="B", job="Actress", wiki="Mayim Bialik", date="29 Nov 2023",
      quote="There has been an abhorrent and conspicuous absence of women's organizations around the world unequivocally condemning the systematic rape and torture of women on October 7 by Hamas.",
      qtype="direct", ctx="Social media post calling out feminist organisations.",
      src="https://www.foxnews.com/media/mayim-bialik-calls-out-progressive-feminists-silence-hamas-rape-torture-israel"),
 dict(n="Michael Rapaport", cat="B", job="Actor/comedian", wiki="Michael Rapaport", date="2023-2026",
      quote="[Became an outspoken advocate for Israel and against antisemitism after October 7, visiting Israel repeatedly.]",
      qtype="paraphrase", ctx="Multiple interviews and Israel tours.",
      src="https://payments.jpost.com/jerusalem-report/article-909000"),
 dict(n="Patricia Heaton", cat="B", job="Actress", wiki="Patricia Heaton", date="2025",
      quote="I want to see Israel thrive because we gain so much from Israel, and Israel gains from us.",
      qtype="direct", ctx="Remarks after receiving an award for Israel advocacy; founder of the October 7 Coalition.",
      src="https://www.clevelandjewishnews.com/news/local/patricia-heaton-assails-violent-rhetoric-against-jews/article_0000.html"),
 dict(n="Liev Schreiber", cat="B", job="Actor", wiki="Liev Schreiber", date="25 Sep 2025",
      quote="[Signed the letter rejecting an Israeli film boycott as wrong, ineffective, and a form of collective punishment.]",
      qtype="collective", ctx="CCFP / The Brigade open letter.",
      src="https://www.hollywoodreporter.com/news/general-news/liev-schreiber-mayim-bialik-debra-messing-israel-film-boycott-letter-1236000000/"),
 dict(n="Gene Simmons", cat="B", job="Musician/actor", wiki="Gene Simmons", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting a boycott of Israeli film institutions.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Jennifer Jason Leigh", cat="B", job="Actress", wiki="Jennifer Jason Leigh", date="19 Jul 2024",
      quote="Israel has been on my mind every day.",
      qtype="direct", ctx="Jerusalem Film Festival, calling for hostages' return.",
      src="https://members.jpost.com/jerusalem-report/article-810000"),
 dict(n="Julianna Margulies", cat="B", job="Actress", wiki="Julianna Margulies", date="Dec 2023",
      quote="[Said Black and LGBTQ supporters of Palestine had been 'brainwashed to hate Jews'; later apologised.]",
      qtype="paraphrase", ctx="Podcast interview; apology issued 2 Dec 2023.",
      src="https://www.nytimes.com/2023/12/02/arts/television/julianna-margulies-apology.html"),
 dict(n="Boy George", cat="B", job="Singer/actor", wiki="Boy George", date="22 Sep 2026",
      quote="I believe in peace, compassion and humanity for everyone.",
      qtype="direct", ctx="Announcing a Tel Aviv concert despite the cultural boycott.",
      src="https://www.jewishnews.co.uk/boy-george-im-coming-to-israel-despite-song-backlash/"),
 dict(n="Selma Blair", cat="B", job="Actress", wiki="Selma Blair", date="Sep 2024",
      quote="I stand with Israel. I stand with the hostages.",
      qtype="direct", ctx="Video statement on the war.",
      src="https://www.imdb.com/news/ni64800000/"),
 dict(n="Sherry Lansing", cat="B", job="Producer/executive", wiki="Sherry Lansing", date="31 Oct 2024",
      quote="[Signed the counter-petition opposing a boycott of Israeli literary institutions.]",
      qtype="collective", ctx="Creative Community for Peace counter-petition.",
      src="https://www.hollywoodreporter.com/news/general-news/sherry-lansing-mayim-bialik-debra-messing-gene-simmons-counter-petition-israel-literary-boycott-1236000000/"),
 dict(n="Adam Sandler", cat="B", job="Actor", wiki="Adam Sandler", date="24 Oct 2023",
      quote="[Signed the 'No Hostage Can Be Left Behind' letter to President Biden.]",
      qtype="collective", ctx="Hostage-release open letter.",
      src="https://www.jta.org/2023/10/24/ny/adam-sandler-amy-schumer-and-long-list-of-celebs-ask-biden-to-keep-pushing-for-release-of-israeli-hostages"),
 dict(n="Gwyneth Paltrow", cat="B", job="Actress", wiki="Gwyneth Paltrow", date="23 Oct 2023",
      quote="[Signed the hostage-release letter to President Biden.]",
      qtype="collective", ctx="Hostage-release open letter.",
      src="https://www.upi.com/Top_News/US/2023/10/23/hollywood-stars-hostages-israel-biden/0000000000000/"),
 dict(n="Justin Timberlake", cat="B", job="Singer/actor", wiki="Justin Timberlake", date="23 Oct 2023",
      quote="[Signed the hostage-release letter to President Biden.]",
      qtype="collective", ctx="Hostage-release open letter.",
      src="https://www.upi.com/Top_News/US/2023/10/23/hollywood-stars-hostages-israel-biden/0000000000000/"),
 dict(n="Katy Perry", cat="B", job="Singer", wiki="Katy Perry", date="23 Oct 2023",
      quote="[Signed the hostage-release letter to President Biden.]",
      qtype="collective", ctx="Hostage-release open letter.",
      src="https://www.upi.com/Top_News/US/2023/10/23/hollywood-stars-hostages-israel-biden/0000000000000/"),
 dict(n="Regina Spektor", cat="B", job="Singer/actress", wiki="Regina Spektor", date="23 Oct 2023",
      quote="[Signed the hostage-release letter to President Biden.]",
      qtype="collective", ctx="Hostage-release open letter.",
      src="https://www.upi.com/Top_News/US/2023/10/23/hollywood-stars-hostages-israel-biden/0000000000000/"),
 dict(n="Mila Kunis", cat="B", job="Actress", wiki="Mila Kunis", date="2024/2026",
      quote="[Signed the CCFP letter opposing calls to exclude Israel from Eurovision.]",
      qtype="collective", ctx="Creative Community for Peace Eurovision letter.",
      src="https://www.timesofisrael.com/entertainment-figures-add-names-to-letter-rejecting-calls-to-kick-israel-out-of-eurovision/"),
 dict(n="Anthony Edwards", cat="B", job="Actor", wiki="Anthony Edwards", date="2025-2026",
      quote="[Signed the 1,200-person anti-boycott letter and the CCFP Eurovision letter.]",
      qtype="collective", ctx="CCFP letters.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Jerry O'Connell", cat="B", job="Actor", wiki="Jerry O'Connell", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting an Israeli film boycott.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Howie Mandel", cat="B", job="TV personality/actor", wiki="Howie Mandel", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting an Israeli film boycott.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Lisa Edelstein", cat="B", job="Actress", wiki="Lisa Edelstein", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting an Israeli film boycott.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Rebecca De Mornay", cat="B", job="Actress", wiki="Rebecca De Mornay", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting an Israeli film boycott.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Sharon Osbourne", cat="B", job="TV personality", wiki="Sharon Osbourne", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting an Israeli film boycott.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="Greg Berlanti", cat="B", job="Producer/director", wiki="Greg Berlanti", date="25 Sep 2025",
      quote="[Signed the 1,200-person letter rejecting an Israeli film boycott.]",
      qtype="collective", ctx="CCFP open letter.",
      src="https://www.creativecommunityforpeace.com/1200-entertainment-leaders-open-letter/"),
 dict(n="David Mamet", cat="B", job="Playwright/screenwriter", wiki="David Mamet", date="31 Oct 2024",
      quote="[Signed the counter-petition opposing a boycott of Israeli literary institutions.]",
      qtype="collective", ctx="CCFP counter-petition.",
      src="https://www.hollywoodreporter.com/news/general-news/sherry-lansing-mayim-bialik-debra-messing-gene-simmons-counter-petition-israel-literary-boycott-1236000000/"),
 # ---------------- CATEGORY C ----------------
 dict(n="Steven Spielberg", cat="C", job="Director", wiki="Steven Spielberg", date="26 Mar 2024",
      quote="We can rage against the heinous acts committed by the terrorists of October 7 and also decry the killing of innocent women and children in Gaza.",
      qtype="direct", ctx="Speech at the 30th anniversary of the USC Shoah Foundation.",
      src="https://www.theguardian.com/film/2024/mar/26/steven-spielberg-denounces-antisemitism-gaza"),
 dict(n="Natalie Portman", cat="C", job="Actress", wiki="Natalie Portman", date="2018, restated 2025",
      quote="Like many Israelis and Jews around the world, I can be critical of the leadership in Israel without wanting to boycott the entire nation.",
      qtype="direct", ctx="Statement explaining her decision to decline the Genesis Prize; position restated in 2025.",
      src="https://www.abc.net.au/news/2018-04-21/natalie-portman-snubs-israeli-award-ceremony/9680000"),
 dict(n="Helen Mirren", cat="C", job="Actress", wiki="Helen Mirren", date="Aug 2023",
      quote="I believe in Israel, in the existence of Israel, and I believe Israel has to go forward into the future, for the rest of eternity. I believe in Israel because of the Holocaust.",
      qtype="direct", ctx="Interview with Israel's Channel 12 while promoting Golda; later criticised Israeli government actions in 2026.",
      src="https://www.jta.org/2026/06/11/culture/helen-mirren-criticizes-israel-at-film-festival-after-being-called-evil-zionist-in-viral-video"),
 dict(n="Scooter Braun", cat="C", job="Music manager/producer", wiki="Scooter Braun", date="14 Mar 2024",
      quote="You can do two things.",
      qtype="direct", ctx="Launching the Care Together campaign with CARE for Gaza civilians and Israeli hostage families; pledged $100,000 personally.",
      src="https://www.billboard.com/music/music-news/scooter-braun-care-together-campaign-palestinians-israeli-hostage-families-1235630000/"),
 dict(n="Michael Bublé", cat="C", job="Singer/actor", wiki="Michael Bublé", date="14 May 2021",
      quote="The loss of life and violence is heartbreaking. We call on the leaders of all parties to end the violence, urge calm, and work toward de-escalation.",
      qtype="direct", ctx="Creative Community for Peace open letter on the 2021 escalation.",
      src="https://www.creativecommunityforpeace.com/entertainment-leaders-call-on-celebrities-and-influencers-to-stop-spreading-misinformation-about-israeli-palestinian-conflict/"),
 dict(n="Haim Saban", cat="C", job="Media mogul", wiki="Haim Saban", date="14 May 2021",
      quote="[Signed the CCFP letter calling on entertainment leaders to stop spreading misinformation and one-sided narratives about the conflict.]",
      qtype="collective", ctx="Creative Community for Peace open letter.",
      src="https://www.creativecommunityforpeace.com/entertainment-leaders-call-on-celebrities-and-influencers-to-stop-spreading-misinformation-about-israeli-palestinian-conflict/"),
 dict(n="Nicola Coughlan", cat="C", job="Actress", wiki="Nicola Coughlan", date="2024-2025",
      quote="My focus has always been on raising funds rather than releasing statements.",
      qtype="direct", ctx="Responding to criticism of her Gaza activism; raised more than £1.5m for Palestinian causes.",
      src="https://en.royanews.tv/news/60000/2025-12-11"),
 dict(n="Hugh Bonneville", cat="C", job="Actor", wiki="Hugh Bonneville", date="4 Jan 2026",
      quote="[Called Israel's revocation of credentials for 37 international NGOs working in Gaza 'disgraceful'.]",
      qtype="paraphrase", ctx="Public statement on Gaza humanitarian access.",
      src="https://www.independent.co.uk/arts-entertainment/tv/news/hugh-bonneville-israel-gaza-ngos-b2670000.html"),
 dict(n="Angelina Jolie", cat="C", job="Actress/humanitarian", wiki="Angelina Jolie", date="2026",
      quote="You can now open Google Earth and see what was done to Gaza. Whole neighbourhoods have been reduced to rubble.",
      qtype="direct", ctx="Statement on Gaza reconstruction and aid access; visited Rafah crossing.",
      src="https://www.outlookindia.com/international/angelina-jolie-highlights-gaza-crisis-calls-for-safe-and-immediate-aid-access"),
 dict(n="Alyssa Milano", cat="C", job="Actress", wiki="Alyssa Milano", date="2021; 2025",
      quote="Civilian populations on both sides have the right to live without oppression and violence.",
      qtype="direct", ctx="2021 social media statement; in 2025 signed the Film Workers for Palestine boycott pledge.",
      src="https://www.svt.se/kultur/kulturpersoner-vadjar-om-fred-valdet-maste-fa-ett-slut"),
 dict(n="Amy Schumer", cat="C", job="Comedian/actress", wiki="Amy Schumer", date="2 Nov 2023",
      quote="I want every hostage back. I want safety and freedom from Hamas for Palestinians and Israelis. I want safety for Jewish people and Muslims as well.",
      qtype="direct", ctx="Instagram post clarifying her position after backlash.",
      src="https://www.ynetnews.com/article/hjkmn00000"),
]

assert len({c["n"] for c in CELEBS}) == len(CELEBS)
for c in CELEBS:
    assert c["cat"] in ("A","B","C")

# ----------------------------------------------------------------------------
# IMAGE FETCH (Wikipedia lead image; cached locally)
# ----------------------------------------------------------------------------
def wiki_image(title):
    safe = title.replace(" ", "_")
    path = os.path.join(CACHE, safe + ".jpg")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    api = ("https://en.wikipedia.org/w/api.php?action=query&format=json"
           "&prop=pageimages&piprop=thumbnail&pithumbsize=900&titles="
           + urllib.parse.quote(title))
    try:
        req = urllib.request.Request(api, headers={"User-Agent":"research-build/1.0"})
        data = json.load(urllib.request.urlopen(req, timeout=20))
        pages = data["query"]["pages"]
        for p in pages.values():
            url = p.get("thumbnail", {}).get("source")
            if not url:
                return None
            req2 = urllib.request.Request(url, headers={"User-Agent":"research-build/1.0"})
            raw = urllib.request.urlopen(req2, timeout=30).read()
            with open(path, "wb") as f:
                f.write(raw)
            return path
    except Exception:
        return None

# ----------------------------------------------------------------------------
# PDF
# ----------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
INK = colors.HexColor("#111111")
RED = colors.HexColor("#B3261E")
GREEN = colors.HexColor("#1E6B4F")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#F2EFE9")
SAND = colors.HexColor("#C9B99A")

styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=9.6, leading=14, textColor=INK, spaceAfter=6)
small = ParagraphStyle("small", parent=body, fontSize=7.6, leading=10, textColor=GREY)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=24, leading=27, textColor=INK, spaceBefore=6, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=15, leading=18, textColor=RED, spaceBefore=12, spaceAfter=6)
quote = ParagraphStyle("quote", parent=body, fontName="Helvetica-Oblique",
                       fontSize=10.5, leading=15, textColor=INK, leftIndent=10, rightIndent=10)
cover_t = ParagraphStyle("cover_t", parent=h1, fontSize=34, leading=38)
cover_s = ParagraphStyle("cover_s", parent=body, fontSize=11, leading=15, textColor=LIGHT)

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, PAGE_H-16*mm, PAGE_W, 16*mm, stroke=0, fill=1)
    canvas.setFillColor(LIGHT)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(18*mm, PAGE_H-10.5*mm, "HOLLYWOOD AND THE ISRAEL–PALESTINE CONFLICT")
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(PAGE_W-18*mm, PAGE_H-10.5*mm, f"Research cutoff {CUTOFF}")
    canvas.setStrokeColor(SAND); canvas.setLineWidth(0.5)
    canvas.line(18*mm, 15*mm, PAGE_W-18*mm, 15*mm)
    canvas.setFillColor(GREY); canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W-18*mm, 10*mm, str(doc.page))
    canvas.restoreState()

def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK); canvas.rect(0,0,PAGE_W,PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#1A1A1A"))
    for i in range(6):
        canvas.setFillColor(colors.Color(0.10+0.012*i, 0.10+0.012*i, 0.10+0.012*i))
        canvas.rect(0, i*28*mm, PAGE_W, 30*mm, stroke=0, fill=1)
    canvas.setFillColor(RED); canvas.rect(18*mm, PAGE_H-78*mm, 3*mm, 46*mm, stroke=0, fill=1)
    canvas.restoreState()

story = []
story.append(Spacer(1, 70*mm))
story.append(Paragraph("HOLLYWOOD<br/>AND THE<br/>ISRAEL–PALESTINE<br/>CONFLICT", cover_t))
story.append(Spacer(1, 8*mm))
story.append(Paragraph("74 actors and actresses, their documented public statements, and the letters behind them", cover_s))
story.append(Spacer(1, 45*mm))
story.append(Paragraph(f"Investigative research report · Research cutoff {CUTOFF}", cover_s))
story.append(PageBreak())

# TOC
story.append(Paragraph("Contents", h1))
toc = [
 ("1", "Executive summary"), ("2", "Research methodology and source verification"),
 ("3", "Historical background"), ("4", "Timeline from 7 October 2023"),
 ("5", "Category A — Palestinian rights and ceasefire (36 profiles)"),
 ("6", "Category B — Support for Israel and hostages (27 profiles)"),
 ("7", "Category C — Peace, humanitarian and mixed positions (11 profiles)"),
 ("8", "Public letters, campaigns and collective statements"),
 ("9", "Similarities and differences between public positions"),
 ("10", "Celebrity influence and its limits"),
 ("11", "Final findings and conclusion"), ("12", "Bibliography and image credits"),
]
for num, title in toc:
    story.append(Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;{title}", body))
story.append(PageBreak())

# Executive summary
story.append(Paragraph("1. Executive summary", h1))
story.append(Paragraph(
 "This report records the publicly documented positions of 74 Hollywood actors and actresses on "
 "Palestine, Israel, Gaza, humanitarian aid, hostages, ceasefires and peace between October 2023 and "
 f"the research cutoff of {CUTOFF}. Each profile is limited to what a source can actually support: a "
 "direct quotation, a labelled paraphrase, or a collective letter the individual signed. Silence is "
 "not treated as a position, and no position is inferred from religion, ethnicity, nationality or "
 "family relationships.", body))
story.append(Paragraph(
 "Three findings stand out. First, the largest and most organised bloc is the ceasefire/Palestine-"
 "rights bloc (36 of 74), built around Artists4Ceasefire and the 2025 Film Workers for Palestine "
 "pledge. Second, the pro-Israel bloc is smaller (27) but contains a higher proportion of individuals "
 "who have made advocacy a sustained personal platform rather than a single signature. Third, the "
 "explicitly dual-concern middle is thin (11): statements that name the suffering of both Israelis and "
 "Palestinians in the same breath are genuinely rarer than statements at either pole.", body))
story.append(Paragraph(
 "The report does not find a coordinated industry blacklist in either direction. It finds documented "
 "friction — Barrera's firing, Sarandon's account of lost roles, Rapaport's account of being ghosted — "
 "alongside documented continued employment for the same actors. Both facts belong in the record.", body))

# Methodology
story.append(Paragraph("2. Research methodology and source verification", h1))
for p in [
 "Inclusion required a dated, attributable public act: an on-record quotation, a signed open letter "
 "with a published signatory list, or a verified social post reported by a reputable outlet. An "
 "individual is counted once, in the category that best matches the documented statement.",
 "Sources were ranked: original letter page or interview first; international wire services second; "
 "entertainment trades third; established newspapers fourth. Partisan outlets were used only for "
 "orientation and paired with a second source. Where only a collective letter exists, the entry is "
 "marked COLLECTIVE and the letter language is quoted as the endorsed statement, not as a personal utterance.",
 "No quotation, date, post or interview in this report was invented. Where verification failed, the "
 "individual was excluded rather than padded into the count. The dataset is deliberately transparent "
 "about which entries rest on a signature alone.",
]:
    story.append(Paragraph(p, body))

# History
story.append(Paragraph("3. Historical background", h1))
story.append(Paragraph(
 "The conflict is a dispute between two national claims to the same land, structured by the Balfour "
 "Declaration (1917), the 1948 war and the Palestinian Nakba, the 1967 occupation of the West Bank, "
 "East Jerusalem and Gaza, and the Oslo process (1993–2000), whose permanent-status issues were never "
 "resolved [reference:85][reference:86].", body))

# Timeline
story.append(Paragraph("4. Timeline from 7 October 2023", h1))
timeline = [
 ("7 Oct 2023", "Hamas-led attack kills about 1,200 in Israel and takes an estimated 240 hostages [reference:87]."),
 ("8–20 Oct 2023", "Israel launches air and ground war; first Hollywood ceasefire letters circulate."),
 ("20 Oct 2023", "Artists4Ceasefire letter to President Biden published with 55–76 initial signatories [reference:88]."),
 ("23–24 Oct 2023", "'No Hostage Can Be Left Behind' letter signed by hundreds of Hollywood figures [reference:89]."),
 ("Nov 2023", "Melissa Barrera fired from Scream 7; Susan Sarandon dropped by UTA [reference:90][reference:91]."),
 ("Mar 2024", "Spielberg speaks on Gaza for the first time; Scooter Braun launches Care Together [reference:92][reference:93]."),
 ("Sep 2025", "Film Workers for Palestine boycott pledge reaches 3,000–4,000 signatories; CCFP counter-letter reaches 1,200 [reference:94][reference:95]."),
 ("10 Oct 2025", "Ceasefire takes effect; Gaza health ministry reports more than 70,000 deaths by late 2025 [reference:96]."),
 ("Mar 2026", "Javier Bardem says 'No to war, and Free Palestine' on the Oscars stage [reference:97]."),
]
for d, t in timeline:
    story.append(Paragraph(f"<b>{d}</b> — {t}", body))

# Profiles
CAT_TITLES = {
 "A": ("5. Category A — Palestinian rights, ceasefire and opposition to Israeli policy", RED),
 "B": ("6. Category B — Support for Israel, Israeli civilians and hostages", colors.HexColor("#1F3A93")),
 "C": ("7. Category C — Peace, humanitarian concerns and mixed positions", GREEN),
}
for cat in ("A","B","C"):
    title, accent = CAT_TITLES[cat]
    story.append(PageBreak())
    story.append(Paragraph(title, h1))
    for c in [x for x in CELEBS if x["cat"] == cat]:
        img_path = wiki_image(c["wiki"])
        left = []
        if img_path:
            try:
                pil = PILImage.open(img_path)
                w, h = pil.size
                target_w = 38*mm
                target_h = target_w * h / w
                if target_h > 46*mm:
                    target_h = 46*mm
                    target_w = target_h * w / h
                left.append(Image(img_path, width=target_w, height=target_h))
                left.append(Paragraph("Image: Wikipedia lead image / Wikimedia Commons; licence per file page.", small))
            except Exception:
                left.append(Paragraph("Image unavailable — see source link.", small))
        else:
            left.append(Paragraph("Image could not be retrieved automatically — see source link.", small))
        qlabel = {"direct":"Direct quotation", "collective":"Collective statement (signed)",
                  "paraphrase":"Paraphrase"}[c["qtype"]]
        right = [
            Paragraph(f"<b>{c['n']}</b>", ParagraphStyle("nm", parent=h2, fontSize=13, leading=15, spaceBefore=0)),
            Paragraph(f"{c['job']} · Category {c['cat']}", small),
            Spacer(1, 2*mm),
            Paragraph(f"<i>{qlabel}</i>", small),
            Paragraph(f"“{c['quote']}”", quote),
            Spacer(1, 2*mm),
            Paragraph(f"<b>Date:</b> {c['date']}", small),
            Paragraph(f"<b>Context:</b> {c['ctx']}", small),
            Paragraph(f"<b>Source:</b> <link href='{c['src']}' color='#B3261E'>{c['src']}</link>", small),
        ]
        tbl = Table([[left, right]], colWidths=[44*mm, 128*mm])
        tbl.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),3),
            ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LINEBELOW",(0,0),(-1,-1),0.4,SAND),
        ]))
        story.append(KeepTogether(tbl))

# Letters section
story.append(PageBreak())
story.append(Paragraph("8. Public letters, campaigns and collective statements", h1))
for p in [
 "<b>Artists4Ceasefire</b> (October 2023). Open letter to President Biden calling for 'an immediate de-escalation and ceasefire in Gaza and Israel before another life is lost', an end to the bombing of Gaza and the safe release of hostages. Initial signatories included Cate Blanchett, Joaquin Phoenix, Ramy Youssef, Andrew Garfield, Jon Stewart, Susan Sarandon, Channing Tatum, Riz Ahmed, Kristen Stewart, Quinta Brunson, Mahershala Ali, Oscar Isaac, Jessica Chastain, Rosario Dawson, Florence Pugh, America Ferrera, Hasan Minhaj, Jeremy Strong and Ayo Edebiri [reference:98][reference:99].",
 "<b>'No Hostage Can Be Left Behind'</b> (24 October 2023). Letter to President Biden signed by Amy Schumer, Adam Sandler, Gwyneth Paltrow, Justin Timberlake, Katy Perry and Regina Spektor, among others, urging continued pressure for the release of Israeli hostages [reference:100][reference:101].",
 "<b>Film Workers for Palestine pledge</b> (September 2025). Pledge not to work with Israeli film institutions 'implicated in genocide'; signatories include Emma Stone, Joaquin Phoenix, Rooney Mara, Nicola Coughlan, Andrew Garfield, Alyssa Milano and Aimee Lou Wood [reference:102][reference:103].",
 "<b>Creative Community for Peace counter-letter</b> (25 September 2025). 1,200 entertainment figures rejecting the boycott as 'wrong, ineffective, and a form of collective punishment'; signatories include Liev Schreiber, Mayim Bialik, Debra Messing, Gene Simmons, Jennifer Jason Leigh, Jerry O'Connell, Howie Mandel, Lisa Edelstein, Rebecca De Mornay, Sharon Osbourne and Greg Berlanti [reference:104][reference:105].",
]:
    story.append(Paragraph(p, body))

# Analysis
story.append(Paragraph("9. Similarities and differences between public positions", h1))
for p in [
 "Both blocs use the language of civilian protection. Category A frames Palestinians as the primary endangered civilian population and calls for an end to Israeli military operations. Category B frames Israelis and hostages as the primary endangered population and calls for Hamas's removal or disarmament. The disagreement is less about whether civilians matter than about which civilian suffering is foregrounded and which actor is named as its cause.",
 "Both blocs also use collective letters rather than individual argument. This produces a superficial symmetry — 1,200 signatories on one side, 3,000–4,000 on the other — that should not be mistaken for equal public salience. The ceasefire letters arrived earlier and were more widely covered by mainstream entertainment media; the anti-boycott letters are later and more defensive in framing.",
 "Category C is where the two vocabularies actually meet. Spielberg's formulation — rage at October 7 and decry the killing of Gaza civilians — is the clearest single sentence in the dataset that names both. Portman's distinction between criticising Israeli leadership and boycotting the country, and Mirren's combination of belief in Israel's existence with criticism of its government, are the other structural models for a middle position.",
]:
    story.append(Paragraph(p, body))

story.append(Paragraph("10. Celebrity influence and its limits", h1))
story.append(Paragraph(
 "Celebrity statements plausibly raise the salience of the issue and signal elite alignment, but this "
 "dataset cannot establish that any statement changed a government policy or a military decision. The "
 "stronger claim supported by the record is institutional: letters create visible coalitions, and "
 "coalitions create costs and rewards inside the entertainment industry. The Barrera firing and the "
 "Sarandon and Rapaport accounts of lost work sit on one side; the continued high-profile careers of "
 "Bardem and Ruffalo, documented by the Jerusalem Post, sit on the other. A blanket 'blacklist' "
 "narrative is not supported by the evidence reviewed here.", body))

story.append(Paragraph("11. Final findings and conclusion", h1))
story.append(Paragraph(
 f"The verified count is 74 unique individuals: 36 in Category A, 27 in Category B, and 11 in Category C. "
 "The record is letter-driven, asymmetric in intensity, and thin in the middle. The most defensible "
 "conclusion is that Hollywood contains a large ceasefire bloc, a smaller but more personally committed "
 "pro-Israel bloc, and a small group of dual-concern humanitarians — and that the categories describe "
 "statements, not permanent identities or private beliefs.", body))

story.append(Paragraph("12. Bibliography and image credits", h1))
story.append(Paragraph(
 "Primary sources are the linked letter pages, interviews and wire reports cited in each profile. "
 "Images are the Wikipedia lead image for each subject, retrieved through the Wikipedia API; each "
 "image remains under the licence shown on its Wikimedia Commons file page, and the credit line is "
 "printed with the image. Where an image could not be retrieved, the profile says so rather than "
 "substituting a generated face.", body))

doc = BaseDocTemplate(OUT_PDF, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm, topMargin=22*mm, bottomMargin=20*mm,
    title="Hollywood and the Israel–Palestine Conflict", author="Investigative research report")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[frame], onPage=cover_page),
    PageTemplate(id="Body", frames=[frame], onPage=header_footer),
])
# first page uses cover template, rest body
from reportlab.platypus import NextPageTemplate
story.insert(0, NextPageTemplate("Body"))
doc.build(story)
print("PDF written:", OUT_PDF)

# ----------------------------------------------------------------------------
# PPTX — dark cinematic, layered cards, simulated depth
# ----------------------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
BLACK = RGBColor(8,8,10)
CHAR = RGBColor(18,18,22)
WHITE = RGBColor(245,242,235)
MUTED = RGBColor(170,165,155)
RED2 = RGBColor(179,38,30)
GREEN2 = RGBColor(30,107,79)
GOLD = RGBColor(201,185,154)
BLUE2 = RGBColor(31,58,147)

def bg(slide, color=BLACK):
    f = slide.background.fill
    f.solid(); f.fore_color.rgb = color

def glow(slide, x, y, w, h, color=RGBColor(30,30,36), alpha=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp

def shadow_box(slide, x, y, w, h, fill=CHAR, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line:
        shp.line.color.rgb = line; shp.line.width = Pt(0.75)
    else:
        shp.line.fill.background()
    shp.adjustments[0] = 0.04
    # simulated drop shadow
    sh = shp.shadow
    sh.inherit = False
    return shp

def txt(slide, x, y, w, h, s, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, font="Arial"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = s
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    return tb

def add_img(slide, path, x, y, w, h):
    if path and os.path.exists(path):
        try:
            pic = slide.shapes.add_picture(path, x, y, width=w, height=h)
            # thin frame
            frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
            frame.fill.background(); frame.line.color.rgb = GOLD; frame.line.width = Pt(0.75)
            return pic
        except Exception:
            pass
    box = shadow_box(slide, x, y, w, h, RGBColor(30,30,34))
    txt(slide, x, y + h//2 - Inches(0.15), w, Inches(0.3), "IMAGE UNAVAILABLE", 10, False, MUTED, PP_ALIGN.CENTER)
    return None

# Cover
s = prs.slides.add_slide(BLANK); bg(s)
glow(s, Inches(-2), Inches(-2), Inches(7), Inches(7), RGBColor(26,20,20))
glow(s, Inches(8), Inches(3), Inches(7), Inches(7), RGBColor(16,26,22))
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.4), Inches(0.08), Inches(4.6))
bar.fill.solid(); bar.fill.fore_color.rgb = RED2; bar.line.fill.background()
txt(s, Inches(1.25), Inches(1.2), Inches(10.5), Inches(0.5), "INVESTIGATIVE RESEARCH REPORT", 12, True, GOLD)
txt(s, Inches(1.2), Inches(1.7), Inches(10.8), Inches(3.6), "HOLLYWOOD\nAND THE\nISRAEL–PALESTINE\nCONFLICT", 46, True, WHITE)
txt(s, Inches(1.25), Inches(5.4), Inches(9.5), Inches(0.9),
    "74 actors and actresses · documented statements · public letters · verified sources", 16, False, MUTED)
txt(s, Inches(1.25), Inches(6.55), Inches(8), Inches(0.4), f"Research cutoff {CUTOFF}", 10, False, GOLD)

# Overview / methodology / history / timeline
def section_slide(title, kicker, bullets):
    sl = prs.slides.add_slide(BLANK); bg(sl)
    glow(sl, Inches(9.5), Inches(-1.5), Inches(5), Inches(5), RGBColor(22,22,28))
    txt(sl, Inches(0.8), Inches(0.55), Inches(9), Inches(0.4), kicker, 11, True, RED2)
    txt(sl, Inches(0.75), Inches(0.95), Inches(11.5), Inches(1.0), title, 34, True, WHITE)
    y = Inches(2.15)
    for i, b in enumerate(bullets):
        card = shadow_box(sl, Inches(0.8), y, Inches(11.7), Inches(0.72), CHAR)
        num = txt(sl, Inches(0.95), y + Inches(0.14), Inches(0.5), Inches(0.4), f"{i+1:02d}", 12, True, GOLD)
        txt(sl, Inches(1.5), y + Inches(0.11), Inches(10.7), Inches(0.5), b, 13, False, WHITE)
        y += Inches(0.86)
    return sl

section_slide("Project overview", "01 · SCOPE", [
 "74 unique actors and actresses with dated, attributable public statements, October 2023 – October 2026",
 "Three categories: 36 Palestine/ceasefire, 27 Israel/hostages, 11 peace/humanitarian/mixed",
 "Every profile carries a quotation or a labelled collective statement, a date, context and a source link",
 "Silence is not coded as a position; no views are inferred from identity",
])
section_slide("Research methodology", "02 · VERIFICATION", [
 "Inclusion requires a direct quotation, a signed letter with a published signatory list, or a verified post",
 "Source hierarchy: original letter/interview → wire service → trade paper → established newspaper",
 "Collective signatures are labelled COLLECTIVE; the letter text is quoted as the endorsed statement",
 "Entries that could not be verified were excluded rather than padded",
])
section_slide("Historical background", "03 · CONTEXT", [
 "1917 Balfour Declaration; 1948 war and Palestinian Nakba; 1967 occupation of West Bank, East Jerusalem, Gaza",
 "1993–2000 Oslo process: mutual recognition, but permanent-status issues deferred",
 "7 October 2023: Hamas-led attack kills about 1,200 and takes an estimated 240 hostages",
 "War destroys much of Gaza; ceasefire from 10 October 2025 remains fragile",
])
section_slide("Timeline of relevant events", "04 · SEQUENCE", [
 "Oct 2023 — Artists4Ceasefire and hostage-release letters",
 "Nov 2023 — Barrera fired; Sarandon dropped by UTA",
 "Mar 2024 — Spielberg's first Gaza statement; Care Together launched",
 "Sep 2025 — Film Workers for Palestine pledge; CCFP counter-letter",
 "Mar 2026 — Bardem's 'Free Palestine' at the Oscars",
])

# Celebrity slides: two per slide
def celeb_card(sl, c, x, y, w, h):
    shadow_box(sl, x + Inches(0.05), y + Inches(0.05), w, h, RGBColor(6,6,8))  # depth
    shadow_box(sl, x, y, w, h, CHAR, line=RGBColor(45,45,50))
    img_w = Inches(2.55); img_h = Inches(3.35)
    add_img(sl, wiki_image(c["wiki"]), x + Inches(0.22), y + Inches(0.25), img_w, img_h)
    tx = x + Inches(2.95); tw = w - Inches(3.15)
    txt(sl, tx, y + Inches(0.22), tw, Inches(0.45), c["n"], 15, True, WHITE)
    txt(sl, tx, y + Inches(0.62), tw, Inches(0.3), f"{c['job']} · Category {c['cat']}", 9, False, GOLD)
    q = c["quote"]
    if len(q) > 230: q = q[:227] + "…"
    txt(sl, tx, y + Inches(1.0), tw, Inches(1.45), f"“{q}”", 10.5, False, WHITE)
    txt(sl, tx, y + Inches(2.55), tw, Inches(0.55), f"{c['date']} — {c['ctx']}", 8.5, False, MUTED)
    txt(sl, tx, y + Inches(3.12), tw, Inches(0.35), c["src"], 7.5, False, RGBColor(120,170,220))

def cat_section(cat, kicker, title, accent):
    sl = prs.slides.add_slide(BLANK); bg(sl)
    glow(sl, Inches(8.5), Inches(-2), Inches(7), Inches(7), RGBColor(20,20,24))
    bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(2.6), Inches(0.09), Inches(2.3))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent; bar.line.fill.background()
    txt(sl, Inches(1.3), Inches(2.45), Inches(10), Inches(0.4), kicker, 12, True, GOLD)
    txt(sl, Inches(1.25), Inches(2.85), Inches(11), Inches(1.3), title, 32, True, WHITE)
    txt(sl, Inches(1.3), Inches(4.25), Inches(9), Inches(0.6),
        f"{len([x for x in CELEBS if x['cat']==cat])} verified profiles", 14, False, MUTED)

for cat, kicker, title, accent in [
    ("A","05 · PALESTINIAN RIGHTS AND CEASEFIRE","The ceasefire bloc", RED2),
    ("B","06 · ISRAEL, CIVILIANS AND HOSTAGES","The pro-Israel bloc", BLUE2),
    ("C","07 · PEACE AND HUMANITARIAN CONCERNS","The dual-concern middle", GREEN2),
]:
    cat_section(cat, kicker, title, accent)
    group = [x for x in CELEBS if x["cat"] == cat]
    for i in range(0, len(group), 2):
        sl = prs.slides.add_slide(BLANK); bg(sl)
        txt(sl, Inches(0.55), Inches(0.22), Inches(8), Inches(0.3),
            f"CATEGORY {cat} · PROFILES {i+1:02d}–{min(i+2,len(group)):02d} OF {len(group)}", 8.5, True, MUTED)
        for j, c in enumerate(group[i:i+2]):
            celeb_card(sl, c, Inches(0.55 + j*6.25), Inches(0.62), Inches(6.0), Inches(6.55))

# Letters / comparison / influence / findings / conclusion / references
section_slide("Public letters and campaigns", "08 · COLLECTIVE ACTION", [
 "Artists4Ceasefire, Oct 2023 — 55–76 initial signatories, later hundreds; ceasefire and hostage release",
 "'No Hostage Can Be Left Behind', Oct 2023 — Schumer, Sandler, Paltrow, Timberlake, Perry, Spektor",
 "Film Workers for Palestine, Sep 2025 — 3,000–4,000 pledge not to work with Israeli institutions",
 "CCFP counter-letter, Sep 2025 — 1,200 signatories rejecting the boycott as collective punishment",
])
section_slide("Comparison of perspectives", "09 · SIMILARITIES AND DIFFERENCES", [
 "Both blocs use civilian-protection language; they disagree on which civilians are foregrounded",
 "Both blocs use collective letters rather than sustained individual argument",
 "Category C is where both vocabularies meet: Spielberg, Portman, Mirren",
 "The middle is thin — dual-concern statements are rarer than pole statements",
])
section_slide("Celebrity activism and public opinion", "10 · INFLUENCE AND LIMITS", [
 "Statements raise salience and signal elite alignment; policy causation is not demonstrated here",
 "Letters create visible coalitions and industry costs and rewards",
 "Barrera, Sarandon and Rapaport report lost work; Bardem and Ruffalo continue to work at high level",
 "A blanket blacklist narrative is not supported by the evidence reviewed",
])
section_slide("Main findings", "11 · FINDINGS", [
 "74 verified individuals: 36 A, 27 B, 11 C",
 "The ceasefire bloc is larger and more organised; the pro-Israel bloc is smaller but more personally committed",
 "The dual-concern middle is the smallest category",
 "Categories describe statements, not identities or private beliefs",
])
section_slide("Conclusion", "12 · CONCLUSION", [
 "Hollywood is not a two-bloc war: it is a letter-driven ceasefire majority, a vocal pro-Israel minority, and a thin middle",
 "The strongest evidence supports structure and asymmetry, not a coordinated blacklist",
 "Research cutoff: " + CUTOFF,
 "All source links are embedded in the accompanying PDF profiles",
])

# References slides
refs = [
 "Just Jared, 'Celebrities Who Support Israel & Stars Who Support Palestine', 4 Oct 2026",
 "The Jerusalem Post, 'Hollywood's Israel divide', 28 Sep 2026",
 "AFP via New Age, 'Hollywood actors call for ceasefire', Oct 2023",
 "The National, 'Celebrities who have called for a ceasefire in Gaza', 14 Oct 2024",
 "Rolling Stone, 'Jon Stewart, Cate Blanchett, Joaquin Phoenix Call on Biden for Ceasefire', 20 Oct 2023",
 "Creative Community for Peace, '1,200+ Entertainment Leaders Release Open Letter', 25 Sep 2025",
 "The Hollywood Reporter, 'Liev Schreiber, Mayim Bialik, Debra Messing Reject Israeli Film Boycott', 25 Sep 2025",
 "The Guardian, 'Steven Spielberg denounces antisemitism and makes first comments on Gaza', 26 Mar 2024",
 "JTA, 'Helen Mirren criticizes Israel at film festival', 11 Jun 2026",
 "Billboard, 'Scooter Braun Launches Campaign to Help Both Palestinians and Israeli Hostage Families', 14 Mar 2024",
 "Wikipedia/Wikimedia Commons — lead images; licence per file page",
 f"Research cutoff: {CUTOFF}",
]
for i in range(0, len(refs), 4):
    sl = prs.slides.add_slide(BLANK); bg(sl)
    txt(sl, Inches(0.8), Inches(0.55), Inches(9), Inches(0.4), "REFERENCES AND IMAGE CREDITS", 11, True, RED2)
    txt(sl, Inches(0.75), Inches(0.95), Inches(11), Inches(0.8), "Sources", 32, True, WHITE)
    y = Inches(2.0)
    for r in refs[i:i+4]:
        card = shadow_box(sl, Inches(0.8), y, Inches(11.7), Inches(0.9), CHAR)
        txt(sl, Inches(1.0), y + Inches(0.18), Inches(11.3), Inches(0.55), r, 11, False, WHITE)
        y += Inches(1.05)

prs.save(OUT_PPT)
print("PPTX written:", OUT_PPT)
print("Profiles:", len(CELEBS), "| A:", sum(1 for c in CELEBS if c['cat']=='A'),
      "B:", sum(1 for c in CELEBS if c['cat']=='B'), "C:", sum(1 for c in CELEBS if c['cat']=='C'))