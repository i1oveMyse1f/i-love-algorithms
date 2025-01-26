---
layout: lecture
title:  "STL. Работа со справкой"
author: i_love_myself
categories: [ cpp ]
toc: true
---

В этом разделе я сделаю небольшой обзор на полезные функции для олимпиад из STL (Standard Template Library) - стандартную библиотеку шаблонов C++, включающую контейнеры и алгоритмы, а так же научу вас читать справку на [cppreference](https://en.cppreference.com/).

Я сделаю сразу несколько оговорок:

1. Я не буду описывать все функции, а только те, которые мне кажутся наиболее полезными. Я рекомендую после лекции самостоятельно изучить все функции, чтобы знать, что они делают, а так же научиться работать со справкой
2. Все описываемые функции находятся в библиотеках [algorithm](https://en.cppreference.com/w/cpp/algorithm) и [numeric](https://en.cppreference.com/w/cpp/numeric)

## Чтение справки

Разберем подробно несколько функций из библиотеки [algorithm](https://en.cppreference.com/w/cpp/algorithm).

### [std::lower_bound](https://en.cppreference.com/w/cpp/algorithm/lower_bound)

Справка делится на несколько частей:

#### Заголовок со список перегрузок

Вариант 1:

```cpp
template<class ForwardIt, class T>
ForwardIt lower_bound(ForwardIt first, ForwardIt last, const T& value );
```

Вариант 2:

```cpp
template< class ForwardIt, class T, class Compare >
ForwardIt lower_bound( ForwardIt first, ForwardIt last, const T& value, Compare comp );
```

Цифры отмечены справа от определения. Кроме того, вы можете заметить, что определения функций могут рахличаться между стандартами, однако на олимпиадной практике вам это не понадобится - можете читать самый первый вариант.

#### Что делает функция

Затем идет небольшой абзац о том, что делает функция. Например, для `std::lower_bound`:

> Searches for the first element in the partitioned range [first, last) which is not ordered before value.

То есть функция находит первый элемент в отсортированном диапазоне, который не меньше `value`.

#### Описание перегрузок

1. The order is determined by `operator<`: Returns the first iterator iter in [first, last) where bool(*iter < value) is false, or last if no such iter exists. If the elements elem of [first, last) are not partitioned with respect to the expression bool(elem < value), the behavior is undefined.
2. The order is determined by comp: Returns the first iterator iter in [first, last) where `bool(comp(*iter, value))` is false, or last if no such iter exists.

То есть две перегрузки отличаются только тем, как определяется порядок элементов. Во втором варианте вы можете передать свою функцию сравнения.

#### Описание параметров

* first, last - the partitioned range of elements to examine
* value - value to compare the elements to
* comp - binary predicate which returns ​true if the first argument is ordered before the second.
The signature of the predicate function should be equivalent to the following:

```cpp
 bool pred(const Type1 &a, const Type2 &b);
```

While the signature does not need to have const &, the function must not modify the objects passed to it and must be able to accept all values of type (possibly const) Type1 and Type2 regardless of value category (thus, Type1 & is not allowed, nor is Type1 unless for Type1 a move is equivalent to a copy(since C++11)).
The type Type1 must be such that an object of type ForwardIt can be dereferenced and then implicitly converted to Type1. The type Type2 must be such that an object of type T can be implicitly converted to Type2.​

Type requirements:

* ForwardIt must meet the requirements of LegacyForwardIterator.
* Compare must meet the requirements of BinaryPredicate. It is not required to satisfy Compare

Обычное по названию функции, названию и типу аргументов уже можно понять что делает функция. Однако, если вы не уверены, то можете прочитать описание параметров.

### Возвращаемое значение

> Iterator to the first element of the range [first, last) not ordered before value, or last if no such element is found.

То есть функция возвращает итератор на первый элемент, который не меньше `value`.

### Временная сложность

Там написано что-то вроде: если итератор имеет RandomAccess, то сложность $O(\log(n))$, иначе $O(n)$.
