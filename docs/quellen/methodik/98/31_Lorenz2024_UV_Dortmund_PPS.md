Photochemical & Photobiological Sciences
https://doi.org/10.1007/s43630-024-00658-8

 ORIGINAL PAPERS



Increasing solar UV radiation in Dortmund, Germany: data and trend
analyses and comparison to Uccle, Belgium
Sebastian Lorenz1 · Felix Heinzl1 · Stefan Bauer2 · Marco Janßen2                  · Veerle De Bock3   ·
Alexander Mangold3 · Peter Scholz‑Kreisel1 · Daniela Weiskopf1

Received: 9 July 2024 / Accepted: 31 October 2024
© The Author(s) 2024


Abstract
Increasing solar ultraviolet radiation (UVR) can raise human exposure to UVR and adversely affect the environment. Precise
measurements of ground-level solar UVR and long-term data series are crucial for evaluating time trends in UVR. This
study focuses on spectrally resolved data from a UVR measuring station in Dortmund, Germany (51.5° N, 7.5° E, 130 m
a.s.l.). After a strict quality assessment, UV data, such as the daily maximum UV Index (­ UVImax) and daily erythemal radiant
 exposure ­(Her,day) values, were analyzed concerning monthly and annual distribution, frequency, occurrence of highest values
and their influencing factors. An advanced linear trend model with a flexible covariance matrix was utilized and applied to
monthly mean values. Missing values were estimated by a validated imputation method. Findings were compared to those
from a station in Uccle, Belgium (50.8° N, 4.3° E, 100 m a.s.l.). Parameters possibly influencing trends in both UVR and
global radiation, such as ozone and sunshine duration, were additionally evaluated. The 1997–2022 trend results show a
statistically significant increase in monthly mean of ­Her,day (4.9% p. decade) and ­UVImax (3.2% p. decade) in Dortmund and
­Her,day (7.5% p. decade) and ­UVImax (5.8% p. decade) in Uccle. Total column ozone shows a slight decrease in the summer
 months. Global radiation increases similarly to the UV data, and sunshine duration in Dortmund increases about twice as
 much as global radiation, suggesting a strong influence of change in cloud cover. To address health-related consequences
 effectively, future adaptation and prevention strategies to climate change must consider the observed trends.
Graphical abstract




Keywords Solar UV radiation · Human health · Trend · UV Index · UV exposure · Ozone
Abbreviations
UVR	    UltraViolet Radiation                                          GR	   Global Radiation
UVImax	 UV Index, daily maximum                                        GRint	Daily integral of GR
Her,day	Daily erythemal radiant exposure                               GRmax	Daily maximum of GR
SED	    Standard Erythemal Dose (= 100 J/m2 erythemal                  TCO	  Total Column Ozone
         radiant exposure)                                              SunD	 Sunshine Duration
                                                                        AOD	  Aerosol Optical Depth
Extended author information available on the last page of the article


                                                                                                              Vol.:(0123456789)
                                                                                             Photochemical & Photobiological Sciences


    Bundesamt für Strahlenschutz, German Federal
BfS	                                                              or the station Uccle, Belgium, is much more sophisticated,
    Office for Radiation Protection                                but provides significantly more information with spectrally
    Deutscher Wetterdienst, German Meteorological
DWD	                                                              resolved data [30]. Well-maintained and calibrated SRM
    Service                                                        provide reliable measurements with lower uncertainty [18,
    Koninklijk Meteorologisch Instituut, Royal
KMI	                                                              31] and are particularly suitable for long-term trend analysis.
    Meteorological Institute of Belgium                                Previous studies analyzing measured data on long-term
                                                                   trends in solar UVR at the Earth's surface have been per-
                                                                   formed using individual wavelengths in the UVA and UVB
1 Introduction                                                     range, as well as using ­Her,day or ­UVImax values. The find-
                                                                   ings for Europe vary widely, from no significant trend in
The harmful effects of solar ultraviolet radiation (UVR)           Finland [32, 33] to a decreasing trend in the UK [34–36]
on public health can lead to various immediate as well as          and an increasing trend in Uccle [33, 37], Thessaloniki [33,
chronic diseases of the skin and eye [1, 2]. The most seri-        36, 38] and Rome in some months [39]. More studies ana-
ous consequence is skin cancer [3–5]; UVR is classified as         lyzed short- and long-term-trends of UVR in Europe based
"completely carcinogenic" (IARC GHS Cat. 1A). In Ger-              on shorter time periods [40, 41], looked at earlier periods
many, the incidence of new skin cancer cases increased             than our study [1, 42, 43] or for future projection [44], are
from about 180,000 to 330,000 per year between 2003 and            based on data reconstruction [45–53] or modelled UVR with
2022 [6], with a 65% rise in fatalities, reaching more than        satellite products [54, 55]. A recent summary of global stud-
4,400 deaths in 2022 [7]. In Belgium, the incidence of new         ies is provided by Bernhard et al. [56]. Due to differences in
skin cancer cases between 2004 and 2022 increased from             evaluated time periods and methodologies, only a qualitative
about 4300 to 14,300 per year [8]. Besides its adverse health      comparison is possible in most cases. Different changes of
effects, exposure to solar UVR can also initiate the synthesis     influencing factors, such as surface reflectivity, cloud cover,
of vitamin D. This issue and further effects of sun exposure       AOD, and total column ozone, are locally different and rel-
on human health and on environment are discussed in com-           evant. Surface reflectivity and cloud cover are affected by
prehensive and current overviews by R.E. Neale et al. [9]          climate change [44, 57]. In recent decades, the impact of
and S. Madronich et al. [10]. Both the daily maximum UV            ozone on the long-term trend of UVR in Europe is minor
Index ­(UVImax) [11] and the daily erythemal radiant expo-         compared to changes in cloudiness and aerosols [33, 35,
sure ­(Her,day) [12] are important parameters to characterize      58]. While ozone may not be a major driver of trends, it
the harmful effects of ground-level UVR.                           still plays a crucial role in Europe. In the short term, ozone
    The amount of solar UVR reaching a specific location on the    can significantly increase solar UVR at the Earth's surface,
Earth's surface depends on numerous parameters [13]: Besides       especially during low-ozone events, leading to higher UV
the altitude and the solar elevation, the most important factors   exposure [59–62]. High-quality long-term measurement
are clouds and cloud cover, the total column ozone (TCO) and       series of ground-level UVR in Europe are sparse in relation
aerosols or rather the aerosol optical depth (AOD). At places      to the large local differences in the previous study results.
covered by snow, the albedo/surface reflectivity has also to be    Furthermore, the current study overview reveals substantial
considered [14–16]. Acute and long-term changes of the influ-      differences in data quality, data processing, handling of data
encing parameters lead to changes in solar UV exposure. These      gaps, and trend analysis methodologies, potentially resulting
changes, caused by ongoing changes in climate, ozone layer and/    in different outcomes.
or anthropogenic aerosols, have the potential to affect humans,        Many studies employ linear trend analysis based on calcu-
life on Earth and the environment with consequences for the        lated monthly anomalies [37, 39]. Other studies, like Hunter
health and well-being of humans and the sustainability of the      et al. [35], used linear and non-linear models to determine a
ecosystem [104].                                                   possible trend. Addressing heterogeneity and autocorrelation
    A major challenge to detect changes in solar UV irra-          is often done by modelling deviations from the seasonal pat-
diance at the Earth's surface and their causes is the high         tern rather than the response values themselves (e.g. [37]).
variability of the influencing parameters as well as the com-      However, a violation of the assumption of uncorrelated and
plex interaction of the change processes [17]. Continuous          homoscedastic error variables leads to underestimated stand-
solar UV monitoring activities and networks can be found           ard errors of trend estimators. The proposed trend model in
in many regions in the world, for instance, in Europe [18,         this article introduces a solution for this issue.
19], Canada [20], the USA [21], Argentina [22], India [23],            This study analyses a long-term series of spectral UV
Thailand [24], Australia [25] or New Zealand [26]. Most UV         measurements from Dortmund, Germany and compares it
monitoring stations are equipped with UV broadband radi-           with data from Uccle, Belgium. The focus is on U   ­ VImax and
ometers (BRM) [27–29]. UV monitoring with spectroradi-             ­Her,day values as they are particularly relevant for human
ometers (SRM) like in the German UV Monitoring network             exposure. A new statistically approach and a specific
Photochemical & Photobiological Sciences

consideration of the handling data gaps is applied and dis-      single wavelength under less favorable conditions (high solar
cussed with respect to its impact on the results.                zenith angle and low wavelength), which would be less than
                                                                 6.9%. The main reasons for the difference are that, for daily
                                                                 integrals or daily maximum values, uncertainties at high
2 Data                                                          solar zenith angle carry less weight and the statistical noise
                                                                 becomes negligibly small, as the daily integrals are based
2.1 UV monitoring station Dortmund                              on several thousand individual wavelength measurements.

