# A tutorial for outlier detection based on sub-population

## What is outlier detection, or anomaly detection?

Outlier detection (also called anomaly detection) refers to the problem of finding patterns in data that do not conform to the expected normal behavior.
Different approaches share the same basic idea: to define certain model as normal cases, outliers are defined as those cases which do not fit the model.
For example, we can define normal cases of heart beat rates as follows: (1) for children 10 years and older,
and adults (including seniors) is 60 - 100 beats per minute; (2) for well-trained athletes is 40 - 60 beats per minute.
So, an adult whose heart beats 40 times per minute is abnormal, and should see the doctor. A well-trained athlete
whose heart beats 100 times per minute is an abnormal case. This example introduces an important concepts in
outlier-detection: subpopulation.

## Local Outlier Factors based on Subpopulation
Whether an object is normal or abnormal within a group, largely relates to the way we define the group.
A man with the height of 1.60 meter is abnormal in north Europe, but normal in the south of Asia.
People die at the age of  40 is normal in some African countries, but abnormal in European countries.
To identify abnormal data in a large dataset, we need to delineate groups to which this data belong.
This introduces the subpopulation-based outlier detection method, i.e. Fleischhacker, et al. (2014)

Fleischhacker, et al. (2014). Fleischhacker, D., Paulheim, H. Bryl, Völker, J., Bizer, Ch.
Detecting Errors in Numerical Linked Data using Cross-Checked Outlier Detection.
In: 13th International Semantic Web Conference, pp 357-372, Riva del Garda, Italy, October 19-23, 2014. Proceedings, Part I.
