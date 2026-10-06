# Acquisition-announcement momentum: desk research notes

Compiled 2026-10-06. Scope: the evidence on whether a target stock reprices *slowly* enough after a takeover announcement to be traded on a seconds-to-hours horizon, plus market-structure, news-latency and legal constraints.

**How to read the citations**
- **[read]**: I fetched the page or PDF and read the passage myself.
- **[snippet]**: the number comes from a search-engine summary of that URL. I did not open the full text, so treat it as weaker.
- **unverified**: I could not find a source. Nothing here is guessed.

---

## Key takeaways for the strategy

1. **Most of the premium now arrives at the announcement, not before it.** The median US target run-up fell from about 10% in the 1980s to about 2% after 2010 ([Dutordoir et al., Financial Management 2021](https://pure.eur.nl/en/publications/a-rundown-of-merger-target-run-ups/) [read]). Historically the run-up was about half the premium: 14.2% run-up against a 15.9% markup in 1975–91 ([Schwert, NBER WP 4863](https://www.nber.org/papers/w4863.pdf) [read]). The jump to capture is therefore large, typically 25–30%: the median target rises 27% ([Van Tassel, NY Fed SR 761](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr761.pdf?la=en) [read]), and the average one-day offer premium was 31% in 1996–2012 ([Augustin et al. WP](https://www.mcgill.ca/desautels/files/desautels/abs_2015_may_0.pdf) [read]).
2. **US targets are almost fully priced by the close of the next trading day.** The median ratio of the day-after price to the offer price was about 97–99% in 2002–2012 ([Bessembinder & Zhang 2015](https://english.ckgsb.edu.cn/sites/default/files/files/Merger_Anomaly_20150417.pdf) [read]). Median first-day arbitrage spreads fell from 4.1–7.9% before 2001 to 1.7–2.6% in 2001–2007 ([Jetley & Ji, FAJ 2010](https://analysisgroup.com/link/f5a479d9a8fb4799b20ff4a989d78a50.aspx) [read]). For US cash deals, the "partly repriced" gap left after day 0 is only a few percent and mostly reflects deal risk. It is not underreaction.
3. **No study I could find measures how much of the target's jump happens in the first 1, 5 or 30 minutes.** This is unverified and is the main research gap. Benchmarks from other news types: macro news is priced within 5 ms in SPY and E-mini futures ([Chordia, Green & Kottimukkalur, RFS 2018](https://ideas.repec.org/a/oup/rfinst/v31y2018i12p4650-4687..html) [read]), and CNBC stock reports are fully priced within about 1 minute ([Busse & Green, JFE 2002](https://ideas.repec.org/a/eee/jfinec/v65y2002i3p415-437.html) [snippet for the numbers]). For M&A in US large caps, expect a window of seconds unless microstructure blocks it.
4. **In the US, exchange process usually removes the intraday window.** Nasdaq companies must notify MarketWatch at least 10 minutes before releasing material news between 7:00 am and 8:00 pm ET. MarketWatch may then halt the stock, usually for 30 minutes or less ([securities-law-blog summary of Nasdaq Rule 5250(b)(1)](https://securities-law-blog.com/2024/07/09/nasdaq-issues-new-faq-on-marketwatch-news-submittals/) [read]). Trading then resumes through a 5-minute display-only period and a Halt Cross ([SEC Rel. 34-88383](https://www.sec.gov/files/rules/sro/nasdaq/2020/34-88383.pdf) [read]). NYSE needs 10 minutes' notice for news released between 7:00 am and 4:00 pm ET ([Hunton](https://hunton.com/insights/legal/nyse-expands-material-news-notification-policy-and-trading-halt-authority-effective-september-28-2015) [read]). Most deals are announced before the open, so the "window" collapses into a thin pre-market session, and the share of US deals announced intraday is unverified.
5. **Most Asian and Australian exchanges halt or block intraday M&A news:**
   - ASX: about 1-hour halt for takeover or scheme announcements ([ASX GN14](https://www.asx.com.au/documents/rules/gn14_asx_market_announcements_platform.pdf) [read])
   - Japan: 15-minute halt ([JPX trading halts](https://www.jpx.co.jp/english/markets/equities/suspended/index.html) [snippet])
   - Korea: 30-minute halt ([KRX](https://global.krx.co.kr/contents/GLB/06/0602/0602010103/GLB0602010103T2.jsp) [read])
   - Philippines: 1-hour halt ([PSE Art. VII](https://documents.pse.com.ph/wp-content/uploads/sites/15/2021/04/Article-VII.pdf) [snippet])
   - Malaysia: 1-hour halt ([The Edge](https://theedgemalaysia.com/article/update-bursa-reserves-right-extend-trading-halt) [read])
   - Hong Kong: inside information is published only in windows outside trading hours ([HKEX FAQ](https://www.HKEX.com.hk/-/media/HKEX-Market/Listing/Rules-and-Guidance/eSubmission-System/Listed-Company-Information-Dissemination-and-Related-Trading-Arrangements/faqinv.pdf) [read])
   - Saudi Arabia: disclosure must be made before the next trading period ([CMA](https://cma.gov.sa/en/Market/NEWS/Pages/CMA_N_3037.aspx) [read])
   - Brazil: disclosure outside trading hours where possible, with an optional suspension ([CVM Res. 44 art. 5](https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol044consolid.pdf) [read])
6. **The best candidates for intraday repricing without a halt are the UK, India and Turkey.**
   - **UK leaks.** After a leak or an untoward price move, the Takeover Panel expects an announcement "within a matter of minutes", released during market hours ([Practice Statement 20](https://code.thetakeoverpanel.org.uk/tp/ps/ps-20.html) [read]). A move of 10%, or 5% in one day, triggers consultation with the Panel ([Rule 2.2](https://code.thetakeoverpanel.org.uk/tp/rules/rule-2/rule-2-2.html) [read]).
   - **India.** Board-meeting outcomes must be disclosed within 30 minutes of the meeting ending, often intraday ([TaxGuru](https://taxguru.in/sebi/overview-amendments-sebi-lodr-regulations-2023.html) [read]). But daily price bands of 2/5/10/20% cap the move, and open offers cover only 26% of shares ([SAST Reg 7(1)](https://ksandk.com/capital-markets/open-offer-sebi-takeover-code/) [snippet]), so targets need not converge to the offer price.
   - **Turkey.** Prices react to KAP disclosures more slowly than in developed markets, with "sizable profit opportunities" for event-driven traders ([Ersan et al., Emerging Markets Review 2021](https://research.sabanciuniv.edu/id/eprint/43385/) [read]). Price limits there are ±10% ([Borsa Istanbul](https://borsaistanbul.com/en/announcement/13357/changes-price-limits-equity-and-derivatives-markets) [read]).
7. **Rumour stories are a separate, tradable but noisy event class.** In newspaper merger rumours from 2000–2011, only 33% were followed by a bid within a year. Targets rose 4.3% on the rumour day (6.9% if the rumour proved true, 3.0% if not), and false-rumour targets gave back 2.7% over the next 20 days ([Ahern & Sosyura, RFS 2015](https://conference.nber.org/conf_papers/f72667/f72667.pdf) [read]).
8. **Post-announcement drift is small and depends on how close the price is to the offer.** Targets priced close to or above the offer on day +1 (top initial-target-price decile) lose 3.5% abnormal over the next 2 months. Targets in the lowest decile gain about 2.2%, which is not robustly significant ([Bessembinder & Zhang](https://english.ckgsb.edu.cn/sites/default/files/files/Merger_Anomaly_20150417.pdf) [read]). Low-latency traders do not appear to cause overreaction to M&A news ([Chordia & Miao](https://mitsloan.mit.edu/sites/default/files/inline-files/Chordia_Miao.pdf) [read], acquirer-side evidence).
9. **For US deals, the press release on a newswire comes before EDGAR.** Deal communications must be filed under Rule 425 "on or before the date of first use" ([17 CFR 230.425](https://www.law.cornell.edu/cfr/text/17/230.425) [snippet]), so EDGAR can lag the wire. EDGAR's own data API has under 1 second of processing delay after dissemination, and the website typically lags the EDGAR timestamp by 1–3 minutes ([SEC API docs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) [read]; [SEC webmaster FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) [read]).
10. **The fastest legitimate sources are institutional machine-readable feeds.** These are Dow Jones, Bloomberg Event-Driven Feeds and LSEG MRN; LSEG claims under 3 ms for its ultra-low-latency headline feed ([LSEG factsheet](https://www.lseg.com/content/dam/data-analytics/en_us/documents/fact-sheets/machine-readable-news-and-quantitative-data-factsheet.pdf) [read]). Since 2014, Business Wire and Marketwired no longer sell direct feeds to HFT firms, and PR Newswire makes feed customers certify they will not use the feed for HFT ([O'Dwyer's](https://www.odwyerpr.com/story/public/1934/2014-02-21/business-wire-pulls-plug-high-speed-traders.html) [read]; [O'Dwyer's on PRN](https://www.odwyerpr.com/story/public/2338/2014-05-01/pr-newswire-adds-curbs-high-speed-trading.html) [snippet]). Retail-priced feeds such as Benzinga run an estimated 1–3 seconds behind Bloomberg and Reuters, according to a reviewer ([LiberatedStockTrader](https://www.liberatedstocktrader.com/benzinga-pro-review-real-time-news/) [read; reviewer claim]).
11. **The legal line is the moment of public release.** The newswire hack — 150,000 press releases stolen, about $100m in profits — ended in prison sentences ([SEC 2015-163](https://www.sec.gov/news/press-release/2015-163) [read]; [USSS/DOJ 2019](https://www.secretservice.gov/press/releases/2019/03/former-hedge-fund-manager-sentenced-60-months-imprisonment-and-ordered-pay) [read]). Hacking is "deceptive" under Rule 10b-5 even without a fiduciary duty ([SEC v. Dorozhko](https://www.sec.gov/litigation/litreleases/2010/lr21465.htm) [snippet]). For tender offers, Rule 14e-3 needs no breach of duty at all ([14e-3 outline](https://www.lexplug.com/outlines/securities-regulation/rule-10b-5-and-securities-fraud/insider-trading/rule-14e-3-tender-offer-context) [snippet]). Trading on already-published rumours or public releases is generally lawful.

---

## 1. Academic and industry evidence

### 1a. Pre-announcement run-up and leakage

| Study | Sample | Key quantitative finding | Source |
|---|---|---|---|
| Keown & Pinkerton (1981, *JF* 36(4):855-869) | 194 merger announcements | Abnormal returns start about 12 days before the announcement; roughly 40–50% of the target's price gain comes before the announcement | Secondary only: [search summary](https://arxiv.org/pdf/2012.11594) [snippet]. Pham & Ausloos, citing K&P, say "half of this adjustment" occurs before the announcement [read]. Original not opened. |
| Schwert (1996, *JFE* 41:153-192; NBER WP 4863, 1994) | 1,398 successful NYSE/Amex takeovers, 1975–91; "main sample" 1,173 | Run-up (CAR, day −42 to −1) averages **14.2%**. Markup (day 0 to delisting or day +126) averages **15.9%**. "The average runup is about half of the total premium." Run-up and markup are **uncorrelated**, so the run-up adds to the bidder's cost. Run-up is 18.5% where the SEC later alleged insider trading. The largest pre-bid rise is in days −21 to −1. | [NBER WP pdf](https://www.nber.org/papers/w4863.pdf) [read] |
| Meulbroek (1992), cited in Schwert | SEC insider-trading cases | Almost half the run-up in the month before the bid falls on days when insiders traded illegally | Via [Schwert WP](https://www.nber.org/papers/w4863.pdf) [read] |
| Dutordoir, Vagenas-Nanos, Verwijmeren & Wu (2021, *Financial Management*) | US targets, 1980s–2010s | **Median target run-up fell from about 10% (1980s) to about 2% after 2010**, explained by tougher insider-trading regulation | [EUR repository](https://pure.eur.nl/en/publications/a-rundown-of-merger-target-run-ups/) [read] |
| Augustin, Brenner & Subrahmanyam (2019, *Mgmt Sci* 65(12):5697-5720) | 1,859 US takeovers, 1996–2012 | About **25%** of deals show significant positive abnormal option volume before the announcement, concentrated in short-dated out-of-the-money calls. More than half of this is not explained by rumours, news or similar factors. The SEC litigates only about 8% of deals (about 7% in the working paper). The average one-day offer premium is **31%**. | [IDEAS](https://ideas.repec.org/a/inm/ormnsc/v65y2019i12p5697-5720.html) [snippet]; [WP pdf](https://www.mcgill.ca/desautels/files/desautels/abs_2015_may_0.pdf) [read] |
| Rodrigues, Souza & Stevenson (2012, *IRFA*) | ASX tick data, 2004–08 | Intraday behaviour of targets is affected by informed traders (especially bidders) at least 3 months before the announcement | [IDEAS](https://ideas.repec.org/a/eee/finana/v21y2012icp23-32.html) [read] |
| Pham & Ausloos (arXiv 2020) | LSE, only 58 deals | 60.7% (2008–12) and 32.5% (2015–19) of the day-0 CAAR was in place by day −1. The small sample and low day-0 CAAR (about 6–8%) make this weak evidence. | [arXiv](https://arxiv.org/pdf/2012.11594) [read] |

**Implication.** The share of the premium in the price before the announcement used to be about 50% (Schwert, Keown & Pinkerton) and is now much smaller for US deals (median run-up about 2%, per Dutordoir et al.). The tradable jump at the announcement is therefore bigger today, but competition for it is fiercer.

### 1b. Speed of adjustment: M&A-specific evidence and benchmarks

**M&A-specific evidence found:**
- **Jennings (1994, *J. Financial Research* 17(2):255-270)**, "Intraday changes in target firms' share price and bid-ask quotes around takeover announcements". IDEAS has no abstract, so the findings are unverified ([IDEAS](https://ideas.repec.org/a/bla/jfnres/v17y1994i2p255-270.html) [read]).
- **Jennings & Mazzeo (1991, *J. Business* 64(2))** study price moves around acquisition announcements. Intraday details are behind JSTOR and unverified ([IDEAS](https://ideas.repec.org/a/ucp/jnlbus/v64y1991i2p139-63.html) [snippet]).
- **Ersan, Şimşir, Simsek & Hasan (2021, *Emerging Markets Review* 47)**, Turkey, all corporate announcements on KAP:
  - Reaction is slower than the millisecond speeds documented in developed markets.
  - Prices react faster to positive news than to negative news.
  - When HFTs were more active before the announcement, prices adjusted more slowly.
  - Event-driven strategies had "sizable profit opportunities" ([Sabanci repository](https://research.sabanciuniv.edu/id/eprint/43385/) [read]).
  - A search summary said reaction starts about 4 s after positive news and about 10 s after negative news, measured as the share of the 300-s response that occurs in the first 60 s ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1566014120305872) [snippet; full text not accessed, so unverified]).
- **Von Beschwitz, Keim & Massa (2013, NBER conference paper)**, "Media-Driven High Frequency Trading":
  - RavenPack analytics arrive about **300 ms** after the Dow Jones Newswire item.
  - When a story is covered by the analytics, prices and volume move more **in the first few seconds** after the news ([pdf](https://conference.nber.org/conf_papers/f69879.pdf) [read]).
- **Chordia & Miao (2019 WP)**, 723 stock-financed deals, 2008–17. They find no evidence that low-latency trading causes overreaction to M&A announcements, and conclude that M&A news "is also quickly and accurately incorporated" when low-latency traders are present. This is evidence on acquirer returns, not targets ([pdf](https://mitsloan.mit.edu/sites/default/files/inline-files/Chordia_Miao.pdf) [read]).
- **Jetley & Ji (FAJ 2010)** give an example: Rohm & Haas jumped more than 60% on the day of Dow's $78 cash bid (10 Jul 2008) and closed at a 5.9% spread ([pdf](https://analysisgroup.com/link/f5a479d9a8fb4799b20ff4a989d78a50.aspx) [read]).
- **Gap: no paper found** that reports the share of the target's day-0 jump realised within the first 1, 5 or 30 minutes. **Unverified.** A practical alternative is to measure it yourself with TAQ and newswire timestamps; WRDS offers a second-by-second intraday event-study tool ([WRDS](https://wrds-www.wharton.upenn.edu/pages/grid-items/intraday-second-second-event-study-upload-your-own-events/) [snippet]).

**General news-speed benchmarks:**

| Study | Setting | Speed and profit numbers | Source |
|---|---|---|---|
| Patell & Wolfson (1984, *JFE* 13:223-252) | Broad Tape earnings and dividend releases | Initial reaction within "a few minutes, at most". Returns from simple trading rules **dissipate within 5–10 minutes**. Effects on volatility persist for hours. | [Stanford GSB](https://www.gsb.stanford.edu/faculty-research/publications/intraday-speed-adjustment-stock-prices-earnings-dividend-announcements) [read] |
| Busse & Green (2002, *JFE* 65:415-437) | CNBC Morning and Midday Call | Prices respond within seconds and positive reports are fully priced **within about 1 minute**. Trading intensity doubles in the first minute. Traders who execute **within 15 s** make small but significant profits. | [IDEAS citation](https://ideas.repec.org/a/eee/jfinec/v65y2002i3p415-437.html) [read]; numbers [snippet] |
| Chordia, Green & Kottimukkalur (2018, *RFS* 31(12)) | Macro releases, SPY and ES | Prices respond **within 5 ms** and trading intensity rises more than 100-fold. Profits are small: about **$19k (SPY) and $50k (ES) per event**. | [IDEAS abstract](https://ideas.repec.org/a/oup/rfinst/v31y2018i12p4650-4687..html) [read] |
| Christensen, Timmermann & Veliyev (arXiv 2026) | After-hours earnings releases | Earnings releases "almost always induce jumps". A post-announcement strategy is consistent with efficient pricing after 2016. | [arXiv](https://arxiv.org/abs/2601.08962) [read] |
| Christie, Corwin & Harris (2002, *JF* 57(3)) | Nasdaq news halts | When a stock reopens after only a 5-minute quote period, quoted spreads **more than double** and volatility is **more than 9×** normal. Next-day reopenings with a 90-minute quote period show little effect. | [IDEAS](https://ideas.repec.org/a/bla/jfinan/v57y2002i3p1443-1478.html) [snippet] |
| Barclay & Hendershott (2003, *RFS* 16(4)) | After-hours trading | Low after-hours volume still produces significant but inefficient price discovery. Pre-open price changes are larger and less noisy than after-close changes. | [IDEAS](https://ideas.repec.org/a/oup/rfinst/v16y2003i4p1041-1073.html) [snippet] |
| Lyle, Rigsby, Stephan & Yohn (2018 WP) | Earnings timing | About 96% of firms announce earnings outside regular hours, split 48% pre-open and 52% post-close. News is absorbed more slowly after pre-open releases than after post-close ones. | [pdf](https://business.columbia.edu/sites/default/files-efs/imce-uploads/LYLE%20LRSY_April_18_2018.pdf) [read] |

### 1c. Merger-arbitrage spreads and returns after the announcement

| Study | Finding | Source |
|---|---|---|
| Mitchell & Pulvino (2001, *JF* 56(6)) | 4,750 mergers, 1963–98. Risk arbitrage earns **about 4% a year** excess return after transaction costs. Returns behave like a short position in index puts: correlated with the market in sharp sell-offs. | [AQR](https://www.aqr.com/library/journal-articles/characteristics-of-risk-and-return-in-risk-arbitrage) [snippet]; [IDEAS](https://ideas.repec.org/a/bla/jfinan/v56y2001i6p2135-2175.html) |
| Baker & Savasoglu (2002, *JFE* 64(1)) | A diversified risk-arbitrage portfolio earns **0.6–0.9% per month** abnormal, 1981–96 | [IDEAS](https://ideas.repec.org/a/eee/jfinec/v64y2002i1p91-115.html) [snippet] |
| Jetley & Ji (2010, *FAJ* 66(2)) | 2,182 deals, 1990–2007, spread measured on the day after the announcement. **Median first-day spread was 4.10–7.94% each year before 2001 and 1.74–2.63% in 2001–07.** For successful deals the median first-day spread fell from 6.39% (1990–95) to 4.62% (1996–2001) to 1.91% (2002–07). The spread "declined by more than 400 bps since 2002". | [pdf](https://analysisgroup.com/link/f5a479d9a8fb4799b20ff4a989d78a50.aspx) [read] |
| Bessembinder & Zhang (2015 WP) | 6,413 deals, 1980–2012. Mean ratio of day-after price to offer price is 93.0% (median 93.7%) and rose about 0.36 percentage points a year. **Median 97.3–98.9% in 2002–2012**; mean for cash deals 94.9%. | [pdf](https://english.ckgsb.edu.cn/sites/default/files/files/Merger_Anomaly_20150417.pdf) [read] |
| Van Tassel (2016, NY Fed SR 761) | 3,836 deals, 1996–2012. The **median target jumps 27%** and then trades at a **3.5% spread** to the offer. 19–22% of deals fail. | [pdf](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr761.pdf?la=en) [read] |
| Verdad (2023 blog) | 835 deals, 2000–2020. 89% close. A long position earns about 2.0% on successful deals and loses 2.8% on cancelled ones, for a blended 1.5%. | [Verdad](https://verdadcap.com/archive/merger-arbitrage) [read] |

**Typical day-1 spread for US cash deals:** a median of roughly 2% since the early 2000s (Jetley & Ji). There is a fat right tail: the 95th-percentile spread was often above 30%.

### 1d. Post-announcement drift and reversal; deal type

- **Initial-target-price deciles** (Bessembinder & Zhang 2015) [read]. Cumulative abnormal returns after day +1 fall steadily as the day-after price moves closer to the offer:
  - Over one week: +0.32% for the lowest decile, −0.74% for the highest.
  - Over two months: +2.21% for the lowest decile, **−3.5%** for the highest, which is significant.
  - Interpretation: a target priced at or above the offer signals over-optimism and tends to drift down. Weaker evidence of underreaction in the lowest decile. ([pdf](https://english.ckgsb.edu.cn/sites/default/files/files/Merger_Anomaly_20150417.pdf))
- **Rumours** (Ahern & Sosyura 2015) [read]:
  - Day-0 abnormal return is 4.3% on average: 6.9% for rumours that came true, 3.0% for false ones.
  - About 3% run-up in the 20 days before the rumour.
  - −1.4% average reversal over 10 days; −2.7% for false rumours over 20 days.
  - False-rumour targets fully reverse over the 41-day window.
  - Only 33% of rumours lead to a bid within 1 year, 27.5% within 6 months and 15.8% within 1 month ([pdf](https://conference.nber.org/conf_papers/f72667/f72667.pdf)).
- **Cash versus stock** (Malmendier, Opp & Saidi, NBER w18211, failed bids 1980–2008):
  - Announcement returns, including the run-up: about **+25% for cash targets and +15% for stock targets**.
  - After the deal fails, cash targets stay about 15% higher while stock targets return to their pre-announcement level ([pdf](https://www.nber.org/system/files/working_papers/w18211/w18211.pdf) [read]).
  - Chen, Chou & Lee (2011, *JBF*) find cash offers raise premiums and target returns only for **overnight** announcements, not daytime ones ([IDEAS](https://ideas.repec.org/a/eee/jbfina/v35y2011i9p2231-2244.html) [read]). That paper confirms a meaningful sample of US deals is announced **during trading hours**, but I could not get the share.
- **Hostile versus friendly** (Schwert 2000, NBER w7085): most deals the press calls hostile are economically indistinguishable from friendly ones. Negotiations are simply made public earlier, so the news arrives in stages, each a possible trading event ([NBER](https://www.nber.org/papers/w7085) [snippet]).
- **Cash premium:** Schwert reports the run-up is slightly lower (11.4%) where equity is the only payment, and higher in tender offers (15.9%) ([WP](https://www.nber.org/papers/w4863.pdf) [read]).
- **Small versus large, and emerging markets:** no rigorous source found on intraday drift by size or in emerging markets. **Unverified.** The only emerging-market evidence on profitability at short horizons is the Turkey paper above.

### 1e. EDGAR dissemination latency

- **Rogers, Skinner & Zechman, "Run EDGAR Run" (*JAR* 55(2):459-505, 2017).** In 2012–13, paying subscribers to the Public Dissemination Service (PDS) received "just over half the filings … in advance of the public posting, with an average 18 second advantage" ([CU Boulder summary](https://www.colorado.edu/business/faculty-research/2018/06/17/run-edgar-run-sec-dissemination-high-frequency-world) [read]).
  - For Form 4 filings, prices, volumes and spreads start responding about **30 s before** public posting ([TheCorporateCounsel blog](https://www.thecorporatecounsel.net/blog/2014/11/edgar-dissemination-still-favoring-subscribers.html) [read]).
  - That blog also cites an "approximately 10 seconds" average and a 40 s mean / 36 s median posting lag. These differ from the CU summary; I would rely on the CU summary.
- **After the WSJ story of 29 Oct 2014**, one subscriber's feed-to-website lag fell from 35 s to 27 s, then to about 3 s and 2.5 s within days ([TheCorporateCounsel](https://www.thecorporatecounsel.net/blog/?p=5258) [read]).
  - On 19 Dec 2014, SEC Chair Mary Jo White announced plans "to ensure that EDGAR filings are available to the public on the SEC website before such filings are made available to PDS subscribers" ([CU Boulder](https://www.colorado.edu/business/faculty-research/2018/06/17/run-edgar-run-sec-dissemination-high-frequency-world) [read]).
  - The changes were reportedly made in Feb 2015 ([search summary](https://law-journals-books.vlex.com/vid/erratum-855682740) [snippet]).
- **EDGAR timing today:**
  - "Filings are often available on sec.gov within 1-3 minutes of the EDGAR system timestamp", and the lag can grow under heavy load ([SEC webmaster FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) [read]).
  - The data.sec.gov **submissions API** has "a typical processing delay of less than a second" ([SEC API page](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) [read]).
- **Newswire versus EDGAR for 8-K and Rule 425 filings:**
  - Reg FD filings must be simultaneous with an intentional public release ([Goodwin Reg FD guide](https://www.goodwinlaw.com/en/resource/off-the-shelf/regulation-fd) [snippet]).
  - Business-combination communications go on file under Rule 425 "on or before the date of first use" ([17 CFR 230.425](https://www.law.cornell.edu/cfr/text/17/230.425) [snippet]). That is a same-day requirement, not a same-second one.
  - Filing agents advertise sending the wire release and the EDGAR filing "simultaneously" ([Federal Filings](https://federalfilings.com/newswire-distribution) [snippet]).
  - I found **no systematic study** measuring the lag from the M&A wire release to the EDGAR 425 or 8-K filing. **Unverified.**

---

## 2. Market structure: does a slow-repricing window exist?

### 2a. United States

- **Nasdaq notice and halt.**
  - Material news released between 7:00 am and 8:00 pm ET needs notice to MarketWatch at least 10 minutes before release; news outside those hours needs notice before 6:50 am ET.
  - MarketWatch "may recommend a temporary trading halt (generally no more than 30 minutes)" ([Securities Law Blog on Rule 5250(b)(1)](https://securities-law-blog.com/2024/07/09/nasdaq-issues-new-faq-on-marketwatch-news-submittals/) [read]).
  - Nasdaq asks companies to release after-close news no earlier than 4:01 pm, preferably 4:05 pm ([Hunton on Nasdaq Issuer Alert 2015-001](https://hunton.sitepilot11.firmseek.com/insights/legal/nasdaq-issues-guidance-on-the-post-market-close-release-of-material-news) [read]).
- **Halt codes** ([Nasdaq Trader](https://www.nasdaqtrader.com/Trader.aspx?id=TradeHaltCodes) [read]):
  - **T1**: news pending.
  - **T2**: news released and being disseminated through a Reg FD-compliant method.
  - **T3**: news fully disseminated; shows the quote-resumption time and the trade-resumption time.
  - **T7**: quotation-only period.
  - Halts appear in the Nasdaq Trader RSS feed with halt time, reason code and resumption times ([RSS](https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts) [read]).
- **Reopening (Nasdaq).**
  - News halts under Rule 4120(a)(1) end with a **5-minute Display Only Period**, then a **Halt Cross** under Rule 4753.
  - The period is extended by 1 minute if the expected cross price moves by the greater of 5% or $0.50, or if market orders would go unexecuted ([SEC Rel. 34-88383](https://www.sec.gov/files/rules/sro/nasdaq/2020/34-88383.pdf) [read]).
  - Christie, Corwin & Harris find spreads more than double and volatility more than 9× normal after these 5-minute reopenings (above).
- **NYSE.**
  - Companies must notify NYSE at least 10 minutes before material news released between 7:00 am and the close.
  - NYSE halts pre-open (7:00–9:30) only at the company's request.
  - After-close news should wait until the closing price is published or 15 minutes after the close, whichever is earlier ([Hunton](https://hunton.com/insights/legal/nyse-expands-material-news-notification-policy-and-trading-halt-authority-effective-september-28-2015) [read]).
  - Reopening is via a DMM Trading Halt Auction under Rule 123D ([NYSE Info Memo 18-02](https://www.nyse.com/publicdocs/nyse/markets/nyse/rule-interpretations/2018/NYSE%20Info%20Memo%2018-02.pdf) [snippet]).
- **LULD (limit up-limit down).**
  - Applies only from 9:30 am to 4:00 pm ET.
  - Bands: 5% for Tier 1 stocks above $3 (S&P 500, Russell 1000), 10% for Tier 2 stocks above $3, and 20% for stocks priced $0.75–$3.
  - Bands double in the last 25 minutes for Tier 1.
  - A stock that stays in a limit state for 15 s gets a **5-minute pause** ([LULD Plan](https://www.luldplan.com/) [read]).
  - So an intraday 30% jump in an unhalted stock would trip LULD repeatedly. In practice M&A news is either halted (T1) or released pre-market, where LULD does not apply.
- **Pre-market.**
  - Sessions run from 4:00 am. Nasdaq expects to move to 23-hour trading from **6 Dec 2026**, subject to SEC approval and SIP readiness; mergers would "generally remain halted until 8:00 a.m. ET on the effective date" ([Cooley, 29 Jul 2026](https://governancebeat.cooley.com/24-hour-trading-nasdaqs-faqs-and-secs-roundtable/) [read]).
  - Liquidity is thin: pre- and post-market together are reportedly under 4% of volume ([Bloomberg Tradebook](https://www.bloomberg.com/professional/?p=46991) [snippet; page returned 403]).
- **When are US deals announced?**
  - "Merger Monday" and pre-open announcements are the norm ([CFI](https://corporatefinanceinstitute.com/resources/valuation/merger-monday/) [snippet]).
  - The **share of US M&A announced during regular hours is unverified**. Chen, Chou & Lee (2011) confirm a daytime subsample exists.
  - For comparison, about 96% of earnings releases come outside regular hours (Lyle et al. 2018 [read]).

### 2b. United Kingdom

- **Takeover Code.** A firm or possible offer must be announced if the target is "the subject of rumour and speculation or there is an untoward movement in its share price".
  - The Panel must be consulted when the price is 10% or more above its lowest level since the approach. A 5% rise in a single day may also count as "untoward" ([Rule 2.2](https://code.thetakeoverpanel.org.uk/tp/rules/rule-2/rule-2-2.html) [read]).
- **Leak announcements:** the Panel expects them "immediately, i.e. within a matter of minutes". If wording is not final, a short announcement goes first ([Practice Statement 20](https://code.thetakeoverpanel.org.uk/tp/ps/ps-20.html) [read]).
  - These are released **during market hours without any automatic halt**, so this is the clearest developed-market intraday window.
- **Possible and firm offers.** A Rule 2.4 possible-offer announcement must name the potential offeror. Rule 2.6 "put up or shut up": firm offer or walk away by 5:00 pm on day 28. Rule 2.7: firm, binding offer ([Rule 2.4](https://code.thetakeoverpanel.org.uk/tp/rules/rule-2/rule-2-4.html), [Rule 2.6](https://code.thetakeoverpanel.org.uk/tp/rules/rule-2/rule-2-6.html), [Rule 2.7](https://code.thetakeoverpanel.org.uk/tp/rules/rule-2/rule-2-7.html) [snippet]).
- **RNS timing.**
  - RNS runs 24/7 and processes about 350,000 announcements a year ([LSEG RNS](https://www.lseg.com/en/capital-markets/regulatory-news-service) [read]).
  - Many announcements land between 7:00 and 7:30 am, before the open, but takeover developments can come intraday "because negotiations have just concluded" ([Investegate](https://www.investegate.co.uk/content/are-morning-rns-announcements-more-influential-than-afternoon-releases) [read]).
- **LSE microstructure.** A 5-minute price-monitoring extension or auction is triggered when the indicative price breaches a tolerance ([LSE ETP price monitoring factsheet](https://docs.londonstockexchange.com/sites/default/files/documents/LSE_ETP_Price_Monitoring_Mechanisms_factsheet.pdf) [snippet]). The equity thresholds (reportedly 3% for FTSE 100 and 5% for others) are **unverified**.

### 2c. Emerging, frontier and other markets

| Market | Intraday release allowed? | Halt or price limits | Window for slow repricing? | Sources |
|---|---|---|---|---|
| **India (NSE/BSE)** | Yes. Board-meeting outcomes within **30 min** of the meeting ending; 12 h for internal events, 24 h for external ones. Top listed companies must verify mainstream-media rumours within 24 h (Reg 30(11)). Open offers are announced on the day of agreement (SAST Reg 13(1)) and cover only **≥26%** of shares (Reg 7(1)). | No news-pending halt found (a negative finding, so unverified). Non-F&O stocks have fixed 2/5/10/20% daily bands; F&O stocks have dynamic 10% bands that can widen after a 15-min cooling-off. | **Yes, but capped.** A target in a 5% band can need several days to reprice. With a partial offer, the price need not reach the offer. | [TaxGuru LODR 2023](https://taxguru.in/sebi/overview-amendments-sebi-lodr-regulations-2023.html) [read]; [SAST Reg 13](https://ca2013.com/toc-regulation-13/) [snippet]; [KS&K Reg 7](https://ksandk.com/capital-markets/open-offer-sebi-takeover-code/) [snippet]; [Rupeezy bands](https://support.rupeezy.in/support/solutions/articles/21000004845-what-are-circuit-limits-or-price-bands) [snippet]; [Fyers](https://support.fyers.in/portal/en/kb/articles/what-are-price-bands) [read] |
| **Japan (TSE, TDnet)** | Yes, but a disclosure such as a merger during trading triggers a halt that lifts **15 min** later. About 40% of firms release earnings right after the close (now 15:30 since 5 Nov 2024). | 15-min halt plus daily yen price limits; limits widen only after a limit-up day with unfilled demand. | Mostly no intraday window. Daily limits can force multi-day repricing on large premiums (exact table unverified). | [JPX halts](https://www.jpx.co.jp/english/markets/equities/suspended/index.html) [snippet; 403]; [JPX price-limit notices](https://www.jpx.co.jp/english/news/1030/20250210-01.html) [snippet]; [Waseda study on TDnet timing](https://www.waseda.jp/fcom/riba/news/6172) [snippet] |
| **Korea (KRX, DART/KIND)** | Yes. | "Important information disclosure" triggers a **30-min** halt; after 14:30, trading resumes the next day. ±30% daily limit since 15 Jun 2015. | No intraday window; ±30% limit binds for large premiums. | [KRX suspension rules](https://global.krx.co.kr/contents/GLB/06/0602/0602010103/GLB0602010103T2.jsp) [read]; [KRX resumption](https://global.krx.co.kr/contents/GLB/06/0602/0602010204/GLB0602010204T3.jsp) [read]; [Etoday on ±30%](https://www.etoday.co.kr/news/view/1127429) [snippet] |
| **Hong Kong (HKEX)** | **No.** Inside information goes out only in windows outside trading hours: 6:00–8:30, 12:00–12:30 and 16:30–23:00 (2020 FAQ). The windows close 30 min before trading. Halts last at most 2 trading days before becoming suspensions. | Halt or suspension pending announcement. A 2013 consultation proposed intraday release with a ≥30-min halt; whether it was implemented is unverified, and the 2020 FAQ still describes window-only release. | No. | [HKEX FAQ (updated 20 Mar 2020)](https://www.HKEX.com.hk/-/media/HKEX-Market/Listing/Rules-and-Guidance/eSubmission-System/Listed-Company-Information-Dissemination-and-Related-Trading-Arrangements/faqinv.pdf) [read]; [2013 consultation](https://mondovisione.com/media-and-resources/news/hkex-publishes-consultation-conclusions-on-trading-halts-2013315/) [read] |
| **Australia (ASX)** | Yes; the market announcements office runs 7:30 am–7:30 pm. | When an announcement is market-sensitive, ASX halts trading: **about 1 hour for takeovers and schemes, about 10 min otherwise**. Companies can also request a halt of up to 2 trading days (LR 17.1). | No for announced deals. The window exists only for unannounced leaks. | [ASX GN14](https://www.asx.com.au/documents/rules/gn14_asx_market_announcements_platform.pdf) [read]; [ASX trading-halt summary](https://www.moneymag.com.au/tpg-blunder-what-you-need-to-know-about-asx-trading-halts) [snippet] |
| **Turkey (Borsa Istanbul, KAP)** | Yes. KAP disclosures arrive intraday, timestamped to the second (as used in Ersan et al.). | ±10% daily limit (Mar 2020 change; current level unverified). 5% single-stock circuit-breaker trigger with a 30-min call (2020). BIST closes a stock to trading when a company fails to explain unusual moves. | **Yes:** reaction is slower and profits were sizable (Ersan et al.), but large premiums hit the ±10% limit. | [BIST 2020 limits](https://borsaistanbul.com/en/announcement/13357/changes-price-limits-equity-and-derivatives-markets) [read]; [Ersan et al.](https://research.sabanciuniv.edu/id/eprint/43385/) [read]; [CNBC-e on closures](https://www.cnbce.com/borsa/borsa-istanbul-duyurdu-bir-hisse-tum-islemlere-kapatildi-h31605) [snippet] |
| **Brazil (B3, CVM)** | Material facts are to be disclosed "whenever possible, before the start or after the close of trading". If disclosure during trading is unavoidable, the investor-relations officer **may request a suspension** "for the time necessary for adequate dissemination". | Suspension is optional. | Partial: an intraday release without suspension is possible but discouraged. | [CVM Res. 44, art. 5 §2](https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol044consolid.pdf) [read] |
| **South Africa (JSE, SENS)** | Unverified. Firms commonly request halts pending price-sensitive announcements. The JSE announced on 4 Aug 2026 that it will retire SENS for a new platform; the date is unspecified. | Halts on request. | Unverified. | [EWN](https://www.ewn.co.za/2026/08/04/jse-to-retire-sens-market-system-under-new-strategy) [read]; [example halt notice](https://sharedata.co.za/v2/scripts/SENS.aspx?id=528187) [snippet] |
| **Saudi Arabia (Tadawul)** | Material developments must be disclosed "as soon as possible and before the trading period following the occurrence". A search summary says disclosures come at least 30 min before trading; that detail is unverified. | Suspensions are mostly for late financial statements. | No: designed to avoid intraday release. | [CMA enforcement notice](https://cma.gov.sa/en/Market/NEWS/Pages/CMA_N_3037.aspx) [read] |
| **Singapore (SGX)** | An issuer receiving notice of a takeover offer must request a trading suspension or halt and announce immediately. Halts can be requested up to 3 days ahead (LR 703 guidance). | Halt. | No for announced deals. | [SGX Rulebook LR 703](https://rulebook.sgx.com/node/5587) [read]; [search summary](https://rulebook.sgx.com/node/3554) [snippet] |
| **Malaysia (Bursa)** | Yes. | A material announcement released during trading triggers a **1-hour** halt (since 3 Aug 2009). No halt applies during the lunch-break window. | No intraday window, but lunch-break releases go straight to the afternoon open. | [The Edge](https://theedgemalaysia.com/article/update-bursa-reserves-right-extend-trading-halt) [read] |
| **Philippines (PSE, PSE Edge)** | Issuer must disclose within 10 min. If the event happens during trading, it must request a halt, lifted **1 hour after dissemination** (or the next day if within 1 hour of the close). | 1-hour halt. | No. | [PSE Disclosure Rules Art. VII](https://documents.pse.com.ph/wp-content/uploads/sites/15/2021/04/Article-VII.pdf) [snippet] |
| **Thailand (SET)** | The "H" (halt) sign is posted until the company discloses material information. | Halt on request or at SET's discretion. | No. | [EGCO/SET notice](https://www.egco.com/en/investor-relations/newsroom/set-announcements/38056/h-sign-posted-on-egco-s-securities) [snippet] |
| **Indonesia (IDX)** | Unverified. | Auto-rejection limits; the lower limit was set to 15% on 8 Apr 2025. Upper tiers unverified. | Unverified. | [Infobank](https://infobanknews.com/?p=332879) [snippet] |

**Bottom line.** Places where announcements are released during continuous trading **without** a mandatory halt:
- UK: leak and Rule 2.2/2.4 announcements.
- India: but price bands and the 26% open offer distort repricing.
- Turkey: but the ±10% limit applies.
- US pre-market and US names a company chose not to halt: thin liquidity.
- Possibly Brazil, when the company does not request a suspension.

Even where an intraday release is allowed, Japan, Korea, ASX, Malaysia and the Philippines impose automatic halts of 10 to 60 minutes.

---

## 3. Fastest legitimate news sources

### 3a. SEC EDGAR

- **PDS feed.**
  - Run by contractor **Maximus Inc.**, which took over via Attain LLC on 1 Jul 2014. Delivered by SFTP/SCP push over a dedicated feed from 6:00 am to 10:00 pm ET.
  - A mandatory monthly, quarterly or annual fee is set in the Subscriber Agreement and is **not published**. The subscriber also pays for its own receiving station ([SEC PDS New Subscriber Document, updated 1 Aug 2025](https://www.sec.gov/files/edgar-pds-new-subscriber-document.pdf) [read]).
  - Since the 2014–15 fix, the SEC's stated aim has been that the website is no later than PDS (above). The current residual latency difference is **unverified**.
- **Free routes.**
  - The Latest Filings search ("getcurrent") and its RSS/Atom feed are "the best resources for getting as close to real time availability as possible" ([SEC FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) [read]).
  - The website is typically 1–3 minutes behind the EDGAR timestamp.
  - The data.sec.gov submissions JSON has under 1 second of processing delay ([SEC API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) [read]).
  - **Fair-access limit: 10 requests per second** with a declared User-Agent ([SEC FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) [read]; [Accessing EDGAR data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) [read]).
  - EDGAR accepts filings from 6:00 am to 10:00 pm ET. Some submissions after 5:30 pm (10:00 pm for Forms 3/4/5) are disseminated the next business day ([SEC](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) [read]).
  - Full-text search indexing lag: "within minutes" per a search summary; **unverified**.
- **Relevance to M&A.** The deal press release usually hits the wire before or alongside the 425 or 8-K filing, so EDGAR is a *confirmation* source rather than the first source. The size of the lag is unverified.

### 3b. Newswires

- **Business Wire** stopped licensing direct feeds to HFT firms in Feb 2014, after a WSJ story on 7 Feb 2014; the CEO said BW "did not give a time advantage" ([O'Dwyer's](https://www.odwyerpr.com/story/public/1934/2014-02-21/business-wire-pulls-plug-high-speed-traders.html) [read]).
- **Marketwired** did the same in Mar 2014 ([IR Magazine](https://irmagazine.com/reporting/marketwired-halts-direct-feeds-hft-firms) [snippet]).
- **PR Newswire** never sold its direct feed to HFT firms. From Apr 2014 it has required feed customers to certify every year that they will not use it for high-speed trading ([O'Dwyer's](https://www.odwyerpr.com/story/public/2338/2014-05-01/pr-newswire-adds-curbs-high-speed-trading.html) [snippet]).
- **Free feeds.** Business Wire, GlobeNewswire and Accesswire offer free web, RSS or email feeds filtered by industry, company or exchange ([GlobeNewswire](https://www.globenewswire.com/newswire-press-release-content) [snippet]; [Business Wire RSS](https://www.editorandpublisher.com/stories/business-wire-adds-rss-feeds,29011) [snippet]; [Accesswire](https://www.issuerdirect.com/platform/accesswire) [snippet]). Their latency compared with the institutional feeds is **unverified**.
- **Release timing:** newswires sell "simultaneous" delivery under Reg FD ([PR Newswire](https://www.prnewswire.co.uk/resources/articles/distribute-press-release-regulated-industries/) [snippet]). Whether releases go out exactly on the minute or on the hour is **unverified**.

### 3c. Professional machine-readable news

- **LSEG Machine Readable News** ([factsheet](https://www.lseg.com/content/dam/data-analytics/en_us/documents/fact-sheets/machine-readable-news-and-quantitative-data-factsheet.pdf) [read]):
  - Reuters plus third-party content.
  - Latency ranges "from less than 3 milliseconds for our Ultra Low Latency Headline Feed" to 1 day for aggregated items.
  - Analytics archive back to 2003 with millisecond timestamps.
  - The factsheet's own example: a Reuters scoop on 11 Jan 2024 that Bain and H&F were vying for DocuSign; DocuSign closed up 9.3%.
- **Bloomberg Event-Driven Feeds** carry textual news (10,000+ headlines a day from 151 bureaus) plus news analytics ([Bloomberg EDF](https://professional.bloomberg.com/products/data/enterprise-catalog/event-driven-feeds) [snippet]).
  - Delivered over B-PIPE and optimised for low latency ([The Trade News 2010](https://www.thetradenews.com/bloomberg-bolsters-machine-readable-news-offering/) [read]).
  - Includes flags for scoops and exclusive M&A stories ([Bloomberg Tech](https://www.bloomberg.com/company/?p=20664) [snippet; 403]).
- **Dow Jones Newswires** run a multicast feed measured in microseconds, hosted in Equinix data centres in NY, Chicago, DC and London, plus an "Elementized" XML feed for algorithms ([Equinix case study](https://www.equinix.com/insights/case-studies/dow-jones) [snippet; 403]).
- **RavenPack** analytics arrive about **300 ms** after the DJ Newswire item, as of 2013 ([von Beschwitz et al.](https://conference.nber.org/conf_papers/f69879.pdf) [read]). RavenPack also ingests The Fly ([Markets Media 2016](https://www.marketsmedia.com/ravenpack-expands-premium-content-coverage-big-data-analytics-partnering-fly) [read]).
- **Benzinga:**
  - Pro plans: Basic $37/mo, Essential $197/mo (adds audio squawk), Options Mentor $381/mo on annual billing. A reviewer measured a "1s – 3s" delay versus Bloomberg and Reuters ([LiberatedStockTrader](https://www.liberatedstocktrader.com/benzinga-pro-review-real-time-news/) [read; not vendor-verified]).
  - Websocket API exists ([Benzinga docs](https://docs.benzinga.com/ws-reference/introduction) [read]; no latency figure given).
  - Also redistributed through the Alpaca websocket at `wss://stream.data.alpaca.markets/v1beta1/news` ([Alpaca docs](https://docs.alpaca.markets/docs/streaming-real-time-news) [read]) and through Polygon.io, now Massive ([snippet](https://apicostcalc.com/de/blog/polygon-massive-rebrand-api-pricing.html)).
- **Squawks and headline services:**
  - Trade The News: claims to be "the fastest source"; pricing not shown ([site](https://www.tradethenews.com/) [read]). One search summary gave $360/mo list; **unverified**.
  - The Fly: $35–65/mo ([snippet](https://theflyonthewall.com)).
  - Newsquawk: $199 or $399/mo ([snippet](https://newsquawk.com/pricing)).
  - First Squawk: pricing unverified.
  - Tiingo: news API exists; real-time latency and pricing unverified ([snippet](https://www.findmymoat.com/vs/databento-vs-tiingo)).
- **X relay accounts.** "Walter Bloomberg" (@DeItaone) is **not affiliated with Bloomberg**. It posts terminal-style headlines, and Bloomberg has tried to identify the owner and revoke its terminal access ([Semafor](https://www.semafor.com/article/04/13/2025/how-bloomberg-and-bloomberg-drove-markets-and-headlines) [read]).
  - On 7 Apr 2025 its false tariff-pause headline "sparked some $2.5 trillion worth of market moves" ([Semafor](https://www.semafor.com/article/04/13/2025/how-bloomberg-and-bloomberg-drove-markets-and-headlines) [read]). This is a reliability risk for automated triggers.

### 3d. Exchange halt feeds

- **Nasdaq Trader halts RSS** gives halt time, reason code (T1/T2/T3, LUDP, M) and resumption times ([RSS](https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts) [read]). It is polled, so latency depends on the polling interval; any update interval is unverified.
- **Real-time halt messages** come through the SIP (UTP) and through Nasdaq TotalView-ITCH "Stock Trading Action" messages ([ITCH spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf) [snippet]; [UTP spec](https://www.utpplan.com/DOC/UtpBinaryOutputSpec.pdf) [snippet]).
- A T1 halt is a **pre-news signal**: news is coming but there is no content yet. Taken alone it is legitimate public information.

### 3e. Rumour and leak reports

- Newspaper rumours: 33% accurate within 1 year; day-0 abnormal return +4.3%; reversal for false rumours (Ahern & Sosyura [read]).
- Accuracy rises with journalist experience, specialised education and industry expertise ([CFA digest](https://rpc.cfainstitute.org/en/research/cfa-digest/2016/06/rumor-has-it-sensationalism-in-financial-media-digest-summary) [snippet]; paper [read]).
- **Wire scoops** ("people familiar with the matter") on Bloomberg or Reuters: no academic estimate found of how often they lead to deals, which is **unverified**. Example from the LSEG factsheet: DocuSign +9.3% on a Reuters scoop.

### 3f. Emerging-market disclosure portals and APIs

| Portal | Access | Cost | Source |
|---|---|---|---|
| NSE India | RSS feeds for announcements, board meetings and results (hosted on nsearchives); paid corporate-data subscription | Free RSS; paid feed (price unverified) | [NSE RSS](https://www.nseindia.com/rss-feed) [snippet]; [NSE corporate data](https://streamer.nseindia.com/market-data/corporate-data-subscription) [snippet] |
| BSE India | No official API found; third-party scrapers exist | Unverified | [Apify scraper](https://apify.com/nexgendata/nse-bse-announcements) [snippet] |
| HKEXnews | Issuer Information Feed Service (IIS): a real-time vendor feed. The fee was cut from HK$96,000 to HK$45,000 per quarter in Jun 2007 (current fee unverified). Public RSS covers exchange news only. | $$ | [HKEX IIS](https://www.hkex.com.hk/Services/Market-Data-Services/Infrastructure/Issuer-Information-feed-Service-(IIS)) [snippet]; [2007 news](https://www.hkex.com.hk/News/News-Release/2007/070305news) [snippet] |
| ASX | ComNews: real-time PDF plus metadata "directly after it is lodged", via ALC, ASX Net, VPN or vendors; fees per schedule. A public JSON endpoint (markitdigital) is reported. | $$ / free (unofficial) | [ASX Company News](https://www.asx.com.au/connectivity-and-data/information-services/company-news) [read]; [snippet on endpoint](https://thenextgennexus.com/2026/06/10/asx-company-announcements-api-trading-signals/) |
| JPX TDnet | Database ¥33,400/mo; Server-Based real-time feed ¥200k setup plus ¥230k/mo; API ¥70k/mo base plus variable fees | $$ | [JPX TDnet](https://www.jpx.co.jp/english/markets/paid-info-listing/tdnet/index.html) [snippet; 403] |
| Korea OpenDART | Free API key; about 20,000 requests a day (secondary source) | Free | [OpenDART news 2020](https://www.asiae.co.kr/en/article/2020012011020597913) [snippet]; [limit via MCP README](https://glama.ai/mcp/servers/@ChangooLee/mcp-opendart/blob/9ccf6b8c59043e564074dfcd5c50298c86cba118/README_en.md) [snippet] |
| KAP (Turkey) | No official public API found; unofficial Python wrapper `pykap` | Unverified | [PyPI](https://pypi.org/project/pykap) [snippet] |
| B3/CVM, JSE SENS, Tadawul, PSE Edge, IDX | Not researched in depth; **unverified** | — | — |

### 3g. Ranked table: US M&A headline latency relative to the first public release

Ranks are inferred from the vendor claims and studies above. Except where cited, latencies are **not independently benchmarked**.

| Rank | Source | Typical latency vs first public release | Cost tier | API | Notes |
|---|---|---|---|---|---|
| 1 | Institutional low-latency feeds (DJ multicast, LSEG MRN ULL, Bloomberg EDF/B-PIPE) | Sub-millisecond to milliseconds after the vendor ingests the item. LSEG claims under 3 ms; DJ measures in microseconds. | $$$ (unpublished) | Yes: multicast/co-lo, B-PIPE | [LSEG](https://www.lseg.com/content/dam/data-analytics/en_us/documents/fact-sheets/machine-readable-news-and-quantitative-data-factsheet.pdf); [Equinix/DJ](https://www.equinix.com/insights/case-studies/dow-jones) |
| 2 | Exchange halt messages (SIP/ITCH Trading Action) | Real time (ms); signals that news is pending, without content | $–$$$ | Yes | [ITCH spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf) |
| 3 | News analytics (RavenPack) | About 300 ms after the DJ item (2013) | $$$ | Yes | [von Beschwitz et al.](https://conference.nber.org/conf_papers/f69879.pdf) |
| 4 | Benzinga API / Alpaca / Polygon websocket | Roughly 1–3 s behind Bloomberg/Reuters (reviewer claim) | $–$$ | Yes (websocket) | [review](https://www.liberatedstocktrader.com/benzinga-pro-review-real-time-news/); [Alpaca](https://docs.alpaca.markets/docs/streaming-real-time-news) |
| 5 | Human squawks (Trade The News, Newsquawk, First Squawk, Benzinga squawk) | Seconds (audio); unverified | $$ | Mostly no (audio/GUI) | see 3c |
| 6 | EDGAR data.sec.gov submissions API | Under 1 s after EDGAR dissemination, but the filing often follows the wire | Free | Yes (10 req/s) | [SEC](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) |
| 7 | EDGAR PDS | Equal to or behind the website by SEC design since 2015 (residual unverified) | $$ (unpublished) | Push SFTP | [SEC PDS](https://www.sec.gov/files/edgar-pds-new-subscriber-document.pdf) |
| 8 | EDGAR website / Latest Filings RSS | 1–3 min after the EDGAR timestamp | Free | RSS/Atom | [SEC FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) |
| 9 | Newswire public websites and RSS | Unverified (likely seconds to minutes) | Free | RSS | see 3b |
| 10 | X relay accounts (@DeItaone etc.) | Seconds to minutes; unauthorised relay with a false-headline risk | Free / X API $ | X API | [Semafor](https://www.semafor.com/article/04/13/2025/how-bloomberg-and-bloomberg-drove-markets-and-headlines) |
| 11 | Nasdaq Trader halts RSS | Depends on polling; unverified | Free | RSS | [RSS](https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts) |

---

## 4. Legal and compliance (US-centric)

- **Material non-public information (MNPI).**
  - Under the misappropriation theory (*O'Hagan*, 1997), an outsider violates §10(b)/Rule 10b-5 by trading on confidential information taken in breach of a duty owed to the source ([Cornell LII](https://www.law.cornell.edu/supremecourt/text/521/642) [snippet]).
  - Rule 10b5-2 lists situations that create a duty of trust or confidence, such as an agreement to keep information confidential or a history of sharing confidences ([GPO CFR](https://www.gpo.gov/fdsys/pkg/CFR-2012-title17-vol3/pdf/CFR-2012-title17-vol3-sec240-10b5-2.pdf) [snippet]).
  - *Carpenter*: trading ahead of the WSJ "Heard on the Street" column before publication was illegal ([SEC Historical Society](https://sechistorical.org/exhibition/fair-to-all-people-the-sec-and-the-regulation-of-insider-trading/counterattack-from-the-supreme-court/carpenter-v-united-states/) [snippet]). The same logic applies to **embargoed press releases**: anyone who receives them under embargo owes a duty, so trading before release is misappropriation. That last step is my inference and should be checked with counsel.
- **Tender offers: Rule 14e-3.** Once a bidder has taken a "substantial step", anyone holding non-public information about the offer that came from the bidder or target must abstain or disclose. **No fiduciary breach is required** ([LexPlug outline](https://www.lexplug.com/outlines/securities-regulation/rule-10b-5-and-securities-fraud/insider-trading/rule-14e-3-tender-offer-context) [snippet]; rule text at [17 CFR 240.14e-3](https://www.law.cornell.edu/cfr/text/17/240.14e-3), not opened).
- **Hacking cases.**
  - *SEC v. Dorozhko* (2d Cir. 2009): a hacker who stole IMS Health earnings and made about $286k on puts. Lying about one's identity to get access is "deceptive" even without a fiduciary duty ([SEC lit. release](https://www.sec.gov/litigation/litreleases/2010/lr21465.htm) [snippet]).
  - **Newswire hacking, 2010–2015 (SEC v. Dubovoy et al.; US v. Korchevsky):**
    - Hackers breached Marketwired, PR Newswire and Business Wire and stole about 150,000 releases. The SEC alleged more than $100m in profits across 32 defendants.
    - In one case, traders began shorting 10 minutes after the company sent the release to the wire and made $511k in the 36 minutes before publication ([SEC 2015-163](https://www.sec.gov/news/press-release/2015-163) [read]).
    - Korchevsky got 60 months and $14.4m forfeiture. The criminal case cited about $30m in profits ([USSS, 22 Mar 2019](https://www.secretservice.gov/press/releases/2019/03/former-hedge-fund-manager-sentenced-60-months-imprisonment-and-ordered-pay) [read]).
  - **EDGAR test-filing hack (2016):** 9 defendants, at least $4.1m in profit, ahead of at least 157 earnings releases ([SEC 2019-1](https://www.sec.gov/news/press-release/2019-1) [read]).
- **Rumours.** Trading on rumours or speculation that are **already published** is generally not insider trading, because the information is public ([summary of case law](https://www.osler.com/en/resources/governance/2014/osc-rejection-of-insider-trading-allegations-empha) [snippet]).
  - But an insider's *confirmation* of a rumour can itself be MNPI (*SEC v. Mayhew*, [case brief](https://www.lexplug.com/casebrief/securities_exchange_commission_v_mayhew_672257437c1a04cf1bedf097) [snippet]).
  - **Unverified:** whether any US case has treated trading on a *published* Bloomberg or Reuters "people familiar" story as illegal. None was found.
- **Paying for faster feeds of public information.** This is generally lawful, but regulators have pushed back on *tiered early access*:
  - NY AG "Insider Trading 2.0": in Jul 2013 Thomson Reuters stopped giving HFT clients the University of Michigan survey 2 seconds early ([Mondo Visione](https://mondovisione.com/news/new-york-attorney-general-schneiderman-secures-agreement-by-thomson-reuters-to-s-201378/) [snippet]). In 2014 the newswire feed curbs followed (§3b).
  - The SEC's own PDS advantage was removed after Rogers, Skinner & Zechman (§1e).
  - Practical rule: buying a feed that every customer gets at the same time as the public release is fine. Buying access *before* the general release (an early tier) is a regulatory and legal red flag.
- **Scraping and terms of service.**
  - *hiQ v. LinkedIn* (9th Cir. Apr 2022): scraping public pages is not "without authorization" under the CFAA. But LinkedIn won on breach of its user agreement (N.D. Cal. Nov 2022), and hiQ agreed to a permanent injunction and $500k ([Morgan Lewis](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2022/12/linkedin-v-hiq-landmark-data-scraping-suit-provides-guidance-to-data-scrapers-and-web-operators) [snippet]; [Proskauer](https://www.proskauer.com/blog/hiq-and-linkedin-reach-proposed-settlement-in-landmark-scraping-case) [snippet]).
  - The SEC caps EDGAR at 10 requests/s, requires a declared User-Agent and blocks undeclared tools ([SEC FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) [read]).
  - Exchange portals such as NSE, HKEXnews and KAP have their own terms of use, which I have not reviewed; treat them as **unverified** risk.

---

## Open questions / unverified items to close with your own data

1. Share of the day-0 target jump realised by +1 s, +1 min, +5 min and +30 min after the first wire timestamp, for US intraday versus pre-market deals. **No published estimate found.**
2. Share of US M&A announcements released during regular hours versus pre-market or after-hours (Chen, Chou & Lee 2011 imply a non-trivial daytime subsample).
3. Lag from the M&A wire release to the EDGAR 425 or 8-K, and the current PDS-versus-website gap.
4. Equity price-monitoring thresholds on the LSE, and the current Borsa Istanbul limit.
5. Current exchange-feed pricing for HKEX IIS, NSE, ASX ComNews and JPX TDnet (my figures are partly from 2007 or search summaries).
