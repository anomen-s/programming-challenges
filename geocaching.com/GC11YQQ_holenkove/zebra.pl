% catch SIGXCPU
:-on_signal(24, _, sig_catch).

sig_catch(_).


sel([L0|Lr], L0, Lr).
sel([L0|Lr], X, [L0|Rem]) :- sel(Lr, X, Rem).
	

sestav([X1,X2,X3,X4,X5,X6], A1, A2, A3, A4, A5, A6, R1, R2, R3, R4, R5, R6) :-
	sel(A1, X1, R1),
	sel(A2, X2, R2),
	sel(A3, X3, R3),
	sel(A4, X4, R4),
	sel(A5, X5, R5),
	sel(A6, X6, R6).


poradi(K, Z, [Z,X2,X3,X4,X5,X6]) :- 	member([Z,X2,X3,X4,X5,X6], K).
jmeno(K, Z, [X1,Z,X3,X4,X5,X6]) :- 	member([X1,Z,X3,X4,X5,X6], K).
cesta(K, Z, [X1,X2,Z,X4,X5,X6]) :- 	member([X1,X2,Z,X4,X5,X6], K).
piti(K, Z, [X1,X2,X3,Z,X5,X6]) :- 	member([X1,X2,X3,Z,X5,X6], K).
boty(K, Z, [X1,X2,X3,X4,Z,X6]) :- 	member([X1,X2,X3,X4,Z,X6], K).
gps(K, Z, [X1,X2,X3,X4,X5,Z]) :- 	member([X1,X2,X3,X4,X5,Z], K).

solve(Res) :-

	Poradi = [1, 2, 3, 4, 5],
	Jmeno = [nedobil, kecufury, dalcoin, logzvrz, peknihrad],
	Cesta = [louka, skala, potok, cesta, housti],
	Piti = [becher, caj, drson, voda, lahvac],
	Boty = [sandaly, kanady, pohorky, farmarky, jarmily],
	Gps = [csx60, pda, legend, geko, vista],
	
	sestav(K1, Poradi, Jmeno, Cesta, Piti, Boty, Gps, R1, R2, R3, R4, R5, R6),
	sestav(K2, R1, R2, R3, R4, R5, R6, S1, S2, S3, S4, S5, S6),
	sestav(K3, S1, S2, S3, S4, S5, S6, T1, T2, T3, T4, T5, T6),
	sestav(K4, T1, T2, T3, T4, T5, T6, U1, U2, U3, U4, U5, U6),
	sestav(K5, U1, U2, U3, U4, U5, U6, [], [], [], [], [], []),

	K = [K1, K2, K3, K4, K5],

%	print(K),nl,
		
	jmeno(K, nedobil, C1), 	cesta(K,louka,C1),
	jmeno(K, kecufury, C2), boty(K,sandaly,C2),
	jmeno(K, dalcoin, C3),	piti(K,becher,C3),

%	. Ten, co prelezl skálu dorazil tesne pred kacerem, co prebrodil potok.
	cesta(K, skala, C4), 	poradi([C4], TMP1, C4), TMP11 is TMP1+1,
	cesta(K, potok, C5),	poradi([C5], TMP11, C5),
	
	cesta(K, skala, C6),	piti(K, caj, C6),
	
	gpc(K, csx60, C7),	boty(K, kanady, C7),
	
	poradi(K, 3, C8),	piti(K, drson, C8),
	
	cesta(K, cesta, C9),	gps(K, pda, C9),
	
	jmeno(K, logzvrz, C10),	poradi(K, 1, C10),
	
% Majitel Legenda (Kc 3000,-) a kacer v pohorkách (Kc 1640,-) dorazili po sobe, ale hádají se, kdo z nich
	gps(K, legend, C11),	boty(K, pohorky, C12),
	poradi([C11], TMP11, C11), poradi([C12], TMP12, C12),
	TMP111 is (TMP11-TMP12), (TMP111=:=1 ; TMP111=:=(-1)),

% Kacer ve farmárkách (Kc 1660,-) a majitel PDA dorazili po sobe a taky se neví, kdo z nich drív	
	boty(K, farmarky, C13),	gps(K, pda, C14),
	poradi([C13], TMP13, C13), poradi([C14], TMP14, C14),
	TMP131 is (TMP13-TMP14), (TMP131=:=1 ; TMP131=:=(-1)),
	
	gps(K, geko, C20),	piti(K, voda, C20),
	
%Logzvrz a ten, kdo vyskocil z houští dorazili po sobe, kdo z nich drív, není známo.
	cesta(K, housti, C22),	poradi(K, 2, C22),


	jmeno(K, peknihrad, C25),	gps(K, vista, C25),

%  Majitel Legenda a ten, co mel s sebou lahváce (Kc 20,-) dorazili po sobe, ale ani tady se neví, kdo z nich drív
	gps(K, legend, C30),	piti(K, lahvac, C31),
	poradi([C30], TMP30, C30), poradi([C31], TMP31, C31),
	TMP300 is (TMP30-TMP31), (TMP300=:=1 ; TMP300=:=(-1)),
	

	Res = K,
	print(Res).
