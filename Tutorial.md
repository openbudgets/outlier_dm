# A tutorial for outlier detection based on sub-population

* What is outlier detection, or anomaly detection?

Outlier detection (also called anomaly detection) refers to the problem of finding patterns in data that do not conform to the expected normal behavior.
Different approaches share the same basic idea: to define certain model as normal cases, outliers are defined as those cases which do not fit the model.
For example, we can define normal cases of heart beat rates as follows: (1) for children 10 years and older,
and adults (including seniors) is 60 - 100 beats per minute; (2) for well-trained athletes is 40 - 60 beats per minute.
So, an adult whose heart beats 40 times per minute is abnormal, and should see the doctor. A well-trained athlete
whose heart beats 100 times per minute is an abnormal case. This example introduces two important concepts in
outlier-detection: subpopulation, and frequent pattern.
