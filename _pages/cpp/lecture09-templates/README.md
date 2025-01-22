---
layout: lecture
title:  "Шаблоны"
author: i_love_myself
categories: [ cpp ]
toc: true
---

## Проблема

В прошлом разделе мы познакомились с итераторами, которые позволяли писать одинаковый код для любого контейнера, в частости мы написали универсальный вывод контейнера и универсальный бинарный поиск (`lower_bound`).

```cpp
for (auto it = s.begin(); it != s.end(); ++it) {
    cout << *it << " ";
}
```

Однако если бы мы попытались обернуть такой код в функцию, то мы столкнулись бы с проблемой: какой тип данных использовать при объявлении функции? Как раз для таких ситуаций и существуют шаблоны - функции, которые принимают "любые" типы данных.

## Объявление шаблона

Шаблон объявляется с помощью ключевого слова `template` и списком параметров шаблона в угловых скобках. Например, вывод элементов вектора:

```cpp
template <typename T>
void print_vector(const vector<T>& v) {
    for (const T& x : v) {
        cout << x << ' ';
    }
    cout << '\n';
}
```

В данном случае `T` - это параметр шаблона, который мы можем использовать внутри функции.

## Как же работает шаблон?

Когда компилятор видит вызов функции с шаблоном, он генерирует код для каждого типа, который был использован в вызове. Например, если мы вызовем `print_vector` для `vector<int>` и `vector<string>`, то компилятор сгенерирует две функции:

```cpp
void print_vector(const vector<int>& v) {
    for (const int& x : v) {
        cout << x << ' ';
    }
    cout << '\n';
}

void print_vector(const vector<string>& v) {
    for (const string& x : v) {
        cout << x << ' ';
    }
    cout << '\n';
}
```

То есть шаблон - это шаблон для генерации кода, а не сам код, который уже будет получен на этапе компиляции.

## Две другие вариции вывода контейнера

На самом деле, как вы могли заметить, наш вывод контейнера потерял некоторую универсальность, так как мы не можем вывести `set` или `map` без дополнительного кода. Давайте попробуем это исправить.

### Вариант 1

```cpp
template <typename T>
void print_container(const T& c) {
    for (const auto& x : c) {
        cout << x << ' ';
    }
    cout << '\n';
}

set<int> s = {1, 2, 3};
print_container(s);
```

### Вариант 2

```cpp
template <typename ForwardIt>
void print_container(ForwardIt first, ForwardIt last) {
    for (ForwardIt it = first; it != last; ++it) {
        cout << *it << ' ';
    }
    cout << '\n';
}

set<int> s = {1, 2, 3};
print_container(v.begin(), v.end());
```

## Почему в С++ тяжело читать ошибки компиляции?

Итак, допустим вы совершили ошибку и в функцию `print_container` передали вовсе не контейнер, а обычный `int`. Тогда статическая проверка типов не подчеркнет ошибку, однако компилятор выдаст ошибку при попытке сгенерировать код для такого вызова из-за того, что у `int` нет метода `begin()`.

Самая большая проблема будет в том, что ошибка компиляции будет выглядеть очень страшно и трудночитаемо из-за шаблонного кода, который будет сгенерирован компилятором.

