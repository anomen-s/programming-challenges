transpose([[]|_], []).
transpose(M, [X|T]) :-
    row(M, X, M1),
    transpose(M1, T).

row([], [], []).
row([[X|Xs]|Ys], [X|R], [Xs|Z]) :- row(Ys, R, Z).

item(B, R, C, Res) :-
    nth1(R, B, Row),
    nth1(C, Row, Res).

solveBoard(B, R, C) :-
    solveRows(B, R),
    transpose(B, BT),
    solveRows(BT, C).


solveRows([], []).
solveRows([Row1|Rows], [R1|Rs]) :-
    genRow(Row1),
%    length(Rows, L), print([Row1, R1, L]),nl,
    sumlist(Row1, R1),
    solveRows(Rows, Rs).

genRow([]).
genRow([R0|Rows]) :-
    numlist(0, 25, Nums),
    member(R0, Nums),
    genRow(Rows).

distinctlist([]).
distinctlist([N0|NR]) :-
    distinctlist(N0, NR),
    distinctlist(NR).
distinctlist(_, []).
distinctlist(N, [N0|NR]) :-
    N=\=N0,
    distinctlist(N, NR).


solve0(B) :-
    B=[[C, T, T], [S, C, M], [C, M, S]],
    solveBoard(B, [13, 12, 12], [8,15,14]),
    distinctlist([C,T,S,M]).

solve1(B) :-
    B=[[C, T, T], [S, C, M], [C, M, S]],
    solveBoard(B, [24, _, 23], [36,20,14]),
    distinctlist([C,T,S,M]).

solve2(B) :-
    B=[[TL, R, T], [A, A, RR], [TL, TL, T]],
    solveBoard(B, [15, 20, 24], [29,_,10]),
    distinctlist([TL,R,T,A,RR]).

solve3(B) :-
    B=[[BL, RR, BL], [RR, D, D], [RR, P, P]],
    solveBoard(B, [48, 18, _], [51,21,18]),
    distinctlist([BL,RR,D,P]).

solve4(B) :-
    B=[[AR, R, M], [AR, M, M], [R, LR, LR]],
    solveBoard(B, [14, 2, 22], [16,17,_]),
    distinctlist([AR, R,M, LR]).

solve5(B) :-
    B=[[NR, C,  BL], [HC, NR, C], [C, BL, HC]],
    solveBoard(B, [15, 14, 9], [14,15,_]),
    distinctlist([NR, C, BL, HC]).

% 2. radek

solve6(B) :-
    B=[[BR, CU,  AR], [PC, PC, CU], [BR, BR, AR]],
    solveBoard(B, [10, _, 8], [7,9,15]),
    distinctlist([BR, CU, AR, PC]).

solve7(B) :-
    B=[[BA, L,  A], [BA, RA, L], [L, A, RA]],
    solveBoard(B, [_, 9, 8], [11,8,8]),
    distinctlist([BA, L, A, RA]).

solve8(B) :-
    B=[[BR, D,  TR], [T, CR, TR], [C, C, BR]],
    solveBoard(B, [18, 20, 21], [_,18,19]),
    distinctlist([BR, D, TR, T, CR, C]).

solve9(B) :-
    B=[[R, SQ,  ST], [SQ, CR, SQ], [CR, ST, R]],
    solveBoard(B, [16, 23, 9], [_,15,16]),
    distinctlist([SQ, ST, CR, R]).

solve10(B) :-
    B=[[O, D,  O], [R, D, R], [SQ, O, SQ]],
    solveBoard(B, [27, _, 12], [17,24,17]),
    distinctlist([O, D, R, SQ]).

solve([B0, [B1], []]):-
    solve0(B0),
    solve1(B1),
    solve3(B3),
    solve4(B4),
    solve6(B6),
    solve9(B9),
    solve10(B10),

    solve2(B2),
    item(B2, 1, 3, B213), member(B213, [9,0,1]),
    item(B2, 1, 2, B212),


    solve5(B5),
    item(B5, 1, 1, B511), B511=9, % tip

    solve7(B7),
    item(B7, 2, 2, B722), member(B722, [2,3]),
    
    solve8(B8),
    item(B8, 2, 2, B822), B822 < 10,
%    item(B8, 1, 2, B212), % same symbol ?


    print('test  '), print(B0), nl,
    print('---'), nl,
    print(B1),nl,
    print(B2),nl,
    print(B3),nl,
    print(B4),nl,
    print(B5),nl,
    print('---'), nl,
    print(B6),nl,
    print(B7),nl,
    print(B8),nl,
    print(B9),nl,
    print(B10),nl,
    
    print('---'), nl,
    
    item(B7, 2, 2, N1),
    item(B2, 1, 3, N2),
    item(B10, 1, 2, N3),
    item(B6, 1, 3, N4),
    item(B8, 2, 2, N5),
    print([50,N1, N2, N3, N4, N5]), nl,

    item(B3, 2, 2, E1),
    item(B5, 1, 1, E2),
    item(B9, 1, 1, E3),
    item(B1, 2, 1, E4),
    item(B4, 2, 3, E5),
    print([14,E1,E2,E3,E4,E5]), nl.


% ? = 0 2 4 8
%
% [50,3,0,7,6,?]
% [14,0,9,4,8,0]
