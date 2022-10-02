# vispupu

## 项目简介
写这个项目是因为隔离玩游戏玩到了圣人模式，不想学习，又玩不下去了。

灵感来源于徐老师文章：[A Basic Checklist for Observational Studies in Political Science](http://yiqingxu.org/public/checklist.pdf)。目前，越来越多的社会科学学者开始把Python作为自己分析工具，但这些主要是用于机器学习相关的工作，而社科传统手艺，解释与推断还是大量依赖R。因此，对于社科学者而言，无论是数据探索，还是数据分析的包都不是很完善（有一说一，Seaborn的封装其实很不错），于是本社科混子试着写了自己第一个包vispupu，希望可以让社科学者用python多少更顺手一点（额，其实也就是瞎写写，不然不会两年不动了）。  

画图工作由matplotlib完成，但是目前版本非常简陋，如果想要修改可以使用matplotlib自定义。
  
主要做的事情是把徐老师的一些建议写成了简单的函数，具体对对应如下： 
- **keyvarview**: Draw the histograms of the key variables, including the treatment and the outcome. Are these distributions highly skewed or have outliers?（完成）
- **missingview**: Understand the missing data problem in your data by making a plot and think about how to deal with it.（完成）
- **vvview**: Draw a bivariate scatterplot of the treatment and the outcome or a scatterplot between the residualized treatment and residualized outcome. Overlay it with a loess curve. Does your result hold when you “winsor” 5% of the extreme values in your treatment or outcome variables?（完成）
- **panelview**: 
  - If you’re analyzing panel data, understanding where your treatment variation comes is crucial. Draw a plot to show how the treatment status changes within a unit over time（完成）
  - If you use a regression discontiguity (RD) design, draw a RD plot for the reduced form. If it’s a fuzzy RD, draw one for the first stage as well. Same for an interrupted time series design.（完成）
- **resultview**: Whisker dot plot to show model result. （这个不是徐老师提到的，只是因为感觉python很少这部分，所以写了一个简单的，完成）

但是目前也有一些没有完成的部分，主要是还在学习，而且写这部分感觉需要移植徐老师的包——我一个社科混子恐怕暂时是做不了的（我尽量努力，只要怪物猎人打的不顺利，我就一定有机会！！）：
- **didview**:If you use difference-in-differences design (or use a twoway fixed effects model), draw a dynamic treatment effect plot.
- - **interview**: If you model includes an interaction term, check whether the linearity assumption looks plausible.（
- **ivview**: If you use an instrumental variable (IV) design, compare your IV estimates with your OLS estimates. A big discrepancy is suspicious (if your primary concern for the OLS is upward bias) and needs explanation. When your instrument, treatment, and outcome variables are continuous, plotting both the first-stage and the reduced form relationships will be helpful.
- 下一步计划是做一些主题模型的封装




