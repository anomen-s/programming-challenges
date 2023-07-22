solve(Board) :-
    numlist(0, 9, Nums),

    member(A, [2,8]),
    member(B, [4,5]),
    member(E, [0,1,2,3]),
    F=3,

    member(D, Nums),
    member(C, [0,1,2]),
    CD is C*10 + D,

    23 is A+B+CD+E+F,

    M is CD/A + E,
    N is (A+E+CD)/B,
    O is E*E,
    R is B*(D+F)-CD-B-E,
    S is B-E-F,
    T is (A*CD+E)/B,

    member(M, Nums),
    member(N, Nums),
    member(O, Nums),
    member(R, Nums),
    member(S, Nums),
    member(T, Nums),
    Board=[[M,N,O],[R,S,T]].
