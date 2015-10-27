
%Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.


%Working clockwise, and starting from the group of three with the numerically lowest external node (4,3,2 in this example), each solution can be described uniquely. For example, the above solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.

%It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight solutions in total.
%Total	Solution Set
%9	4,2,3; 5,3,1; 6,1,2
%9	4,3,2; 6,2,1; 5,1,3
%10	2,3,5; 4,5,1; 6,1,3
%10	2,5,3; 6,3,1; 4,1,5
%11	1,4,6; 3,6,2; 5,2,4
%11	1,6,4; 5,4,2; 3,2,6
%12	1,5,6; 2,6,4; 3,4,5
%12	1,6,5; 3,5,4; 2,4,6


%By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon ring is 432621513.

% Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings. 
%What is the maximum 16-digit string for a "magic" 5-gon ring?

%observations:
%- to get 16 digits, 10 must be external node
%- less than 150k combinations
%
%

solve(Res) :-
    numlist(1,10, Nums0),
    
    select(A1, Nums0, Nums1),
    select(A2, Nums1, Nums2),A2<10,
    select(A3, Nums2, Nums3),A3<10,
    SUM is A1+A2+A3,
    select(A4, Nums3, Nums4), A4>A1,
    A6 is SUM-A3-A4, A6<10,
    select(A6, Nums4, Nums5),
    select(A7, Nums5, Nums6), A7>A1,
    A9 is SUM-A6-A7, A9<10,
    select(A9, Nums6, Nums7),
    select(A10, Nums7, Nums8), A10>A1,
    A12 is SUM-A10-A9, A12<10,
    select(A12, Nums8, Nums9),
    A13 is SUM-A2-A12, A13>A1,
    select(A13, Nums9, []),
    
    Res=[[A1,A2,A3],[A4,A3,A6],[A7,A6,A9], [A10,A9,A12],[A13,A12,A2]].

    