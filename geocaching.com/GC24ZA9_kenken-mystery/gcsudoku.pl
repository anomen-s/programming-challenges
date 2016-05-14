
numbers([1,2,3,4,5,6,7,8,9]).

row(A1,A2,A3,A4,A5,A6,A7,A8,A9) :-
	A1=\=A2,A1=\=A3,A1=\=A4,A1=\=A5,A1=\=A6,A1=\=A7,A1=\=A8,A1=\=A9,
	A2=\=A3,A2=\=A4,A2=\=A5,A2=\=A6,A2=\=A7,A2=\=A8,A2=\=A9,
	A3=\=A4,A3=\=A5,A3=\=A6,A3=\=A7,A3=\=A8,A3=\=A9,
	A4=\=A5,A4=\=A6,A4=\=A7,A4=\=A8,A4=\=A9,
	A5=\=A6,A5=\=A7,A5=\=A8,A5=\=A9,
	A6=\=A7,A6=\=A8,A6=\=A9,
	A7=\=A8,A7=\=A9,
	A8=\=A9.

% select item
sel([L0|Lr], L0, Lr).
sel([L0|Lr], X, [L0|Rem]) :-
	sel(Lr, X, Rem).

printrow([A,B,C,D,E,F,G,H,I|R],R) :-
	print(A),print(' '),print(B),print(' '),print(C),print(' '),print(D),print(' '),
	print(E),print(' '),print(F),print(' '),print(G),print(' '),print(H),print(' '),
	print(I),nl.
printboard(B):-
	printrow(B,R1),printrow(R1,R2),printrow(R2,R3),
	printrow(R3,R4),printrow(R4,R5),printrow(R5,R6),
	printrow(R6,R7),printrow(R7,R8),printrow(R8,[]).


solve(Board) :-
	numbers(N),

	
	Board = [
	A1,B1,C1,D1,E1,F1,G1,H1,I1,
	A2,B2,C2,D2,E2,F2,G2,H2,I2,
	A3,B3,C3,D3,E3,F3,G3,H3,I3,
	A4,B4,C4,D4,E4,F4,G4,H4,I4,
	A5,B5,C5,D5,E5,F5,G5,H5,I5,
	A6,B6,C6,D6,E6,F6,G6,H6,I6,
	A7,B7,C7,D7,E7,F7,G7,H7,I7,
	A8,B8,C8,D8,E8,F8,G8,H8,I8,
	A9,B9,C9,D9,E9,F9,G9,H9,I9],

%%%%         RADEK                  3x3 BLOK		 sloupec	constraints	
% RADEK1
	sel(N,	 A1,R1C1),		sel(N,	 A1,C1C1),	member(A1, [2,3,1,6]),
	sel(R1C1,B1,R1C2),		sel(N,	 B1,C2C1),
	sel(R1C2,C1,R1C3),		sel(N,	 C1,C3C1),
	sel(R1C3,D1,R1C4),		sel(N,	 D1,C4C1),	17 is (C1+D1),
	sel(R1C4,E1,R1C5),		sel(N,	 E1,C5C1),
	sel(R1C5,F1,R1C6),		sel(N,	 F1,C6C1),	12 is (E1+F1),
	sel(R1C6,G1,R1C7),		sel(N,	 G1,C7C1),
	sel(R1C7,H1,R1C8),		sel(N,	 H1,C8C1),	3 is abs(G1-H1),
	sel(R1C8,I1,[]),		sel(N,	 I1,C9C1),

