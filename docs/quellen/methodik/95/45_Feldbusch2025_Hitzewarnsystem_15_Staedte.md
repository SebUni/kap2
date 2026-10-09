                                                                  Environment International 203 (2025) 109746


                                                                   Contents lists available at ScienceDirect


                                                               Environment International
                                                          journal homepage: www.elsevier.com/locate/envint


Full length article

Assessing the effectiveness of the heat health warning system in preventing
mortality in 15 German cities: A difference-in-differences approach
Hanna Feldbusch a,b,c,* , Alexandra Schneider c , Franziska Matthies-Wiesler c,d ,
Andreas Matzarakis e,f , Annette Peters b,c,g, Susanne Breitner-Busch a,c,1, Veronika Huber a,c,1
a
  Institute for Medical Information Processing, Biometry, and Epidemiology (IBE), Faculty of Medicine, LMU Munich, Marchioninistraße 15, 81377 München, Germany
b
  Pettenkofer School of Public Health, Munich, Germany
c
  Institute of Epidemiology, Helmholtz Zentrum München, German Research Center for Environmental Health, Ingolstädter Landstraße 1, 85764 Neuherberg, Germany
d
  German Alliance on Climate Change and Health (KLUG), Berlin, Germany
e
  Chair of Environmental Meteorology, Institute of Earth and Environmental Sciences, University of Freiburg DE-79085 Freiburg, Germany
f
  Democritus University of Thrace, GR-69100 Komotini, Greece
g
  German Centre for Cardiovascular Research (DZHK), Partner Site Munich Heart Alliance, Munich, Germany




A R T I C L E I N F O                                     A B S T R A C T

Handling Editor: Adrian Covaci                            Background: Heatwaves pose significant risks to human health. Implementing heat health warning systems
                                                          (HHWS) has been widely adopted as a preventive measure. However, the effectiveness of the German HHWS in
Keywords:                                                 reducing mortality during heat episodes across different cities has scarcely been researched.
Extreme heat                                              Objective: This study aimed to assess the effect of HHWS on mortality during heat episodes in 15 major cities in
Heat health warning system
                                                          Germany and explore city-specific factors influencing the effectiveness of heat alerts.
Heat alerts
                                                          Methods: Daily all-cause mortality data during the warm-season months (May to September) from 1993 to 2020
Mortality
Quasi-experimental methods                                were linked with heat alert data and meteorological information. A difference-in-differences approach was
Germany                                                   employed to estimate the city-specific effects of heat alerts on mortality. In the second stage, meta-regression
                                                          models were used to pool the city-specific estimates and examine the heterogeneity across cities.
                                                          Results: Substantial variation in the city-specific associations was observed, with some cities exhibiting significant
                                                          reductions in mortality during heat episodes after the HHWS implementation while others showed no significant
                                                          effect. The pooled relative risk (RR) from the second-stage analysis, based on the meta-variables averaged across
                                                          all cities studied, suggested no overall significant protective effect of heat alerts on mortality (RR = 1.00, 95 %
                                                          CI: 0.98 to 1.01). However, when controlling for the meta-variables recreational area per person, total population,
                                                          and population density, we found a significant but small protective effect of heat alerts across all cities studied (RR
                                                          = 0.85, 95 % CI: 0.75 to 0.97).
                                                          Conclusion: According to our results, the effectiveness of heat alerts varied considerably across the cities, sug­
                                                          gesting the importance of considering city-specific factors, such as population size, population density, and the
                                                          presence of blue and green urban infrastructure. Understanding these factors can help improve the effectiveness
                                                          of HHWS and tailor interventions to address the specific characteristics of different urban areas within heat-
                                                          health action plans.




1. Introduction                                                                                Kirkpatrick and Lewis 2020; Romanello et al. 2022). Exposure to
                                                                                               extreme heat and the associated heat stress can cause adverse effects on
    Heatwaves constitute a growing public health concern in the context                        human health and increase morbidity and mortality (Ebi et al. 2021).
of climate change, as they are globally increasing in intensity, frequency,                    Risk groups include young children, adults older than 65 years, people
and duration (Hess et al. 2023; Mücke and Litvinovitch 2020; Perkins-                          with pre-existing cardiopulmonary and other chronic diseases, as well as



 * Corresponding author at: Institute of Epidemiology, Helmholtz Zentrum München, German Research Center for Environmental Health, Ingolstädter Landstraße 1,
85764 Neuherberg, Germany.
    E-mail address: hanna.feldbusch@helmholtz-munich.de (H. Feldbusch).
  1
    Shared last authorship.

https://doi.org/10.1016/j.envint.2025.109746
Received 27 February 2025; Received in revised form 21 June 2025; Accepted 21 August 2025
Available online 23 August 2025
0160-4120/© 2025 The Author(s). Published by Elsevier Ltd. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/).
H. Feldbusch et al.                                                                                                     Environment International 203 (2025) 109746


outdoor workers (An der Heiden et al. 2020; Basagaña et al. 2011; Ebi            2020). A smartphone application was introduced in 2012/2013, as the
et al. 2021; Sheffield et al. 2018). The extreme heatwave 2003 was                general weather app (Warnwetterapp) of the German Weather Service.
associated with more than 70,000 premature deaths across 12 European              A more specific application focusing on potentially adverse health im­
countries (Robine et al. 2008). It highlighted the impact of extreme heat         pacts (named “Gesundheitswetterapp”) followed in 2020. The heat
on mortality and the need for public health interventions to mitigate             warnings are also included in the Emergency Information and Warning
heat-related adverse health effects (Mücke and Litvinovitch 2020;                 App (NINA) of the Federal Office of Civil Protection and Disaster
Robine et al. 2008; Toloo et al. 2013). In Germany, the highest amount            Assistance. More information about the updated German HHWS can be
of heat-related deaths for the last three decades occurred in 1994, with          found elsewhere (Matzarakis et al. 2020).
10,100 (95 % CI: 8,100 to 12,400) heat-related deaths, followed by                     For Germany there is a harmonized guidance for the implementation
2003, with 9,500 deaths (95 % CI: 7,200 to 12,000) (Winklmayr et al.              of HHAPs since 2017 (Federal Ministry for the Environment Nature
2022). In the summer of 2022, one of the hottest seasons on record in             Conservation Building and Nuclear Safety 2017) and a national heat
Europe, Germany recorded one of the highest summer heat-related                   protection plan issued by the Federal Ministry of Health since 2023
mortality numbers, with an estimated 8,173 heat-related deaths (95 %              (Federal Ministry of Health 2023). Even though Germany has a imple­
CI: 5,374 to 11,018) (Ballester et al. 2023). Huber et al. (2024) estimated       mented and updated HHWS, which could be used in HHAPs as already
heat-related deaths in Germany for the summer of 2022 at 9,100 (95 %              existing system (Matthies et al. 2008), HHAPs or public health actions
CI: 7,300 to 10,700), using daily mortality and temperature data,                 following heat alerts are still not systematically and comprehensively
whereas previous studies of the Robert Koch Institute (RKI) estimated             implemented across federal states, municipalities and cities (Janson
the heat-related excess mortality at 4,500, using data on a weekly basis          et al. 2023; Kaiser et al. 2021; Matthies-Wiesler et al. 2021). Due to the
(Winklmayr and an der Heiden 2022).                                               scarcity of comprehensive data on implemented HHAPs or public health
    As a result of the 2003 heatwave, the World Health Organization               actions following heat alerts, our study explicitly accounts for the HHWS
(WHO) Regional Office for Europe introduced a guidance on heat-health             only.
action plans (HHAP) in 2008 in order to protect human health from                      Urban populations are especially exposed to heat due to the urban
adverse heat affects through a portfolio of prevention and protection             heat island (UHI) effect, which represents the temperature difference
measures at different levels (Matthies et al. 2008). One key component            (sometimes up to 10 ◦ C) between an urban area and the surrounding
of a HHAP is an accurate and timely heat health warning system                    rural areas (Hannemann et al. 2023; Menberg et al. 2013). In Germany,
(HHWS). Based on meteorological forecasts, a HHWS serves as tool to               up to 68.1 % of the population lives in urban areas (Taubenböck et al.
alert the public about temperature conditions that pose a risk to health.         2022), and the degree of urbanization is expected to increase further in
Consequently, the HHAP lead body and stakeholders shall be informed               the coming decades (United Nations (UN) 2018). During extreme heat
by the HHWS to trigger response actions according to the warning level            events, the local UHI effect is superimposed on the regional temperature,
as defined in the HHAP (Matthies et al. 2008; WHO Regional Office for             increasing the severity of the extreme event (Gabriel and Endlicher
Europe 2021). By 2019, 16 European HHWS had been reviewed (Basarin                2011). In addition, UHI can affect the association between high tem­
et al. 2020; Casanueva et al. 2019; Matzarakis et al. 2020). The HHWS in          peratures and mortality (Cuerdo-Vilches et al. 2023; Goggins et al.
Germany was developed by the German Weather Service (Deutscher                    2012). It is, therefore, of particular interest to investigate the protective
Wetterdienst, DWD) and implemented in 2005 (Matzarakis 2016; Mat­                 effect of HHWS on mortality during heat episodes in urban populations
zarakis et al. 2020).                                                             (Gabriel and Endlicher 2011).
    To assess the human thermal stress, the DWD calculates the thermal                 Despite implementing the HHWS and other measures to protect
