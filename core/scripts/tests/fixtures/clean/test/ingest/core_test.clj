(ns ingest.core-test
  (:require [clojure.test :refer [deftest is]]))

(deftest ^{:covers [:INV-2]} no-loss-on-crash (is true))
(deftest ^{:covers [:FR-1]} accepts-valid (is true))
(deftest ^{:covers [:INV-1 :BR-2]} apply-once (is true))
