## Notes:
* L2 is not robust to outliers as square terms blows up the error differences of the outliers and the regularization term tries to fix it by penalizing the weights.
* Ridge regression performs better when all the input features influence the output and all with weights are of roughly equal size.

And,<br>
**L1 Regularization**<br>
* L1 penalizes sum of absolute value of weights.
* L1 has a sparse solution
* L1 has multiple solutions
* L1 has built in feature selection
* L1 is robust to outliers
* L1 generates model that are simple and interpretable but cannot learn complex patterns<br>

**L2 Regularization**<br>
* L2 regularization penalizes sum of square weights.
* L2 has a non sparse solution
* L2 has one solution
* L2 has no feature selection
* L2 is not robust to outliers
* L2 gives better prediction when output variable is a function of all input features
* L2 regularization is able to learn complex data patterns
