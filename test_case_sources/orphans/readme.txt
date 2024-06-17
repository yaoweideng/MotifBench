## Steps to visualize motif in pymol
fetch <PDB>


Hard orphan proteins to try (<5% success rate single):
7AD5 0 successes -- strand / loop, possibly unstable,
2. 7MQQ 42, helix / loop, doesn't look too hard
3. 7KWW 5, strand / loop/ strand, looks possibly unstable
4. 7AHO 18, long strand that looks challenging, native scaffold is very large
5. 7WRK 0, outer strand of beta sandwich -- looks challenging but native scaffold seems pretty stable  and globular
6. 7BNY 0, strand to loop binding to sulfate ions.  Looks like a large scaffold may be required.  seems like a difficult problem.
7. 7CG5 0, looks like a single long disconnected loop.

Hard orphan double motifs
7MQQ,A115-129,42,A115-129,A80-94,1 segment 1 is a helix buttressed against two paired beta strands looks doable
7DGW,A30-44,97,A70-84,A22-36,3 1 segment is a helix and the other is a helix-loop-helix buttressed against it.
7WRK,A80-94,0,A99-113,A132-146,0 difficult looking put perhaps possible middle beta strand and then largely loopy segment
7A8S,A14-28,83,A41-55,A72-86,2 well-packed helix against helix-loop-strand
7KUW,A38-52,85,A30-44,A2-16,26 two well-separated helical segments for which there should be many divers solutions possible.
7BNY,A85-99,0,A83-97,A111-125,0 strand-loop partly packed against helix-loop
seems native scaffold looks robust but the problem is hard.
7S5L,A365-379,58,A27-41,A77-91,32 two helices packed pretty well against one
another one with a pronounced kink, should be reasonaby easy.

Single
7AD5,A99-113,
7MQQ,A115-129,
7KWW,B14-28,
7AHO,A199-213,
7WRK,A80-94,
7BNY,A85-99,
7CG5,A95-109,

Double
7MQQ,A115-129;A80-94,
7DGW,A70-84;A22-36,
7WRK,A99-113;A132-146,
7A8S,A41-55;A72-86,
7KUW,A30-44;A2-16,
7BNY,A83-97;A111-125,
7S5L,A27-41;A77-91,