% RADEK-2
	sel(N,	 A2,R2C1),		sel(C1C1,A2,C1C2),	6 is (A1*A2),
	sel(R2C1,B2,R2C2),		sel(C2C1,B2,C2C2),	
	sel(R2C2,C2,R2C3),		sel(C3C1,C2,C3C2),	14 is (B1+B2+C2),
	sel(R2C3,D2,R2C4),		sel(C4C1,D2,C4C2),	
	sel(R2C4,E2,R2C5),		sel(C5C1,E2,C5C2),	
	sel(R2C5,F2,R2C6),		sel(C6C1,F2,C6C2),
	sel(R2C6,G2,R2C7),		sel(C7C1,G2,C7C2),
	sel(R2C7,H2,R2C8),		sel(C8C1,H2,C8C2),	
	sel(R2C8,I2,[]),		sel(C9C1,I2,C9C2),	8 is (I1+I2),


% RADEK-3
	sel(N,	 A3,R3C1),		sel(C1C2,A3,C1C3),	
	sel(R3C1,B3,R3C2),		sel(C2C2,B3,C2C3),	17 is (A3+B3),
	sel(R3C2,C3,R3C3),		sel(C3C2,C3,C3C3),
	sel(R3C3,D3,R3C4),		sel(C4C2,D3,C4C3),	
	sel(R3C4,E3,R3C5),		sel(C5C2,E3,C5C3),	8 is abs(E2-E3),
	sel(R3C5,F3,R3C6),		sel(C6C2,F3,C6C3),	3 is abs(F2-F3),
	sel(R3C6,G3,R3C7),		sel(C7C2,G3,C7C3),	2 is abs(G2-G3),
	sel(R3C7,H3,R3C8),		sel(C8C2,H3,C8C3),	
	sel(R3C8,I3,[]),		sel(C9C2,I3,C9C3),

%	printboard(Board), %debug

% RADEK-4
	sel(N,	 A4,R4C1),		sel(C1C3,A4,C1C4),	
	sel(R4C1,B4,R4C2),		sel(C2C3,B4,C2C4),
	sel(R4C2,C4,R4C3),		sel(C3C3,C4,C3C4),
	sel(R4C3,D4,R4C4),		sel(C4C3,D4,C4C4),	576 is (D2*C3*D3*C4*D4),
	sel(R4C4,E4,R4C5),		sel(C5C3,E4,C5C4),	
	sel(R4C5,F4,R4C6),		sel(C6C3,F4,C6C4),	45 is (E4*F4),
	sel(R4C6,G4,R4C7),		sel(C7C3,G4,C7C4),
	sel(R4C7,H4,R4C8),		sel(C8C3,H4,C8C4),	14 is (H2+H3+H4+G4),
	sel(R4C8,I4,[]),		sel(C9C3,I4,C9C4),	15 is (I3+I4),
                                
% RADEK-5
	
	sel(N,	 A5,R5C1),		sel(C1C4,A5,C1C5),
	sel(R5C1,B5,R5C2),		sel(C2C4,B5,C2C5),
	sel(R5C2,C5,R5C3),		sel(C3C4,C5,C3C5),	
	sel(R5C3,D5,R5C4),		sel(C4C4,D5,C4C5),	
	sel(R5C4,E5,R5C5),		sel(C5C4,E5,C5C5),	3 is abs(D5-E5),
	sel(R5C5,F5,R5C6),		sel(C6C4,F5,C6C5),	
	sel(R5C6,G5,R5C7),		sel(C7C4,G5,C7C5),	
	sel(R5C7,H5,R5C8),		sel(C8C4,H5,C8C5),	14 is (F5+G5+H5),
	sel(R5C8,I5,[]),		sel(C9C4,I5,C9C5),	I5=4,

%	printboard(Board), %debug

% RADEK-6
	sel(N,	 A6,R6C1),		sel(C1C5,A6,C1C6),	22 is (A4+A5+A6),
	sel(R6C1,B6,R6C2),		sel(C2C5,B6,C2C6),	40 is (B4*B5*B6),
	sel(R6C2,C6,R6C3),		sel(C3C5,C6,C3C6),	8 is abs(C5-C6),
	sel(R6C3,D6,R6C4),		sel(C4C5,D6,C4C6),	
	sel(R6C4,E6,R6C5),		sel(C5C5,E6,C5C6),
	sel(R6C5,F6,R6C6),		sel(C6C5,F6,C6C6),	% E6/F6 == 2
	sel(R6C6,G6,R6C7),		sel(C7C5,G6,C7C6),	
	sel(R6C7,H6,R6C8),		sel(C8C5,H6,C8C6),	
	sel(R6C8,I6,[]),		sel(C9C5,I6,C9C6),