index perceived temperature (PT) based on the numerical weather                   human health from heat, high temperatures in the warm-season months
forecast, using a standardized “Klima-Michel” or “Klima-Michel Senior”,           still take their toll on human health and mortality. Therefore, it is
for elderly people, to model all mechanisms of energy exchange between            essential to evaluate the effectiveness of the HHWS on mortality during
human body and thermal environment. Short-term heat acclimatization               heat episodes and to identify socioeconomic and environmental factors
is considered by adjusting the thermal stress thresholds through stored           that might modify the effect. While some previous studies examined the
PT values of the past 30 days (Casanueva et al. 2019; Matzarakis et al.           association between HHWS (Heudorf and Schade 2014; Morabito et al.
2020). Since 2007, the HHWS was extended to include a building                    2012; Toloo et al. 2013) or HHAPs (de’Donato et al. 2018; Fouillet et al.
simulation model to estimate the nocturnal indoor thermal conditions,             2008; Heudorf and Schade 2014) and mortality, mainly by pre-post
as most people spent the night indoors (Pfafferott and Becker 2008). For          analyses, very few studies used a quasi-experimental design to esti­
cities with more than 100,000 inhabitants an urban heat island effect             mate the effect of HHWS or HHAPs on mortality. A quasi-experimental
(UHI) was added to the meteorological forecast to represent the                   method already applied in this context is the difference-in-differences
nocturnal conditions of urban areas more precise (Matzarakis et al.               (DID) approach. The results of studies using a DID approach range
2020). The automatically generated warning proposals are published                from protective effects to no detectable effect of heat alerts or HHAPs on
only with the confirmation and with possible adjustments of a bio­                mortality in Canadian and US cities (Benmarhnia et al. 2016; Wein­
meteorologist. The heat health warnings for German counties are                   berger et al. 2018; Wu et al. 2023). In particular, HHAPs appear to have
directed at governmental authorities, ministries of the federal states,           a greater protective impact for specific subgroups, such as people 65
nursing homes, and the general public. The heat alerts are disseminated           years and older (Benmarhnia et al. 2016). Varying effects were also
electronically via the internet, subscription newsletters, smartphone             evident at the city level (Weinberger et al. 2018). To the best of our
applications, and On the DWD website (https://www.dwd.de), heat                   knowledge, no such studies exist for Germany or any other European
alerts are displayed in maps linked to explanatory text. This text pro­           country.
vides information on the expected intensity of heat stress, the affected               To address this research gap (Heudorf and Schade 2014), we used a
altitude range, additional details for the elderly and urban areas when           DID approach combined with random forest classification to assess the
relevant, and recommendations for health-protective behavior. This                effects of heat alerts on all-cause mortality in Germany’s 15 most
textual information is also part of all mentioned dissemination ways.             populated cities. Our specific aims were (i) to examine whether the city-
The warning also provides information on the duration (number of days)            specific DID estimators suggest a protective effect of heat alerts on
the heat alert has been active. Additionally, mass media (radio and               mortality during heat episodes in the respective city, and (ii) to pool the
television) can broadcast the warning, making it more widely known to             city-specific effects and examine potential heterogeneity between the
the public. This usually prompts conventional and electronic print                city-specific estimators based on city-specific socioeconomic and envi­
media to publish further reports and offer advice on how to protect one’s         ronmental characteristics as well as the presence of geographical
own health as well as that of others in need of care (Matzarakis et al.           dependencies.

                                                                              2
H. Feldbusch et al.                                                                                                      Environment International 203 (2025) 109746


2. Materials and methods                                                            forecast, and days were classified as non-eligible if no heat alert forecast
                                                                                    was issued on this day. For the classification of eligible and non-eligible
2.1. Data sources                                                                   days before the implementation of the HHWS (1993–2004), we imple­
                                                                                    mented a random forest classification algorithm, based on observed
2.1.1. Mortality data                                                               meteorological data. Based on a set of meteorological variables, the al­
   We used the daily counts of all-cause deaths from the Research Data              gorithm identified eligible (hot) days on which heat alerts would have
Centres of the German Statistical Offices for the 15 largest German cities          most likely been issued if the HHWS had already been implemented at
between 1993 and 2020 (Berlin, Bremen, Cologne, Dortmund, Dresden,                  the time (for details, see Appendix A. Random forest classification and
Duisburg, Dusseldorf, Essen, Frankfurt am Main, Hamburg, Hannover,                  Fig. A.1). The effect of the heat alerts on the all-cause daily death count
Leipzig, Munich, Nuremberg, and Stuttgart). There were no missing                   per city was estimated as the difference in daily mortality between
values for the study period.                                                        eligible days and non-eligible days before the HHWS implementation
                                                                                    compared to the difference between eligible days and non-eligible days
2.1.2. Meteorological data                                                          after HHWS implementation. Therefore, the counterfactual quantity of
    We obtained daily observations of mean, minimum, and maximum                    interest was the difference in the daily death count between eligible days
air temperature (◦ C), mean relative humidity (%), and daily mean spe­              and non-eligible days that would have been observed during 2005–2020
cific humidity (gram of water vapor/ kilogram of humid air) for each                if the HHWS had not been implemented (Benmarhnia et al. 2016).
city measured at DWD stations from 1993 to 2020 (Deutscher Wetter­                       Key assumptions of the DID analysis are that i) the implementation of
dienst (DWD) 2023) (Table A.1). The thermal index perceived temper­                 the HHWS was the only intervention that might have caused a change in
ature (PT) is an important thermal index used in the German HHWS                    the association between heat and mortality before and after HHWS
(Matzarakis et al. 2020). As neither the PT data nor the exact PT                   implementation, and that ii) before the HHWS implementation, eligible
calculation models were available to us, we calculated the daily                    and non-eligible days have parallel trends in the outcome mortality. The
apparent temperature (Kalkstein and Valimont 1986; Steadman 1979)                   second assumption means that the trend in the mortality observed
for daily mean and maximum air temperature using an algorithm of                    during non-eligible days is a good approximation of the counterfactual
Lanzinger et al. (Lanzinger et al. 2016). We consider the apparent                  trend in the mortality, which would have been observed during eligible
temperature the best available approximation of PT. All meteorological              days without HHWS implementation (Abadie and Cattaneo 2018; Alari
variables utilized in the analyses, including the number of missing                 et al. 2021). The trends in pre-HHWS period are optimally parallel, but
values, are summarized in Table A.2 (Matzarakis et al. 2020).                       presumably not congruent, as the eligible days are expected to be hotter
                                                                                    with a subsequent more death attributable to heat than non-eligible
2.1.3. Heat alert data (2005–2020)                                                  days. To test the parallel trend assumption in the DID analyses, we
    Official heat alerts for each city were also obtained from the DWD for          plotted the daily mortality for eligible and non-eligible days during the
2005 to 2020 on daily basis. Except for Hannover (Hannover region) and              pre-HHWS and post-HHWS periods, including linear trendlines for each
Munich (city with a district), all districts in which the cities were located       group (Fig. A.2). If the lines appeared to be approximately parallel in the
were urban. The dataset included information on the district name, the              pre-HHWS period, we assumed the parallel trend assumption to be ful­
corresponding federal state, the date of the heat alert, and the warning            filled for the respective city (Wing et al. 2018). Subsequently, in the
level (1 = strong and 3 = extreme heat stress). As the thresholds for the           second-stage analyses, a distinction was made between all cities and the
warning levels were region-specific and took acclimatization into ac­               subset of cities appearing to fulfill the parallel trend assumption.
count, we only distinguished between days with and without heat alerts                   City-specific DID quasi-Poisson models with an offset (total number
(Casanueva et al. 2019; Deutscher Wetterdienst (DWD), 2021). No                     of inhabitants per year) were used to estimate the effect of heat alerts on
further distinction was made according to the warning level.                        daily all-cause death counts. Based on previous literature, the models
                                                                                    were adjusted for temporal patterns (day of the week, year, day of the
2.1.4. Metavariables (city-level characteristics)                                   year, and date), daily mean temperature, and relative humidity (Barreca
   We obtained annual records of ten socioeconomic variables from the               2012; Benmarhnia et al. 2016). We incorporated relative humidity as a
INKAR database for each city from 1995 to 2020 and five environmental               control variable instead of specific humidity (Davis et al. 2016) due to
variables per city from 2016 to 2020 (Bundesinstitut für Bau- Stadt- und            much fewer missing values and a weaker correlation with mean tem­
Raumforschung (BBSR) 2023) (for details, see Table A.3). For the years              perature compared to specific humidity (Fig. A.3). The formula for the
1993 and 1994, we extrapolated the following variables: total number of             DID main model per city is provided in Appendix A (formula DID main
inhabitants, the proportion of inhabitants aged 65 years and older (in              model).
%), and mean life expectancy of a newborn in years, based on the mean                    The DID estimate represents the adjusted interaction term between
change observed in the subsequent two years. Additionally, we included              the estimated effect of eligible versus non-eligible days, and the esti­
the German Index of Socioeconomic Deprivation (GISD) as a socioeco­                 mated effect of the pre-HHWS (1993–2004) versus post-HHWS
nomic variable, which is based on the three dimensions of occupation,               (2005–2020) period. To estimate non-parametric 95 % confidence in­
education, and income from the INKAR database (Michalski et al. 2022).              tervals (CI) and variance for the adjusted DID estimates, we employed
                                                                                    bootstrapping with 1000 samples (Carpenter and Bithell 2000). To
