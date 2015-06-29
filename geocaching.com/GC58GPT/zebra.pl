vedle(M1,M2, [M1,M2|_]).
vedle(M1,M2, [M2,M1|_]).
vedle(M1,M2, [_|Lodi]) :-
    vedle(M1, M2, Lodi).

poradi(M1,M2, [M1,M2|_]).
poradi(M1,M2, [_|Lodi]) :-
    poradi(M1, M2, Lodi).


narodnost([], []).
narodnost([s(M,_,_,_,_)|Lodi], Prvky):-
    select(M, Prvky, P2),
%    print('select '), print([M]),print(Prvky),print(P2),nl,
    narodnost(Lodi, P2).

komin([], []).
komin([s(_, M,_,_,_)|Lodi], Prvky):-
    select(M, Prvky, P2),
    komin(Lodi, P2).

cil([], []).
cil([s(_, _,M,_,_)|Lodi], Prvky):-
    select(M, Prvky, P2),
    cil(Lodi, P2).

naklad([], []).
naklad([s(_, _,_,M,_)|Lodi], Prvky):-
    select(M, Prvky, P2),
    naklad(Lodi, P2).

odjezd([], []).
odjezd([s(_, _,_,_, M)|Lodi], Prvky):-
    select(M, Prvky, P2),
    odjezd(Lodi, P2).

%%%%%%%%%%
%s(narodnost,komin, cil, naklad,cas)
%%%%%%%%%%

solve(Board) :-
 Board=[S1,_,S3,_,S5],
    S3=s(_,cerny, _, _, 8),

 narodnost(Board, [recka, spanelska, anglicka, francouzska,  brazilska]),

     member(s(recka, cerveny, hamburk, kava, 6), Board),
     member(s(francouzska, modry, _, _, _), Board),

 komin(Board, [cerny, bily, zeleny, modry, cerveny]),

     member(s(brazilska, _, manila, _, _), Board),

 cil(Board, [marseille, manila, hamburk, portsaidu, janov]),

     member(s(_, _, _, obili, _), [S1,S5]),
     
 naklad(Board, [kava, kakao, obili, ryze, caj]),

     poradi(s(francouzska, modry, _, _,_), s(_,_,_,kava,_), Board),
     vedle(s(_, _, _, ryze,_), s(_,zeleny,_,_,_), Board),
     vedle(s(_, _, _, ryze,_), s(_,_,_,obili,_), Board),
     vedle(s(_, _, _, _,7), s(_,bily,_,_,_), Board),
     poradi(s(_, _, _, kakao,_), s(_,_,marseille,_,_), Board),
     poradi(s(_, _, marseille, _,_), s(spanelska,_,_,_,7), Board),
     member(s(anglicka, _, _, _, 9), Board),
     member(s(_, _, janov, _, 5), Board),

 odjezd(Board, [5, 6, 7, 8, 9]),

 
 print(Board),nl,
 nl.


%---------
% Loď vezoucí obilí kotví vedle lodi vezoucí rýži.
% Vedle lodi, která vyplouvá v 7, je loď s bílým komínem.
% Španělská vyráží v 7 a je napravo lodi jedoucí do Marseile.
% Vedle lodi vezoucí rýži je loď se zeleným komínem.
% Prostřední má černý komín.
% Loď s černým komínem vyplouvá v osm.
% Řecká vyplouvá v 6 a veze kávu.
% Do Hamburku vyplouvá loď v šest.
% Anglická vyplouvá v 9.
% Brazilská loď má namířeno do Manily.
% Loď do Janova vyplouvá v 5.
% Do Hamburka jede loď s červeným komínem.
% Loď kotvící na kraji veze obilí.
% Francouzská je vlevo od lodi vezoucí kávu a má modrý komín.
% Hned vpravo od lodi vezoucí kakao je loď, která jede do Marseille.
