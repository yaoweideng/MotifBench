# Test cases

We drop several 11 examples from the original 25 problems in the benchmark:
* Four problems have short, medium, and long variations with the same motif.
  These are replaced with a single problem.
* One problem (6VW1) involves building a scaffold comprising two chains and
  so is dropped
* Two problems (1PRW and 1QJG) have particularly been known to have
  particularly large discrepancies between AF2 single   sequence and ESMfold
  predictions.


There was a mistake in the benchmark specification (supplementary table 9)
in the range specification for the motif extracted from 6EXZ.  The table
indicates the range A28-42 but this is beyond the range experimentally
resolved residues.  The mistake was that the motif was indexed based on the
first resolved residue and is corrected in the updated motif specification.


