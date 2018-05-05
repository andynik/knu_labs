% Variants 3 & 4 for Prolog test #2
% use SWI-Prolog (https://swish.swi-prolog.org) for compiling


%%% var #3
% mergesort
% reverse (list with lists)
% lcm

%%% var #4
% quicksort
% multizipper
% polynom outcome in point


%%% mergesort

list_head(_, 0, []).
list_head([H|T], N, [H|Sub]) :-
	N1 is N-1,
	list_head(T, N1, Sub).

list_tail(T, 0, T).
list_tail([_|T], N, R) :-
	N1 is N-1,
	list_tail(T, N1, R).

merge(A, [], A).
merge([], B, B).
merge([Ha|Ta], [Hb|Tb], [Ha|Sub]) :-
	Ha < Hb,
	merge(Ta, [Hb|Tb], Sub).

merge([Ha|Ta], [Hb|Tb], [Hb|Sub]) :-
	Ha >= Hb,
	merge([Ha|Ta], Tb, Sub).

mergesort([H], [H]).
mergesort(List, Sorted) :-
			length(List, Number),
			Half is Number // 2,
			list_head(List, Half, H),
			list_tail(List, Half, T),
			mergesort(H, A),
			mergesort(T, B),
			merge(A, B, Sorted).

?- mergesort([1, 5, 100, 8, 7], S)
% S = [1, 5, 7, 8, 100]


%%% reverse a list with lists

rev([], []) :- !.

rev([H|T], X) :-
    !,
    rev(H, NewH),
    rev(T, NewT),
    append(NewT, [NewH], X).

rev(X, X).

?- rev([1, [2, 4], 3, 5], X)
% X = [5, 3, [4, 2], 1]

			
%%% lcm
			
lcm(X, Y, Z) :-
	Z is abs(X * Y) / gcd(X,Y).

?- lcm(4, 5, R)
% R = 20


%%% quicksort

pivot(_, [], [], []).
pivot(Pivot, [Head|Tail], [Head|LessOrEqualThan], GreaterThan) :- Pivot >= Head, pivot(Pivot, Tail, LessOrEqualThan, GreaterThan). 
pivot(Pivot, [Head|Tail], LessOrEqualThan, [Head|GreaterThan]) :- pivot(Pivot, Tail, LessOrEqualThan, GreaterThan).

quicksort([], []).
quicksort([Head|Tail], Sorted) :- pivot(Head, Tail, List1, List2), quicksort(List1, SortedList1), quicksort(List2, SortedList2), append(SortedList1, [Head|SortedList2], Sorted).

?- quicksort([2, 1, 5, 6, 0], S)
% S = [0, 1, 2, 5, 6]


%%% zipper for three lists (counting for 0.5 out of 1 points in the task)

X = [5, 3, [4, 2], 1]

zip([], [], [], []).
zip([X|Xs], [Y|Ys], [Z|Zs], [X,Y,Z|Ws]) :- zip(Xs,Ys,Zs,Ws).

?- zip([a, b, c], [1, 2, 3], [3, 4, 5], X)
% X = [a, 1, 3, b, 2, 4, c, 3, 5]


%%% poly (via Gorner)

poly([], _X, 0):-!.
poly([An], _X, An):-!.
poly([A|TailMultipliers], X, B):-
  poly(TailMultipliers, X, NextB),
  B is A + NextB*X.

% a1 + a2 * x + a3 * x^2
% 1 + 2 * x + 3 * x^2, x=2
?- poly([1, 2, 3], 2, R)
% R = 17
