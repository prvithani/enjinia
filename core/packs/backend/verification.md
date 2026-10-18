# backend: verification

Tiers: formal (TLA+ via `core/scripts/tlc`), property, example
(spec section 4.5).

## Evidence for trace_check

trace_check reads JUnit XML. Produce it by wrapping the repo's own run, not
by changing the repo's runner:

- Clojure: `clojure.test.junit/with-junit-output` around `run-tests`,
  writing to a file:
  `(with-open [w (io/writer "report.xml")] (binding [clojure.test/*test-out* w] (clojure.test.junit/with-junit-output (clojure.test/run-tests 'ns ...))))`
- Python: `pytest --junitxml=report.xml`.
- ClojureScript and others: the runner's JUnit reporter if it has one;
  otherwise record the summary in `review.md` and mark the evidence
  `summary-only`.

Test names in the report must equal the `deftest` names that carry
`covers` metadata.
