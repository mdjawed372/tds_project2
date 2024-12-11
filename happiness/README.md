# Analyzing Global Well-Being: Insights from Life Ladder Data

## Dataset Description

In a quest to understand global well-being, we examined a comprehensive dataset comprising various socio-economic indicators across multiple countries over several years. The dataset contains the following columns:

- **Country name**: Name of the country 
- **Year**: The specific year of the observation
- **Life Ladder**: A measure of subjective well-being, capturing how individuals rate their current lives
- **Log GDP per capita**: The logarithm of the GDP per capita, representing economic prosperity
- **Social support**: A measure indicating how much individuals feel they have someone to rely on
- **Healthy life expectancy at birth**: Expected years of life in good health at birth
- **Freedom to make life choices**: A measure of the level of freedom individuals feel they have in making life choices
- **Generosity**: A metric indicating the degree of charitable behavior in each country
- **Perceptions of corruption**: How individuals perceive the level of corruption in their society 
- **Positive affect**: The frequency with which people experience positive emotions
- **Negative affect**: The frequency of negative emotions experienced by individuals
- **is_outlier**: A flag indicating whether the data point is an outlier

## Types of Analysis Performed

1. **Missing Value Handling**: 
   We began by examining the dataset for missing values. Initial findings indicated that several columns had a small percentage of missing entries, particularly in the **Generosity** and **Perceptions of corruption** columns. We applied median imputation for numeric fields and mode imputation for categorical fields to ensure that our analysis remained robust without losing significant data.

2. **Correlation Analysis**: 
   Next, we conducted a correlation analysis to understand how various factors interact with the **Life Ladder** score. A heatmap visualizing the correlations showed that **Social support**, **Log GDP per capita**, and **Healthy life expectancy at birth** had strong positive correlations with **Life Ladder**, suggesting that higher levels of these indicators were associated with greater life satisfaction.

3. **Outlier Detection using Isolation Forest**: 
   We implemented an Isolation Forest algorithm to identify outliers in the dataset. This was particularly useful in discovering countries that reported unusually high or low **Life Ladder** scores compared to their socio-economic indicators, revealing data points that warranted closer examination.

4. **Clustering using K-Means**: 
   Finally, we utilized K-Means clustering to group countries based on their socio-economic attributes. After standardizing our data, we determined that 4 clusters provided meaningful divisions. Countries within the same cluster displayed similarities in terms of their **Life Ladder** scores and the underlying variables.

## Key Findings and Insights

- The analysis revealed that higher **Log GDP per capita** significantly correlates with better **Life Ladder** scores, underscoring the impact of economic strength on subjective well-being.
- Countries with stronger **Social support** systems tend to report higher life satisfaction, indicating the importance of community and relationships.
- Outliers were found primarily in developing nations, where **Life Ladder** ratings were unexpectedly low despite relatively high GDP per capita, prompting questions about social and political factors affecting individual happiness.
- The K-Means clustering identified distinct groupings, with one cluster consisting of high-income countries exhibiting high scores across all indicators, while another cluster contained low-income countries where low scores on economic and social metrics translated to lower well-being.

## Implications and Suggestions

The insights drawn from this analysis offer several significant implications:

- **Policy Development**: Policymakers should focus on enhancing social support systems and community connectivity in regions where it correlates strongly with well-being. This can involve investing in mental health programs and community centers.
- **Economic Strategies**: Economic policies should not just aim at increasing per capita income but also consider improving social services, healthcare access, and reducing corruption to elevate subjective well-being.
- **Further Study**: Further qualitative research should be conducted to comprehend the socio-political environments of the outliers identified. Understanding these dynamics can aid in addressing the unique factors impacting life satisfaction in those nations.
- **Targeted Interventions**: Tailoring interventions in lower-income countries to address both economic development and social welfare will be essential in improving overall life satisfaction ratings.

By leveraging these insights, nations can strive toward improving quality of life and enhancing the well-being of their citizens.