2.2. Study design and statistical analysis                                          provide a simplified interpretation of the results, we report the relative
                                                                                    risks (RR). A RR of less than one indicates a decrease in daily mortality
    We used an extended two-stage design for environmental research to              attributable to heat alerts, interpreted as evidence that due to alerts
firstly estimate the city-specific effects of heat alerts on all-cause mor­         people protect themselves or are protected adequately from heat. If the
tality during heat episodes by a DID approach and secondly pool these               HHWS is ineffective in reducing mortality during heat episodes, for
city-specific effects in a meta-regression (Sera and Gasparrini 2022).              example, by not reaching vulnerable people with heat alerts, the RR
                                                                                    would be greater than or equal to one.
2.2.1. Difference-in-differences approach (first-stage analyses)
    In the DID approach, all-cause mortality for the population of each             2.2.2. Meta-regression (second-stage analyses)
city was compared before and after HHWS implementation in 2005 on                      In the second stage, we used meta-regression models to pool the city-
so-called ‘eligible’ (hot) and ‘non-eligible’ (non-hot) days during the             specific DID estimates and to examine (part of) the observed heteroge­
warm season (May to September). After implementing the HHWS                         neity across the cities and potential geographical dependencies. In all
(2005–2020), eligible days corresponded to days with a heat alerts                  second-stage models, the city-specific DID estimators of the first-stage

                                                                                3
H. Feldbusch et al.                                                                                                         Environment International 203 (2025) 109746


analyses were used as outcome variables, and the models were fitted                  regression model was fitted without any adjustments (basic DID model).
using maximum likelihood estimation (MLE).                                           The second linear model included adjustments for temporal patterns,
    We compared four different meta-regression models (Model 0 to                    mean temperature, and relative humidity, similar to the main quasi-
Model 3). Model 0 was a basic meta-regression model with no predictors,              Poisson model.
only intercepts, and one random effect per city to account for potential                All analyses were conducted using R software (version 4.2.3). For
differences between the cities. Model 1 included two levels of random                second-stage analyses, the R package ‘mixmeta’ was used (Sera et al.
effects (cities nested within federal states) to examine the presence of             2019).
geographical dependencies, specifically whether cities within the same
federal state (Bundesland) exhibited more similarity than cities in                  3. Results
different federal states. Model 2 was a mixed-effect regression model,
adding fixed-effect meta-variables to model 0 to identify environmental              3.1. Descriptive statistics
and socioeconomic factors that possibly explain a quota of heterogeneity
by being associated with the effectiveness of heat alerts on mortality. We               During the study period from 1993 to 2020, a total of 1,731,269 all-
employed a stepwise procedure, guided by the Akaike information cri­                 cause deaths occurred in the warm-season months of May to
terion (AIC), to select the best set of 16 meta-variables. In the analyses           September. The average number of daily deaths was 26.9 for all cities,
described, the arithmetic mean of all given values in the study period per           ranging from a minimum of 3 deaths per day to a maximum of 266 deaths.
city was included for each of the 16 environmental and socioeconomic                 Munich had the lowest mean mortality rate (2.51 per 100,000 in­
(meta-) variables (for more detailed information, refer to Table A.4).               habitants) throughout the study period, while Essen had the highest
Model 3 was the same as Model 2, but with two levels of random effects               mortality rate, followed by Leipzig and Nuremberg (3.67, 3.41, and 3.21
(as in Model 1). We assessed heterogeneity in all four models using the              per 100,000 inhabitants). Within the study period, a percentage of 5.66 %
Cochrane Q Test of Heterogeneity. Considering that the variables pop­                eligible days (3,635 out of 64,260 days) occurred. The mean yearly
ulation and population density could be correlated (Figs. A4 and A.5), we            number of eligible days was higher in the post-HHWS period (144 days)
additionally examined the presence of multicollinearity by calculating               compared to the pre-HHWS period (112 days) (Table 1). Among the 15
the variance inflation factor (VIF) for models 2 and 3. The final second-            cities, Hamburg had the fewest number of eligible days (164 days), fol­
stage model was selected based on AIC and Bayesian information cri­                  lowed by Bremen (178 eligible days). In contrast, Stuttgart had the
terion (BIC).                                                                        highest number of eligible days (355 days), with Frankfurt having the
    The DID effect estimate pooled across cities (expressed as RR) was               second-highest number (334 eligible days). Among eligible and non-
the prediction from the final meta-regression model based on the aver­               eligible days, the arithmetic means and interquartile ranges of daily
ages of the selected meta-variables across cities. We also reported the              mean, maximum and minimum temperature were very similar in the pre-
intercept of the final model as an alternative pooled estimator, which               and post-HHWS period (Table 1). Descriptive statistics for each city,
controls for the identified meta-variables.                                          including the actual number of heat warnings issued, are outlined in
                                                                                     Tables A.5 to A.19 in the Appendix.
2.2.3. Sensitivity analyses                                                              In the graphical assessment of the parallel trend assumption during
    As a sensitivity analysis, we first tested an alternative definition, only       the pre-HHWS period, we observed very similar trends in mortality on
based on observed data, of “eligible” and “non-eligible” days to assess              eligible and non-eligible days for the cities of Bremen, Duisburg, Essen,
the robustness of the chosen approach. For this purpose, we defined                  Frankfurt, Hannover, Munich, and Nuremberg. Conversely, the assump­
“eligible” days only based on the random forest classification for the               tion appeared to be violated for Berlin, Cologne, Dortmund, Dresden,
entire study period (warm-season months of 1993–2020). Second, we                    Dusseldorf, Hamburg, Leipzig, and Stuttgart. Outliers in both groups of
were more restrictive in defining non-eligible days by considering only              eligible and non-eligible days appeared to affect the trendlines and
days on which temperature and relative humidity were above pre­                      limited the conclusiveness of the graphical verification of the parallel
defined thresholds. The thresholds were the minimum values of daily                  trend assumption (Fig. A.2). Consequently, our subsequent analyses
mean, minimum, and maximum temperature, as well as of relative hu­                   differentiated between all cities and the seven cities with very similar
midity of the “eligible” days throughout the study period. Third, we                 mortality trends before 2005.
defined shorter study periods, specifically the warm-season months of
May to September, for a) three years (2002–2007); b) five years                      3.2. City-specific effects of heat alerts on mortality
(2000–2009); and c) 10 years (1995–2014) before and after HHWS
implementation in 2005. Fourth, to test the potential impact of years                    Among the 15 cities analyzed, six cities showed RRs of less than one,
with extreme heat exposure, we excluded a) all and b) one of the six                 while the RRs of nine cities were greater than or equal to one (Fig. 1;
years with the highest counts of heat-related deaths from 1993 to 2020               Table A.20). Notably, Berlin exhibited a statistically significant RR of
(specifically, 1994, 2003, 2006, 2015, 2018, 2019) according to                      less than one (RR = 0.95, 95 % CI: 0.91 to 0.99, p-value < 0.01), sug­
(Winklmayr et al. 2022).                                                             gesting a significant reduction in mortality due to heat alerts. Addi­
    We tested several modifications to assess the quasi-Poisson first-stage          tionally, Frankfurt (RR = 0.94, 95 % CI: 0.88 to 1.00, p-value < 0.05)
model’s robustness. These included fitting the first-stage model a)                  and Hamburg (RR = 0.95, 95 % CI: 0.90 to 1.00, p-value < 0.05)
without any adjustments (basic DID model), b) adjusting only for tem­                demonstrated significant RRs of less than one, while Duisburg showed a
poral patterns, c) adjusting for temporal patterns, relative humidity, and           significant RR greater than one (RR = 1.09, 95 % CI: 1.01 to 1.18, p-
daily maximum temperature, d) adjusting for temporal patterns, relative              value < 0.05). Among the seven cities fulfilling the parallel trends
humidity, and the running mean of the mean temperature of the pre­                   assumption, two cities had RRs of less than one, while five cities had RRs
vious three days. Furthermore, we fitted our first-stage model e) without            greater than or equal to one. Specifically, Frankfurt exhibited a statis­
an offset, and f) additionally adjusted, besides temporal patterns, rela­            tically significant RR of less than one, and Duisburg showed a significant
tive humidity, and mean temperature, for the proportion of inhabitants               RR greater than one.
65 years and older and the life expectancy in years. The DID estimators
obtained from the sensitivity analyses were pooled using the same meta-              3.3. Pooled effects of heat alerts on mortality
regressions as in the main second-stage model. Finally, we performed
two linear regression models as a complementary analysis with the daily                 The basic meta-regression random effects models (Model 0) produced
mortality rate per 100,000 inhabitants as the outcome variable (dividing             pooled estimates without adjustment for city-specific characteristics,
the number of daily deaths by the population per city). One linear                   representing the average association between heat alerts and mortality

                                                                                 4
H. Feldbusch et al.                                                                                                            Environment International 203 (2025) 109746


