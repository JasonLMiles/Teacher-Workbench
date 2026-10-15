# Formula patterns
Illustrative English/US formula syntax; adapt to the actual locale and column references. Verify in the destination. These formulas are not instructional cut scores.

Assume C2 = earned/observed count, D2 = possible/opportunities, E2 = status. Enter a comparable count only when the status is `observed`.

Percent in F2:
```excel
=IF(OR(E2<>"observed",COUNT(C2:D2)<2,D2<=0),"",C2/D2)
```
COUNT checks that both counts are numeric and retains a measured zero. Validate missing-value behavior in the actual calculation engine rather than relying on an untested empty-string equality check.

Format F as percent. Validate C and D as nonnegative with C <= D for a success/opportunity measure; use a different design for metrics where that relationship does not apply. A genuine 0/10 yields 0%; an absent or unobserved record stays blank.

Equal-weight mean of nonblank comparable percentages:
```excel
=IF(COUNT(F2:F101)=0,"",AVERAGE(F2:F101))
```
An equal-weight mean of observations differs from pooled success/opportunity counts when denominators vary. Select and label the intended interpretation; never average scores from unrelated constructs. A graph must identify metric, dates, units and relevant support/task changes.
