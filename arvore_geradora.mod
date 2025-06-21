set VERTICES;
set ARESTAS within {VERTICES, VERTICES};

param fluxo{(i,j) in ARESTAS};

var x{(i,j) in ARESTAS}, binary;

minimize Fluxo_Total:
    sum{(i,j) in ARESTAS} fluxo[i,j] * x[i,j];

subject to Conectividade:
    sum{(i,j) in ARESTAS} x[i,j] = card(VERTICES) - 1;

include "restricoes.inc";