Table 1
Descriptive statistics pre- and post-heat health warning system (HHWS) period for eligible and non-eligible days.
  Variables *, **, ***                     Pre-HHWS period (1993–2004)                                    Post-HHWS period (2005–2020)

                                           Non-eligible days (n = 26,152)   Eligible days (n = 1,339)     Non-eligible days (n = 34,424)      Eligible days (n = 2,296)

  Number of days per year                  2,179.3     ​                    111.6       ​                 2,151.5     ​                       143.5      ​
  Daily number of all-cause deaths (IQR)   26.9        (15.0–29.0)          31.1        (17.0–31.0)       26.6        (15.0–29.0)             30.5       (18.0–33.0)
  Mean temperature [◦ C (IQR)]             16.1        (13.6–18.9)          24.6        (23.6–25.9)       16.6        (14.0–19.1)             24.6       (23.1–26.1)
  Maximum temperature [◦ C (IQR)]          21.0        (17.8–24.5)          31.6        (30.2–33.2)       21.7        (18.5–24.9)             31.8       (29.7–33.7)
  Minimum temperature [◦ C (IQR)]          11.6        (9.2–13.9)           17.7        (16.4–18.8)       11.6        (8.9–13.9)              17.5       (16.0–18.8)
  Relative humidity [% (IQR)]              72.0        (64.0–81.0)          58.0        (51.0–66.0)       72.0        (63.6–80.0)             59.0       (52.0–68.0)
  Apparent temperature [◦ C (IQR)]         22.0        (17.9–26.6)          36.2        (34.5–38.3)       23.0        (18.8–27.4)             36.8       (34.3–39.2)

* Median values, followed by the interquartile range (IQR), are provided for each continuous variable except the daily number of all-cause deaths.
** For daily number of all-cause deaths, mean values are provided, followed by the interquartile range (IQR).
*** For number of days per year, mean values are provided.


across the 15 and seven cities. This basic model showed a moderate                      the effect sizes of the DID estimators from the linear models could not be
heterogeneity across all cities and the seven cities fulfilling the parallel            directly compared to the quasi-Poisson models, it was evident that the
trend assumption (Table 2). The observed heterogeneity cannot be                        same city-specific estimators became significant, and the effect di­
accounted for by grouping into federal states (Model 1) since the                       rections were highly similar (see Tables A.39 and A.40).
multilevel models (Model 1) showed similar or higher heterogeneity
compared to the basic models (Model 0). The final second-stage model,                   4. Discussion
explaining most of the observed heterogeneity, was the stepwise
selected multiparameter model (Model 2). It included the metavariables                      This study is one of the first comprehensive studies examining the
recreational area per person, total population, and population density as               impact of heat alerts on mortality in 15 major German cities. The results
predictors for all cities and the metavariables water area and total pop­               of the first-stage analyses revealed substantial heterogeneity in the
ulation for the subset of the seven cities (Table 2). No protective effect              effectiveness of the HHWS in preventing deaths on hot days across cities.
was found for the pooled RR predicted based on the average of the                       This variability was evident in both the full set of cities and the subgroup
identified meta-variables, neither for all cities (RR = 1.00, 95 % CI: 0.98             of cities fulfilling the parallel trends assumption of the difference-in-
to 1.01) nor the seven cities fulfilling the parallel trend assumption (RR              differences (DID) approach. Our pooled findings indicated no signifi­
= 1.01, 95 % CI: 0.98 to 1.03). By contrast, a significant but small                    cant overall protective effect, or a significant but small protective effect
protective pooled effect (intercept of the final second-stage model) was                of heat alerts on all-cause mortality across the studied cities.
found across all cities (RR = 0.85, 95 % CI: 0.75 to 0.97) and the sub­                     These inconsistent results align with previous conflicting evidence
group of the seven cities (RR = 0.90, 95 % CI: 0.81 to 0.99), when                      on the effectiveness of HHWS in preventing mortality. Some studies
adjusting for the identified city-specific meta-variables.                              have reported a reduced heat-related mortality after implementing a
                                                                                        heat alert system (Fouillet et al. 2008; Heudorf and Schade 2014;
3.4. Sensitivity analyses results                                                       Morabito et al. 2012) or heat prevention plans (de’Donato et al. 2018;
                                                                                        Hess et al. 2018; Martínez-Solanas and Basagaña 2019; Schifano et al.
    The random forest classification analyses and the analyses with re­                 2012). By contrast, a study from Adelaide, for example, provided no
strictions in the group of non-eligible days did not result in substantial              evidence of a reduction in mortality but a significant reduction in
changes in the effects compared to the main model. The only difference                  morbidity after implementing a heat alert system (Nitschke et al. 2016).
concerned the pooled RR (intercept of the meta-regression model) for the                However, these studies may be susceptible to confounding due to factors
seven cities, which was no longer significant using a more restrictive                  changing over time, other than the implementation of heat alert systems
definition of non-eligible days (Fig. 2; Table A.21 and A.22). Shortening               or heat health action plans (HHAPs), such as structural adaptation
the study periods led to a smaller pooled RR for all cities, whereas the                measures (for example, higher air conditioning prevalence), changes in
pooled RR for the seven cities meeting the parallel trend assumption                    baseline health status, or shifting in socioeconomics (Weinberger et al.
showed little changes (Fig. 2; Tables A.23 to A.25). When excluding the                 2021; Weinberger et al. 2018). To avoid this form of confounding, a few
six years with the highest number of heat-related deaths from 1993 to                   studies, including this one, compared days with and without heat alerts
2020, the pooled RR of the seven cities remained robust, while the                      while adjusting for time-varying factors (Benmarhnia et al. 2016;
pooled RR of all cities lost significance (Table A.26). When excluding                  Weinberger et al. 2021; Weinberger et al. 2018). Two of these studies
each of the six years with extreme heat episodes in turn, the exclusion of              examined the effectiveness of National Weather Service heat alerts in
2003 and 1994 revealed the greatest changes in effect size on city-level.               preventing mortality in 20 US cities and among adults aged 65 and over
The exclusion of 2003 revealed an RR increase, especially in Cologne,                   in the United States. Both studies found no evidence of an association
Dortmund, Dusseldorf, Frankfurt, and Stuttgart. The exclusion of 1994                   between heat alerts and reduced mortality, except for Philadelphia
revealed an RR increase, especially in Berlin, Bremen, Dresden, and                     (Weinberger et al. 2021; Weinberger et al. 2018).
Hamburg (refer to Tables A.27 to A.32 and Fig. A.7). The pooled RR                          In addition to our study, a DID approach has been applied in a Ca­
remained robust, when excluding each of the six years, except for 2003,                 nadian and a Korean study (Benmarhnia et al. 2016; Heo et al. 2019).
where the pooled RR of all and the seven cities lost significance.                      While in the Canadian study the effect of heat action plans (HAPs) on
Nevertheless, the pooled RR of the cities fulfilling the DID assumptions                mortality was assessed, stratified by sex, age, and socioeconomic status
demonstrated consistently high robustness in the sensitivity analyses,                  (Benmarhnia et al. 2016), the Korean study focused on the effect of a
with pooled RR (intercept of the meta-regression model) ranging from                    heat wave warning system on all-cause mortality across various sub­
0.85 (95 % CI: 0.76 to 0.96) to 0.92 (95 % CI: 0.83 to 1.02).                           groups (Heo et al. 2019). Given these methodological differences, direct
    We tested several modifications of the first-stage quasi-Poisson                    comparisons between our findings and those of these studies are limited.
model, and the city-specific and pooled results remained highly                         The Canadian study reported that the reduction in mortality attributable
consistent (Fig. A.6; Tables A.33 to A.38), indicating the robustness of                to HAPs was more pronounced among elderly people and residents of
our first-stage model. The results of the additional linear analyses                    low-education neighborhoods (Benmarhnia et al. 2016). In contrast, in
further confirmed the robustness of the city-specific findings. Although                the Korean study evidence was found for a decrease in all-cause

                                                                                    5
H. Feldbusch et al.                                                                                                            Environment International 203 (2025) 109746




Fig. 1. City-specific and pooled estimates of relative risk (RR) from the first-stage quasi-Poisson models and the second-stage meta-regression (bottom), for all cities
and the seven cities fulfilling the DID parallel trends assumption (selected cities), with 95 % confidence intervals. RR < 1 suggests that the implementation of the heat
health warning system (HHWS) reduced all-cause mortality during heat episodes. RR ≥ 1 suggests no protective effect of the HHWS. Filled symbols show significant
estimates (p < 0.05), open symbols non-significant results.


mortality for the subgroup of people aged 19–64 without education                       of heat alerts on mortality in different spatial units (Weinberger et al.
(− 0.144 deaths per 1,000,000 people, 95 % CI: − 0.227 to − 0.061) and                  2018; Wu et al. 2023). More specifically, the estimated effect of HHWS
for children aged 0–19 (− 0.555 deaths per 1,000,000 people, 95 % CI:                   on mortality for Frankfurt was in qualitative agreement with Heudorf
− 0.993 to − 0.117). Unlike our study and the Canadian study, the                       and Schade (2014), who found a decreased excess mortality during heat
Korean study did not compare pre- and post-implementation periods of                    waves after the implementation of a HHWS and HHAP in that city.
the heat alert or HAP in DID analyses. Instead, Heo et al. (2019) used the              Further evidence on initial evaluations of the HHWS is given for the state
discrepancy between the alerts and the monitored temperature, dis­                      of Hessen (where Frankfurt is located), showing that the HHWS effec­
tinguishing between correct and incorrect forecast.                                     tively reduced hospital admissions among residents of elderly care and
    Our observations of heterogeneous city-specific effects were consis­                nursing homes with heat-related symptoms (Koppe 2009). Although the
