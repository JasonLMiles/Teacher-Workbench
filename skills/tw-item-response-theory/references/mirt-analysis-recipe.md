# Optional R/mirt calibration recipe — requires execution and review

Status: instructional analysis template. R/mirt was not available in the release build environment; this recipe was not executed there. The separate Python curve demonstration was executed and checked. Never report this recipe as a fitted model until it actually runs on suitable data.

Verify the installed version and current API against the author's [mirt reference](https://philchalmers.github.io/mirt/docs/reference/mirt.html) and [item-information reference](https://philchalmers.github.io/mirt/docs/reference/iteminfo.html). The API supports binary/polytomous models, missing values as NA and optional standard-error estimation. In mirt, Rasch and generic 1PL specifications have distinct scale/variance conventions; state the actual one used.

## Prepare before running
Complete assets/model-analysis-spec.md and assets/calibration-readiness.md. Build a matrix containing only scored item responses, no IDs or group columns. Preserve a separate missing-reason and correction register. Do not recode all missing values to incorrect. The short starter below intentionally covers only a unidimensional binary Rasch fit, not arbitrary polytomous, DIF or linking analyses.

```r
# Save as analysis.R only after completing a suitable analysis specification.
# Requires a preinstalled, verified version of R and mirt.
library(mirt)
set.seed(20260929)
x <- read.csv("binary_item_responses.csv", check.names=FALSE,
              na.strings="NA", stringsAsFactors=FALSE)
stopifnot(ncol(x) >= 2, nrow(x) >= 2,
          all(vapply(x, is.numeric, logical(1))))
stopifnot(all(is.na(as.matrix(x)) | as.matrix(x) %in% c(0, 1)))
# These mechanical checks are not an adequate-sample or model-validity test.
print(colSums(!is.na(x)))
fit <- mirt(x, model=1, itemtype="Rasch", SE=TRUE,
            method="EM", verbose=FALSE)
saveRDS(fit, "rasch_fit.rds")
capture.output(sessionInfo(), file="session-info.txt")
capture.output(print(fit), file="fit-summary.txt")
capture.output(coef(fit, IRTpars=TRUE, simplify=FALSE),
               file="parameters.txt")
```

Before reporting any estimates, use the verified installed API to inspect convergence and estimation warnings, parameter uncertainty, boundary/extreme patterns, global and item fit, residual dependence and dimensionality sensitivity. Document quadrature/tolerance and any changes. Sparse tables can make fit diagnostics unavailable or unstable; state that limit instead of claiming a pass. If SE or convergence fails, do not silently refit with diagnostics omitted and present the result as complete.

For 2PL/3PL or polytomous work, author a new justified specification with appropriate scale/category checks. For DIF/linking, require the group/anchor design, model and uncertainty plan. This starter does not implement them. If the host cannot execute R or another verified library, deliver the plan and a CTT alternative where useful; do not invent output.