% RADEK-7
	sel(N,	 A7,R7C1),		sel(C1C6,A7,C1C7),
	sel(R7C1,B7,R7C2),		sel(C2C6,B7,C2C7),	3 is abs(A7-B7),
	sel(R7C2,C7,R7C3),		sel(C3C6,C7,C3C7),
	sel(R7C3,D7,R7C4),		sel(C4C6,D7,C4C7),
	sel(R7C4,E7,R7C5),		sel(C5C6,E7,C5C7),
	sel(R7C5,F7,R7C6),		sel(C6C6,F7,C6C7),
	sel(R7C6,G7,R7C7),		sel(C7C6,G7,C7C7),
	sel(R7C7,H7,R7C8),		sel(C8C6,H7,C8C7),
	sel(R7C8,I7,[]),		sel(C9C6,I7,C9C7),	7 is (I6+I7),


% RADEK-8

	sel(N,	 A8,R8C1),		sel(C1C7,A8,C1C8),	
	sel(R8C1,B8,R8C2),		sel(C2C7,B8,C2C8),
	sel(R8C2,C8,R8C3),		sel(C3C7,C8,C3C8),	
	sel(R8C3,D8,R8C4),		sel(C4C7,D8,C4C8),	280 is (D6*C7*D7*D8),
	sel(R8C4,E8,R8C5),		sel(C5C7,E8,C5C8),	6 is abs(E7-E8),
	sel(R8C5,F8,R8C6),		sel(C6C7,F8,C6C8),	5 is abs(F7-F8),
	sel(R8C6,G8,R8C7),		sel(C7C7,G8,C7C8),	2 is abs(G7-G8),
	sel(R8C7,H8,R8C8),		sel(C8C7,H8,C8C8),	144 is (G6*H6*H7*H8),
	sel(R8C8,I8,[]),		sel(C9C7,I8,C9C8),	


% RADEK-9
	sel(N,	 A9,R9C1),		sel(C1C8,A9,[]),	6 is (A8+A9),
	sel(R9C1,B9,R9C2),		sel(C2C8,B9,[]),	60 is (B8*C8*B9),
	sel(R9C2,C9,R9C3),		sel(C3C8,C9,[]),	
	sel(R9C3,D9,R9C4),		sel(C4C8,D9,[]),	6 is abs(C9-D9),
	sel(R9C4,E9,R9C5),		sel(C5C8,E9,[]),	
	sel(R9C5,F9,R9C6),		sel(C6C8,F9,[]),	% E9 / F9 = 2
	sel(R9C6,G9,R9C7),		sel(C7C8,G9,[]),	
	sel(R9C7,H9,R9C8),		sel(C8C8,H9,[]),	17 is (G9+H9),
	sel(R9C8,I9,[]),		sel(C9C8,I9,[]),	18 is (I8*I9),


%sloupce
	row(A1,A2,A3,A4,A5,A6,A7,A8,A9),
	row(B1,B2,B3,B4,B5,B6,B7,B8,B9),
	row(C1,C2,C3,C4,C5,C6,C7,C8,C9),
	row(D1,D2,D3,D4,D5,D6,D7,D8,D9),
	row(E1,E2,E3,E4,E5,E6,E7,E8,E9),
	row(F1,F2,F3,F4,F5,F6,F7,F8,F9),
	row(G1,G2,G3,G4,G5,G6,G7,G8,G9),
	row(H1,H2,H3,H4,H5,H6,H7,H8,H9),
	row(I1,I2,I3,I4,I5,I6,I7,I8,I9),


	printboard(Board).
	
