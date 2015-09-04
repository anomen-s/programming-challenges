%3) Billyho manzelka Aghata ma rada modrou barvu.
%6) Arthur a Ria si odnesli knihu Posledni poklona Sherlocka Holmese.
%7) Johnova manzelka ma rada zlutou barvu a prinesla knihu Studie v sarlatove.
%9) Knihu Udoli strachu si odvezl jeden manzelsky par v Mercedesu-Benz.
%12) Jamesova manzelka ma rada fialovou barvu.
%14) Joel , ktery odjel ve voze Bentley, prinesl Navrat Sherlocka Holmese.
%15) Manzele, kteri prinesli knihu Pes baskervilsky, si odvezli knihu Studie v sarlatove.
%16) Daimlerem odjela milovnice zelene barvy.
%17) Hotelieri si odvezli knihu Pes baskervilsky.
%18) Fordem odjeli inspektori.
%19) Amy odjela v BMW, prinesla knihu Posledni poklona Sherlocka Holmese a odvezla si knihu, kterou prinesli manzele Weaverovi.
%20) Tomyho manzelce se libi bila barva a odvezla si knihu Podpis ctyr.
%21) Knihu Archiv Sherlocka Holmese prinesla dama, ktera ma rada hnedou barvu a odjela z letiste Jaguarem.
%22) Knihu Podpis ctyr prinesli manzele, kteri odjeli Rolls-Roycem “

printres([]).
printres([X|R]) :-
    print(X), nl,
    printres(R).

solve(R) :-
	A=t(kellet,	tovarnik, K1,	navrat_sh, B1,	M1,	F1,	A1),
	B=t(pitt,	spisovatel,K2,	R1,	B2,	M2,	F2,	A2),
	C=t(lowen,	Z1, 	K3,	R2,	cervena, mark,	janet,	A3),
	D=t(miller,	ucitel,	K4,	R3,	B3,	M3,	jennifer, praga_alfa),
	E=t(lemon,	ucetni,	dobrodruz_sh, R4, B4,	M4,	F3,	A4),
	F=t(davenheim,	banker,	K5,	R5,	B5,	M5,	eva,	A5),
	G=t(moss, 	Z2,	K6,	R6,	ruzova,	M6,	ellie,	A6),
	H=t(weaver, 	cestovatel, K7,	R7,	B6,	clint,	zoe,	A7),
	R=[D,C,A,E,F,G,B,H],

	member(t(_, cestovatel, _, _, _, clint, zoe, _), R),
	member(t(_, hotelier, _, pes_basker, _, _, _, _), R),
	member(t(_, inspektor, _, _, _, _, _, ford), R),
	member(t(_, _, _, _, modra, bill, aghata, _), R),
	member(t(_, _, posl_poklona_sh, K7, _, _, amy, bmw), R),
	member(t(_, _, _, posl_poklona_sh, _, arthur, ria, _), R),
	member(t(_, _, studie_sarlat, _, zluta, john, _, _), R),
	member(t(_, _, _, udoli_strachu, _, _, _, mercedes), R),
	member(t(_, _, _, _, fialova, james, _, _), R),
	member(t(_, _, navrat_sh, _, _, joel, _, bentley), R),
	member(t(_, _, pes_basker, studie_sarlat, _, _, _, _), R),
	member(t(_, _, _, _, zelena, _, _, daimler), R),
	member(t(_, _, _, podpis_ctyr, bila, tomy, _, _), R),
	member(t(_, _, archiv_sh, _, hneda, _, _, jaguar), R),
	member(t(_, _, podpis_ctyr, _, _, _, _, rolls_royce), R),

	K5 \= R5,  % obecne Kx \= Rx

	printres(R),
	nl.

