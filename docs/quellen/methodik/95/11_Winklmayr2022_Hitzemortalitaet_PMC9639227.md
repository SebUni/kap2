Textdruck des Hauptbereichs (article) durch KAP3, kein Bilddruck; Abbildungen nur mit Unterschrift.
Quelle: https://pmc.ncbi.nlm.nih.gov/articles/PMC9639227/ (abgerufen 27.09.2026 06:56 UTC, HTTP 200, SHA-256 der Rohdatei 4df6e16c8ac934b40220b4b8ea29f55ef85dd35e571bd1e3d67a727154a2ca9d).
Rohdatei daneben: 11_Winklmayr2022_Hitzemortalitaet_PMC9639227.html

Dtsch Arztebl Int
. 2022 Jul 1;119(26):451–457. doi: 10.3238/arztebl.m2022.0202
Search in PMC
Search in PubMed
View in NLM Catalog
Add to search
Heat-Related Mortality in Germany From 1992 to 2021
Claudia Winklmayr
Claudia Winklmayr, M.Sc.
1Department of Infectious Disease Epidemiology, Robert Koch Institute (RKI), Berlin, Germany
Find articles by Claudia Winklmayr
1,*, Stefan Muthers
Stefan Muthers, Dr. phil.-nat.
2Research Centre Human Biometeorology, Deutscher Wetterdienst (DWD), Freiburg, Germany
Find articles by Stefan Muthers
2, Hildegard Niemann
Hildegard Niemann, Dr.-Ing.
3Department of Epidemiology and Health Monitoring, Robert Koch Institute (RKI), Berlin, Germany
Find articles by Hildegard Niemann
3, Hans-Guido Mücke
Hans-Guido Mücke, Dr. rer. nat.
4Department of Environmental Hygiene, German Environment Agency (UBA), Berlin, Germany
Find articles by Hans-Guido Mücke
4, Matthias an der Heiden
Matthias an der Heiden, Dr. rer. nat.
1Department of Infectious Disease Epidemiology, Robert Koch Institute (RKI), Berlin, Germany
Find articles by Matthias an der Heiden
1
Author information
Article notes
Copyright and License information
1Department of Infectious Disease Epidemiology, Robert Koch Institute (RKI), Berlin, Germany
2Research Centre Human Biometeorology, Deutscher Wetterdienst (DWD), Freiburg, Germany
3Department of Epidemiology and Health Monitoring, Robert Koch Institute (RKI), Berlin, Germany
4Department of Environmental Hygiene, German Environment Agency (UBA), Berlin, Germany
✉*Abteilung für Infektionsepidemiologie Robert Koch-Institut Nordufer 20, 13353 Berlin, Germany winklmayrc@rki.de
Received 2021 Dec 21; Accepted 2022 Apr 13; Issue date 2022 Jul.
PMC Copyright notice
PMCID: PMC9639227  PMID: 35583101
See letter "Obesity is a Risk Factor" in volume 120 on page 188.
See letter "In Reply" in volume 120 on page 188.
See letter "Conceptual Misunderstanding" in volume 120 on page 188.
Abstract
Background
2018–2020 were unusually warm years in Germany, and the summer of 2018 was the second warmest summer since record-keeping began in 1881. Higher temperatures regularly lead to increased mortality, particularly among the elderly.
Methods
We used weekly data on all-cause mortality and mean temperature from the period 1992–2021 and estimated the number of heat-related deaths in all of Germany, and in the northern, central, and southern regions of Germany, employing a generalized additive model (GAM). To characterize long-term trends, we compared the effect of heat on mortality over the decades.
Results
Our estimate reveals that the unusually high summer temperatures in Germany between 2018 and 2020 led to a statistically significant number of deaths in all three years. There were approximately 8700 heat-related deaths in 2018, 6900 in 2019, and 3700 in 2020. There was no statistically significant heat-related increase in deaths in 2021. A comparison of the past three decades reveals a slight overall decline in the effect of high temperatures on mortality.
Conclusion
Although evidence suggests that there has been some adaptation to heat over the years, the data from 2018–2020 in particular show that heat events remain a significant threat to human health in Germany.
Extreme heat and prolonged periods of heat are important risk factors for human health. Numerous studies have not only shown that high temperatures result in an increased burden on the health care system (1, 2), but also provided evidence of a systematic correlation between heat events and increased mortality (3– 6). For Germany, the effect of heat on mortality has been quantified both for individual federal states (7– 12) and nationwide (3, 13– 16).
High ambient temperatures have a variety of effects on the human body, for example reduced blood viscosity due to increased fluid loss, which exerts considerable strain on the cardiovascular system, or the challenge to maintain a constant body temperature (17, 18). In particular, preexisting conditions, such as diseases of the respiratory system, may be aggravated (19, 20). Since heat is rarely identified as a direct cause of death, statistical methods have to be used to estimate the number of heat-related deaths. This article builds on the modeling approaches applied in studies on heat-related mortality between 1992 and 2017 as well as between 2001 and 2015 and estimates the number of heat-related deaths between 1992 and 2021, using a generalized additive model (GAM) (21).
Methods
Data
As in the 1992–2017 study (3), we used all-cause mortality data of the German Federal Statistical Office (StBA, Statistisches Bundesamt) per calendar week in the period from 1992 to 2021 (22). These data are aggregated by four age groups (<65, 65–74, 75–84, and 85+ years of age) and by federal state. In addition, we made use of the StBA’s official population statistics as well as the results of the population projection for the year 2021 (scenario G2-L2-W2, assuming moderate developments in birth rate, life expectancy and net migration) (23).
For the temperature data, we used hourly air temperature measurements of 52 stations of the surface observation network of the German Weather Service (Deutscher Wetterdienst, DWD). These data were first averaged over the 24 hours of the day and then over calendar week and federal state. We also considered the previously analyzed period 1992–2017, on the one hand, to ensure stable adaption of the seasonal pattern due to the longer observation period, and, on the other hand, to allow for comparability with previous estimates. As before, we analyzed only the summer half-year (calendar weeks 15–40) and distinguished the following three decades: 1992–2001, 2002–2011 and 2012–2021. Furthermore, we grouped the federal states into three major regions: “North” (Bremen, Hamburg, Mecklenburg-Western Pomerania, Lower Saxony, Schleswig-Holstein), “Central“ (Berlin, Brandenburg, North Rhine-Westphalia, Rhineland-Palatinate, Saarland, Hesse, Saxony, Saxony-Anhalt, Thuringia) and “South“ (Baden-Wuerttemberg, Bavaria). This approach allowed us to take specific regional features of the effect of high temperatures on mortality into account.
Model
We used a generalized additive model (GAM) (21) and the R statistical software (version 4.0.5, package “mgcv” [24]) to model the curve of all-cause mortality observed during the study period. For each region and age group, the modelled all-cause mortality curve is composed of a long-term trend, a seasonally recurring pattern and exposure-response curves which quantify the relative effect of mean temperature on mortality of the same week and the following three weeks.
Based on the exposure-response curves, we identified temperature thresholds for each age group, region and decade above which temperature has a relevant effect on mortality. We refer to a calendar week during which the mean temperature is above the threshold as a “heat week” and to contiguous periods of heat weeks as “heat periods”. Since the thresholds are close to 20 °C, we occasionally use this temperature value as an indicator of a heat week.
We refer to the mortality to be expected if the weekly mean temperature always remained below the threshold as “background mortality”. The difference between the modeled mortality curve and the background mortality yields the “heat-related mortality“. If the 95% confidence interval of the estimated heat-related mortality is entirely above zero, we speak of a significant number of deaths. For a detailed description of the modelling used and the sensitivity analyses conducted refer to the “Methods” eSupplement and (3).
Results
Heat-related deaths
Figure 1 shows the estimated number of heat-related deaths in Germany in the period 1992–2021. Between 2018 and 2020, heat-related deaths occurred in significant numbers for three consecutive years for the first time during the study period. The year 2018, in particular, is with an estimated number of about 8700 heat-related deaths similar in magnitude to the historical heat years 1994 and 2003 (each about 10 000 deaths). For the years 2019 and 2020, the model estimates approximately 6900 and 3700 deaths, respectively. The numbers of deaths are comparable to those in the years 2006, 2010 and 2015. For 2021, no significant heat-related increase in (all-cause) mortality was found. The estimated numbers of deaths and confidence intervals for the decade 2012–2021 are also summarized in the Table; the results for the entire period since 1992 are presented in the eTable.
Figure 1.
Open in a new tab
Estimated number of heat-related deaths in Germany in the period 1992–2021. Years with significant numbers of heat-related deaths (5% significance level) are highlighted in red. Years with marginally significant numbers of heat-related deaths (10% significance level) are highlighted in beige. In addition, the estimated numbers of heat-related deaths with 95% confidence intervals are listed in the Table and eTable.
Table. The estimated numbers of heat-related deaths with 95% confidence intervals for the period 2012–2021**.
Year
;
Estimated number of heat-related deaths [95% confidence interval]
;
;
2012 ;
1000 [–1100; 3200] ;
2013
;
3000 [1100; 5100]
;
2014 ;
1000 [–1100; 2900] ;
2015
;
6000 [3900; 8200]
;
2016 ;
1800 [–600; 4 300] ;
2017 ;
1400 [–800; 3400] ;
2018
;
8700 [6700; 10 900]
;
2019
;
6900 [4600; 9300]
;
2020
;
3700 [1 400; 5600]
;
2021 ;
1700 [–700; 4300] ;
Open in a new tab
*Values in bold are statistically significant.
Figure 2 shows the development of mortality over time (deaths per 100 000 population) in the period 2018–2021. Between 2018 and 2020, in particular, both the modelled and the observed all-cause mortality was significantly higher than the modelled background mortality.
Figure 2.
Open in a new tab
Mortality over time (deaths per 100 000 population) in the period 2018–2021. The gray line shows the reported all-cause mortality, the red line shows the mortality estimated by the model (only in the summer half-year) and the blue line shows the estimated background mortality (expected mortality without heat). Weeks with weekly mean temperatures (averaged across all federal states) above 20 °C are highlighted in yellow. The slightly increased all-cause mortality in spring 2020 and the significantly increased all-cause mortality in winter 2020/21 are explained by the first and second wave of the COVID-19 pandemic. A regional breakdown of the time series can be found in eFigure 1.
The eFigures 1 and 2 show a more detailed breakdown of mortality rates over time by the three regions (North, Central, South) and a comparison of heat-related mortality by region and age group. In line with previous findings (3, 9, 15), there is a clear indication that the group aged 85 years and over is the most affected in all regions. The heat periods in the years 2018 and 2020 were shorter in the northern region, but still associated with a high number of heat-related deaths.
eFigure 1.
Open in a new tab
The time series of mortality (death per 100 000 population) for the period 2018–2021, stratified by the northern, central and southern regions. The gray line shows the reported all-cause mortality, the red line shows the mortality estimated by the model (only in the summer half-year) and the blue line shows the estimated background mortality. Weeks with weekly mean temperatures (averaged across all federal states) above 20°C are highlighted in yellow. In the years 2018 to 2020, a shorter duration of the heat periods is noted in the northern region. The increased mortality in spring 2020 in the southern region is explained by the first wave of the COVID-19 pandemic. The high mortality rates due to the second wave of the COVID-19 pandemic in the 2020/2021 winter were drawn beyond the limits of the y-axis to avoid distorting the depiction of the summer mortality.
eFigure 2.
Open in a new tab
The heat-related mortality (deaths per 100 000 population) in the period 2018–2021, stratified by region and age group. Despite the shorter duration of the heat periods (efigure 1) in the northern region, the heat-related mortality in the oldest age group in this region is comparable to the central and southern region mortality rates.
Figure 3 shows the shapes of the exposure-response curves of the current week and the previous week for the age group over 85 years in the three regions (North, Central and South) in the period 2012–2012. It can be seen here that the temperature threshold at which the effect of heat on mortality can be considered relevant is somewhat lower in the northern region (19.7 °C) compared to the central region (20.2 °C) and southern region (20.8 °C). Moreover, in the northern region the exposure-response curves of the current week and the previous week show a considerably steeper rise for temperatures above the threshold. Thus, an effect of heat on mortality, which increases from the southern to the northern regions, is noted. Consequently, the expected number of heat-related deaths (per 100 000 population of the same age group) for a specific weekly mean temperature is somewhat higher in the northern region and somewhat lower in the southern region compared to the center of Germany.
Figure 3.
Open in a new tab
Exposure-response curves of the current week (dotted line) and the previous week (solid line) for the 85+ age group in the period 2012–2012, stratified by the three regions “North“, “Central“ and “South“. In each case, the minimum of the exposure-response curve of the previous week is highlighted with a black “x” and marks the temperature threshold above which both the temperature of the previous week and the temperature of the current week result in an increase in mortality. Temperature ranges above the threshold are highlighted in gray. The temperature threshold increases from north to south.
Changes in the estimation of the exposure-response curves
Figure 4 shows the exposure-response curves for the age group 85 years by geographical region and decade. Overall, a significant increase in mortality is observed for weekly mean temperatures above 20 °C. Over the decades, a slight flattening of the curves can be observed, especially in the central region, i.e. in the period 2012–2021 the same weekly mean temperature resulted in a weaker increase in mortality compared to, for example, the period 1992–2001. A summary of the exposure-response curves for the various regions and age groups is provided in the “Analysis” eSupplement.
Figure 4.
Open in a new tab
The trend of the exposure-response curves for the three regions “North“, “Central“ and “South“ over the decades. The results for the 85+ age group are depicted because the strongest effects are observed in this age group. The three decades 1992 to 2001 (red), 2002 to 2011 (blue) and 2012 to 2021 (green) show a slightly declining trend which is particularly evident in the central region. Since in the northern region weekly mean temperatures above 25 °C occur significantly less frequently, the estimates in this area are associated with greater uncertainty, a fact that is reflected in the wider confidence intervals.
Special features of the years 2018–2020 and the effect of heat period duration
Figure 2 and eFigure 1 show that the model can generally provide a good representation of mortality over time. However, mortality during the heat periods 2018 and 2020 is slightly underestimated, while it is slightly overestimated in 2019. This may be explained by differences in the character of the heat waves in these three years.
In all three regions, the year 2018 was characterized by an unusually long heat period (up to nine weeks in the southern region and up to five weeks in the northern and central regions). In addition, remarkably high weekly mean temperatures were measured (up to 26.6 °C in the central and southern regions; up to 25.1 °C in the northern region). Although very high temperatures were also measured in 2019 (maximum weekly mean temperatures of 25.8 °C in the central region, 25.7 °C in the southern region and 25 °C in the northern region), these heat periods were repeatedly interrupted by weeks with lower temperatures. Finally, in the year 2020 again a prolonged period of heat (up to five weeks in the central and southern regions, up to three weeks in the northern region) was observed; however, the maximum weekly mean temperature was significantly lower compared to the year 2018 (maximum weekly mean temperature of 24.9 °C).
The effect of explicitly including heat period duration in the model was assessed; however, taking this parameter into account did not result in a relevant improvement of the description of the observed data. A detailed summary of key temperature figures during the study period is provided in the “Data” eSupplement.
Discussion
In each of the years from 2018 to 2020, the number of heat weeks was higher compared to the numbers in the other years of the 2012–2021 decade. The year 2018 particularly stands out, as not only did above-average periods of prolonged heat occur, but, in addition, exceptionally high temperatures were measured. However, significant differences in the duration and number of heat periods are observed between the regions (see also the “Data” eSupplement). In the period 2018–2020, heat-related mortality was also found to be considerably above the rates of the other years of the decade. In the year 2018, the estimated number of heat-related deaths was comparable to those in the historical heat years 1994 and 2003. However, a direct comparison of mortality rates in the various weeks shows that despite comparable temperatures fewer deaths occurred in 2018 compared to 1994 and 2003 (“Analysis” eSupplement). In 2021, only sporadic heat weeks were observed which did not result in a significant increase in all-cause mortality.
Impact of the period 2018–2020 on the total decade
Since the exposure-response curves are estimated per decade, the inclusion of the comparably hot years 2018–2020 necessitated a re-estimation of the exposure-response curves for the decade 2012–2021, which showed a steeper rise compared to the model based on the data up to 2017 (3). This implies that the estimated number of heat-related deaths for this decade also needs to be revised slightly upward. The updated estimates are within the 95% confidence intervals of the previous estimation (see “Analysis” eSupplement).
Duration of heat periods
By taking the duration of heat periods into account, only minor improvements in model fit were obtained and no significant changes in the estimates of heat-related deaths were noted. A possible explanation could be that calendar weeks as a unit are not fine enough to fully capture the time course of a prolonged heat period. In particular, an alternation between hot and cooler days within a week and the magnitude of cooling at night cannot be clearly differentiated based on weekly figures; for example, with the use of weekly data the duration of a heat period tends to be overestimated (“Data” eSupplement). The analysis of daily mortality data could help to identify an optimum time unit.
Finally, phenomena other than temperature could also play a role, such as the occurrence and concentration of air pollutants, humidity and the position of a heat period in the calendar year (25). For example, in (26) it was shown that mortality during the first days of the heat waves in 2003 and 2015 differed significantly despite comparable temperature curves. These differences may be explained by the considerably higher humidity during the 2015 heat wave.
Comparison with other models
Some federal states, such as Hesse (10), Baden-Wuerttemberg (11), Berlin, and Brandenburg (27), publish estimates of the number of heat-related deaths on a regular basis. In these models, background mortality is calculated using the mean mortality rates of the previous years excluding periods with known heat events. The advantage of these models over the modelling approach used in our study is their ease of use, as they do not require any specialized statistical software. However, the challenge with these models is that, with extreme heat events occurring in increasing frequency, increasingly longer periods of time must be excluded, thereby potentially confounding the estimated background mortality. Furthermore, the exposure-response relationship cannot be directly quantified, so temperature thresholds and adjustment processes must be described in some other way.
In addition, the topic of heat-related mortality is increasingly becoming the focus of international studies. In 2020, for example, the indicator “heat-related mortality“ was included in the Lancet Countdown on Health and Climate Change. An estimated 296 000 heat deaths occurred worldwide in 2018, of which 20 000 were estimated to have occurred. in Germany alone (6). However, this estimate is based on the assumption of a globally uniform exposure-response curve, and seasonal fluctuations in mortality were only broadly taken into account. While this simplified approach allows to estimate heat-related mortality on a global scale, it may lead to considerable overestimation or underestimation in some countries (with regard to the significance of regional differences, see also [28]).
Adaption to heat periods in Germany
The development of the exposure-response curves over the decades, as shown in Figure 4, reveals that in general the effects of the same weekly mean temperatures on mortality were weaker in the decade 2012–2021 compared to, for example, the decade 1992–2001. This may be interpreted as an indication that some adjustment to recurrent heat periods has taken place in the population.
The data analyzed by us do not allow to draw conclusions about what caused this limited adjustment. Possible explanations include individual behavioral changes due to greater awareness, such as wearing light clothing, adequate hydration and moving to shaded or air-conditioned areas (29). For example, information about heat events is also made available by the Heat Health Warning System (HHWS) of the German Weather Service (30).
Since the elderly and those with preexisting conditions are affected most, the topic of heat prevention continues to be a focus in the health and care sectors, based on initial implementation experiences (2). When initiating adaptation strategies at the community level, coordination and interdisciplinary interaction is essential (31, 32). To this end, the 2020 Conference of Health Ministers emphasized the need for heat-health action plans (“Hitzeaktionsplan”) in its relevant resolution, noting that these should be prepared by 2025 (33).
Outlook
Numerous studies suggest that the frequency of extreme heat events with, at times, dramatic effects on human health is likely to increase in Germany as a result of climate change (4, 20, 34– 38). The study of heat-related mortality makes a significant contribution to the evaluation of health risks. Our updated analysis reveals for the first time significant numbers of heat-related death in three consecutive years, highlighting the fact that heat events continue to be a serious threat to the health of the population in Germany. There is still an ongoing need and challenge to significantly improve the handling of heat periods in Germany and to adequately protect vulnerable groups of the population.
eTable. The estimated numbers of heat-related deaths with 95% confidence intervals for the period 1992–2021*.
Year
;
Estimated number of heat-related deaths [95% confidence interval]
;
;
1992
;
2800 [600; 5000]
;
1993 ;
0 [–2600; 2 100] ;
1994
;
10 100 [8 100; 12 400]
;
1995
;
2800 [800; 4700]
;
1996 ;
300 [–1900; 2200] ;
1997 ;
2100 [0; 4100] ;
1998 ;
600 [–1900; 2800] ;
1999 ;
900 [–1000; 3200] ;
2000 ;
400 [–1700; 2400] ;
2001
;
2700 [800; 4600]
;
2002 ;
1300 [–1000; 3200] ;
2003
;
9500 [7200; 12 000]
;
2004 ;
1300 [–800; 3200] ;
2005 ;
1400 [–900; 3600] ;
2006
;
7500 [5400; 9500]
;
2007 ;
500 [–1600; 2500] ;
2008 ;
900 [–1100; 3100] ;
2009 ;
500 [–1600; 2400] ;
2010
;
4500 [2300; 6300]
;
2011 ;
100 [–1900; 2300] ;
2012 ;
1000 [–1100; 3200] ;
2013
;
3000 [1100; 5100]
;
2014 ;
1000 [–1100; 2900] ;
2015
;
6000 [3900; 8200]
;
2016 ;
1800 [–600; 4300] ;
2017 ;
1400 [–800; 3400] ;
2018
;
8700 [6700; 10 900]
;
2019
;
6900 [4600; 9300]
;
2020
;
3700 [1400; 5600]
;
2021 ;
1700 [–700; 4300] ;
Open in a new tab
*Values in bold are statistically significant.
Acknowledgments
Translated from the original German by Ralf Thoene, MD.
Footnotes
Conflict of interest
The authors declare no conflict of interest.
Funding
This study was developed as part of the project “DAS: Advancement and Harmonization of the Indicator for Heat-related Excess Mortality in Germany” (funding code 3720 48 203 1) and funded by the German Environment Agency, Nature Conservation, Nuclear Safety and Consumer Protection (BMUV, Bundesministeriums für Umwelt, Naturschutz, nukleare Sicherheit und Verbraucherschutz) and carried out on behalf of the German Federal Environment Agency (UBA, Umweltbundesamt).
References
1.Bunker A, Wildenhain J, Vandenbergh A, et al. Effects of air temperature on climate-sensitive mortality and morbidity outcomes in the elderly; a systematic review and meta-analysis of epidemiological evidence. EBioMedicine. 2016;6:258–268. doi: 10.1016/j.ebiom.2016.02.034. [DOI] [PMC free article] [PubMed] [Google Scholar]
2.Herrmann A, Haefeli WE, Lindemann U, Rapp K, Roigk P, Becker C. Epidemiology and prevention of heat-related adverse health effects on elderly people. Z Gerontol Geriatr. 2019;52:487–502. doi: 10.1007/s00391-019-01594-4. [DOI] [PubMed] [Google Scholar]
3.an der Heiden M, Muthers S, Niemann H, Buchholz U, Grabenhenrich L, Matzarakis A. Heat-related mortality: an analysis of the impact of heatwaves in Germany between 1992 and 2017. Dtsch Arztebl Int. 2020;117:603–609. doi: 10.3238/arztebl.2020.0603. [DOI] [PMC free article] [PubMed] [Google Scholar]
4.Eis D, Helm D, Laußmann D, Stark K. Klimawandel und Gesundheit. Ein Sachstandsbericht. DAZ. 2008;148:66–71. [Google Scholar]
5.Gasparrini A, Armstrong B. The impact of heat waves on mortality. Epidemiology. 2011;22:68–73. doi: 10.1097/EDE.0b013e3181fdcd99. [DOI] [PMC free article] [PubMed] [Google Scholar]
6.Watts N, Amann M, Arnell N, et al. The 2020 report of The Lancet Countdown on health and climate change: responding to converging crises. Lancet. 2021;397:129–170. doi: 10.1016/S0140-6736(20)32290-X. [DOI] [PMC free article] [PubMed] [Google Scholar]
7.Breitner S, Wolf K, Peters A, Schneider A. Short-term effects of air temperature on cause-specific cardiovascular mortality in Bavaria, Germany. Heart. 2014;100:1272–1280. doi: 10.1136/heartjnl-2014-305578. [DOI] [PubMed] [Google Scholar]
8.Rai M, Breitner S, Wolf K, Peters A, Schneider A, Chen K. Impact of climate and population change on temperature-related mortality burden in Bavaria, Germany. Environ Res Lett. 2019 [Google Scholar]
9.an der Heiden M, Buchholz U, Uphoff H. Schätzung der Zahl hitzebedingter Sterbefälle und Betrachtung der Exzess-Mortalität; Berlin und Hessen, Sommer 2018. Epid Bull. 2019;23:193–197. [Google Scholar]
10.Siebert H, Uphoff H, Grewe HA. Monitoring heat-related mortality in Hesse. Bundesgesundheitsblatt - Gesundheitsforschung - Gesundheitsschutz. 2019;62:580–588. doi: 10.1007/s00103-019-02941-x. [DOI] [PubMed] [Google Scholar]
11.Statistisches Landesamt Baden-Württemberg. Baden-Württemberg: Annähernd 1700?»Hitzetote« im Sommer 2019. www.statistik-bw.de/Presse/Pressemitteilungen/2020171 (last accessed on 12 May 2022) 2020 [Google Scholar]
12.Huber V, Krummenauer L, Peña-Ortiz C, et al. Temperature-related excess mortality in German cities at 2 °C and higher degrees of global warming. Environ Res. 2020;186 doi: 10.1016/j.envres.2020.109447. 109447. [DOI] [PubMed] [Google Scholar]
13.Zacharias S, Koppe C, Mücke HG. Climate change effects on heat waves and future heat wave-associated IHD mortality in Germany. Climate. 2015;3:100–117. [Google Scholar]
14.Zacharias S, Koppe C, Mücke HG. Influence of heat waves on ischemic heart diseases in Germany. Climate. 2014;2:133–152. [Google Scholar]
15.an der Heiden M, Muthers S, Niemann H, Buchholz U, Grabenhenrich L, Matzarakis A. Estimation of heat-related deaths in Germany between 2001 and 2015. Bundesgesundheitsblatt - Gesundheitsforschung - Gesundheitsschutz. 2019:571–579. doi: 10.1007/s00103-019-02932-y. [DOI] [PubMed] [Google Scholar]
16.Karlsson M, Ziebarth N. Population health effects and health-related costs of extreme temperatures: comprehensive evidence from Germany. J Environ Econ Manage. 2018;91:93–117. [Google Scholar]
17.Havenith G. Heidelberg: Springer. Berlin: 2005. Temperature regulation, heat balance and climatic stress In: Extreme weather events and public health responses; pp. 69–80. [Google Scholar]
18.Keatinge WR, Coleshaw SRK, Easton JC, Cotter F, Mattock MB, Chelliah R. Increased platelet and red cell counts, blood viscosity, and plasma cholesterol levels during heat stress, and mortality from coronary and cerebral thrombosis. Am J Med. 1986;81:795–800. doi: 10.1016/0002-9343(86)90348-7. [DOI] [PubMed] [Google Scholar]
19.Michelozzi P, Accetta G, De Sario M, et al. High temperature and hospitalizations for cardiovascular and respiratory causes in 12 European cities. Am J Respir Crit Care Med. 2009;179:383–389. doi: 10.1164/rccm.200802-217OC. [DOI] [PubMed] [Google Scholar]
20.Schlegel I, Muthers S, Matzarakis A. Einfluss des Klimawandels auf die Morbidität und Mortalität von Atemwegserkrankungen. www.umweltbundesamt.de/en/publikationen/einfluss-des-klimawandels-auf-die-morbiditaet (last accessed on 12 May 2022) 2021 [Google Scholar]
21.Wood SN. Generalized additive models: An introduction with R. Second edition. New York: Chapman and Hall/CRC. 2006 [Google Scholar]
22.Statistisches Bundesamt (DESTATIS) Sonderauswertung Sterbefälle. www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.html. (last accessed on 12 May 2022) 2019 [Google Scholar]
23.Statistisches Bundesamt (DESTATIS) Bevölkerung im Wandel. Annahmen und Ergebnisse der 14. koordinierten Bevölkerungsvorausberechnung. www.destatis.de/DE/Presse/Pressekonferenzen/2019/Bevoelkerung/pressebroschuere-bevoelkerung.pdf?__blob=publicationFile (last accessed on 12 May 2022) 2017 [Google Scholar]
24.R Core Team. www.r-project.org/ (last accessed on 12 May 2022) Vienna, Austria: 2020. R: A language and environment for statistical computing. [Google Scholar]
25.Ragettli MS, Röösli M. Gesundheitliche Auswirkungen von Hitze in der Schweiz und die Bedeutung von Präventionsmassnahmen Schweizerisches Tropen- und Public Health-Institut: Schlussbericht Juli. www.nccs.admin.ch/dam/nccs/de/dokumente/website/sektoren/gesundheit/swisstph-2020-gesundheitliche-auswirkungen-von-hitze-2019-vergleich.pdf.download.pdf/SwissTPH_2020_Gesundheitliche Auswirkungen von Hitze_2019_Vergleich 2003-2015-2018_def.pdf (last accessed on 12 May 2022) [Google Scholar]
26.Muthers S, Laschewski G, Matzarakis A. The summers 2003 and 2015 in South-West Germany: heat waves and heat-related mortality in the context of climate change. Atmosphere (Basel) 2017;8 [Google Scholar]
27.Axnick M. Hitzebedingte Sterblichkeit in Berlin und Brandenburg. Zeitschrift für amtliche Stat Berlin Brand. 2021:34–39. [Google Scholar]
28.Vicedo-Cabrera AM, Sera F, Gasparrini A. Hands-on tutorial on a modeling framework for projections of climate change impacts on health. Epidemiology. 2019;30:321–329. doi: 10.1097/EDE.0000000000000982. [DOI] [PMC free article] [PubMed] [Google Scholar]
29.Gosling SN, Hondula DM, Bunker A, et al. Adaptation to climate change: a comparative analysis of modeling methods for heat-related mortality. Environ Health Perspect. 2017;125:1–14. doi: 10.1289/EHP634. [DOI] [PMC free article] [PubMed] [Google Scholar]
30.Matzarakis A, Laschewski G, Muthers S. The heat healthwarning system in Germany—application and warnings for 2005 to 2019. Atmosphere (Basel) 2020;11:1–13. [Google Scholar]
31.Kaiser T, Kind C, Dudda L, Sander K. Klimawandel, Hitze und Gesundheit: Stand der gesundheitlichen Hitzevorsorge in Deutschland und Unterstützungsbedarf der Bundesländer und Kommunen Climate change, heat and health: status of heat prevention in Germany and need for support of federal states. UMID - Umwelt + Mensch Informationsdienst 01/2021. :27–37. [Google Scholar]
32.Blättner B, Janson D, Grewe HA. Heat-health action plans in the parliaments of the German federal states: political discourses on health protection and climate change. Prävention und Gesundheitsforderung. 2020;15:296–302. [Google Scholar]
33.Gesundheitsministerkonferenz. TOP: 5.1 Der Klimawandel - eine Herausforderung für das deutsche Gesundheitswesen. www.berlin.de/sen/archiv/gpg-2016-2021/2020/pressemitteilung.998587.php (last accessed on 12 May 2022) 2020 [Google Scholar]
34.Christidis N, Jones G, Stott P. Dramatically increasing chance of extremely hot summers since the 2003 European heatwave. Nat Clim Chang. 2015;5:46–50. [Google Scholar]
35.Deutschländer T, Mächel H. Temperatur inklusive Hitzewellen. In: Klimawandel in Deutschland Berlin, Heidelberg: Springer Spektrum. 2017:47–56. [Google Scholar]
36.Kahlenborn W, Porst L, Voß M, et al. Klimawirkungs- und Risikoanalyse 2021 für Deutschland. www.umweltbundesamt.de/publikationen/KWRA-Zusammenfassung (last accessed on 12 May 2022) 2021 [Google Scholar]
37.Vicedo-Cabrera AM, Scovronick N, Sera F, et al. The burden of heat-related mortality attributable to recent human-induced climate change. Nat Clim Chang. 2021;11:492–500. doi: 10.1038/s41558-021-01058-x. [DOI] [PMC free article] [PubMed] [Google Scholar]
38.Mücke HG, Litvinovitch J. Heat extremes, public health impacts, and adaptation policy in Germany. Int J Environ Res Public Health. 2020;17 doi: 10.3390/ijerph17217862. [DOI] [PMC free article] [PubMed] [Google Scholar]
Articles from Deutsches Ärzteblatt International are provided here courtesy of Deutscher Arzte-Verlag GmbH
