# vispupu

## 项目简介
灵感来源于徐老师文章：[A Basic Checklist for Observational Studies in Political Science](http://yiqingxu.org/public/checklist.pdf)。目前，越来越多的社会科学学者开始把Python作为自己分析工具，但这些主要是用于机器学习相关的工作，而社科传统手艺，解释与推断还是大量依赖R。因此，对于社科学者而言，无论是数据探索，还是数据分析的包都不是很完善（有一说一，Seaborn的封装其实很不错），于是本社科混子试着写了自己第一个包vispupu，希望可以让社科学者用python多少更顺手一点。  

目前写的十分简单
  
主要做的事情是把徐老师的建议写成了一些建议函数，具体功能如下： 
- **keyvarview**: Draw the histograms of the key variables, including the treatment and the outcome. Are these distributions highly skewed or have outliers?
- **missingview**: Understand the missing data problem in your data by making a plot and think about how to deal with it.
- **vvview**: Draw a bivariate scatterplot of the treatment and the outcome or a scatterplot between the residualized treatment and residualized outcome. Overlay it with a loess curve. Does your result hold when you “winsor” 5% of the extreme values in your treatment or outcome variables?
- **interview**: If you model includes an interaction term, check whether the linearity assumption looks plausible.
- **panelview**: If you’re analyzing panel data, understanding where your treatment variation comes is crucial. Draw a plot to
show how the treatment status changes within a unit over time
- **didview**:If you use difference-in-differences design (or use a twoway fixed effects model), draw a dynamic treatment
effect plot.
- **ivview**: If you use an instrumental variable (IV) design, compare your IV estimates with your OLS estimates. A big discrepancy is suspicious (if your primary concern for the OLS is upward bias) and needs explanation. When your instrument, treatment, and outcome variables are continuous, plotting both the first-stage and the reduced form relationships will be helpful.
- **resultview**: Whisker dot plot to show model result. 

## 简明使用指南


