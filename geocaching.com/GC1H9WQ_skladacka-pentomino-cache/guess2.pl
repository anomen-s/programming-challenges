:- on_signal(24, _, sig_catch).
sig_catch(_).

% Pentomino Cache

% board, piece, startpos, id, outboard
fill(Board, [P|PX], Start, ID) :-
	CP is P+Start,
	nth0(CP, Board, ID),
	fill(Board, PX, Start, ID).

fill(_, [], _, _).

printboard(B,W) :-
    getrow(B,W,Row,Rest),
    print(Row), nl,
    printboard(Rest,W).

printboard([],_) :- print('------'),nl.

getrow([B0|B], W, [B0|R], Rest) :-
    W > 0, W1 is W-1,
    getrow(B, W1, R, Rest).

getrow(R, 0, [], R).

checkwidth(W, PW, Pos) :-
    Left is Pos mod W,
    Max is W - PW,
    Left =< Max.

shape(R, W, Shapes) :-
    member(S, Shapes),
    reshape(S, W, R).

reshape([S0|S], W, [R0|Res]) :-
    R0 is (S0 mod 10) + ((S0//10)*W),
    reshape(S, W, Res).

reshape([], _, []).
    

solve(B) :-
	length(B, 60), %deska
	member(W, [10,5,12,6]), %vybrat_sirku
	MaxPos is 60-W-1,
	numlist(0,MaxPos,PList), %pozice_pro_levy_horni_roh_dilku

	shape(AShape, W, [[0,1,2,11,21],[1,11,20,21,22]]),
	shape(BShape, W, [[2,10,11,12,13],[0,1,2,3,11]]),
	shape(CShape, W, [[1,10,11,12,21]]),
	shape(DShape, W, [[0,10,11,12,22]]),
	shape(EShape, W, [[0,10,11,12,21]]),
	shape(FShape, W, [[3,10,11,12,13]]),
	shape(GShape, W, [[0,1,11,12,13]]),
	shape(HShape, W, [[0,10,11,21,22]]),
	shape(IShape, W, [[0,10,20,30,40]]),
	shape(JShape, W, [[0,1,10,20,21]]),
	shape(KShape, W, [[0,1,2,10,11]]),
	shape(LShape, W, [[0,10,20,21,22], [0,1,2,12,22]]),
	
	select(PosA, PList, PL1),
	checkwidth(W, 3, PosA),
	fill(B, AShape, PosA, a_8),

	select(PosB, PL1, PL2),
	checkwidth(W, 4, PosB),
	fill(B, BShape, PosB, b_8),

	select(PosC, PL2, PL3),
	checkwidth(W, 3, PosC),
	fill(B, CShape, PosC, c_0),

	select(PosD, PL3, PL4),
	checkwidth(W, 3, PosD),
	fill(B, DShape, PosD, d_5),

	select(PosE, PL4, PL5),
	checkwidth(W, 3, PosE),
	fill(B, EShape, PosE, e_1),

	select(PosF, PL5, PL6),
	checkwidth(W, 4, PosF),
	fill(B, FShape, PosF, f_2),

	select(PosG, PL6, PL7),
	checkwidth(W, 4, PosG),
	fill(B, GShape, PosG, g_3),

	select(PosH, PL7, PL8),
	checkwidth(W, 3, PosH),
	fill(B, HShape, PosH, h92),

	select(PosI, PL8, PL9),
	checkwidth(W, 1, PosI),
	fill(B, IShape, PosI, i71),

	select(PosJ, PL9, PLA),
	checkwidth(W, 2, PosJ),
	fill(B, JShape, PosJ, je4),

	select(PosK, PLA, PLB),
	checkwidth(W, 3, PosK),
	fill(B, KShape, PosK, k_5),

	printboard(B, W),

	select(PosL, PLB, _),
	checkwidth(W, 3, PosL),
	fill(B, LShape, PosL, ln0),

	printboard(B, W).