tent with studies from the US, which also observed heterogeneous effects                DWD uniformly disseminated the heat alerts via various channels


                                                                                    6
H. Feldbusch et al.                                                                                                              Environment International 203 (2025) 109746


Table 2
Results of the second-stage random-effects meta-regression models: Basic and final multiparameter models based on city-specific difference-in-differences (DID) es­
timators for all cities and the seven cities fulfilling the DID parallel trend assumption (selected cities).
  Model                               Coefficient               Relative Risk          95 % CI*          p-Value*          I-squared            AIC              BIC

  Basic model (all cities)            (Intercept)               0.99                   [0.97,1.01]           0.41              35.24 %          − 50.46          − 49.04
                                      (Intercept)**             0.85                   [0.75,0.97]         < 0.05               0.00 %          − 57.40          − 53.86
        Final model (all cities)      Recreational area         1.00                   [1.00,1.01]         < 0.01
                                      Population                1.00                   [1.00,1.00]         < 0.01
  ​                                   Population density        1.00                   [1.00,1.00]           0.06          ​                    ​                ​

  Basic model (selected cities)       (Intercept)               1.00                   [0.97,1.03]           0.90              43.18 %          − 20.29          − 20.40

                                      (Intercept)**             0.90                   [0.81,0.99]         < 0.05               0.00 %          − 23.98          − 24.20
      Final model (selected cities)   Water area                1.02                   [1.01,1.03]         < 0.01
                                      Population                1.00                   [1.00,1.00]           0.12

* Parametric 95% confidence interval and p-value of the relative risk of each estimate.
** Intercepts of the final models represent the pooled estimates.




Fig. 2. Pooled relative risks (RR) of the sensitivity analyses for all cities (intercepts of the meta regression: black, predicted RR based on the average of the meta
variables across all cities: red) and the seven cities fulfilling the DID parallel trends assumption (intercepts: turquoise, predicted RR: purple), with 95 % confidence
intervals. Filled symbols show significant estimates (p < 0.05), open symbols non-significant results.


(Matzarakis et al. 2020), where interested parties could directly inform                information campaigns. It can also be expected that general awareness
themselves, there were differences in heat alert dissemination at the                   and understanding of heat related health risks have increased in the
state level. For example, an evaluation study by the German Federal                     population over the last 20 years, since the HHWS has first been
Environment Agency of Germany found that only six federal German                        established. While these aspects go beyond the scope of this study,
states disseminated heat alerts to healthcare facilities at their own re­               further research can help to differentiate the effects of HHWS alerts with
sponsibility (Capellaro and Sturm 2015). However, we could not explain                  regard to their coverage in reaching the population and the connection
the observed heterogeneity with more similarity for cities nested within                with respective heat health messages and measures. Hence, in­
the same state.                                                                         vestigations assessing the awareness, knowledge, attitude and practice
    Another factor that may contribute to the observed heterogeneity in                 of the population, including vulnerable population groups, can shed
the first-stage results is the local implementation and quality of HHAP or              more light on potential factors influencing the effectiveness of heat
other designated concepts with measures to protect human health from                    alerts. One example of such an investigation is the PACE study,
heat effects. Although all 15 cities have published measures for the                    providing information on public awareness and perception of heat-
protection of human health against heat, it cannot be assumed that all                  related health risks (Lehrer et al. 2024). Furthermore, the existing
measures have actually been implemented (Hannemann et al. 2023). In                     HHAPs and heat health measurements have yet to be evaluated; there­
addition, there is a significant heterogeneity in the comprehensiveness                 fore, the effect of these on heat-related mortality and morbidity remains
and scope of the published measures (Hannemann et al. 2023; Winkl­                      unclear (Blättner et al. 2020; Hannemann et al. 2023).
mayr et al. 2023). Even though there is no detailed information available                   Our meta-analysis suggested that the city-specific proportion of
on which actions have been put in place and where, it can be assumed                    water area and recreational area per person (predominantly green area),
that some heat health action was carried out beyond the mere heat                       in addition to population size and population density, may be associated
health warning. This lack of this information may be based in the lack of               to the effectiveness of heat alerts on mortality, explaining a large part of
a clearly defined responsibilities in heat health protection on national,               the observed heterogeneity in city-specific effects. Comparing these
federal and local levels and the resulting heterogeneity of approaches                  second-stage results with other results in similar contexts is difficult
and measures in Germany (Matthies-Wiesler et al. 2021). This means,                     because of the lack of comparable studies. In the study of Weinberger
that it cannot be disentangled in how far the identified effects of heat                et al. (Weinberger et al. 2018), second-stage meta-regression models
alerts on mortality during heat episodes are linked to the HHWS and the                 were applied to explain variability in heat alert effectiveness across 20
alerts alone, or whether they are connected to the way the heat alerts are              US cities but with different city-level characteristics. Thereby, no asso­
disseminated and integrated with respective heat health actions, such as                ciation was found between the metavariables mean daily maximum heat


                                                                                   7
H. Feldbusch et al.                                                                                                      Environment International 203 (2025) 109746


index, air conditioning prevalence, percent of inhabitants 65 years and             impact on the effect of heat warnings on mortality. Another important
older, percent of heat alerts published as excessive heat warnings, and             limitation of our study was that we did not analyze lagged effects. While
the effectiveness of heat alerts (Weinberger et al. 2018). Previous studies         there is a risk of ecological fallacies due to the partly high level of ag­
on the modification of heat-related mortality by urban green or blue                gregation (Roumeliotis et al. 2021), this study provides initial evidence
(water) indicated a protective effect of these variables on heat-related            of city-level characteristics that modify the effect of heat alerts on
mortality (Burkart et al. 2016; Choi et al. 2022). In contrast, a study             mortality during heat episodes. We were unable to address the heat-
from Hong Kong found no significant protective effects of green and blue            health action plans (HHAP) in the analyzed cities and could not deter­
infrastructure on heat-related mortality risk (Song et al. 2022). Still,            mine to what extent the inhabitants are informed about heat alerts and
assuming the general protective effects of green and blue infrastructure            respective preventive and protective measures. Nevertheless, we
on heat-related mortality in the studied cities, this could lower the effect        focused on one core element indicated by the WHO for the successful
of heat alerts on mortality on heat days. These theoretical considerations          implementation of HHAPs: The HHWS (Matthies et al. 2008; WHO
could explain our results: the more green and blue infrastructure were              Regional Office for Europe 2021; WMO and WHO 2015). Further
present, the higher the RR, because the population was comparatively                research is required to explore this further.
well protected from heat independent of the existence of a HHWS.
Regarding population size, it is remarkable that cities with more in­               5. Conclusion
habitants are better positioned to receive external funding, including EU
funds, to initiate and implement measurements (Hannemann et al. 2023;                   Our research concludes that the implementation of a heat health
Otto et al. 2021) to protect human health from heat, which might in­                warning system (HHWS) in Germany in 2005 has contributed to a sig­
crease the protective effect of heat alerts. However, the variables pop­            nificant but small decrease in mortality during heat episodes across 15
ulation size and population density showed inconsistent effects in terms of         German cities, once inter-city differences in the number of inhabitants,
direction and significance in the final second-stage models.                        population density and the presence of blue and green urban infra­
    One strength of this study is the application of a DID design, which is         structure are controlled for. However, our first-stage results indicate
generally well-established in public health research (Dimick and Ryan               considerable heterogeneity in the city-specific effects of heat alerts,
2014; Wing et al. 2018). Although the DID approach is not a perfect                 ranging from significant protective effects to significant ineffectiveness.
replacement for randomized experiments, it can help understand the                  Our results can be useful for cities and municipalities when developing
causal relationship between heat alerts and mortality on heat days                  and implementing HHAPs. They suggest that the effect of city-specific
(Wing et al. 2018). In applying the approach, one of the most chal­                 factors together with heat alerts need to be considered when devel­
lenging tasks is to assess the credibility of the assumption of common              oping measures for the core element of long-term urban planning to
trends (Wing et al. 2018). Unlike the studies from Montreal and Korea               reduce heat exposure. Future research will need to elucidate whether
(Benmarhnia et al. 2016; Heo et al. 2019), we sought to validate the                HHWSs unfold their effectiveness without respective heat health mea­
parallel trends assumption with graphical evidence, following the                   sures as part of a HHAP. Our study contributes to moving forward the
approach of a study of Alari et al. (2021). The graphical verification              efforts in heat health protection and underlines the need to develop and
indicated that for eight of the 15 cities, the city-specific trends in mor­         implement HHWS as part of HHAP and in combination with heat health
tality in eligible and non-eligible days were not approximately parallel            actions at local level. Similar study approaches could potentially
in the pre-HHWS period (1993–2004). Contrary to the study of Alari                  contribute to the evaluation of the effectiveness of overall HHAPs in
et al. (2021), we did not exclude these cities from further analysis.               terms of reducing mortality during heat episodes.
However, we reported the results separately, as the year-to-year varia­
tion of mortality during eligible and non-eligible days was high, which
                                                                                    CRediT authorship contribution statement