```txt
c.cpp: In instantiation of ‘void print_container(const T&) [with T = int]’:
c.cpp:25:20:   required from here
c.cpp:8:5: error: ‘begin’ was not declared in this scope
    8 |     for (const auto& x : c) {
      |     ^~~
c.cpp:8:5: note: suggested alternatives:
In file included from /usr/local/twix-gcc-13/include/c++/13.2.0/string:53,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/bits/locale_classes.h:40,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/bits/ios_base.h:41,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/ios:44,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/ostream:40,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/iostream:41,
                 from c.cpp:1:
/usr/local/twix-gcc-13/include/c++/13.2.0/bits/range_access.h:114:37: note:   ‘std::begin’
  114 |   template<typename _Tp> const _Tp* begin(const valarray<_Tp>&) noexcept;
      |                                     ^~~~~
In file included from /usr/local/twix-gcc-13/include/c++/13.2.0/string_view:48,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/bits/basic_string.h:47,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/string:54:
/usr/local/twix-gcc-13/include/c++/13.2.0/bits/ranges_base.h:489:44: note:   ‘std::ranges::__cust::begin’
  489 |     inline constexpr __cust_access::_Begin begin{};
      |                                            ^~~~~
In file included from /usr/local/twix-gcc-13/include/c++/13.2.0/bits/stl_iterator_base_types.h:71,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/bits/stl_construct.h:61,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/bits/char_traits.h:57,
                 from /usr/local/twix-gcc-13/include/c++/13.2.0/ios:42:
/usr/local/twix-gcc-13/include/c++/13.2.0/bits/iterator_concepts.h:984:10: note:   ‘std::ranges::__cust_access::begin’
  984 |     void begin(const auto&) = delete;
      |          ^~~~~
c.cpp:8:5: error: ‘end’ was not declared in this scope
    8 |     for (const auto& x : c) {
      |     ^~~
c.cpp:8:5: note: suggested alternatives:
/usr/local/twix-gcc-13/include/c++/13.2.0/bits/range_access.h:116:37: note:   ‘std::end’
  116 |   template<typename _Tp> const _Tp* end(const valarray<_Tp>&) noexcept;
      |                                     ^~~
/usr/local/twix-gcc-13/include/c++/13.2.0/bits/ranges_base.h:490:42: note:   ‘std::ranges::__cust::end’
  490 |     inline constexpr __cust_access::_End end{};
      |                                          ^~~
/usr/local/twix-gcc-13/include/c++/13.2.0/bits/ranges_base.h:137:10: note:   ‘std::ranges::__cust_access::end’
  137 |     void end(const auto&) = delete;
```

Такие ошибки будут встречаться вам часто, потому что весь стандартный код C++ написан с использованием шаблонов и при неаккуратном их использовании вы будете сталкиваться с подобными ошибками. Более того, реальные проекты будут содержать еще больше шаблонного кода, поэтому ошибки компиляции будут еще длиннее.

Еще раз, обратите внимание, что проверка корректности кода возможна только на этапе компиляции - ваша IDE будет бессильна. Данная проблема показывает, что шаблоны очень ограничены по функционалу и не могут требовать каких-либо методов у типов, которые передаются в шаблон. Однако в C++20 появилась возможность использовать `concept`'ы, которые позволяют делать более сложные статические проверки, которые защищают от подобного рода ошибок. Мы не будем их рассматривать в этом курсе, но вы можете почитать про них самостоятельно.

## Удобный ввод-вывод вектора в стандартный поток

В олимипадном программировании редко нужно выводить `set` или `map`, а лишних ошибок компиляции я бы хотел избежать, поэтому обычно я пишу вывод только для вектора.

```cpp
template <typename T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    for (const T& x : v) {
        os << x << ' ';
    }
    os << '\n';
    return os;
}
```

* `ostream&` - это ссылка на поток вывода (например, `cout` имеет такой тип)
* `operator<<` - это оператор вывода, который вы используете при выводе в стандартный поток
* Функция возвращает `ostream&`, чтобы можно было выводить несколько векторов через `<<` в одной строке:

```cpp
vector<int> v = {1, 2, 3};
cout << v << v;
// эквивалентно
(cout << v) << v;
```

Аналогичный код для ввода вектора с использованием входного потока:

```cpp
template <typename T>
istream& operator>>(istream& is, vector<T>& v) {
    for (T& x : v) {
        is >> x;
    }
    return is;
}

int main() {
    int n;
    cin >> n;
    vector<int> v(n);
    cin >> v;
}
```

Обратите внимание, что наши функции ввода-вывода будут работать и с многомерными векторами (подумайте, почему).

## Упражнения

> Напишите шаблонную функцию `max_element`, которая принимает итераторы на начало и конец контейнера и возвращает итератор на максимальный элемент в контейнере.

Решение: раздел possible implenetation [std::max_element](https://en.cppreference.com/w/cpp/algorithm/max_element)

> Напишите шаблонную функцию `accumulate`, которая принимает итераторы на начало, конец контейнера и начальное значение и возвращает сумму элементов в контейнере.

Решение: раздел possible implenetation [std::accumulate](https://en.cppreference.com/w/cpp/algorithm/accumulate)