In Germany, the Federal Office for Radiation Protection          2.2 UV monitoring station Uccle
(BfS) operates a nationwide network for solar UV monitor-
ing in cooperation with the Federal Environment Agency           Uccle is a residential municipality in the South of the Brus-
(UBA), Germany's National Meteorological Service (DWD)           sels Region and is located about 230 km from Dortmund and
and other associated institutions such as the Federal Insti-     100 km from North Sea shore. The UV monitoring station
tute for Occupational Safety and Health (BAuA). BAuA             (50.8° N, 4.3° E, 100 m a.s.l.) is operated by the Royal Mete-
operates the UV monitoring station in Dortmund (51.5°            orological Institute (KMI) of Belgium. It is equipped with
N, 7.5° E, 130 m a.s.l.). Dortmund is located in the Ruhr        two Brewer ozone spectrophotometers (#016 since 1984 and
area, a densely populated region with 10 million inhabitants.    #178 since 2002; [37]). The instruments are integrated in
The UV monitoring station has been providing spectrally          the European network EuBrewNet [66], in the World Ozone
resolved data on solar UV irradiance since August 1996.          and Ultraviolet Radiation Data Centre (WOUDC) and in
The station is equipped with a spectroradiometer (Bentham,       the Network for the Detection of Atmospheric Composition
DTM 300) measuring the horizontal spectral UV irradi-            Change (NDACC, Brewer016). The instruments perform
ance from sunrise to sunset. A detailed description of the       UV scans with constant wavelength steps of 0.5 nm, from
uncertainties of the spectral UV measurements performed          290 to 325 nm (Brewer #016) and from 287.5 to 363 nm
with such an instrument can be found e.g. in Fountoulakis        (Brewer #178). For wavelengths above 325 nm (363 nm,
et al. [63] or Diémonz et al. [64]. For the Dortmund data        respectively), the irradiance values are extrapolated using
set, the diffuser temperature was not corrected as it was not    a theoretical spectrum [67, 68] weighted by the intensity at
recorded. However, due to diffuser heating, the temperature      325 nm (363 nm, respectively). The measurement interval
is stabilized above the change point of the diffuser [65].       is around 30 min, a frequency typically used in the Brewer
On-site audits with the world reference QASUME were              network [66]. Thus, the ­UVImax according to WHO specifi-
not performed. However, the 1000W lamp (LDU 100 H),              cations is calculated directly from the daily maximum value.
used to check and re-calibrate the working standard in Dort-     Brewer #016 and Brewer #178 are calibrated each second
mund, was directly calibrated against the national standard      year against a NIST traceable 1000W DXW lamp. Each
at the National Metrology Institute (PTB) and periodically       month, the stability of the UV spectral observations of the
checked/re-calibrated every few years (expanded uncertainty      instruments is checked with 50 W UV lamps, i.e., that it
of the lamp in the certificates < 1.5%). The PTB-traceable       is checked that the UV measurements stay within or better
calibration of the measurement system with the working           than ± 5% uncertainty with respect to the last calibration. If
standard was conducted at least once a year and was identi-      the uncertainty becomes larger than ± 5%, a new UV cali-
cal over the entire period. The radiometric uncertainty (esti-   bration file is made, taking into account the last UV lamp
mated to be < 2.0% expanded) is approximately randomly set       checks. A total standard uncertainty of ± 5% can therefore
during calibrations.                                             be assumed for the Uccle UV time series (including corre-
   In the German solar UV monitoring network, different          lated and uncorrelated contributions). The instruments were
wavelength steps from 290 to 450 nm are used at all stations     compared to the world traveling reference unit QASUME in
with double monochromators. Table 1 shows the steps of
spectral wavelength. The high resolution in the range of the     Table 1  Spectral wavelength steps of the double monochromator sys-
393er Fraunhofer lines allows the wavelength accuracy of         tem in Dortmund
each spectrum to be monitored. The high resolution at the
                                                                 Wavelength Range[nm]      Measurement Step [nm]      Note
ozone edge enhances the measurement accuracy in the UVB
range. The UV spectra are measured at intervals of 6 min.        290–320                   0.5                        ozone edge
   In considering daily values (e.g. UVB daily radiant expo-     320–390                   5
sure) in this configuration, the total uncertainty of meas-      392–394                   0.075                      distinctive
urements is estimated to be approximately 2.5% (expanded)                                                               Fraunhofer
                                                                                                                        lines
after data processing (Sect. 2.4). This is significantly lower
                                                                 395–450                   5
than a worst-case total uncertainty of a measurement of a
                                                                                         Photochemical & Photobiological Sciences

2004 [69]. For this study, data from Brewer #016 were used        Together with the calibration data, erroneous spectra
when available. Otherwise data from the in-parallel measur-    were subsequently corrected wherever reliably possible.
ing Brewer #178 were used. Thus, after 2002 data gaps only     The UVA irradiance, UVB irradiance and erythemal
occurred if both instruments were down at the same time.       irradiance were calculated from the remaining spectra.
                                                               The resulting daily courses for approximately 9000 days
2.3 Global radiation, sunshine duration and ozone             (from 1996 to 2022) were screened individually to iden-
                                                               tify system failures in the course of the day that would
Additional datasets of global radiation (GR), sunshine         lead to errors in the calculation of the U  ­ VImax or a daily
duration (SunD) [70] and TCO were investigated to bet-         integral. ­UVImax is the daily maximum of a 30-min time
ter understand the potential main drivers of trends in         average value of the erythemal irradiance [11]. For bet-
solar UV radiation (TCO, clouds, aerosols). In contrast        ter comparability of the ­U VI max values, the ­U VI max is
to UVB radiation values, and consequently erythemal            used with decimal places. For ­UVImax values, the rejected
radiation values, GR is largely unaffected by current          values are mainly on days with missing measurement
TCO levels but is primarily influenced by factors, such        at midday. To minimize the exclusion of correct data
as aerosol optical depth (AOD) and cloudiness. SunD, on        and maximize the exclusion of calculation errors, no
the other hand, is mainly influenced by cloudiness alone.      fixed interruption time was chosen for exclusion. Each
For the location Dortmund, a GR and SunD data set was          interruption was considered individually based on the
used measured by the DWD at a meteorological station           prevailing weather conditions, especially clouds. On
(DWD ID 1117) in the city of Bochum (10 km from the            cloudless days, the U ­ VI max can be reliably calculated if
UV monitoring station). The data set includes data of          only spectra at the sun's zenith ± 20 min are available.
the hourly sum of global radiation in J/cm 2 and data of       On days with broken clouds, this time period had to be
hourly sunshine duration in minutes. For the location          significantly extended.
Uccle, a global radiation data set is used detected by the        During data processing, it was found that the measure-
KMI at the same location as the UV data. The measuring         ments in Dortmund started irregularly after sunrise in the
interval of the global radiation in Uccle is 10 min.           first years of the measurement series. Therefore, the daily
   The TCO values from the Tropospheric Emission               erythemal radiant exposure ­( H er,day) was only calculated
Monitoring Internet Service (TEMIS) are used for the           for the period from 1.5 h after sunrise to 1.5 h before
parameter ozone. The TEMIS data set provides the local         sunset on all days of the time series (the 1.5 h correspond
solar noon ozone from a Multi-Sensor Reanalysis MSR-2          to a sun elevation of around 10° above the horizon). The
(v2.0–2.2) [71, 72]. The data are available for both loca-     integral limits ensure that the daily integrals of the indi-
tions and without gaps over the entire analysis period.        vidual years are comparable over the entire measurement
                                                               period. In case of interruptions, it was decided on a case-
2.4 Data processing                                           by-case basis whether the data could be used, e.g. based
                                                               on the prevailing cloud conditions. In the Uccle data set,
For data processing of the Dortmund data set, various          the daily U­ VI max and the H
                                                                                           ­ er,day are rejected when there
quality checks were performed by BfS to identify wave-         was an interruption of 2 h or more of the measurements
length shifts, irradiance deviations, calibration errors and   between sunrise and sunset. The values of H     ­ er,day in this
other technical failures and measurement errors: First,        study are given in Standard Erythemal Doses (SED) [12].
all approximately 1 million spectra were checked for           One SED corresponds to an erythemal radiant exposure
wavelength shift compared to the Fraunhofer lines. A           of 100 J/m 2.
limit of ± 0.15 nm was set as the permissible deviation.          A plausible check was performed for global radiation
In addition, various wavelength ratios were checked over       and sunshine duration values of Dortmund, before they
the course of the day and year to find wavelength shifts       were used. In case of erroneous values or interruptions,
in the spectra outside the Fraunhofer line regions. The        all values of the day were rejected. The daily maximum
calibration data were evaluated to identify irradiance         of global radiation ­( GR max ) and the daily integral of
deviations. An imputation method described by Heinzl           Global radiation ­(GRint) and sunshine duration were cal-
et al. [73] supports the search for deviations from the        culated from the remaining data set. For Dortmund, G      ­ Rint
irradiance calibration between calibration steps and the       and sunshine duration values were calculated analogous
retrospective check of the calibrations. In addition, dark     to the UV data by integration from 1.5 h after sunrise to
current and scan duration parameters were evaluated for        1.5 h before sunset. The calculated daily sunshine dura-
anomalies to identify further technical failures and meas-     tion values are given in hours. For Uccle, the 10-min
urement errors.                                                interval of global radiation values allows the calculation
                                                               of ­G R max analogous to the U ­ VI max based on a 30-min
Photochemical & Photobiological Sciences

average. The ­GR int was set from sunrise to sunset which              annual mean values in Sect. 4.1.6 and 4.1.7, where inclusion
corresponds to the calculation of the ­H er,day in Uccle.              of imputed data is necessary to avoid a bias.

2.5 Handling data gaps                                                3.1.1 Definition of normal, low and high ozone days

 After data processing, data gaps for both U   ­ VImax and H­ er,day   Low ozone has been defined differently in previous stud-
 occur on around 12% of the days in the Dortmund. In Uccle,            ies [46, 59–62, 74–76]. In this study, the annual course of
­UVImax values were missing for around 1% of days in the               ozone and threshold for low/high ozone is calculated with
 period from 1997 to 2022 (1991–2022: 4%) and H       ­ er,day val-    a simplified approach based on total column ozone values
 ues for around 3% of days (1991–2022: 11%). To fill the data          from 1996 to 2022: For each day of the year, the median,
 gaps of U
         ­ VImax, ­Her,day, and daily integral of UVB irradiance,      the average and the standard deviation σ are calculated from
 the validated mixed imputation method [73] is used with               the respective day and all values from the three days before
 TCO und global radiation as predictors. For the imputation            and three days after. The statistics for each day of the year
 in case of UVA irradiance gaps, only global radiation was             are based on approx. 190 TCO values. The annual curves
 used as predictor because the influence of ozone on UVA               calculated in this way are shown in Fig. 1 together with the
 irradiance is negligible. For trend analysis of global radia-         ozone values of all years.
 tion and sunshine duration, gaps in the data sets of these               A resulting average ± σ curve is smoothed and serves as
 values were filled by an average-imputation method [73].              a threshold curve for low/high ozone values. Ozone val-
                                                                       ues between smoothed average ± σ are defined as normal,
                                                                       low ozone values as values lower than average-σ and high
3 Methods                                                             ozone values as values exceeding average + σ. The resulting
                                                                       low ozone threshold curve corresponds approximately the
3.1 Descriptive analysis                                              threshold curve described by Fragkos et al. [74]. For a fre-
                                                                       quency analysis, the term very low ozone is used to describe
The descriptive analysis is focused to characterize the local          low ozone values below average-2σ (Fig. 1, red dashed line).
conditions and correlations of the parameters at the station
in Dortmund. It describes the underlying values for the trend
analysis and gives a comparison of the Dortmund und Uccle
data set. Data without imputation of gaps were used in the
descriptive analysis. An exception is the calculation of the



Fig. 1  Annual course of total
column ozone in Dortmund
calculated from TEMIS values
of 1996–2022 (blue dots): mean
(black line), median (orange
line), mean ± σ (blue lines) and
smoothed mean ± σ (red lines)
used as low/high ozone thresh-
old curve
                                                                                                 Photochemical & Photobiological Sciences

3.1.2 Determination of annual course of potential highest            3.2 Trend analysis
       values
                                                                      We investigated the trend of UV data, global radiation, sun-
 The annual courses of potential highest daily values of              shine duration and total column ozone using a linear model,
­UVImax and ­Her,day, global radiation and sunshine duration          as it allows us to derive a simple, but quantitative statement
 represent a sort of cloudless annual profile, which was cal-         of a trend. The trend analysis was performed on the imputed
 culated on the basis of the long-term measurement dataset.           data set for the parameters U  ­ VImax, ­Her,day, TCO, global
 To determine the annual courses of potential highest val-            radiation ­(GRmax, ­GRint), sunshine duration, daily integral
 ues, an envelope of all annual courses from 1997 to 2022 is          of UVA and UVB, and ratio of daily integral UVA to UVB.
 created by identifying the highest measured value for each              The trend analysis is based on monthly values as in other
 specific day of the year across all years. The resulting curve       studies (e.g. [37]). In the proposed linear model, called
 is then smoothed to filter out the outlier-days and the days on      ‘BfS trend model’ in the following, the monthly mean yt
 which there was no cloudless day in all years. To determine          of month t (e.g. of ­UVImax) increases linearly by 𝛽1 per
 the envelope of ­UVImax and ­Her,day values, only days with          month, starting at an initial level 𝛽0 . The seasonal fluctua-
 normal ozone are considered to analyze the impact of the             tions around the general linear trend are modelled using the
 normal ozone annual course and low ozone events on the               effect-coded monthly variables Jant,…,Novt and the corre-
 UV data separately. For global radiation (­ GRint, ­GRmax) and       sponding regression coefficients 𝛽2 , ⋯ , 𝛽12 . The error vari-
 sunshine duration, all days are taken for the calculation. The       able 𝜀t describes the deviation from this pattern for a specific
 daily ratio of actual ­GRint values to a potential highest ­GRint    month.
 value serves as indicator for a cloudiness for a specific day.
 It has to be remarked that limiting the daily integral from
                                                                      yt = 𝛽0 + 𝛽1 ∙ t + 𝛽2 ∙ Jant + ⋯ + 𝛽12 ∙ Novt + 𝜀t             (1)
 1.5 h after sunrise to 1.5 h before sunset leads to an offset of         Instead of assuming uncorrelated errors or autocorrelated
 3 h to the total day length for sunshine duration and an aver-       errors of the order 1 (e.g. [78, 79]), we used a linear trend
 age annual deviation of 1–2% for ­Her,day values. This offset        model that provides a heteroskedasticity and autocorrelation
 also reduces the annual average for G    ­ Rint by 3.2%, with a      consistent estimation of the covariance matrix implemented
 standard deviation of just 0.1% for all years of the period.         in the package ‘sandwich’ for the software R by Zeileis [80]
                                                                      to address heteroscedasticity and autocorrelation in the UV
3.1.3 Correlation analysis over the course of the year               data. The complete deduction of the linear model and covari-
                                                                      ance matrix can be found in the appendix. Student’s t test
The correlation coefficients of ­UVImax to total column               for a non-zero trend was used for analysis. Since the t test
ozone, ­GRmax and sunshine duration and of H      ­ er,day to total   is robust against deviations from the normal distribution for
column ozone, ­GRint and sunshine duration were calculated.           more than 30 observations, and this condition is satisfied
To analyze the correlations of the variables under all-sky            with more than 300 months, a violation of the normal dis-
conditions, the correlation coefficients were calculated              tribution assumption is acceptable.
separately for each day of the year. The resulting correla-               Results are presented as trend per decade
tion coefficients over the course of the year are nearly inde-        (10 years ∙ 12 month ∙ 𝛽 1) related to the mean value of the
pendent of annual course of solar elevation. The correlation          analyzed time period to provide stability against year-to-year
calculation on each day of the year is based on data from             fluctuations. Additionally, as a reference-independent trend
the respective day (for all years), plus the data from 5 days         result, we also report the absolute trend per decade.
prior and 5 days afterward (for all years). For example, to
calculate the correlations on September 4th, all available
values from August 30th to September 9th from the years
between 1996 and 2022 are included. The range of ± 5 days             4 Results
was chosen to suppress sufficiently the annual influence of
the solar elevation with short period, but still be able to make      Measured UV data from approximately 8400 days at the Dort-
a well-founded correlation statement with enough data. Due            mund station, over a period from August 1996 to December
to the long series of measurement data, each individual cal-          2022, were used for analysis (Fig. 2a, daily ­UVImax values
culation of the correlation coefficient is therefore based on         (left) and ­Her,day values (right)). Occurring data gaps are une-
180–291 days. The exact number varies due to gaps in the              venly distributed and vary in length. To avoid bias due to these
data sets. For interpretation, a correlation classification by        gaps, a data set with imputed data (Fig. 2b) is used for the
Hinkle et al. [77] was used.                                          trend analyses and the calculation of the annual mean values
                                                                      in Sects. 4.1.6 and 4.1.7. Since the incomplete year 1996 could
Photochemical & Photobiological Sciences




Fig. 2  Heatmap of U ­ VImax values (left) and H ­ er,day values (right)   to the WHO UV Index color scale [6, 11], ­Her,day values are displayed
based on measured data from Dortmund, a without imputation of              using a continuous color scale. 97% of the imputed values are derived
missing values and b after imputation of missing values. Each row          from available TCO and GR values (model-based imputation), just
corresponds to a single year, and within each row, the colored lines       3% from statistical means (average-based imputation) [73]
depict the daily values. The U
                             ­ VImax value colors are chosen according


also lead to a bias in the annual values and trend analysis, data          4.1 Descriptive analysis
from January 1997 onwards are used for these analyses.
                                                                           4.1.1 Monthly distribution of UV data and annual
                                                                                  frequency of ­UVImax and ­Her,day

                                                                           Box plots and density estimates for daily ­H er,day values
                                                                           (Fig. 3) and ­U VI max values (Fig. 4) grouped by month
                                                                                       Photochemical & Photobiological Sciences

demonstrate that the highest values in Dortmund occur in       Dortmund and Uccle datasets, only the monthly mean for
the months of June and July, strongly correlated with solar    the Uccle data is illustrated as a grey curve in Fig. 3 and
elevation. At greater solar elevation, an increased abso-      Fig. 4. For both locations, on average 83% of the annual
lute dispersion can be observed. The H ­ er,day and U
                                                    ­ VImax    cumulative ­H er,day is detected from April to September.
datasets from Uccle have a similar monthly distribution.      ­UVImax values ≥ 3 (2.5) occur mainly (94%) between April
Consequently, for comparative purposes between the             and September.

Fig. 3  Daily erythemal radiant
exposure ­Her,day from Dort-
mund 1996–2022 grouped in
months, presented as box plots
(box: interquartile range, black
lines: median, crosses: mean,
Whisker: minimum and maxi-
mum data distribution within
1.5 times the interquartile
range) with density estimates;
Grey curve: monthly mean
of ­Her,day values from Uccle
1996–2022. The statistics are
based on 600–800 values for
each month




Fig. 4  UVImax values from
Dortmund 1996–2022 grouped
in months, presented as box
plots (box: interquartile range,
black lines: median, crosses:
mean, Whisker: minimum and
maximum data distribution
within 1.5 times the inter-
quartile range) with density
estimates; grey curve: monthly
median of ­UVImax values from
Uccle 1991–2022 for compari-
son




Fig. 5  UVA daily radiant
exposure values (315–400 nm)
from Dortmund 1996–2022
grouped in months, presented
as box plots (box: interquartile
range, black lines: median,
crosses: mean, Whisker:
minimum and maximum data
distribution within 1.5 times the
interquartile range) with density
estimates
Photochemical & Photobiological Sciences

Fig. 6  UVB daily radiant
exposure values (290–315 nm)
from Dortmund 1996–2022
grouped in months, presented
as box plots (box: interquartile
range, black lines: median,
crosses: mean, Whisker:
minimum and maximum data
distribution within 1.5 times the
interquartile range) with density
estimates




                                                                           Corresponding plots for daily integral of UVA (Fig. 5)
                                                                        and UVB (Fig. 6) show a similar behavior in the annual
                                                                        course compared to ­Her,day. The Ratio of UVA to UVB
                                                                        (Fig. 7) highlights the differences between these values.
                                                                           The proportion of UVB radiation in UVR is three times
                                                                        higher in summer than in winter and remains relatively
                                                                        constant from May to September. The annual course is
                                                                        asymmetrical to the summer solstice and shifts toward later
                                                                        months (Fig. 7).
                                                                           From the annual frequency of daily U ­ VImax values (Fig. 8
                                                                        left), it can be seen that approximately half of the days in
                                                                        Dortmund have a U    ­ VImax value equal to or less than 2.
                                                                        Days with ­UVImax values of 3, 4, 5, or 6 occur with roughly
                                                                        equal frequency. The number of days with a ­UVImax 7 is
                                                                        significantly lower, and days with a ­UVImax of 8 are rare.
                                                                        The frequency analyses of ­Her,day, shows that approximately
Fig. 7  Ratio of monthly mean daily radiant exposure UVA (Fig. 5) to    one-third of the days fall into the lowest range of 0–5 SED
monthly mean daily radiant exposure UVB (Fig. 6)                        (Fig. 8 right), which corresponds to the number of days with




Fig. 8  Mean annual daily ­UVImax (left) and ­Her,day (right) frequency of Dortmund with error bars representing the annual minimum and maxi-
mum of occurred number of days from 1997 to 2022
                                                                                                          Photochemical & Photobiological Sciences




Fig. 9  Time series of the annual U
                                  ­ VImax (left) and ­Her,day (right) frequencies of Dortmund from 1997 to 2022 calculated with imputed data set


­UVImax value 0 and 1 (Fig. 8 left). More detailed yearly-                   sunrise to 1.5 h before sunset. The course sunshine duration
 resolved frequencies of ­UVImax and H­ er,day are illustrated in            and global radiation are correlated with the solar elevation
 the Fig. 9. Despite year-to-year variation, a slight tendency               resulting in a symmetrical curve to the summer solstice.
 of increasing number of days with higher U  ­ VImax and H ­ er,day          The course of the potential highest ­Her,day is additionally
 is visible.                                                                 shifted towards later months. The annual course of median
                                                                             of ozone shows an increase in ozone values between October
4.1.2 Annual course of potential highest values                             and March, and a decrease between April and September
                                                                             (Fig. 10, blue line). The ratio of the actual global duration on
The annual courses of potential highest H ­ er,day values under              a day in relation to the maximum potential global duration
normal ozone condition in Dortmund are given in Fig. 10.                     on this day is used as a parameter for cloudiness in further
For comparison, the annual courses of the potential highest                  analyses.
daily sunshine duration and the potential highest daily global                  The corresponding plot for the annual course of the
radiation ­(GRint) are included in the diagram. It has to be                 potential highest values of daily ­UVImax, sunshine dura-
remarked that all daily values are integrals from 1.5 h after                tion, global radiation ­(GRmax) and median of total column




Fig. 10  Annual courses of potential highest daily values at normal          ­(GRint) (grey line, first right scale) and the annual course of median
ozone conditions for ­Her,day (orang line, left scale), the sunshine dura-    of ozone according 3.1.1 (dark blue line, second right scale). Summer
tion (SunD) (red line, third right scale), and the daily global radiation     solstice is marked by a vertical line
Photochemical & Photobiological Sciences




Fig. 11  Annual courses of potential highest daily values at normal          grey line, first right scale) and the annual course of median of total
ozone conditions for U­ VImax (colored bars, left scale), sunshine dura-     column ozone according 3.1.1 (blue line, second right scale)
tion (SunD, red line, third right scale), daily global radiation (­ GRmax,



ozone is shown in the Fig. 11. The annual course of G­ Rmax                  4.1.3 Correlation analyses of ­Her,day und UVI with other
values is approximately symmetrical to the summer sol-                              variables
stice, whereas the U­ VImax curve is shifted towards later
months. Additionally, a slight attenuation of ­GRmax values                    Figure 12 visualizes the correlation results of ­Her,day and
from June to September and a slight increase in the pre-                     ­UVImax values, respectively, with other variables as the
ceding months can also be observed in the Uccle data and                       course of the year. H
                                                                                                   ­ er,day (Fig. 12, left) and global radiation
does not occur in the ­GRint curve (Fig. 10). The causes of                   ­(GRint, blue dots) show a constant very high correlation in
these variances were not investigated in this study.                           the summer months, which is also still high to a very high
                                                                               in the winter months. The correlation of ­Her,day with the sun-
                                                                               shine duration (red dots) is lower but still high. The expected




Fig. 12  Correlation coefficients of ­Her,day (left) and ­UVImax (right) values with sunshine duration (SunD), global radiation and total column
ozone as a course of a year based on data set from the location Dortmund in the period 1996 to 2022 at all-sky-conditions
                                                                                                 Photochemical & Photobiological Sciences

                                                                        year. ­UVImax (Fig. 12, right) shows a constant high correla-
                                                                       tion with the daily maximum values of the global radiation
                                                                       ­(GRmax, blue dots) and a lower but still moderate to high cor-
                                                                        relation with the daily sunshine duration (red dots). Under
                                                                        the considered all-sky conditions, the correlation of ­Her,day
                                                                      and ­UVImax values with TCO is low and even negligible in
                                                                        the winter months. Correlation of sunshine duration to daily
                                                                        UVA and UVB radiant exposure is high / very high on most
                                                                        days between March and September (Fig. 13). The correla-
                                                                        tion of sunshine duration to UVB is slightly lower than to
                                                                        UVA. If the correlation coefficients of ­Her,day to sunshine
                                                                      duration from Fig. 12 were plotted in Fig. 13, the values
                                                                      would, as expected, fall between those of UVA and UVB.
                                                                           When plotting all H ­ er,day and U
                                                                                                            ­ VImax values from Dort-
                                                                      mund against each other in a scatterplot and marking each
                                                                      value with a color according to the prevailing cloudiness on
Fig. 13  Correlation coefficients of sunshine duration (SunD) with    that day (Fig. 14), it can be observed that days with low or
daily UVA and UVB radiant exposure as a course of a year based on     no cloudiness (red dots) are at the upper boundary of the
data set from the location Dortmund in the period 1996–2022 at all-
sky-conditions                                                        pattern and show an approximate linear relationship between
                                                                      ­Her,day and ­UVImax. It also shows, that on days with UVI-
                                                                        max < 3, ­Her,day values can exceed 10 SED on some days.
differences arise because SunD only indicates whether a
cloud is between the measuring device and the sun (binary             4.1.4 Condition for highest values of ­UVImax and ­Her,day
response for direct solar radiation). GR, in contrast, can also
indicate how much solar radiation passes through a cloud              Examining the main influencing factors (solar elevation,
and how much diffuse solar radiation reaching the measur-             total column ozone and global radiation) for the days of
ing device. Consequently, the correlation between GR and              the 200 highest H ­ er,day values in the entire measurement
­Her,day is stronger. Variability in cloud cover, compounded by       series from Dortmund (approximately 9000 days), it can be
 shorter day lengths in winter, can lead to differences in the        observed that on these days high solar elevation, low ozone
 correlation coefficient of SunD to UV values throughout the          levels, and low cloud cover coincide:


Fig. 14  Scatterplot of ­Her,day
 and ­UVImax values measured at
 Dortmund (1996–2022) with
 colored dots indicating cloudi-
 ness by the ratio of the actual
 global radiation ­(GRint) to the
calculated daily potential high-
est global radiation (Fig. 10).
Higher values of the ratio (red
dots) correspond to cloudless
conditions, while lower values
(blue dots) indicate overcast
skies. The vertical line in
the plot marks the range of
­UVImax ≥ 3
Photochemical & Photobiological Sciences

• On 93% of these days, there was below-average ozone                  4.1.5 Low ozone events
  (ozone < annual mean total column ozone level).
• On 42% of these days, there was even low ozone                       Low ozone events can significantly increase ground-level
  (ozone < annual mean-σ total column ozone level).                    solar UVR, especially in absence of clouds. Figure 15 pre-
• On 90% of these days, the ratio of actual global radiation           sents ­UVImax values for selected periods in Dortmund, dur-
  ­(GRint) to potential highest global radiation is higher than        ing which these low ozone events occurred. At similar solar
  87%.                                                                 elevation, the ­UVImax values increase with increasing nega-
• 99% of these days occurred between 30 days before and                tive deviation from the ozone mean value. The exemplary
   41 days after the summer solstice.                                  low ozone events shown in Fig. 15 ranged from 10 to 19%
                                                                       in the months from April to July. For the low ozone event in
   For the 200 highest ­UVImax values, the conditions regard-          February 2023, an increase of 53% is detected. A separate
ing ozone and the distance of the days to the summer solstice          plot for Uccle has been omitted because, within the limits of
are nearly identical to the highest ­Her,day days. Additionally,       measurement accuracy, the increases in ­UVImax are identical
the ratio of actual global radiation (­ GRmax) to potential high-      at low ozone events with comparable cloudiness.
est global radiation is higher than 85% on 90% of days with                Observing the frequency of days with low ozone (mean
the highest ­UVImax.                                                   -σ) in the radiation protection-relevant summer months
   The distribution of days with the highest 200 UV val-               (Apr–Sept) with the condition of little to no clouds at mid-
ues across the first half (1997–2009) and second half                  day (global radiation ­GRmax > 90%) in Dortmund, it can be
(2010–2022) of the data series is as follows: Of the days              seen that in the second half of the period (2010–2022) there
with the highest ­UVImax values, 98 occurred in the first half         occur about 8% more days (165 days) than in the first period
and 102 in the second half. Regarding the days with the                (1997–2009: 153 days). If we focus only on the days with
highest ­Her,day values, 87 occurred in the first half and 113         very low ozone (mean-2 σ), their frequency increases from
in the second half.                                                    6 days (1997–2009) to 16 days (2010–2022).




Fig. 15  Daily ­UVImax values (colored bars) for exemplary low ozone   of these days with the number of standard deviations below mean
events separated by dashed lines; percentage increase of the high-     according to 3.1.1 (blue), and the year of the occurring low ozone
est ­UVImax value within each period relative to the potential high-   event
est ­UVImax value (Fig. 11), and respective total ozone column value
                                                                                                        Photochemical & Photobiological Sciences

4.1.6 Annual mean of ­Her,day compared to GR and TCO                      For both stations, annual values of H ­ er,day, ­UVImax, summer
                                                                           TCO (Apr–Sept), and global radiation ­(GRint) were com-
Ground-level solar UV values and global radiation, as well                 pared (Fig. 17).
as atmospheric ozone levels, exhibit year-to-year fluctua-                    It can be observed that all annual values from both loca-
tions. To address the question of whether years with high                  tions are generally in the same level. The differences occur-
global radiation and/or low ozone levels correspond to high                ring in ­Her,day in a few years are also visible in the global
annual UV radiation, the annual values of ­Her,day (red bars),             radiation data in the same years. Black circles highlight peri-
global radiation (­GRint, black line) and TCO (blue line,                  ods where global radiation and ­Her,day in Dortmund exceeded
inverted scale) are compared (Fig. 16). For the ozone data,                Uccle, green circle indicates an exemplary period during
the annual median of daily summer ozone values (Apr–Sept)                  which global radiation and ­Her,day in Uccle exceeded Dort-
is chosen since the majority of annual UVR occurs in the                   mund. The annual ozone data from Dortmund und Uccle
summer and thus the ozone values in summer have a greater                  differ hardly.
influence on annual UVR.                                                      To illustrate the impact of the different measurement
   The comparison shows that in years with exceptionally                   intervals (6 min in Dortmund, approx. 30 min in Uccle)
low ozone values, the annual H   ­ er,day increases significantly.         on ­UVImax data, the dashed blue line represents the annual
This can be seen comparing the years 2018 and 2020: In                     mean values from Dortmund based on a 30-min analysis.
2018, the annual mean of global radiation exceeds that of                  On average, this adjustment results in a 1.7% increase in
2020, implying higher H­ er,day values in 2018. Due to the very            the annual U­ VImax values from Dortmund. To illustrate the
low ozone levels in 2020, the ­Her,day values for that year were           difference between annual summer TCO values and annual
additionally elevated and exceed the values of 2018. Even in               TCO values (all month), the latter are additionally plotted
years with above-average ozone levels, the ozone influence                 for Dortmund with a dashed blue line.
is discernible. For instance, in the year 2010, the annual
value of H
         ­ er,day decreases, contrary to expectations based                4.2 Trend analyses
solely on global radiation.
                                                                           The trend analysis is based on monthly mean values of
4.1.7 Station comparison                                                  imputed data. Correcting the data gaps with imputed
                                                                           data (Fig. 2) results in remarkable changes for some of
After comparing the annual mean values of ­Her,day from                    the monthly means (Figs. 18 and 19, grey and numbered
Dortmund to the influence factors global radiation and ozone               circles). The linear trend is visualized with a dashed red
in chapter 4.1.6, the next step involves comparing data from               line and shows an increase over the 26 years. The seasonal
Dortmund and Uccle. This aims to identify differences in                   course around the trend with the highest value in June and
annual UV radiation values and investigate how differences                 the lowest value in December is shown by a solid red line.
can be traced back to differences in the influencing factors.              Years with low (e.g. 1998, 2007, 2012) and high (e.g. 2003,




Fig. 16  Time series of annual mean of ­Her,day in Dortmund (red bars), annual mean of the daily global radiation ­(GRint, black line) and annual
median of summer ozone values (Apr–Sept, blue dashed line, inverted scale)
Photochemical & Photobiological Sciences

Fig. 17  Time series comparison
of annual mean values from
Dortmund (blue line) and Uccle
(red lines) of ­Her,day, daily
  ­UVImax values with additional
 ­UVImax values from Dortmund
  based on 30 min data (blue
  dashed line), annual median
  of TCO considering summer
  months (Apr–Sept, inverted
  scale) with additional annual
  TCO values (all month, blue
  dashed line) and annual mean
  of daily global radiation ­(GRint);
Black circles highlight periods
where global radiation in Dort-
mund exceeded that in Uccle,
while a green circle indicates
an exemplary period during
which global radiation in Uccle
exceeded that in Dortmund.
Annual mean values for both
­Her,day and ­UVImax include
imputation data for data gaps
for both stations




2006, 2022) monthly means of ­Her,day and ­UVImax in summer    months (Fig. 3, Fig. 20 in Appendix), demonstrating heter-
clearly stand out.                                             oskedastic behavior.
   The estimated autoregressive order and the results of the
Durbin–Watson test confirm that the monthly means of the       4.2.1 Trend results
UV data, even after considering the trend and seasonal pat-
tern, are autocorrelated. In addition, the dispersion of the   Table 2 presents the trend results for ­UVImax and ­Her,day in
UV data in the summer months is higher than in the winter      Dortmund and Uccle for the period 1997–2022 (26 years)
                                                                                             Photochemical & Photobiological Sciences

Fig. 18  Monthly means of
­Her,day from Dortmund based
on partially missing daily
values (grey circles) and based
on partially imputed daily
values (numbered circles;
number = month); model fit
(solid red line) and linear trend
(dashed red line) for monthly
means based on partially
imputed daily values




Fig. 19  Monthly means of
­UVImax from Dortmund based
 on partially missing daily
 values (grey circles) and based
 on partially imputed daily
 values (numbered circles;
 number = month); model fit
 (solid red line) and linear trend
 (dashed red line) for monthly
 means based on partially
 imputed daily values




Table 2  Trend analysis results      Location                Dortmund              Uccle                      Uccle
for ­UVImax and ­Her,day (SED)
for Dortmund and Uccle with          Period                  1997–2022 (26y)       1997–2022 (26y)            1991–2022 (32y)
imputation at data gaps and BfS
trend model with standard error                              UVImax     Her,day    UVImax       Her,day       UVImax       Her,day
and 95% confidence interval
                                     Trend p. decade   abs   0.09       0.62 SED   0.16         0.94 SED      0.16         0.70 SED
(CI)
                                     Trend p. decade   [%]   3.2        4.9        5.8          7.5           5.6          5.6
                                     Standard error    [%]   1.4        1.8        1.0          1.5           0.8          1.1
                                     95% CI            [%]   0.4–6.0    1.4–8.4    3.7–7.8      4.6–10.4      4.0–7.2      3.5–7.8
Photochemical & Photobiological Sciences

Table 3  Trend analysis results for daily UVA and UVB radiant expo-                  intervals, the trends can be considered similar. Comparing
sure for Dortmund with imputation at data gaps and BfS trend model                   the different periods (1997–2022 vs 1991–2022) for Uccle
with standard error and 95% confidence interval (CI)
                                                                                    ­UVImax the trend for ­UVImax are nearly constant (5.8% vs
Location                     Dortmund                                                5.6%) while the trend for ­Her,day drops from 7.5% to 5.6%.
Period                       1997–2022 (26y)                                         Repeating the analysis with the data without imputation for
                                                                                     missing data shows a slightly higher increase compared to
                             UVA                 UVB            UVA/UVB
                                                                                     the results with imputed data (see Table 5). Using the stand-
Trend p. decade      abs     35.8 kJ/m2          335 J/m2       2.8                  ard linear model on these data, results demonstrate the same
Trend p. decade      [%]     6.2                 3.5            3.1                  percentage increase but the 95% CI is significantly smaller
Standard error       [%]     1.5                 1.7            1.0                  (see Table 6).
95% CI               [%]     3.2–9.3             0.2–6.9        1.2–5.1                 In addition to ­UVImax and ­Her,day, trends in the daily
                                                                                     radiant exposure of UVA (315 nm to 400 nm) and UVB
                                                                                     (290 nm to 315 nm), and the ratio of UVA to UVB radiant
and additionally for Uccle from 1991 to 2022 (32 years).                             exposure were analyzed for Dortmund. Significant increases
All trend analyses indicate statistically significant increases                      were found for both, with the UVA daily radiant exposure
for ­UVImax and H
                ­ er,day as the corresponding 95% confidence                         increasing almost twice as much as the UVB daily radiant
intervals lie above zero. The observed trends are larger                             exposure (Table 3). This is also reflected in the rise of the
for Uccle than for Dortmund, and larger in H     ­ er,day than in                    UVA-to-UVB ratio.
­UVImax. However, considering the overlap of the confidence

Table 4  Trend analysis results for monthly mean values of global                   Sept) for Dortmund with BfS trend model based on monthly mean
radiation ­(GRint, ­GRmax), daily sunshine duration (SunD) and total                with standard error and 95% confidence interval (CI)
column ozone (TCO) for all month and for summer months (Apr–
Location                            Dortmund
Period                              1997–2022 (26y)
                                    GRmax               GRint                  SunD              SunD (Apr-Sept)        TCO             TCO (Apr-Sept)

Trend p. decade       abs           4.64 kWh/m2         46.3 kWh/m2            0.46 h            0.66 h                 0.35 DU*        -2.98 DU
Trend p. decade       [%]           3.0                 4.6                    11.3              11.1                   0.1*            -0.9
Standard error        [%]           0.9                 1.5                    2.3               2.5                    0.5             0.4
95% CI                [%]           1.1–4.8             1.6–7.7                6.7–15.9          6.2–16.1               –0.8–1.1        – 1.75–( – 0.03)

Not significant trends are marked with *


Table 5  Trend analysis results         Location                          Dortmund                    Uccle                        Uccle
for ­UVImax and ­Her,day for
Dortmund and Uccle without              Period                            1997–2022 (26y)             1997–2022 (26y)              1991–2022 (32y)
imputation at data gaps (Fig. 2a)
and BfS trend model based on                                              UVImax       Her,day        UVImax       Her,day         UVImax     Her,day
monthly mean with standard
                                        Trend p. decade         abs       0.10         0.71 SED       0.16         0.102 SED       0.16       0.99 SED
error and confidence interval
(CI)                                    Trend p. decade         [%]       3.7          5.6            5.8          8.1             5.7        8.0
                                        Standard error          [%]       1.5          1.8            1.0          1.6             0.8        1.3
                                        95% CI                  [%]       0.8–6.6      1.9–9.2        3.7–7.8      5.0–11.3        4.1–7.3    5.5–10.5



Table 6  Results of a standard          Location                           Dortmund                     Uccle                       Uccle
                  ­ VImax and
trend analysis of U
­Her,day for Dortmund and Uccle         Period                             1997–2022 (26y)              1997–2022 (26y)             1991–2022 (32y)
without imputation at data gaps
(Fig. 2a) and standard linear                                              UVImax         Her,day       UVImax       Her,day        UVImax       Her,day
trend model based on monthly
                                        Trend p. decade         abs        0.10           0.71          0.16         1.02           0.16         0.99
anomalies with standard error
and confidence interval (CI)            Trend p. decade         %          3.7            5.6           5.8          8.1            5.7          8.0
                                        Standard error          %          0.9            1.2           0.7          1.1            0.5          0.9
                                        95% CI                  %          1.9–5.4        3.2–7.9       4.4–7.1      5.9–10.3       4.7–6.7      6.1–9.7
                                                                                                 Photochemical & Photobiological Sciences

   Trends in the additional variables for the period                  Vienna [29]. The main contributing factors to these differ-
1997–2022 in Dortmund were analyzed (Table 4). A signifi-             ences are primarily latitude and varying typical cloud cover
cant increase of a similar magnitude to that of ­UVImax and           situations.
­Her,day was found for global radiation ­(GRint and ­GRmax). For          Looking at the annual frequency of daily ­UVImax val-
total column ozone data, no statistically significant change         ues shows that approximately half of the days in Dortmund
over the period was found when considering all ozone data.           have a U ­ VImax value ≥ 3 (Fig. 8). According to WHO rec-
A statistically significant decrease in total column ozone is         ommendations, sun protection is necessary for these days
observed during the summer months. The most substantial               [11]. Days with ­UVImax values of 3, 4, 5, and 6 occur with
increase is observed in the daily sunshine duration (SunD),           roughly equal frequency. The number of days with a U       ­ VImax
with a 11.3% per decade.                                             of 7 is significantly lower, and days with a ­UVImax of 8 are
                                                                     rare and restricted to specific combinations of influencing
                                                                     factors (total column ozone, solar elevation, cloud cover).
4.2.2 Impact of data gap handling and trend model                 ­UVImax values ≥ 3 occur mainly (94%) between April and
                                                                     September. On average, 83% of the annual cumulative H         ­ er,day
The influence of improved data gap handling on the out-              occurs from April to September.
come of trend analysis can be demonstrated by repeating                   Approximately one-third of the days per year falls into the
the calculations using the dataset with gaps (e.g. Fig-              range of 0–5 daily SED H     ­ er,day (Fig. 8, Fig. 9). This quan-
ure 2a). Table 5 presents the results of these calculations           tity corresponds to the number of days with ­UVImax value
based on U ­ VI max and H­ er,day data from Dortmund and             0 and ­UVImax value 1, as expected from the scatterplot of
Uccle. Both for Dortmund and Uccle, the outcome indi-                ­Her,day and ­UVImax (Fig. 14). This scatterplot also demon-
cates a slightly higher increase compared to the results              strates that days with low or no cloud cover (red dots), are at
presented in Table 2.                                                 the upper boundary of the pattern and show an approximate
   The influence of the improved BfS trend model on the               linear relationship between ­Her,day and ­UVImax. The slope
outcome of trend analysis can be demonstrated by repeating           is nearly identical to the evaluation of data from Spain [41]
the calculations using the dataset with gaps and a standard          and higher than in the evaluation of data from New Zee-
linear model applied to the monthly anomalies. The results           land [81]. This discrepancy is attributed to differences in
(Table 6) demonstrate the same percentage increase (com-             daylight duration, which result in higher H      ­ er,day values for
pared to Table 5); however, the 95% confidence interval is            the same U ­ VImax in Spain and Germany. Consistent with
significantly smaller.                                               findings in other studies, it is observed that on days with
                                                                   ­UVImax < 3 (2.5), the daily accumulation of ­Her,day values
                                                                     can exceed 10 SED. A closer examination reveals that even
5 Discussion                                                        at noon on these days, a value of 2.5 SED per hour is not
                                                                     reached. The threshold of 2.5 SED per hour is considered as
This study is the first comprehensive analysis of data from          the limit for visible skin damage for fair skin, as proposed by
a station of the German Solar UV Monitoring Network. It              Fitzpatrick [81, 82]. Cloudless days with U      ­ VImax < 3 (2.5)
shows distinct changes in ground-level solar UVR and its             and ­Her,day > 10 SED usually occur in March and September/
influencing factors, in particular global radiation and total         October in Dortmund/Uccle. Our findings thus affirm the
column ozone. The trend analysis shows a clear increase in            practicability of the WHO recommendations for protection
UV exposure across nearly three decades.                              for ­UVImax ≥ 3 [11].
                                                                          Considering the annual courses of potential highest
                                                                   ­UVImax and H     ­ er,day values, a shift to the summer solstice
5.1 UV exposure in Dortmund                                         towards later months can be observed. Like at the UVA/
                                                                     UVB ratio course (Fig. 7), this shift can be attributed to the
The dispersion of daily UV data (e.g. Figure 3) primarily            annual course of ozone values, which are independent of
arises from the cloud cover situation, with greater solar            solar elevation. In the months around and after the summer
elevation leading to increased absolute dispersion. The dif-         solstice, particular attention must be paid to the WHO sun
fering fluctuations contribute to the heteroscedasticity of          protection measures [11], as the highest ­UVImax and ­Her,day
the measurement data. When comparing the monthly mean                in the year could be expected here.
values of unweighted UVA and UVB (Figs. 5, 6) to litera-                  In addition to annual course of normal ozone, low
ture data, they are in the expected order of magnitude. For          ozone events can significantly influence ground-level UVR
example, they appear slightly lower than values observed in          [59–62], especially in absence of clouds. For the observed
                                                                     low ozone events occurring in Dortmund (Fig. 15), the
                                                                    ­UVImax values increase with increasing negative deviation
Photochemical & Photobiological Sciences

  from the ozone mean value (for cloudless conditions and              coefficient of sunshine duration with ­Her,day is higher than
  similar solar maximum elevation). In winter, this is com-            of sunshine duration with U     ­ VImax (Fig. 12). A change in
  pounded by the fact that changes in TCO have a stronger              sunshine duration thus has a stronger effect on H        ­ er,day than
  influence on U­ VImax at ground level due to the longer path         on ­UVImax which is consistent with the different H       ­ er,day and
  of UVR through the atmosphere. Hence, the high percent-            ­UVImax trends. Regarding the UV influencing parameter
  age ­UVImax enhancement of over 50%, as seen in February             ozone, the results show a slight but significant decrease in
  2023, is not expected during the summer months. It has to            the summer months (Table 4). Due to the much more sig-
  be remarked, that for the reported cases the aerosol situa-          nificant change in global radiation, it can be concluded that
  tion was not considered. Aerosol effects can counteract the          the changes in monthly mean U      ­ VImax and H ­ er,day values are
­UVImax increase at low ozone events [62, 74]. However,                primarily driven by a influencing factor also affecting the
  since lower ozone in Dortmund usually leads to a greater             global radiation. Considering the trend in SunD, this indi-
 ­UVImax increase, (for cloudless conditions and similar solar         cates a change in cloud cover as a main driver. The decreas-
  maximum elevation) it can be assumed that aerosol effect             ing summer ozone certainly influences ­UVImax and ­Her,day
  on the low ozone events is at least a small or even negligible       changes; however, it is just a minor driver.
  in Dortmund.                                                            When comparing the locations, it becomes evident that
     From a radiation protection perspective, it is important          in Uccle, the trend in monthly mean ­Her,day and U      ­ VImax val-
  that the observed superelevations often occur following              ues is higher than in Dortmund. This difference was to be
  a period of inclement weather with low ­UVImax values.               expected from the comparison of the annual means (Fig. 17),
 ­UVImax exposure then rises sharply, and a low ozone event            as in Dortmund, the annual UV values were mostly higher
  significantly amplifies this increase. In spring, it is further      than those in Uccle from 1999 to around 2004 and lower
  compounded by the fact that the solar elevation angle exhib-         from 2013 to 2017. In the years 2018–2021, the annual mean
  its the highest day-to-day increase over the course of the           values of H ­ er,day for both stations were comparable. How-
  year. This contributes to a further elevation in the typically       ever, the UVR levels at both stations for the entire period
  abrupt rise in UV levels. Some studies show that under               are similar (Fig. 3). Higher annual H    ­ er,day values in Uccle
  expected climatic changes, low ozone events might become             are associated with higher annual global radiation in Uccle
  more frequent in the future during Northern Hemisphere               and vice versa (Fig. 17). Regarding the annual means of
  spring [83, 84].                                                    ­UVImax, Uccle tends to have higher values than Dortmund.
                                                                       This difference partly arises from distinct measurement
5.2 Trend in UV exposure                                              intervals, which result in slightly higher U    ­ VImax values in
                                                                       Uccle. However, this effect alone does not account for the
For monthly mean values of U     ­ VImax and ­Her,day, the results     observed differences, as evidenced by a ­UVImax calculation
indicate a clear increase that is statically significant at both       for Dortmund with a 30-min interval (dashed blue U            ­ VImax
locations (Table 2). For Dortmund, the magnitude of the                line in Fig. 17). Additional differences may be attributed to
trend in ­UVImax and ­Her,day, as well as the difference between       localized cloud cover effects at solar noon. McKenzie et al.
both values, aligns well with the change in daily maximum              [91] see differences in the use of single maximum values
and daily integral of global radiation (Table 4). An increase          instead of mean maximum values for the ­UVImax determina-
of global radiation can be primary traced back to a decrease/          tion and attribute this to reduced cloud effects in the case of
change of aerosols, clouds and their interactions [85–88]. In          single maximum values.
the case of aerosols, one distinguishes between direct aer-               Based on the trend analysis of the longer period
osol effects (e.g. changing AOD), semi-direct effects and              1991–2022 (32 years) for Uccle, it can be observed that
indirect effects [88]. The semi-direct and indirect effects            the trends for the monthly mean ­UVImax values remain
are linked with aerosol–cloud interaction. In case of clouds,          relatively stable compared to the 1997–2022 analysis but
various studies indicate that changes in cloud cover are               with a smaller 95% CI for the longer period (Table 2). The
also influenced by greenhouse gases (GHGs) and climate                 change in monthly mean ­Her,day values calculated for the
change [89, 90]. The specific proportion of cloud and aero-            longer period (1991–2022) is identical to the change in
sol cause of the global radiation increase in the examined            ­UVImax values and lower than the ­Her,day change calculated
period (1996–2022) at the locations Dortmund and Uccle                 for the period 1997–2022. It has to be remarked that differ-
cannot be estimated within the scope of this study. However,           ent ­Her,day trends of Uccle for the two periods (1991–2022
the strong increase in monthly mean of local sunshine dura-            vs. 1997–2022) only become apparent when using data set
tion compared to the global radiation trend (Table 4) sug-             with imputed data (Table 5).
gests a strong effect of decreasing cloud cover in Dortmund,              In the results of the trend analysis of unweighted UVA
as sunshine duration almost exclusively depends on cloud               and UVB radiation (monthly mean of daily radiant exposure)
cover and negligible on AOD. In addition, the correlation              in Dortmund, significant increases and an almost twice as
                                                                                              Photochemical & Photobiological Sciences

 large trend in UVA radiation as compared to UVB radiation          per decade in Rome in some months [39], and a strongly
 are observed (Table 3). Consequently, the UVA-to-UVB               positive trend in Thessaloniki of 8% per decade [36]. The
 ratio also increases significantly. As expected, the trend per     trend in Thessaloniki was mainly driven by changes in aero-
 decade in ­Her,day (Table 2) falls between the changes in UVA      sols [38], indications of significant changes in cloud cover
 and UVB. The ozone trend analysis excluded the parameter           and ozone were not found [33].
 ozone as a main driver for the trend of the UVA/UVB ratio.             In contrast to annual ozone values, the annual summer
 Decreasing AODs [86] are also unlikely to be the cause of          ozone values show a decreasing trend (Fig. 16 and Table 4).
 our UVA/UVB ratio trend result. Although aerosol radiative         A 1% change in total ozone column can lead to a significant
 impact depends on the amount, size, and type of the atmos-         change of spectral irradiance in the UVB range (about 3%
 pheric particles, what can change the ratio of UVA–UVB             for 300 nm, 7% for 295 nm) [30] and an increase of around
 through various effects, the scattering of aerosols is gen-        1.2% in erythemal irradiance [93, 94]. For every 1% total
 erally stronger at shorter wavelengths. This effect remains        ozone column decrease, the incidence of melanoma is pro-
 even with decreasing AOD even if the absolute scattering           jected to rise between 1 and 2%, the incidence of squamous
 intensity decreases, which therefore still leads to a relatively   cell carcinoma between 3% and 4.6% and basal cell carci-
 stronger reduction in UVB than UVA scattering at a given           noma between 1.7% and 2.7% [95].
 AOD. Because of the overall stronger scattering at shorter             Our ozone trend results (Table 4) are consistent with
 wavelengths, a decreasing AOD trend would therefore result         other studies: In northern mid-latitudes (35–60° N), no trend
 in a relatively greater increase in UVB over UVA at ground         in annual mean total ozone column is observed [56]. A study
 level. For example, Fountoulakis et al. [38] analyzed a            by Malinović-Milićević et al. [49] analyzed ozone trends in
 long-term ground-level UV dataset from Thessaloniki and            Novi Sad, Serbia separated by seasons. They observed sta-
 demonstrated a disproportionately high increase in UVB             tistically significant negative trend of annual ozone values
 radiation with decreasing AOD levels. At least a portion of        for summer ( – 0.8% p. decade), spring (– 0.5% p. decade),
 the different increase in UVA and UVB can be attributed to         and autumn (– 1.0% p. decade) over the period 1997–2018.
 the strong increase in sunshine duration because the inves-        Similarly, in a study by Fountoulakis et al. [39], significant
 tigated correlations between sunshine duration and UVA             negative trends in total ozone were reported for Rome in
 as well as sunshine duration and UVB indicate a slightly           April and September for the period 1996–2020. They noted
 higher correlation coefficient between sunshine duration and       that these trends coincided with positive trends in Geo-
 UVA throughout the year (Fig. 13). Additionally, the greater       potential Height (GPH) over extensive regions, indicating
 increase in UVA radiation compared to global radiation             an upward shift of the tropopause to higher altitudes. This
­(GRint) is consistent with decreasing cloud cover [92]. The        is congruent with anticorrelation of the tropopause height
 extent to which indirect aerosol effects play a role, if any,      and the total ozone column [96]. A rising altitude of the
 and how significant they are, is an important open question        tropopause can be attributed to climate change associated
 that needs to be examined in other studies.                        with the warming of the troposphere [97, 98]. Steinbrecht
    When looking at the observed long-term changes in               et al. discussed in detail the possible causes of the absence or
 ground-level UVR across all of Europe, a highly heterogene-        delay of an expected increasing trend in total column ozone,
 ous pattern emerges. Influencing factors (clouds, total ozone      including the influence of climate change [99], which was
 column, AOD) have different effects at different locations         also addressed by Langematz [100].
 and with respect to the large differences there are only very          The lack of annual ozone trend and negative summer
 few high-quality long-term measurement series in Europe            ozone trend could be also explained by a temporal shift
 [32–43]. With the detailed comparison of the results from          of the annual course of ozone towards earlier months (see
 Dortmund with those from Uccle, statements on the signifi-         Fig. 21 in appendix). At such a shift, lower ozone values
 cant increase of ground-level UVR on a similar latitude in         occur between April and September while the annual aver-
 central Europe are confirmed. With Uccle UV data of the            age remains unchanged. Such a temporal shift would result
 period from 1996 to 2017, Fountoulakis et al. [36] found an        in ozone values tending to decrease during the period of
 increase of 5% per decade for UVB (307.5 nm) which is in           highest solar elevation in the year, potentially leading to con-
 similar magnitude to our findings. An increasing trend in          ditions for higher ­UVImax and ­Her,day values.
 Uccle was also found by De Bock et al. analyzing the ­Her,day
 monthly mean values of 1991–2013 (+ 7% p. decade) [37].            5.3 Impact of data gap handling and trend model
 Decreasing attenuation by AOD and cloud cover have so far
 been identified as main contributors in Uccle [33, 37]. Fur-       In this study, the issue of data gap handling was addressed
 ther analyses across Europe range from no significant long-        using a developed and validated imputation method [73].
 term trend in Finland [32, 33] to a decreasing trend of 7–8%       The applied imputation method prevents a significant
 per decade in the UK [34–36], to positive trend of up to 5%        bias due to data gaps. To demonstrate the impact of the
Photochemical & Photobiological Sciences

imputation method on trend results, additional trend analy-           ozone events result in a superelevation of U
                                                                                                                 ­ VImax values
ses were conducted using a dataset containing data gaps (for          in the magnitude of 10–20% in the summer half-year;
Dortmund: Fig. 2). The results indicate that in most cases,           an extremely low ozone event in Feb. 2023 leads to an
there is an increased trend per decade (Table 5) compared             increase in ­UVImax of over 50%.
to the results obtained with imputation (Table 2). Stand-
ard errors remain constant or similar. The increasing trends          The findings of this study underscore the importance
are likely attributed to the temporal appearance of the data       of developing additional measures to counter the rising
gaps. Changes in the trends are traceable to both to the           UV exposure in Europe. To achieve this objective, further
missing months in the data set of Dortmund and to monthly          research is required into the influence of climate change and
means with missing daily values. In a different temporal           the interaction of the main influencing factors. The observed
gap appearance, a decrease in trend per decade could also          trends must be factored into future adaptive and preventive
be possible.                                                       strategies against the current climate change to minimize
    In our trend analysis, we improved the standard linear         health-related consequences effectively.
model to account for autocorrelation and heteroscedastic-
ity present in our datasets. An additional advantage of our
approach is the direct use of monthly mean values, bypass-         Appendix
ing the need for monthly anomalies. For comparison, the
­Her,day and U­ VImax data (with gaps) were analyzed using         Trend analysis
 a standard linear model based on monthly anomalies. The
 results Table 6 asreveal nearly identical changes/trends per      Details of trend model
 decade compared to the advanced model without imputation
 at data gaps (Table 5), as expected due to similar slope cal-     The model (Eq. (1)) in Sect. 3.2 can be written in matrix
 culations. However, a distinction arises in the larger standard   notation as:
 error and significantly expanded 95% confidence interval
 when using the advanced BfS model. The non-consideration
                                                                   y = X𝜷 + 𝜺                                                (2)
 of existing autocorrelation and heteroscedasticity would lead     with the column vector of response variable values
 to an underestimation of the standard errors of the trend esti-   y = (y1 , … , yn )T from the first to the last month n , the
 mates. In general, this becomes crucial when assessing the        error vector 𝜺 = (𝜀1 , … , 𝜀n )T , the coefficient vector
 significance of trend results with a low change per decade.       𝜷 = (𝛽0 , ⋯ 𝛽12 )T and the n × 13 design matrix

                                                                       ⎛ 1 t1 ⋯ ⎞
6 Conclusion                                                      X = ⎜⋮ ⋮ ⋯⎟                                               (3)
                                                                       ⎜        ⎟
                                                                       ⎝ 1 tn ⋯ ⎠
In this study, a 26-year series of spectrally resolved data on
the solar UVR from Dortmund, Germany, was evaluated                    Here, the superscript index T denotes the transposed vec-
and compared to Uccle, Belgium. Increasing trends were             tor or matrix. The values t1 , ⋯ , tn counts the months from 1
detected. Increasing solar UVR can lead to higher human            (Jan 1990) to 396 (Dec 2022). This means, for instance, that
UV exposure and can adversely affect the environment.              t1 = 85 and tn = 396 for analyses in the period from January
                                                                   1997 to December 2022. With the assumption of normally
• The trend analysis shows a significant increase in ­Her,day      distributed errors, the maximum likelihood (ML) estimate
  and ­UVImax in Dortmund, Germany, for the period of              for the coefficient vector 𝜷 is given by
  1997–2022, with even higher values in Uccle, Belgium.               (    )    T
  In Dortmund, the rise in both H  ­ er,day and U ­ VImax corre-   ̂ = XT X −1 X y
                                                                   𝜷                                                         (4)
  lates well with the trend in global radiation. This together
  with a strong trend in sunshine duration indicates a             whereas in the standard linear model uncorrelated error vari-
  change in cloud cover as the primary driver. In terms of         ables with the same variance 𝜎 2 for all months are assumed,
  radiation protection, an impact of the H  ­ er,day and ­UVImax   we used a linear model that provides a heteroskedasticity and
  trends on public health has to be expected thus cannot be        autocorrelation consistent estimation of the general covari-
  numerated.                                                       ance matrix 𝛀 of 𝜺 ∼ N(0, 𝛀), which have been suggested in
• A statistically significant decrease in summer ozone             the econometric literature (e.g. [101, 102]) and implemented
  (Apr–Sept) levels contributes to higher UVB, ­UVImax             in the package ‘sandwich’ for the software R by Zeileis [80].
  and ­Her,day values. If this trend continues, we have to         Thus, for the covariance matrix of 𝜷 ̂ one gets
  expect earlier and longer periods of high solar UVR. Low
                                                                                                       Photochemical & Photobiological Sciences

   ( ) (    )    T   (   )                                               plot (residuals vs. fitted values) exhibits "chaotic" behavior.
    ̂ = XT X −1 X 𝛀X
Cov 𝜷              ̂ XT X −1                                     (5)
                                                                         Additionally, it was tested whether the residual plot (residu-
                                                                         als vs. time, grouped by months) displays the same disper-
with
                                                                         sion in all months.
       ( ( )(   )T )
   ̂ =E v 𝜷
XT 𝛀X     ̂ v(𝜷)
              ̂                                                  (6)     Residuals

where v(𝜷) = XT (y − X𝜷) . Assuming an autoregressive                    See Fig. 20
structure with a weight vector w = (w0 , w1 , … , wn−1 ), a het-
eroscedasticity and autocorrelation consistent estimation of             Measurement uncertainties in the trend analysis
the covariance matrix of the coefficient estimates in a linear
regression model is given by Zeileis [80]:                               The correlated contributions to the measurement uncer-
                           ( )(      )T                                  tainty, which remain approximately constant for a specific
           ∑
   ̂ =
XT 𝛀X                       ̂ vt (𝜷)
                  w|s−t| vs 𝜷     ̂
                                                                 (7)     month over the years, and include potential systematic errors
            s,t                                                          e.g. due to diffuser temperature or angular response, are
                                                                         incorporated into the month term of the trend model for
   This approximation is done after the coefficient vector 𝜷
                                                                         both stations. The remaining contributions to measurement
has been estimated. We determine the weights for specific
                                                                         uncertainty are mainly related to the radiometric uncertainty
lags l as proposed by Andrews [102]:
                                                                         set during calibrations. As mentioned in Sect. 2.1, this radio-
         (            )                                                  metric uncertainty (< 2% expanded) for the Dortmund sta-
       3 𝑠𝑖𝑛z
wl = 2         − 𝑐𝑜𝑠z                                    (8)             tion is randomly set during calibrations conducted at least
      z      z
                                                                         once a year. We therefore assume this remaining (radiomet-
with z = 6𝜋∕5 ∙ l∕B. The bandwidth B is determined adap-                 ric) uncertainty has negligible impact on the results of the
tively, analogous to Andrews [102]. Unlike fixed or pre-                 trend analysis. We apply the same assumption to the trend
determined bandwidths, the adaptive method adjusts the                   analysis of the Uccle data. Although the remaining con-
bandwidth dynamically based on the characteristics of the                tributions to measurement uncertainty are expected to be
data itself.                                                             somewhat higher here than in Dortmund, we still consider
   The autocorrelation structure of the response values was              the assumption justified due to the monthly check and the
examined by analysis of the residuals. For this purpose, the             presence of a mostly concurrently operating second meas-
autoregressive order of the residuals was estimated and a                urement system explained in Sect. 2.2.
Durbin–Watson test [103] was applied. Regarding homo-
geneity of variance, it was investigated whether the residual




Fig. 20  Studentized residuals depending on the fitted values (left) and months (right) for ­Her,day [SED] values from Dortmund calculated with
imputation at data gaps (Fig. 2) and BfS trend model (chapter 3.2)
Photochemical & Photobiological Sciences

                                                                     Acknowledgements The authors would like to thank the regional cli-
                                                                     mate office Hamburg of the German Meteorological Service and the
                                                                     Tropospheric Emission Monitoring Internet Service for providing data
                                                                     of the global radiation, sunshine duration data and total column ozone.
                                                                     The authors are also grateful to Lionel Doppler, Stefan Wacker, Mario
                                                                     Blumthaler, Ilias Fountoulakis, Hartwig Denecke and Bernd Heinold
                                                                     for their valuable discussions on various aspects of the results.

                                                                     Author contributions Study design, material preparation, data col-
                                                                     lection, and analysis were performed by Sebastian Lorenz and Felix
                                                                     Heinzl. The drafts of the manuscript were written by Sebastian Lorenz
                                                                     and Felix Heinzl, and all authors commented on previous versions of
                                                                     the manuscript. All authors read and approved the final manuscript.

                                                                     Funding Open Access funding enabled and organized by Projekt
                                                                     DEAL. The authors declare that no funds, grants, or other supports
                                                                     was received.

                                                                     Data availability Researchers interested in accessing our data can con-
Fig. 21  Annual courses of 7-day-median ozone in Dortmund for dif-   tact us via the corresponding author. We will handle inquiries on a
ferent 13-year periods: 1971–1983 (black), 1984–1996 (red), 1997–    case-by-case basis, as different requests may require different options
2009 (blue) and 2010–2022 (green) smoothed by LOESS filter           and responsibilities. Please rest assured that the data is available for
                                                                     scientific purposes.

Development of annual course of ozone                                Declarations
To investigate a possible change of the annual course of             Conflict of interest The authors declare that they have no conflict of
ozone values, the annual median course of ozone was sep-             interests.
arately calculated for the first (1997–2009) and second half         Sustainability This study focuses on ground-level solar UV radiation
(2010–2022) of the period. Additional TEMIS data from                and identifies both changes and their potential causes. The research rep-
1984 to 1996 and 1971 to 1983 were used to calculate                 resents a significant contribution to the United Nations' 2030 Agenda
two further 13-year periods (Fig. 21). The annual courses            Sustainable Development Goals (SDGs). It specifically addresses the
                                                                     SDGs 3 (Good health and well-being), 11 (Sustainable cities and com-
are smoothed by a LOESS filter for a better visualization            munities), 13 (Climate action) and 15 (Life on land). Barnes et al. [104]
of changes. It is clear to see how the Montreal Proto-               provide a comprehensive overview of direct and indirect connections
col (1987/1989) halted the significant decline of ozone              between the topic and further SDGs.
throughout the entire year. Subsequently (red, blue and
green line), only a minor decrease in ozone is observable            Open Access This article is licensed under a Creative Commons Attri-
in spring and summer, accompanied by a slight increase in            bution 4.0 International License, which permits use, sharing, adapta-
                                                                     tion, distribution and reproduction in any medium or format, as long
autumn and winter. This change is consistent with a tem-             as you give appropriate credit to the original author(s) and the source,
poral shift of the annual course towards earlier times. Such         provide a link to the Creative Commons licence, and indicate if changes
a temporal shift is particularly obvious between the last            were made. The images or other third party material in this article are
two periods 1997–2009 (blue line) and 2010–2022 (green               included in the article’s Creative Commons licence, unless indicated
                                                                     otherwise in a credit line to the material. If material is not included in
line). Further research is needed, on how the parameters             the article’s Creative Commons licence and your intended use is not
influencing total column ozone affect the annual course              permitted by statutory regulation or exceeds the permitted use, you will
of ozone.                                                            need to obtain permission directly from the copyright holder. To view a
   It is worth noting that when comparing ozone levels               copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.
across different time periods, the solar cycle (SC) can also
be a contributing factor. To exclude bias resulting from the
choice of start and end points, time periods of 1976–1985            References
(SC21), 1986–1996 (SC22), 1997–2008 (SC23), and
                                                                       1. Ambach, W., & Blumthaler, M. (1993). Biological effective-
2009–2020 (SC24) were compared, roughly coinciding                        ness of solar UV radiation in humans. Experientia, 49(9),
with completed solar cycles, instead of using fixed 13-year               747–753. https://​doi.​org/​10.​1007/​BF019​23543
periods. A difference can only be seen in the minor fluc-              2. Lucas, R. M., Yazar, S., Young, A. R., Norval, M., de Gruijl,
tuations along the curves. The tendency of a temporal shift               F. R., Takizawa, Y., Rhodes, L. E., Sinclair, C. A., & Neale,
                                                                          R. E. (2019). Human health in relation to exposure to solar
can be shown in the same manner.                                          ultraviolet radiation under changing stratospheric ozone and
                                                                                                                 Photochemical & Photobiological Sciences

    climate. Photochemical & Photobiological Sciences, 18(3),                           in occupational settings. International Journal of Environmental
    641–680. https://​doi.​org/​10.​1039/​C8PP9​0060D                                   Research and Public Health. https://​doi.​org/​10.​3390/​ijerp​h1507​
 3. El Ghissassi, F., Baan, R., Straif, K., Grosse, Y., Secretan,                       1507
    B., Bouvard, V., Benbrahim-Tallaa, L., Guha, N., Freeman,                       17. Bornman, J. F., Barnes, P. W., Robson, T. M., Robinson, S. A.,
    C., Galichet, L., & Cogliano, V. (2009). A review of human                          Jansen, M. A. K., Ballare, C. L., & Flint, S. D. (2019). Linkages
    carcinogens—Part D: Radiation. The Lancet Oncology, 10(8),                          between stratospheric ozone, UV radiation and climate change
    751–752. https://​doi.​org/​10.​1016/​S1470-​2045(09)​70213-X                       and their implications for terrestrial ecosystems. Photochemical
 4. De Fabo, E. C., Noonan, F. P., Fears, T., & Merlino, G. (2004).                     & Photobiological Sciences, 18(3), 681–716. https://​doi.​org/​10.​
    Ultraviolet B but not ultraviolet A radiation initiates mela-                       1039/​c8pp9​0061b
    noma. Cancer Research, 64(18), 6372–6376. https://​doi.​org/​                   18. Gröbner, J., Blumthaler, M., Kazadzis, S., Bais, A., Webb, A.,
    10.​1158/​0008-​5472.​CAN-​04-​1454                                                 Schreder, J., Seckmeyer, G., & Rembges, D. (2006). Quality
 5. Parker, E. R. (2021). The influence of climate change on skin                       assurance of spectral solar UV measurements: Results from 25
    cancer incidence – A review of the evidence. International                          UV monitoring sites in Europe, 2002 to 2004. Metrologia, 43(2),
    Journal of Women’s Dermatology, 7(1), 17–27. https://​doi.​org/​                    S66–S71. https://​doi.​org/​10.​1088/​0026-​1394/​43/2/​s14
    10.​1016/j.​ijwd.​2020.​07.​003                                                 19. Schmalwieser, A. W., Grobner, J., Blumthaler, M., Klotz, B.,
 6. Krebsregisters Schleswig-Holstein. Prognose Hautkrebs,                              De Backer, H., Bolsee, D., Werner, R., Tomsic, D., Metelka, L.,
    Hochrechnung für Deutschland 2024. Retrieved 20.09.2024                             Eriksen, P., Jepsen, N., Aun, M., Heikkila, A., Duprat, T., Sand-
    from https://​w ww.​k rebs​r egis​t er-​s h.​d e/​p rogn​o se-​h autk​r ebs-​       mann, H., Weiss, T., Bais, A., Toth, Z., Siani, A. M., & O’Hagan,
    aktua​lisie​r t-​fuer-​2024                                                         J. (2017). UV index monitoring in Europe. Photochemical &
 7. Federal Statistical Office. (2024). 75 % mehr stationäre Haut-                      Photobiological Sciences, 16(9), 1349–1370. https://​doi.​org/​10.​
    krebsbehandlungen im Jahr 2022 als 20 Jahre zuvor [press                            1039/​c7pp0​0178a
    release]. https://​www.​desta​tis.​de/​DE/​Presse/​Press​emitt​eilun​           20. McElroy, C. T., Kerr, J. B., McArthur, L. J. B., & Wardle, D. I.
    gen/​Zahl-​der-​Woche/​2024/​PD24_​22_​p002.​html                                   (1994). Ground-based monitoring of UV-B Radiation in Can-
 8. Belgian Cancer Registry. Data App Drawing module. Retrieved                         ada. In R. H. Biggs & M. E. B. Joyner (Eds.), Stratospheric
    20.09.2024 from https://​belgi​an-​cancer-​regis​try.​shiny​apps.​io/​              ozone depletion/UV-B radiation in the biosphere (pp. 271–282).
    data_​app/                                                                          Springer.
 9. Neale, R. E., Lucas, R. M., Byrne, S. N., Hollestein, L., Rhodes,               21. Kaye, J. A., Hicks, B. B., Weatherhead, E. C., Long, C. S., &
    L. E., Yazar, S., Young, A. R., Berwick, M., Ireland, R. A., &                      Slusser, J. (1999). U.S. interagency UV monitoring program
    Olsen, C. M. (2023). The effects of exposure to solar radiation                     established and operating. Eos, Transactions American Geo-
    on human health. Photochemical and Photobiological Sciences.                        physical Union. https://​doi.​org/​10.​1029/​99eo0​0075
    https://​doi.​org/​10.​1007/​s43630-​023-​00375-8                               22. Cede, A. (2002). Monitoring of erythemal irradiance in the
10. Madronich, S., Bernhard, G. H., Neale, P. J., Heikkila, A.,                         Argentine ultraviolet network. Journal of Geophysical Research.
    Andersen, M. P. S., Andrady, A. L., Aucamp, P. J., Bais, A. F.,                     https://​doi.​org/​10.​1029/​2001j​d0012​06
    Banaszak, A. T., Barnes, P. J., Bornman, J. F., Bruckman, L. S.,                23. Lamy, K., Portafaix, T., Brogniez, C., Lakkala, K., Pitkänen,
    Busquets, R., Chiodo, G., Hader, D. P., Hanson, M. L., Hylander,                    M. R. A., Arola, A., Forestier, J. B., Amelie, V., Toihir, M. A.,
    S., Jansen, M. A. K., Lingham, G., & Neale, R. E. (2024). Con-                      & Rakotoniaina, S. (2021). UV-Indien network: Ground-based
    tinuing benefits of the Montreal Protocol and protection of the                     measurements dedicated to the monitoring of UV radiation over
    stratospheric ozone layer for human health and the environment.                     the western Indian Ocean. Earth System Science Data, 13(9),
    Photochemical and Photobiological Sciences, 23(6), 1087–1115.                       4275–4301. https://​doi.​org/​10.​5194/​essd-​13-​4275-​2021
    https://​doi.​org/​10.​1007/​s43630-​024-​00577-8                               24. Janjai, S., Kirdsiri, K., Masiri, I., & Nunez, M. (2010). An inves-
11. World Health Organization, World Meteorological Organization,                       tigation of solar erythemal ultraviolet radiation in the tropics: A
    United Nations Environment Programme and International Com-                         case study at four stations in Thailand. International Journal
    mission on Non-Ionizing Radiation Protection. (2002). Global                        of Climatology, 30(12), 1893–1903. https://​doi.​org/​10.​1002/​joc.​
    solar UV index : a practical guide. In. Geneva: World Health                        2006
    Organization. https://​apps.​who.​int/​iris/​handle/​10665/​42459               25. Gies, P., Roy, C., Javorniczky, J., Henderson, S., Lemus-Des-
12. International Commission on Illumination (cie). (2020). Interna-                    champs, L., & Driscoll, C. (2004). Global solar UV index: Aus-
    tional Lighting Vocabulary, (2nd ed.). https://​doi.​org/​10.​25039/​               tralian measurements, forecasts and comparison with the UK.
    S017.​2020                                                                          Photochemistry and Photobiology, 79(1), 32–39. https://​doi.​org/​
13. Bais, A. F., Bernhard, G., McKenzie, R. L., Aucamp, P. J.,                          10.​1111/j.​1751-​1097.​2004.​tb098​54.x
    Young, P. J., Ilyas, M., Jockel, P., & Deushi, M. (2019). Ozone-                26. McKenzie, R., Bodeker, G. E., Keep, D. J., Kotkamp, M., &
    climate interactions and effects on solar ultraviolet radiation.                    Evans, J. (1996). UV radiation in New Zealand: North-to-South
    Photochemical & Photobiological Sciences, 18(3), 602–640.                           differences between two sites, and relationship to other latitudes.
    https://​doi.​org/​10.​1039/​c8pp9​0059k                                            Weather and Climate, 16(1), 17–26. https://​doi.​org/​10.​2307/​
14. Weihs, P., Simic, S., Laube, W., Mikielewicz, W., Rengarajan, G.,                   44279​891
    & Mandl, M. (1999). Albedo influences on surface UV irradiance                  27. Hulsen, G., & Grobner, J. (2007). Characterization and calibra-
    at the Sonnblick high-mountain observatory (3106-m altitude).                       tion of ultraviolet broadband radiometers measuring erythemally
    Journal of Applied Meteorology., 38(11), 1599–1610. https://d​ oi.​                 weighted irradiance. Applied Optics, 46(23), 5877–5886. https://​
    org/​10.​1175/​1520-​0450(1999)​038%​3c1599:​Aiosui%​3e2.0.​Co;2                    doi.​org/​10.​1364/​ao.​46.​005877
15. Kreuter, A., Buras, R., Mayer, B., Webb, A., Kift, R., Bais,                    28. Blumthaler, M. (2018). UV monitoring for public health. Inter-
    A., Kouremeti, N., & Blumthaler, M. (2014). Solar irradiance                        national Journal of Environmental Research and Public Health.
    in the heterogeneous albedo environment of the Arctic coast:                        https://​doi.​org/​10.​3390/​ijerp​h1508​1723
    Measurements and a 3-D model study. Atmospheric Chemis-                         29. Schmalwieser, A. W., Klotz, B., Schwarzmann, M., Baumgartner,
    try and Physics, 14(12), 5989–6002. https://​doi.​org/​10.​5194/​                   D. J., Schreder, J., Schauberger, G., & Blumthaler, M. (2019).
    acp-​14-​5989-​2014                                                                 The Austrian UVA-Network. Photochemistry and Photobiology,
16. Turner, J., & Parisi, A. V. (2018). Ultraviolet radiation Albedo                    95(5), 1258–1266. https://​doi.​org/​10.​1111/​php.​13111
    and Reflectance in review: The influence to ultraviolet exposure
Photochemical & Photobiological Sciences

 30. Seckmeyer, G., Bais, A., Bernhard, G., Blumthaler, M., Booth,         42. Fitzka, M., Simic, S., & Hadzimustafic, J. (2012). Trends in spec-
     C. R., Disterhoft, P., Eriksen, P., McKenzie, R. L., Miyauchi,            tral UV radiation from long-term measurements at Hoher Sonn-
     M., & Roy, C. (2001). Instruments to measure solar ultraviolet            blick, Austria. Theoretical and Applied Climatology, 110(4),
     radiation, part 1, spectral instruments. Global atmosphere watch.         585–593. https://​doi.​org/​10.​1007/​s00704-​012-​0684-0
     (Vol. 125). Geneva: World Meteorological Organization.                43. Smedley, A. R. D., Rimmer, J. S., Moore, D., Toumi, R., &
 31. Garane, K., Bais, A. F., Kazadzis, S., Kazantzidis, A., & Meleti,         Webb, A. R. (2012). Total ozone and surface UV trends in the
     C. (2006). Monitoring of UV spectral irradiance at Thessaloniki           United Kingdom: 1979–2008. International Journal of Climatol-
     (1990–2005): Data re-evaluation and quality control. Annales              ogy, 32(3), 338–346. https://​doi.​org/​10.​1002/​joc.​2275
     Geophysicae, 24(12), 3215–3228. https://​d oi.​o rg/​1 0.​5 194/​     44. Eleftheratos, K., Kapsomenakis, J., Fountoulakis, I., Zerefos, C.
     angeo-​24-​3215-​2006                                                     S., Jöckel, P., Dameris, M., Bais, A. F., Bernhard, G., Kouklaki,
 32. Lakkala, K., Heikkilä, A., Kärhä, P., Ialongo, I., Karppinen, T.,         D., Tourpali, K., Stierle, S., Liley, J. B., Brogniez, C., Auriol,
     Karhu, J. M., Lindfors, A. V. and Meinander, O. (2017). 25 years          F., Diémoz, H., Simic, S., Petropavlovskikh, I., Lakkala, K., &
     of spectral UV measurements at Sodankylä. Radiation Processes             Douvis, K. (2022). Ozone, DNA-active UV radiation, and cloud
     in the Atmosphere and Ocean (IRS2016) AIP Conf. Proc., 1810.              changes for the near-global mean and at high latitudes due to
     https://​doi.​org/​10.​1063/1.​49755​68                                   enhanced greenhouse gas concentrations. Atmospheric Chemis-
 33. Fountoulakis, I., Zerefos, C. S., Bais, A. F., Kapsomenakis, J.,          try and Physics, 22(19), 12827–12855. https://​doi.​org/​10.​5194/​
     Koukouli, M.-E., Ohkawara, N., Fioletov, V., De Backer, H., Lak-          acp-​22-​12827-​2022
     kala, K., Karppinen, T., & Webb, A. R. (2018). Twenty-five years      45. Rieder, H. E., Holawe, F., Simic, S., Blumthaler, M., Krzyścin,
     of spectral UV-B measurements over Canada, Europe and Japan:              J. W., Wagner, J. E., Schmalwieser, A. W., & Weihs, P. (2008).
     Trends and effects from changes in ozone, aerosols, clouds, and           Reconstruction of erythemal UV-doses for two stations in Aus-
     surface reflectivity. Comptes Rendus Geoscience, 350(7), 393–             tria: A comparison between alpine and urban regions. Atmos-
     402. https://​doi.​org/​10.​1016/j.​crte.​2018.​07.​011                   pheric Chemistry and Physics, 8(20), 6309–6323. https://​doi.​
 34. Hooke, R. J., Higlett, M. P., Hunter, N., & O’Hagan, J. B. (2017).        org/​10.​5194/​acp-8-​6309-​2008
     Long term variations in erythema effective solar UV at Chilton,       46. Rieder, H. E., Staehelin, J., Weihs, P., Vuilleumier, L., Maeder, J.
     UK, from 1991 to 2015. Photochemical & Photobiological Sci-               A., Holawe, F., Blumthaler, M., Lindfors, A., Peter, T., Simic, S.,
     ences, 16(11), 1596–1603. https://​doi.​org/​10.​1039/​c7pp0​0053g        Spichtinger, P., Wagner, J. E., Walker, D., & Ribatet, M. (2010).
 35. Hunter, N., Rendell, R. J., Higlett, M. P., O’Hagan, J. B., & Hay-        Relationship between high daily erythemal UV doses, total
     lock, R. G. E. (2019). Relationship between erythema effective            ozone, surface albedo and cloudiness: An analysis of 30years of
     UV radiant exposure, total ozone, cloud cover and aerosols in             data from Switzerland and Austria. Atmospheric Research, 98(1),
     southern England, UK. Atmospheric Chemistry and Physics,                  9–20. https://​doi.​org/​10.​1016/j.​atmos​res.​2010.​03.​006
     19(1), 683–699. https://​doi.​org/​10.​5194/​acp-​19-​683-​2019       47. Román, R., Bilbao, J., & de Miguel, A. (2015). Erythemal ultra-
 36. Fountoulakis, I., Diémoz, H., Siani, A.-M., Laschewski, G.,               violet irradiation trends in the Iberian Peninsula from 1950 to
     Filippa, G., Arola, A., Bais, A. F., De Backer, H., Lakkala, K.,          2011. Atmospheric Chemistry and Physics, 15(1), 375–391.
     Webb, A. R., De Bock, V., Karppinen, T., Garane, K., Kapsom-              https://​doi.​org/​10.​5194/​acp-​15-​375-​2015
     enakis, J., Koukouli, M.-E., & Zerefos, C. S. (2020). Solar UV        48. den Outer, P. N., Slaper, H., Kaurola, J., Lindfors, A., Kazantz-
     irradiance in a changing climate: Trends in Europe and the sig-           idis, A., Bais, A. F., Feister, U., Junk, J., Janouch, M., & Josefs-
     nificance of spectral monitoring in Italy. Environments, 7(1), 1.         son, W. (2010). Reconstructing of erythemal ultraviolet radiation
     https://​doi.​org/​10.​3390/​envir​onmen​ts701​0001                       levels in Europe for the past 4 decades. Journal of Geophysical
 37. De Bock, V., De Backer, H., Van Malderen, R., Mangold,                    Research. https://​doi.​org/​10.​1029/​2009j​d0128​27
     A., & Delcloo, A. (2014). Relations between erythemal UV              49. Malinović-Milićević, S., Radovanović, M. M., Mijatović, Z., &
     dose, global solar radiation, total ozone column and aero-                Petrović, M. D. (2022). Reconstruction and variability of high
     sol optical depth at Uccle, Belgium. Atmospheric Chemistry                daily erythemal ultraviolet doses and relationship with total
     and Physics, 14(22), 12251–12270. https://​doi.​org/​10.​5194/​           ozone, cloud cover, and albedo in Novi Sad (Serbia). Interna-
     acp-​14-​12251-​2014                                                      tional Journal of Climatology. https://​doi.​org/​10.​1002/​joc.​7803
 38. Fountoulakis, I., Bais, A. F., Fragkos, K., Meleti, C., Tourpali,     50. Bilbao, J., Román, R., de Miguel, A., & Mateos, D. (2011).
     K., & Zempila, M. M. (2016). Short- and long-term variability of          Long-term solar erythemal UV irradiance data reconstruction
     spectral solar UV irradiance at Thessaloniki, Greece: Effects of          in Spain using a semiempirical method. Journal of Geophysical
     changes in aerosols, total ozone and clouds. Atmospheric Chem-            Research: Atmospheres. https://​doi.​org/​10.​1029/​2011j​d0158​36
     istry and Physics, 16(4), 2493–2505. https://​doi.​org/​10.​5194/​    51. Trepte, S., & Winkler, P. (2004). Reconstruction of erythemal
     acp-​16-​2493-​2016                                                       UV irradiance and dose at Hohenpeissenberg (1968–2001) con-
 39. Fountoulakis, I., Diémoz, H., Siani, A. M., di Sarra, A., Meloni,         sidering trends of total ozone, cloudiness and turbidity. Theoreti-
     D., & Sferlazzo, D. M. (2021). Variability and trends in surface          cal and Applied Climatology, 77(3–4), 159–171. https://​doi.​org/​
     solar spectral ultraviolet irradiance in Italy: On the influence of       10.​1007/​s00704-​004-​0034-y
     geopotential height and lower-stratospheric ozone. Atmospheric        52. Čížková, K., Láska, K., Metelka, L., & Staněk, M. (2018).
     Chemistry and Physics, 21(24), 18689–18705. https://​doi.​org/​           Reconstruction and analysis of erythemal UV radiation time
     10.​5194/​acp-​21-​18689-​2021                                            series from Hradec Králové (Czech Republic) over the past 50
 40. Simic, S., Weihs, P., Vacek, A., Kromp-Kolb, H., & Fitzka, M.             years. Atmospheric Chemistry and Physics, 18(3), 1805–1818.
     (2008). Spectral UV measurements in Austria from 1994 to                  https://​doi.​org/​10.​5194/​acp-​18-​1805-​2018
     2006: Investigations of short- and long-term changes. Atmos-          53. Reuder, J., & Koepke, P. (2005). Reconstruction of UV radiation
     pheric Chemistry and Physics, 8(23), 7033–7043. https://​doi.​            over Southern Germany for the past decades. Meteorologische
     org/​10.​5194/​acp-8-​7033-​2008                                          Zeitschrift, 14(2), 237–246. https://​doi.​org/​10.​1127/​0941-​2948/​
 41. Bilbao, J., & de Migue, A. (2020). Erythemal solar irradiance,            2005/​0027
     UVER, and UV Index from ground-based data in Central Spain.           54. Vuilleumier, L., Harris, T., Nenes, A., Backes, C., & Vernez, D.
     Applied Sciences, 10(18), 6589. https://​doi.​org/​10.​3390/​app10​       (2021). Developing a UV climatology for public health purposes
     186589                                                                    using satellite data. Environment International, 146, 106177.
                                                                               https://​doi.​org/​10.​1016/j.​envint.​2020.​106177
                                                                                                          Photochemical & Photobiological Sciences

55. Vitt, R., Laschewski, G., Bais, A., Diémoz, H., Fountoulakis, I.,             D., Jaroslawski, J., Simic, S., Stanec, M., Steinmetz, M., Tax, R.
    Siani, A.-M., & Matzarakis, A. (2020). UV-index climatology for               and Villaplana Guerrero, J. M. (2004). Report of site visits round
    Europe based on satellite data. Atmosphere, 11(7), 727. https://​             2004 (EUR 21398 EN).
    doi.​org/​10.​3390/​atmos​11070​727                                       70. World Meteorological Organization (WMO). (2021). Measure-
56. Bernhard, G. H., Bais, A. F., Aucamp, P. J., Klekociuk, A. R.,                ment of meteorological variables. Guide to instruments and
    Liley, J. B., & McKenzie, R. L. (2023). Stratospheric ozone,                  methods of observation, Vol 1 (8th ed.). WMO.
    UV radiation, and climate interactions. Photochemical & Pho-              71. Van Geffen, J., Van Weele, M., Allaart, M., & Van der, A. R.
    tobiological Sciences, 22(5), 937–989. https://​doi.​org/​10.​1007/​          (2017). TEMIS UV index and UV dose MSR-2 data products,
    s43630-​023-​00371-y                                                          version 2. Dataset. Royal Netherlands Meteorological Institute
57. Bais, A. F., McKenzie, R. L., Bernhard, G., Aucamp, P. J., Ilyas,             (KNMI). https://​doi.​org/​10.​21944/​temis-​uv-​msr2-​v2
    M., Madronich, S., & Tourpali, K. (2015). Ozone depletion and             72. Van der, A. R. J., Allaart, M. A. F., & Eskes, H. J. (2015).
    climate change: Impacts on UV radiation. Photochemical &                      Extended and refined multi sensor reanalysis of total ozone for
    Photobiological Sciences, 14(1), 19–52. https://​doi.​org/​10.​1039/​         the period 1970–2012. Atmospheric Measurement Techniques,
    c4pp9​0032d                                                                   8(7), 3021–3035. https://​doi.​org/​10.​5194/​amt-8-​3021-​2015
58. Fountoulakis, I., Natsis, A., Siomos, N., Drosoglou, T., & Bais,          73. Heinzl, F., Lorenz, S., Scholz-Kreisel, P., & Weiskopf, D. (2024).
    A. F. (2019). Deriving aerosol absorption properties from solar               Filling data gaps in long-term solar UV monitoring by statistical
    ultraviolet radiation spectral measurements at Thessaloniki,                  imputation methods. Photochemical & Photobiological Sciences,
    Greece. Remote Sensing. https://​doi.​org/​10.​3390/​rs111​82179              23(7), 1265–1278. https://​doi.​org/​10.​1007/​s43630-​024-​00593-8
59. Rieder, H. E., Jancso, L. M., Di Rocco, S., Staehelin, J., Maeder,        74. Fragkos, K., Bais, A. F., Fountoulakis, I., Balis, D., Tourpali,
    J. A., Peter, T., Ribatet, M., Davison, A. C., De Backer, H., Koe-            K., Meleti, C., & Zanis, P. (2015). Extreme total column ozone
    hler, U., Krzyścin, J., & Vaníček, K. (2011). Extreme events in               events and effects on UV solar radiation at Thessaloniki, Greece.
    total ozone over the Northern mid-latitudes: An analysis based                Theoretical and Applied Climatology, 126(3–4), 505–517.
    on long-term data sets from five European ground-based stations.              https://​doi.​org/​10.​1007/​s00704-​015-​1562-3
    Tellus B: Chemical and Physical Meteorology. https://d​ oi.o​ rg/1​ 0.​   75. Laschewski, G., & Matzarakis, A. (2023). Long-Term changes of
    1111/j.​1600-​0889.​2011.​00575.x                                             positive anomalies of erythema-effective UV irradiance associ-
60. Schwarz, M., Baumgartner, D. J., Pietsch, H., Blumthaler, M.,                 ated with low ozone events in Germany 1983–2019. Environ-
    Weihs, P., & Rieder, H. E. (2018). Influence of low ozone epi-                ments. https://​doi.​org/​10.​3390/​envir​onmen​ts100​20031
    sodes on erythemal UV-B radiation in Austria. Theoretical and             76. Petropavlovskikh, I., Evans, R., McConville, G., Manney, G.
    Applied Climatology, 133(1), 319–329. https://​doi.​org/​10.​1007/​           L., & Rieder, H. E. (2015). The influence of the North Atlan-
    s00704-​017-​2170-1                                                           tic oscillation and El Niño-Southern oscillation on mean and
61. Martínez-Lozano, J. A., Utrillas, M. P., Núñez, J. A., Tamayo, J.,            extreme values of column ozone over the United States. Atmos-
    Marín, M. J., Esteve, A. R., Cañada, J., & Moreno, J. C. (2011).              pheric Chemistry and Physics, 15(3), 1585–1598. https://​doi.​
    Ozone mini-holes over Valencia (Spain) and their influence on                 org/​10.​5194/​acp-​15-​1585-​2015
    the UV erythemal radiation. International Journal of Climatol-            77. Hinkle, D. E., Wiersma, W., & Jurs, S. G. (2003). Applied sta-
    ogy, 31(10), 1554–1566. https://​doi.​org/​10.​1002/​joc.​2173                tistics for the behavioral sciences (5th ed.). Cham: Houghton
62. Raptis, I.-P., Eleftheratos, K., Kazadzis, S., Kosmopoulos, P.,               Mifflin Company.
    Papachristopoulou, K., & Solomos, S. (2021). The combined                 78. Bojkov, R., Bishop, L., Hill, W. J., Reinsel, G. C., & Tiao, G.
    effect of ozone and aerosols on erythemal irradiance in an                    C. (1990). A statistical trend analysis of revised dobson total
    extremely low ozone event during May 2020. Atmosphere, 12(2),                 ozone data over the Northern-hemisphere. Journal of Geo-
    145. https://​doi.​org/​10.​3390/​atmos​12020​145                             physical Research-Atmospheres, 95(D7), 9785–9807. https://​
63. Fountoulakis, I., Diémoz, H., Siani, A. M., Hülsen, G., & Gröb-               doi.​org/​10.​1029/​JD095​iD07p​09785
    ner, J. (2020). Monitoring of solar spectral ultraviolet irradiance       79. Weatherhead, E. C., Reinsel, G. C., Tiao, G. C., Meng, X.-L.,
    in Aosta. Italy. Earth System Science Data, 12(4), 2787–2810.                 Choi, D., Cheang, W.-K., Keller, T., DeLuisi, J., Wuebbles,
    https://​doi.​org/​10.​5194/​essd-​12-​2787-​2020                             D. J., Kerr, J. B., Miller, A. J., Oltmans, S. J., & Frederick,
64. Diémoz, H., Siani, A. M., Casale, G. R., di Sarra, A., Serpillo,              J. E. (1998). Factors affecting the detection of trends: Statis-
    B., Petkov, B., Scaglione, S., Bonino, A., Facta, S., Fedele, F.,             tical considerations and applications to environmental data.
    Grifoni, D., Verdi, L., & Zipoli, G. (2011). First national inter-            Journal of Geophysical Research: Atmospheres, 103(D14),
    comparison of solar ultraviolet radiometers in Italy. Atmospheric             17149–17161. https://​doi.​org/​10.​1029/​98jd0​0995
    Measurement Techniques, 4(8), 1689–1703. https://​doi.​org/​10.​          80. Zeileis, A. (2004). Econometric computing with HC and HAC
    5194/​amt-4-​1689-​2011                                                       covariance matrix estimators. Journal of Statistical Software.
65. Ylianttila, L., & Schreder, J. (2005). Temperature effects of PTFE            https://​doi.​org/​10.​18637/​jss.​v011.​i10
    diffusers. Optical Materials, 27(12), 1811–1814. https://​doi.​org/​      81. McKenzie, R. L., & Lucas, R. M. (2018). Reassessing impacts
    10.​1016/j.​optmat.​2004.​11.​008                                             of extended daily exposure to low level solar UV radiation.
66. Rimmer, J. S., Redondas, A., & Karppinen, T. (2018). EuBrewNet                Science and Reports, 8(1), 13805. https://​d oi.​o rg/​1 0.​1 038/​
    – A European brewer network (COST Action ES1207), an over-                    s41598-​018-​32056-3
    view. Atmospheric Chemistry and Physics, 18(14), 10347–                   82. Fitzpatrick, T. B. (1988). The validity and practicality of sun-
    10353. https://​doi.​org/​10.​5194/​acp-​18-​10347-​2018                      reactive skin types I through VI. Archives of Dermatology,
67. McKinlay, A. F., & Diffey, B. L. (1987). A reference action                   124(6), 869–871. https://​doi.​org/​10.​1001/​archd​erm.​124.6.​869
    spectrum for ultraviolet induced erythema in human skin. CIE              83. von der Gathen, P., Kivi, R., Wohltmann, I., Salawitch, R. J.,
    Journal, 6, 17–22.                                                            & Rex, M. (2021). Climate change favours large seasonal loss
68. International Organization for Standardization and International              of Arctic ozone. Nature Communications, 12(1), 3886. https://​
    Commission on Illumination (2019).Erythema reference action                   doi.​org/​10.​1038/​s41467-​021-​24089-6
    spectrum and standard erythema dose (ISO/CIE 17166:2019).                 84. Butchart, N., Scaife, A. A., Bourqui, M., de Grandpré, J.,
    https://​www.​iso.​org                                                        Hare, S. H. E., Kettleborough, J., Langematz, U., Manzini,
69. Gröbner, J., Kazadzis, S., Schreder, J., Bolsée, D., Brogniez, C.,            E., Sassi, F., Shibata, K., Shindell, D., & Sigmond, M. (2006).
    De Backer, H., Di Sarra, A. G., Feister, U., Görts, P., Henriques,            Simulations of anthropogenic change in the strength of the
Photochemical & Photobiological Sciences

        Brewer-Dobson circulation. Climate Dynamics, 27(7–8), 727–              94. Kim, J., Cho, H. K., Mok, J., Yoo, H. D., & Cho, N. (2013).
        741. https://​doi.​org/​10.​1007/​s00382-​006-​0162-4                       Effects of ozone and aerosol on surface UV radiation variability.
    85. Pfeifroth, U., Sanchez-Lorenzo, A., Manara, V., Trentmann,                  Journal of Photochemistry and Photobiology B: Biology, 119,
        J., & Hollmann, R. (2018). Trends and variability of surface                46–51. https://​doi.​org/​10.​1016/j.​jphot​obiol.​2012.​11.​007
        solar radiation in europe based on surface- and satellite-based         95. López Figueroa, F. (2011). Climate change and the thinning of
        data records. Journal of Geophysical Research: Atmospheres,                 the ozone layer: Implications for dermatology. Actas Dermo-
        123(3), 1735–1754. https://​doi.​org/​10.​1002/​2017j​d0274​18              Sifiliográficas (English Edition), 102(5), 311–315. https://​doi.​
    86. Wild, M., Wacker, S., Yang, S., & Sanchez-Lorenzo, A. (2021).               org/​10.​1016/​s1578-​2190(11)​70813-7
        Evidence for clear-sky dimming and brightening in Central               96. Steinbrecht, W., Claude, H., Köhler, U., & Hoinka, K. P. (1998).
        Europe. Geophysical Research Letters. https://​doi.​org/​10.​1029/​         Correlations between tropopause height and total ozone: Implica-
        2020g​l0922​16                                                              tions for long-term changes. Journal of Geophysical Research:
    87. Dong, B., Sutton, R. T., & Wilcox, L. J. (2022). Decadal trends             Atmospheres, 103(D15), 19183–19192. https://​doi.​org/​10.​1029/​
        in surface solar radiation and cloud cover over the North Atlan-            98jd0​1929
        tic sector during the last four decades: Drivers and physical           97. Meng, L., Liu, J., Tarasick, D. W., Randel, W. J., Steiner, A.
        processes. Climate Dynamics, 60(7–8), 2533–2546. https://​doi.​             K., Wilhelmsen, H., Wang, L. and Haimberger, L. (2021). Con-
        org/​10.​1007/​s00382-​022-​06438-3                                         tinuous rise of the tropopause in the Northern Hemisphere over
    88. Li, J., Carlson, B. E., Yung, Y. L., Lv, D., Hansen, J., Penner, J.         1980–2020. Sci Adv, 7(45), eabi8065. https://​doi.​org/​10.​1126/​
        E., Liao, H., Ramaswamy, V., Kahn, R. A., Zhang, P., Dubovik,               sciadv.​abi80​65
        O., Ding, A., Lacis, A. A., Zhang, L., & Dong, Y. (2022). Scat-         98. Lin, P., Paynter, D., Ming, Y., & Ramaswamy, V. (2017).
        tering and absorbing aerosols in the climate system. Nature                 Changes of the tropical tropopause layer under global warming.
        Reviews Earth & Environment, 3(6), 363–379. https://​doi.​org/​             Journal of Climate, 30(4), 1245–1258. https://​doi.​org/​10.​1175/​
        10.​1038/​s43017-​022-​00296-7                                              jcli-d-​16-​0457.1
    89. Norris, J. R., Allen, R. J., Evan, A. T., Zelinka, M. D., O’Dell,       99. Steinbrecht, W., Hegglin, M. I., Harris, N., & Weber, M. (2018).
        C. W., & Klein, S. A. (2016). Evidence for climate change in                Is global ozone recovering? Comptes Rendus Geoscience, 350(7),
        the satellite cloud record. Nature, 536(7614), 72–75. https://​             368–375. https://​doi.​org/​10.​1016/j.​crte.​2018.​07.​012
        doi.​org/​10.​1038/​natur​e18273                                       100. Langematz, U. (2018). Future ozone in a changing climate.
    90. Eleftheratos, K., Kapsomenakis, J., Zerefos, C. S., Bais, A.                Comptes Rendus Geoscience, 350(7), 403–409. https://​doi.​org/​
        F., Fountoulakis, I., Dameris, M., Jöckel, P., Haslerud, A. S.,             10.​1016/j.​crte.​2018.​06.​015
        Godin-Beekmann, S., Steinbrecht, W., Petropavlovskikh, I.,             101. White, H. (1980). A heteroskedasticity-consistent covariance-
        Brogniez, C., Leblanc, T., Liley, J. B., Querel, R., & Swart,               matrix estimator and a direct test for heteroskedasticity. Econo-
        D. P. J. (2020). Possible effects of greenhouse gases to ozone              metrica, 48(4), 817–838. https://​doi.​org/​10.​2307/​19129​34
        profiles and DNA active UV-B irradiance at ground level.               102. Andrews, D. W. K. (1991). Heteroskedasticity and autocorre-
        Atmosphere. https://​doi.​org/​10.​3390/​atmos​11030​228                    lation consistent covariance matrix estimation. Econometrica.
    91. McKenzie, R., Bernhard, G., Liley, B., Disterhoft, P., Rhodes,              https://​doi.​org/​10.​2307/​29382​29
        S., Bais, A., Morgenstern, O., Newman, P., Oman, L., Brogniez,         103. Durbin, J., & Watson, G. S. (1971). Testing for serial correlation
        C., & Simic, S. (2019). Success of montreal protocol demon-                 in least squares regression. III. Biometrika, 58(1), 1–19. https://​
        strated by comparing high-quality UV measurements with                      doi.​org/​10.​1093/​biomet/​58.1.1
        “World Avoided” calculations from two chemistry-climate mod-           104. Barnes, P. W., Williamson, C. E., Lucas, R. M., Robinson, S.
        els. Science and Reports, 9(1), 12332. https://​doi.​org/​10.​1038/​        A., Madronich, S., Paul, N. D., Bornman, J. F., Bais, A. F.,
        s41598-​019-​48625-z                                                        Sulzberger, B., Wilson, S. R., Andrady, A. L., McKenzie, R.
    92. Blumthaler, M., Ambach, W., & Salzgeber, M. (1994). Effects of              L., Neale, P. J., Austin, A. T., Bernhard, G. H., Solomon, K. R.,
        cloudiness on global and diffuse Uv irradiance in a high-moun-              Neale, R. E., Young, P. J., Norval, M., & Zepp, R. G. (2019).
        tain area. Theoretical and Applied Climatology, 50(1–2), 23–30.             Ozone depletion, ultraviolet radiation, climate change and pros-
        https://​doi.​org/​10.​1007/​Bf008​64899                                    pects for a sustainable future. Nature Sustainability, 2(7), 569–
    93. McKenzie, R. L., Matthews, W. A., & Johnston, P. V. (2012).                 579. https://​doi.​org/​10.​1038/​s41893-​019-​0314-2
        The relationship between erythemal UV and ozone, derived from
        spectral irradiance measurements. Geophysical Research Letters,
        18(12), 2269–2272. https://​doi.​org/​10.​1029/​91gl0​2786




Authors and Affiliations
                                                                               2
                                                                                   Federal Institute for Occupational Safety and Health,
                                                                                   Friedrich‑Henkel‑Weg 1‑25, 44149 Dortmund, Germany
* Sebastian Lorenz                                                             3
                                                                                   Royal Meteorological Institute of Belgium, Ringlaan 3,
  slorenz@bfs.de                                                                   1180 Brussels, Belgium
1
       Federal Office for Radiation Protection, Ingolstaedter
       Landstrasse 1, 85764 Oberschleissheim, Germany
