% Room of Levers
% solves puzzle with levers in level 11 in Eye of the Beholder 

switch(0,1).
switch(1,0).

switch(1, [L1,L2,L3,L4,L5,L6,L7,L8], [L1S,L2 ,L3S,L4 ,L5S,L6 ,L7 ,L8 ]) :- switch(L1,L1S),switch(L3,L3S),switch(L5,L5S).
switch(2, [L1,L2,L3,L4,L5,L6,L7,L8], [L1 ,L2S,L3 ,L4S,L5S,L6S,L7 ,L8 ]) :- switch(L2,L2S),switch(L4,L4S),switch(L5,L5S),switch(L6,L6S).
switch(3, [L1,L2,L3,L4,L5,L6,L7,L8], [L1 ,L2S,L3S,L4 ,L5 ,L6S,L7S,L8 ]) :- switch(L2,L2S),switch(L3,L3S),switch(L6,L6S),switch(L7,L7S).
switch(4, [L1,L2,L3,L4,L5,L6,L7,L8], [L1S,L2 ,L3 ,L4S,L5 ,L6 ,L7 ,L8 ]) :- switch(L1,L1S),switch(L4,L4S).
switch(5, [L1,L2,L3,L4,L5,L6,L7,L8], [L1 ,L2 ,L3 ,L4 ,L5S,L6 ,L7 ,L8S]) :- switch(L5,L5S),switch(L8,L8S).
switch(6, [L1,L2,L3,L4,L5,L6,L7,L8], [L1 ,L2 ,L3 ,L4 ,L5 ,L6S,L7 ,L8 ]) :- switch(L6,L6S).
switch(7, [L1,L2,L3,L4,L5,L6,L7,L8], [L1 ,L2 ,L3 ,L4 ,L5 ,L6 ,L7S,L8 ]) :- switch(L7,L7S).
switch(8, [L1,L2,L3,L4,L5,L6,L7,L8], [L1S,L2 ,L3 ,L4 ,L5 ,L6 ,L7S,L8S]) :- switch(L1,L1S),switch(L7,L7S),switch(L8,L8S).


step(9, LIn, LIn, []).

step(I, LIn, LOut, [1|Hist]) :-	I < 9, I1 is I+1, switch(I, LIn, LInS), step(I1, LInS, LOut, Hist).

step(I, LIn, LOut, [0|Hist]) :- I < 9, I1 is I+1, step(I1, LIn, LOut, Hist).


% solve(Starting sequence, Ending sequence) prints which levers should be switched to achieve given result
solve(Start, End) :- step(1, Start, End, Hist),	print([Start, End, Hist]).

% example
solve :- solve([0,0,0,0,0,0,0,0],[0,1,0,0,0,0,1,0]).

