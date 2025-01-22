---
layout: lecture
title:  "Вспомогательные типы данных: pair, tuple, struct"
author: i_love_myself
categories: [ cpp ]
toc: true
---

Регулярно бывает такое, что вы хотите вернуть из функции несколько переменных, а не одну. Разберем эту проблему на примере функции `divmod`, которая возвращает результат деления и остаток от деления двух чисел:

```cpp
<output_type> divmod(int a, int b) {
    return { a / b, a % b };
}
```

Разберем, каким же может быть `<output_type>`: мы рассмотрим каждый из трех возможных вариантов, разобрав их преимущества и недостатки каждого из них.

### Struct

Первый вариант - создать новую структуру, которая будет содержать все необходимые переменные.

```cpp
struct Divmod {
    int div;
    int mod;
};

Divmod divmod(int a, int b) {
    return {a / b, a % b};
}

int main() {
    Divmod result = divmod(10, 3);
    cout << result.div << " " << result.mod << "\n";
}
```

Данный подход универсален, однако создавать каждый раз новую структуру может быть неудобно, зато очень понятно с точки зрения использования результатов. В промышленном программировании обычно используют именно этот вариант из-за самой лучшей читабельности.

### [Pair](https://en.cppreference.com/w/cpp/utility/pair)

Второй вариант - использовать `pair`.

```cpp
pair<int, int> divmod(int a, int b) {
    return {a / b, a % b};
}

int main() {
    pair<int, int> result = divmod(10, 3);
    cout << result.first << " " << result.second << "\n";
}
```

`pair` - это структура, которая хранит два элемента разных типов. В данном случае это два целых числа. Важным приемуществом `pair` над `struct` является то, что он уже встроен в стандартную библиотеку C++ и у него определен `operator<` - это позволяет сравнивать любые две пары в лексикографическом порядке, а так же позволяет отсортировать массив из пар без дополнительного кода, в отличии от `struct`.

### [Tuple](https://en.cppreference.com/w/cpp/utility/tuple)

Что если вам нужно вернуть больше двух переменных из функции? Тогда вы можете либо воспользьзоваться каким-то из уже известными вам вриантов: `struct` или вложенными `pair`, например:

```cpp
pair<int, pair<int, int>> divmodsum(int a, int b) {
    return {a / b, {a % b, a + b}};
}

int main() {
    pair<int, pair<int, int>> result = divmodsum(10, 3);
    cout << result.first << " " << result.second.first << " " << result.second.second << "\n";
}
```

Но вопрос удобства использования вложенных пар смешён. Поэтому в С++ есть расширение пары - `tuple`, в котором вы можете хранить сколько угодно переменных любого типа:

```cpp
tuple<int, int, int> divmodsum(int a, int b) {
    return {a / b, a % b, a + b};
}

int main() {
    tuple<int, int, int> result = divmodsum(10, 3);
    cout << get<0>(result) << " " << get<1>(result) << " " << get<2>(result) << "\n";
}
```

У `tuple`, так же как и у `pair` определен `operator<`, что позволяет сравнивать два `tuple` в лексикографическом порядке.

### [Structured bindings](https://en.cppreference.com/w/cpp/language/structured_binding)

К сожалению, обращение к элементам `tuple` происходит по индексу через метод `get`, что не всегда удобно. Однко начиная с C++17 можно использовать __structured bindings__:

```cpp
auto [div, mod, sum] = divmodsum(10, 3);
cout << div << " " << mod << " " << sum << "\n";
```

Structured bindings будут работать с любым из перечисленных типов данных в данном разделе: `pair`, `tuple`, `struct`. Рекомендую использовать их, так как они делают код более читаемым и понятным.