was consistent with observations on mortality during heat episodes in
the respective period in Germany (Winklmayr et al. 2022). A second
                                                                                        Hanna Feldbusch: Writing – original draft, Visualization, Valida­
strength of our study is that we devoted more attention to sensitivity
                                                                                    tion, Software, Methodology, Investigation, Formal analysis, Data
analyses, assessing the key assumptions that support the research de­
                                                                                    curation, Conceptualization. Alexandra Schneider: Writing – review &
sign’s internal validity, as the year-to-year mortality variation was high
                                                                                    editing. Franziska Matthies-Wiesler: Writing – review & editing.
(Wing et al. 2018). Overall, the city-specific and pooled effects appeared
                                                                                    Andreas Matzarakis: Writing – review & editing. Annette Peters:
robust in sensitivity analyses, especially the estimator of the seven cities,
                                                                                    Writing – review & editing. Susanne Breitner-Busch: Writing – review
where the graphical evaluation supported the given parallel trends
                                                                                    & editing, Methodology, Conceptualization. Veronika Huber: Writing –
assumption. However, the sensitivity analyses generally supported a
                                                                                    review & editing, Methodology, Data curation, Conceptualization.
high internal validity of the applied DID models, especially for the
selected cities (Wing et al. 2018).
    The most important limitation of our study was that we were unable              Funding
to analyze subgroups or further outcomes, for example cause-specific
mortality or hospital admission due to the aggregated mortality data.                   This work partly received funding from the European Union’s Ho­
Other studies have shown that specific subgroups vulnerable to heat,                rizon 2020 research and innovation programme (Marie Skłodowska-
such as children and older adults, seem to benefit more from heat alerts            Curie Grant Agreement No.: 101032087).
(Benmarhnia et al. 2016; Heo et al. 2019). As the first-stage analyses do
not require any adjustments for age or sex to determine the city-specific
DID estimators, these are still valid given the DID assumptions. The                Declaration of competing interest
results point out that the estimator for the seven cities, where the
graphical evaluation supported the given parallel trends assumption,                    The authors declare that they have no known competing financial
was more robust than the all-cities estimator. This could indicate a                interests or personal relationships that could have appeared to influence
violation of the DID assumptions for the eight cities, where the graphical          the work reported in this paper.
evaluation did not support the parallel trends assumption, may leading
to a biased all-cities estimator. Additionally, a possible prediction error,        Appendix A. Supplementary material
resulting from the fact that alerts are issued based on weather forecasts,
could have contributed to biases in the DID estimators (Heo et al. 2019).              Supplementary data to this article can be found online at https://doi.
Further studies are needed to examine this prediction error and its                 org/10.1016/j.envint.2025.109746.

                                                                                8
H. Feldbusch et al.                                                                                                                               Environment International 203 (2025) 109746


Data availability                                                                                   Dimick, J.B., Ryan, A.M., 2014. Methods for evaluating changes in health care policy: the
                                                                                                        difference-in-differences approach. J. Am. Med. Assoc. 312, 2401–2402. https://doi.
                                                                                                        org/10.1001/jama.2014.16153.
    The data that has been used is confidential.                                                    Ebi, K.L., Capon, A., Berry, P., Broderick, C., de Dear, R., Havenith, G., Honda, Y.,
                                                                                                        Kovats, R.S., Ma, W., Malik, A., Morris, N.B., Nybo, L., Seneviratne, S.I., Vanos, J.,
References                                                                                              Jay, O., 2021. Hot weather and heat extremes: health risks. Lancet 398, 698–708.
                                                                                                        https://doi.org/10.1016/s0140-6736(21)01208-3.
                                                                                                    Federal Ministry for the Environment Nature Conservation Building and Nuclear Safety.
Abadie, A., Cattaneo, M.D., 2018. Econometric methods for program evaluation. Ann.                      Recommendations for Action. Heat Action Plans to protect human health. 2017.
     Rev. Econ. 10, 465–503. https://doi.org/10.1146/annurev-economics-080217-                          https://www.bmuv.de/WS4443-1.
     053402.                                                                                        Federal Ministry of Health. Hitzeschutzplan für Gesundheit des BMG. 2023. https
Alari, A., Schwarz, L., Zabrocki, L., Le Nir, G., Chaix, B., Benmarhnia, T., 2021. The                  ://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/H/Hit
     effects of an air quality alert program on premature mortality: a difference-in-                   zeschutzplan/230727_BMG_Hitzeschutzplan.pdf.
     differences evaluation in the region of Paris. Environ. Int. 156, 106583. https://doi.         Fouillet, A., Rey, G., Wagner, V., Laaidi, K., Empereur-Bissonnet, P., Le Tertre, A.,
     org/10.1016/j.envint.2021.106583.                                                                  Frayssinet, P., Bessemoulin, P., Laurent, F., De Crouy-Chanel, P., Jougla, E.,
An der Heiden, M., Muthers, S., Niemann, H., Buchholz, U., Grabenhenrich, L.,                           Hémon, D., 2008. Has the impact of heat waves on mortality changed in France since
     Matzarakis, A., 2020. Heat-related mortality. Dtsch. Arztebl. Int. 117, 603–609.                   the European heat wave of summer 2003? A study of the 2006 heat wave. Int. J.
     https://doi.org/10.3238/arztebl.2020.0603.                                                         Epidemiol. 37, 309–317. https://doi.org/10.1093/ije/dym253.
Ballester, J., Quijal-Zamorano, M., Méndez Turrubiates, R.F., Pegenaute, F.,                       Gabriel, K.M.A., Endlicher, W.R., 2011. Urban and rural mortality rates during heat
     Herrmann, F.R., Robine, J.M., Basagaña, X., Tonne, C., Antó, J.M., Achebak, H.,                  waves in Berlin and Brandenburg, Germany. Environ. Pollut. 159, 2044–2050.
     2023. Heat-related mortality in Europe during the summer of 2022. Nat. Med.                        https://doi.org/10.1016/j.envpol.2011.01.016.
     https://doi.org/10.1038/s41591-023-02419-z.                                                    Goggins, W.B., Chan, E.Y., Ng, E., Ren, C., Chen, L., 2012. Effect modification of the
Barreca, A.I., 2012. Climate change, humidity, and mortality in the United States.                      association between short-term meteorological factors and mortality by urban heat
     J. Environ. Econ Manage. 63, 19–34. https://doi.org/10.1016/j.jeem.2011.07.004.                    islands in Hong Kong. PLoS One 7, e38551. https://doi.org/10.1371/journal.
Basagaña, X., Sartini, C., Barrera-Gómez, J., Dadvand, P., Cunillera, J., Ostro, B.,                  pone.0038551.
     Sunyer, J., Medina-Ramón, M., 2011. Heat waves and cause-specific mortality at all            Hannemann, L., Janson, D., Grewe, H.A., Blättner, B., Mücke, H.-G., 2023. Heat in
     ages. Epidemiology 22, 765–772. https://doi.org/10.1097/                                           German cities: a study on existing and planned measures to protect human health.
     EDE.0b013e31823031c5.                                                                              J. Public Health. https://doi.org/10.1007/s10389-023-01932-2.
Basarin, B., Lukić, T., Matzarakis, A., 2020. Review of biometeorology of heatwaves and            Heo, S., Nori-Sarma, A., Lee, K., Benmarhnia, T., Dominici, F., Bell, M.L., 2019. The use
     warm extremes in Europe. Atmosphere 11, 1276. https://doi.org/10.3390/                             of a quasi-experimental study on the mortality effect of a heat wave warning system
     atmos11121276.                                                                                     in Korea. Int. J. Environ. Res. Public Health 16, 2245. https://doi.org/10.3390/
Benmarhnia, T., Bailey, Z., Kaiser, D., Auger, N., King, N., Kaufman, J.S., 2016.                       ijerph16122245.
     A difference-in-differences approach to assess the effect of a heat action plan on heat-       Hess, J.J., Errett, N.A., McGregor, G., Busch Isaksen, T., Wettstein, Z.S., Wheat, S.K.,
     related mortality, and differences in effectiveness according to sex, age, and                     Ebi, K.L., 2023. Public health preparedness for extreme heat events. Annu. Rev.
     socioeconomic status (Montreal, Quebec). Environ. Health Perspect. 124,                            Public Health 44, 301–321. https://doi.org/10.1146/annurev-publhealth-071421-
     1694–1699. https://doi.org/10.1289/ehp203.                                                         025508.
Blättner, B., Janson, D., Roth, A., Grewe, H.A., Mücke, H.-G., 2020. Gesundheitsschutz             Hess, J.J., Lm, S., Knowlton, K., Saha, S., Dutta, P., Ganguly, P., Tiwari, A., Jaiswal, A.,
     bei hitzeextremen in deutschland: was wird in ländern und kommunen bisher                         Sheffield, P., Sarkar, J., Bhan, S.C., Begda, A., Shah, T., Solanki, B., Mavalankar, D.,
     unternommen? Bundesgesundheitsbl. Gesundheitsforsch. Gesundheitsschutz 63,                         2018. Building resilience to climate change: pilot evaluation of the impact of india’s
     1013–1019. https://doi.org/10.1007/s00103-020-03189-6.                                             first heat action plan on all-cause mortality. J. Environ. Public Health 2018,
Bundesinstitut für Bau- Stadt- und Raumforschung (BBSR). Laufende Raumbeobachtung                       7973519. https://doi.org/10.1155/2018/7973519.
     des BBSR - INKAR. 2023. https://www.inkar.de/.                                                 Heudorf, U., Schade, M., 2014. Heat waves and mortality in Frankfurt am Main,
Burkart, K., Meier, F., Schneider, A., Breitner, S., Canário, P., Alcoforado, M.J.,                    Germany, 2003-2013: what effect do heat-health action plans and the heat warning
     Scherer, D., Endlicher, W., 2016. Modification of heat-related mortality in an elderly             system have? Z. Gerontol. Geriatr. 47, 475–482. https://doi.org/10.1007/s00391-
     urban population by vegetation (Urban Green) and proximity to water (urban blue):                  014-0673-2.
     evidence from Lisbon, Portugal. Environ Health Perspect 124, 927–934. https://doi.             Huber, V., Breitner-Busch, S., He, C., Matthies-Wiesler, F., Peters, A., Schneider, A.,
     org/10.1289/ehp.1409529.                                                                           2024. Heat-related mortality in the extreme summer of 2022: an analysis based on
Capellaro, M., Sturm, D., 2015. Evaluation of Information Systems Relevant to Climate                   daily data. Dtsch Arztebl Int 2024. https://doi.org/10.3238/arztebl.m2023.0254.
     Change and Health. Volume 1: Adaption to Climate Change: Evaluation of Existing                Janson, D., Kaiser, T., Kind, C., 2023. Analyse von Hitzeaktionsplänen und
     National Information Systems (UV-Index, Heat Warning System, Airborne Pollen and                   gesundheitlichen Anpassungsmaßnahmen an Hitzeextreme in Deutschland. Umwelt
     Ozone Forecasts) from a Public Health Perspective – How to Reach Vulnerable                        Und Gesundheit. https://doi.org/10.60810/openumwelt-7319.
     Populations. Umwelt und Gesundheit 2015;3:1-144.                                               Kaiser, T., Kind, C., Dudda, L., Klimawandel, S.K., 2021. Hitze und Gesundheit: stand der
Carpenter, J., Bithell, J., 2000. Bootstrap confidence intervals: when, which, what? A                  gesundheitlichen Hitzevorsorge in Deutschland und Unterstützungsbedarf der
     practical guide for medical statisticians. Stat. Med. 19, 1141–1164. https://doi.org/              Bundesländer und Kommunen. UMID - Umwelt + Mensch Informationsdienst. https
     10.1002/(sici)1097-0258(20000515)19:9.                                                             ://www.umweltbundesamt.de/sites/default/files/medien/4031/publikationen/umi
Casanueva, A., Burgstall, A., Kotlarski, S., Messeri, A., Morabito, M., Flouris, A.D.,                  d_01-2021-beitrag_3_hitze.pdf.
     Nybo, L., Spirig, C., Schwierz, C., 2019. Overview of existing heat-health warning             Kalkstein, L.S., Valimont, K.M., 1986. An evaluation of summer discomfort in the United
     systems in Europe. Int. J. Environ. Res. Public Health 16, 2657. https://doi.org/                  States using a relative climatological index. Bull. Am. Meteorol. Soc. 67, 842–848.
     10.3390/ijerph16152657.                                                                            https://doi.org/10.1175/1520-0477(1986)067<0842:AEOSDI>2.0.CO;2.
Choi, H.M., Lee, W., Roye, D., Heo, S., Urban, A., Entezari, A., Vicedo-Cabrera, A.M.,              Koppe, C., 2009. The heat health warning system of the german meteorological service.
     Zanobetti, A., Gasparrini, A., Analitis, A., Tobias, A., Armstrong, B., Forsberg, B.,              UMID Special Issue Climate Change and Health 3, 39–43.
     Íñiguez, C., Åström, C., Indermitte, E., Lavigne, E., Mayvaneh, F., Acquaotta, F.,          Lanzinger, S., Schneider, A., Breitner, S., Stafoggia, M., Erzen, I., Dostal, M.,
     Sera, F., Orru, H., Kim, H., Kyselý, J., Madueira, J., Schwartz, J., Jaakkola, J.J.K.,             Pastorkova, A., Bastian, S., Cyrys, J., Zscheppang, A., Kolodnitska, T., Peters, A.,
     Katsouyanni, K., Diaz, M.H., Ragettli, M.S., Pascal, M., Ryti, N., Scovronick, N.,                 2016. Ultrafine and fine particles and hospital admissions in central Europe. Results
     Osorio, S., Tong, S., Seposo, X., Guo, Y.L., Guo, Y., Bell, M.L., 2022. Effect                     from the UFIREG study. Am. J. Respir. Crit. Care Med. 194, 1233–1241. https://doi.
     modification of greenness on the association between heat and mortality: a multi-                  org/10.1164/rccm.201510-2042OC.
     city multi-country study. EBioMedicine 84, 104251. https://doi.org/10.1016/j.                  Lehrer, L., Geiger, M., Sprengholz, P., Jenny, M., Temme, H.L., Shamsrizi, P., Eitze, S.,
     ebiom.2022.104251.                                                                                 Betsch, C., 2024. Study protocol of the planetary health action survey PACE: a serial
Cuerdo-Vilches, T., Díaz, J., López-Bueno, J.A., Luna, M.Y., Navas, M.A., Mirón, I.J.,                cross-sectional survey to assess the readiness to act against climate change. BMJ
     Linares, C., 2023. Impact of urban heat islands on morbidity and mortality in heat                 Open 14. https://doi.org/10.1136/bmjopen-2024-091093.
     waves: observational time series analysis of Spain’s five cities. Sci. Total Environ.          Martínez-Solanas, È., Basagaña, X., 2019. Temporal changes in temperature-related
     890, 164412. https://doi.org/10.1016/j.scitotenv.2023.164412.                                      mortality in Spain and effect of the implementation of a Heat Health Prevention
Davis, R.E., McGregor, G.R., Enfield, K.B., 2016. Humidity: a review and primer on                      Plan. Environ. Res. 169, 102–113. https://doi.org/10.1016/j.envres.2018.11.006.
     atmospheric moisture and human health. Environ. Res. 144, 106–116. https://doi.                Matthies-Wiesler, F., Herrmann, M., Schulz, C., Gepp, S., Jung, L., Schneider, A.,
     org/10.1016/j.envres.2015.10.014.                                                                  Breitner-Busch, S., 2021. The Lancet Countdown on Health and Climate Change -
de’Donato, F., Scortichini, M., De Sario, M., de Martino, A., Michelozzi, P., 2018.                     Policy Brief für Deutschland. The Lancet Countdown on Health and Climate Change,
     Temporal variation in the effect of heat and the role of the Italian heat prevention               the German Medical Association, Institute of Epidemiology of Helmholtz Zentrum
     plan. Public Health 161, 154–162. https://doi.org/10.1016/j.puhe.2018.03.030.                      Muenchen, Charite Universitaetsmedizin Berlin, Potsdam Institute for Climate
Deutscher Wetterdienst (DWD). Historische Hitzewarnungen in Deutschland, Version                        Impact Research (PIK). https://www.klimawandel-gesundheit.de/wp-content/
     v001. 2021. https://opendata.dwd.de/climate_environment/health/historical_al                       uploads/2021/10/20211020_Lancet-Countdown-Policy-Germany-2021_Documen
     erts/heat_warnings/.                                                                               t_v2.pdf.
Deutscher Wetterdienst (DWD). Daily station observations (temperature, pressure,                    Matthies, F., Bickler, G., Marin, N.C., Hales, S., 2008. Heat-health action plans: guidance.
     precipitation, sunshine duration, etc.) for Germany. 2023. https://opendata.dwd.de/                WHO Regional Office for Europe. https://www.who.int/publications/i/item/9789
     climate_environment/CDC/observations_germany/climate/daily/kl/.                                    289071918.
                                                                                                    Matzarakis, A., 2016. Das Hitzewarnsystem des Deutschen Wetterdienstes (DWD) und
                                                                                                        seine Relevanz für die menschliche Gesundheit. Gefahrstoffe 76, 457–460.


                                                                                                9
H. Feldbusch et al.                                                                                                                                  Environment International 203 (2025) 109746

Matzarakis, A., Laschewski, G., Muthers, S., 2020. The heat health warning system in                      the elderly from 1998-2010: results from a multicenter time series study in Italy.
    Germany—application and warnings for 2005 to 2019. Atmos. 11, 170. https://doi.                       Environ. Health 11, 58. https://doi.org/10.1186/1476-069x-11-58.
    org/10.3390/atmos11020170.                                                                        Sera, F., Armstrong, B., Blangiardo, M., Gasparrini, A., 2019. An extended mixed-effects
Menberg, K., Bayer, P., Zosseder, K., Rumohr, S., Blum, P., 2013. Subsurface urban heat                   framework for meta-analysis. Stat. Med. 38, 5429–5444. https://doi.org/10.1002/
    islands in German cities. Sci. Total Environ. 442, 123–133. https://doi.org/10.1016/                  sim.8362.
    j.scitotenv.2012.10.043.                                                                          Sera, F., Gasparrini, A., 2022. Extended two-stage designs for environmental research.
Michalski, N., Reis, M., Tetzlaff, F., Herber, M., Kroll, L.E., Hövener, C., Nowossadeck, E.,            Environ. Health 21, 41. https://doi.org/10.1186/s12940-022-00853-z.
    Hoebel, J., 2022. German index of socioeconomic deprivation (GISD): revision,                     Sheffield, P.E., Herrera, M.T., Kinnee, E.J., Clougherty, J.E., 2018. Not so little
    update and application examples. J. Health Monit. 2–23. https://doi.org/10.25646/                     differences: variation in hot weather risk to young children in New York City. Public
    10641.                                                                                                Health 161, 119–126. https://doi.org/10.1016/j.puhe.2018.06.004.
Morabito, M., Profili, F., Crisci, A., Francesconi, P., Gensini, G.F., Orlandini, S., 2012.           Song, J., Lu, Y., Zhao, Q., Zhang, Y., Yang, X., Chen, Q., Guo, Y., Hu, K., 2022. Effect
    Heat-related mortality in the Florentine area (Italy) before and after the exceptional                modifications of green space and blue space on heat-mortality association in Hong
    2003 heat wave in Europe: an improved public health response? Int. J. Biometeorol.                    Kong, 2008-2017. Sci. Total Environ. 838, 156127. https://doi.org/10.1016/j.
    56, 801–810. https://doi.org/10.1007/s00484-011-0481-y.                                               scitotenv.2022.156127.
Mücke, H.G., Litvinovitch, J.M., 2020. Heat extremes, public health impacts, and                      Steadman, R.G., 1979. The Assessment of sultriness. Part I: A temperature-humidity
    adaptation policy in Germany. Int. J. Environ. Res. Public Health 17. https://doi.                    index based on human physiology and clothing science. J. Appl. Meteorol. Climatol.
    org/10.3390/ijerph17217862.                                                                           18, 861–873. https://doi.org/10.1175/1520-0450(1979)018<0861:TAOSPI>2.0.
Nitschke, M., Tucker, G., Hansen, A., Williams, S., Zhang, Y., Bi, P., 2016. Evaluation of a              CO;2.
    heat warning system in Adelaide, South Australia, using case-series analysis. BMJ                 Taubenböck, H., Droin, A., Standfuß, I., Dosch, F., Sander, N., Milbert, A., Eichfuss, S.,
    Open 6, e012125. https://doi.org/10.1136/bmjopen-2016-012125.                                         Wurm, M., 2022. To be, or not to be ‘urban’? a multi-modal method for the
Otto, A., Kern, K., Haupt, W., Eckersley, P., Thieken, A.H., 2021. Ranking local climate                  differentiated measurement of the degree of urbanization. Comput. Environ. Urban
    policy: assessing the mitigation and adaptation activities of 104 German cities. Clim.                Syst. 95, 101830. https://doi.org/10.1016/j.compenvurbsys.2022.101830.
    Change 167, 5. https://doi.org/10.1007/s10584-021-03142-9.                                        Toloo, G., FitzGerald, G., Aitken, P., Verrall, K., Tong, S., 2013. Evaluating the
Perkins-Kirkpatrick, S.E., Lewis, S.C., 2020. Increasing trends in regional heatwaves. Nat.               effectiveness of heat warning systems: systematic review of epidemiological
    Commun. 11, 3357. https://doi.org/10.1038/s41467-020-16970-7.                                         evidence. Int. J. Public Health 58, 667–681. https://doi.org/10.1007/s00038-013-
Pfafferott, J., Becker, P., 2008. Erweiterung des Hitzewarnsystems um die Vorhersage                      0465-2.
    der Wärmebelastung in Innenräumen. Bauphysik 30, 237–243. https://doi.org/                      United Nations (UN), 2018. World Urbanization Prospects: The 2018 Revision.
    10.1002/bapi.200810031.                                                                           Weinberger, K.R., Wu, X., Sun, S., Spangler, K.R., Nori-Sarma, A., Schwartz, J.,
Robine, J.M., Cheung, S.L., Le Roy, S., Van Oyen, H., Griffiths, C., Michel, J.P.,                        Requia, W., Sabath, B.M., Braun, D., Zanobetti, A., Dominici, F., Wellenius, G.A.,
    Herrmann, F.R., 2008. Death toll exceeded 70,000 in Europe during the summer of                       2021. Heat warnings, mortality, and hospital admissions among older adults in the
    2003. C. R. Biol. 331, 171–178. https://doi.org/10.1016/j.crvi.2007.12.001.                           United States. Environ. Int. 157, 106834. https://doi.org/10.1016/j.
Romanello, M., Di Napoli, C., Drummond, P., Green, C., Kennard, H., Lampard, P.,                          envint.2021.106834.
    Scamman, D., Arnell, N., Ayeb-Karlsson, S., Ford, L.B., Belesova, K., Bowen, K.,                  Weinberger, K.R., Zanobetti, A., Schwartz, J., Wellenius, G.A., 2018. Effectiveness of
    Cai, W., Callaghan, M., Campbell-Lendrum, D., Chambers, J., van Daalen, K.R.,                         National Weather Service heat alerts in preventing mortality in 20 US cities. Environ.
    Dalin, C., Dasandi, N., Dasgupta, S., Davies, M., Dominguez-Salas, P., Dubrow, R.,                    Int. 116, 30–38. https://doi.org/10.1016/j.envint.2018.03.028.
    Ebi, K.L., Eckelman, M., Ekins, P., Escobar, L.E., Georgeson, L., Graham, H.,                     WHO Regional Office for Europe. Heat and health in the WHO European Region: updated
    Gunther, S.H., Hamilton, I., Hang, Y., Hänninen, R., Hartinger, S., He, K., Hess, J.J.,              evidence for effective prevention. Copenhagen; 2021.
    Hsu, S.C., Jankin, S., Jamart, L., Jay, O., Kelman, I., Kiesewetter, G., Kinney, P.,              Wing, C., Simon, K., Bello-Gomez, R.A., 2018. Designing difference in difference studies:
    Kjellstrom, T., Kniveton, D., Lee, J.K.W., Lemke, B., Liu, Y., Liu, Z., Lott, M.,                     best practices for public health policy research. Annu. Rev. Public Health 39,
    Batista, M.L., Lowe, R., MacGuire, F., Sewe, M.O., Martinez-Urtaza, J., Maslin, M.,                   453–469. https://doi.org/10.1146/annurev-publhealth-040617-013507.
    McAllister, L., McGushin, A., McMichael, C., Mi, Z., Milner, J., Minor, K., Minx, J.C.,           Winklmayr, C., an der Heiden, M., 2022. Hitzebedingte Mortalität in Deutschland 2022.
    Mohajeri, N., Moradi-Lakeh, M., Morrissey, K., Munzert, S., Murray, K.A., Neville, T.,                Epidemiologisches Bulletin 3–9. https://doi.org/10.25646/10695.3.
    Nilsson, M., Obradovich, N., O’Hare, M.B., Oreszczyn, T., Otto, M., Owfi, F.,                     Winklmayr, C., Matthies-Wiesler, F., Muthers, S., Buchien, S., Kuch, B., An der
    Pearman, O., Rabbaniha, M., Robinson, E.J.Z., Rocklöv, J., Salas, R.N., Semenza, J.                  Heiden, M., Mücke, H.G., 2023. Heat in Germany: health risks and preventive
    C., Sherman, J.D., Shi, L., Shumake-Guillemot, J., Silbert, G., Sofiev, M.,                           measures. J. Health Monit. 8, 3–32. https://doi.org/10.25646/11651.
    Springmann, M., Stowell, J., Tabatabaei, M., Taylor, J., Triñanes, J., Wagner, F.,               Winklmayr, C., Muthers, S., Niemann, H., Mücke, H.G., Heiden, M.A., 2022. Heat-related
    Wilkinson, P., Winning, M., Yglesias-González, M., Zhang, S., Gong, P.,                              mortality in Germany from 1992 to 2021. Dtsch. Arztebl. Int. 119, 451–457. https://
    Montgomery, H., Costello, A., 2022. The 2022 report of the Lancet Countdown on                        doi.org/10.3238/arztebl.m2022.0202.
    health and climate change: health at the mercy of fossil fuels. Lancet 400,                       WMO and WHO. Heatwaves and Health: Guidance on Warning-System Development. In:
    1619–1654. https://doi.org/10.1016/s0140-6736(22)01540-9.                                             McGregor G.R., Bessemoulin P., Ebi K., Menne B., eds; 2015.
Roumeliotis, S., Abd ElHafeez, S., Jager, K.J., Dekker, F.W., Stel, V.S., Pitino, A.,                 Wu, X., Weinberger, K.R., Wellenius, G.A., Dominici, F., Braun, D., 2023. Assessing the
    Zoccali, C., Tripepi, G., 2021. Be careful with ecological associations. Nephrology                   causal effects of a stochastic intervention in time series data: are heat alerts effective
    (Carlton) 26, 501–505. https://doi.org/10.1111/nep.13861.                                             in preventing deaths and hospitalizations? Biostatistics. https://doi.org/10.1093/
Schifano, P., Leone, M., De Sario, M., de’Donato, F., Bargagli, A.M., D’Ippoliti, D.,                     biostatistics/kxad002.
    Marino, C., Michelozzi, P., 2012. Changes in the effects of heat on mortality among




                                                                                                 10
