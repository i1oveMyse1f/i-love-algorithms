---
layout: lecture
title:  "Классы в C++"
author: i_love_myself
categories: [ cpp ]
toc: true
---

# Классы в языке C++

Вы уже умеете пользоваться стандартными классами, такими как ```string```, ```vector``` и другие. Пора научиться писать нечто похожее на примере класса для работы с арифметикой остатков. Но для начала немного синтаксиса:

```cpp
class SimpleClass {
    // привет, я пример самого простого класса
};
```

## Публичные и приватные переменные


В классах можно хранить любые переменные, например:

```cpp
class Point {
    int x;
    int y;
}
```

Но если вы попробуете обратиться к полям x и y, то у вас ничего не выйдет:

```cpp
int main() {
    Point p = { 1, 2 };
    cout << p.x << ' ' << p.y; // Compile Error
}
```

Всё дело в том, что по умолчанию любая переменная (а далее, и любой метод) являются ___приватными___. То есть пользователь класса не имеет к ним доступ, а разработчик класса - имеет. Это сделано для того, чтобы пользователи класса не стреляли себе в ногу при использовании чужого класса и не лезли в "скрытые" поля. Вы можете написать слово ```public```, чтобы переменная была ___публичной___, иначе говоря, вы имели к ней доступ из программы. Ниже вы можете увидеть, как работают ключевые слова ```public``` и ```private``` в C++:

```cpp
class PublicPrivateClass {
    int this_is_a_private_variable;
    double this_is_private_variable_too;
public:
    int this_is_a_first_public_variable_in_this_class;
    int this_is_a_second_public_variable_in_this_class;
private:
    int this_is_a_private_variable_again;
};
```

Кроме того, в C++ есть ещё и структуры (`struct`), которые почти ничем не отличаются за исключением того, что объекты в нем по умолчанию являются ```public```:

```cpp
struct PublicPrivateClass {
    int this_is_a_public_variable;
    double this_is_public_variable_too;
private:
    int this_is_a_private_variable;
public:
    int this_is_a_public_variable_again;
};
```

## Методы класса

У классов (и структур) можно создавать методы, например:

```cpp
struct SimpleMethod {
    int x, y;

    double size() {
        return sqrt(x * x + y * y);
    }
}

int main() {
    SimpleMethod t = { 1, 1 };
    cout << t.size();
}
```

О более продвинутых возможностях класса мы поговорим на примере арифметики остатков.

## Арифметика остатков

Часто в задачах по олимпиадному программировнию требуется посчитать ответ по модулю некоторого простого числа. Например, если вам нужно посчитать число Фибоначчи по модулю `1000000007`, то вам нужно считать ответ по модулю `1000000007` после каждой операции. Для этого идеально подходит класс для работы с арифметикой остатков.

Как сделать удобный класс для работы с арифметикой остатков? Он должен:

* Удобно создаваться
* Уметь складывать, вычитать, умножать и делить остатки
* Уметь выводиться в поток вывода
* Быть очень быстрым

То есть, в идеале мы должны уметь в следующий набор операций:

```cpp
static const int MOD = 11;

Mint a = 5;
Mint b = 7;

Mint c = a + b; // 5 + 7 = 1
Mint d = a * b; // 5 * 7 = 8
Mint e = a / b; // 5 / 7 = 8

c += 2; // 1 + 2 = 3

cout << c; // 3

Mint f = a + 7; // 5 + 7 = 1
Mint g = 7 + a; // 7 + 5 = 1
```

Мы будем писать наиболее эффективный код, поэтому будем по минимуму использовать операции взятия по модулю. Например, если мы складываем два числа и берем остаток, то взятие остатка можно заменить на одно вычитание в предположении, что числа меньше чем остаток!


### Конструктор

Для начала нам нужно создать конструктор, который будет принимать число и модуль:

```cpp
class Mint {
public:
    Modulo(int value_, int mod_) {
        value = value_; // внутри класса можно обращаться к приватным переменным
        mod = mod_;
        assert(value >= 0 && value < mod); // убедимся, что числа изначально лежат в нужном диапазоне
    }

private:
    int value;
    int mod;
};

int main() {
    const int MOD = 11;
    Mint a(5, MOD);
    Mint b(7, MOD);
}
```

Начиная с C++11 появились списки инициализации. Они упрощают написание конструкторов, а так же делают их более эффективными с точки зрения производительности, а именно избавляют от лишних копирований: внутри конструктора переменные инициализилизруются сразу, а не сначала создаются, а потом присваиваются. Синтаксис следующий:

```cpp
class Mint {
public:
    Modulo(int value, int mod) : value(value), mod(mod) {
        assert(value >= 0 && value < mod);
    } // С++ сам поймет, где value - это поле класса, а где - аргумент функции

private:
    int value;
    const int mod;
}
```

Несколько замечаний:
* У списка инициализации есть небольшое ограничение: инициализировать можно только в порядке объявления переменных в классе (но некоторые поля можно просто пропустить)
* Обратите внимание, что в этот раз mod - константа! В прошлый раз мы не могли бы перезаписать константу в теле конструктора, а в списке инициализации можем. Ещё раз задумайтесь, почему!

Конструткоров может быть сколько угодно, они могут различаться по количеству аргументов и их типам. Например, вот так можно создать конструктор по умолчанию:

```cpp
class Mint {
public:
    Modulo() : value(0), mod(1) {
    }

    Modulo(int mod) : value(0), mod(mod) {
        assert(value >= 0 && value < mod);
    }

    Modulo(int value, int mod) : value(value), mod(mod) {
        assert(value >= 0 && value < mod);
    }

private:
    int value;
    const int mod;
}

Mint a; // value = 0, mod = 1
Mint b(11); // value = 0, mod = 11
Mint c(5, 11); // value = 5, mod = 11
```

Однако неудобно каждый раз передавать модуль в качестве аргумента. Есть несколько способов сделать это удобнее, например, воспользоваться аргументами по умолчанию:

```cpp
static const int MOD = 11;

class Mint {
public:
    Modulo(int value = 0, int mod = MOD) : value(value), mod(MOD) {
        assert(value >= 0 && value < mod);
    }

private:
    int value;
    const int mod;
}

Mint a; // value = 0, mod = 11
Mint b(5); // value = 0, mod = 5
Mint c(5, 13); // value = 5, mod = 13
```

Важно знать, что аргументы по умолчанию должны быть справа от всех остальных аргументов (то есть суффиксом аргументов).

Другой способ - это использовать шаблоны. Этот способ мне нравится больше, поэтому мы будем использовать его.

### Шаблонный класс

Шаблонные классы позволяют создавать классы, которые могут принимать в качестве аргументов другие классы. Например, вектор - это шаблонный класс динамического массива, который принимает в качестве аргумента тип элемента массива: `vector<int>` или `vector<string>`. Синтаксис шаблонного класса следующий:

```cpp
template<class T>
class Vector {
    T* data; // указатель на массив элементов
    int size; // размер массива
};

int main() {
    Vector<int> a;
    Vector<string> b;
}
```

Как работают шаблонные классы? Всё магия произойдет ещё на этапе компиляции. Компилятор создает новый класс для каждого типа, который вы передаете в качестве аргумента. Например, если вы создаете `Vector<int>`, то компилятор создает класс `VectorInt`, если вы создаете `Vector<string>`, то компилятор создает класс `VectorString`.

На самом деле шаблоны позволяют принимать не только типы, но и значения. Например, это используется в `array` из стандартной библиотеки:

```cpp
array<int, 10> a;
array<int, 100> b;
```


Давайте создадим шаблонный класс, который будет принимать модуль в качестве шаблонного параметра:

```cpp
template<int mod>
class Modulo {
    int value;

public:
    Modulo(int value) : value(value) {
        assert(value >= 0 && value < mod);
    }
};

using Mint = Modulo<1000000007>;

int main() {
    Mint a = 5;
    Mint b = 7;
}
```

### Операторы

Чтобы зарабаотала арифметика остатков, в C++ нужно перегрузить операторы. Например, чтобы заработал оператор сложения, нужно перегрузить `operator+`:

```cpp
template<int mod>
class Modulo {
    int value;

public:
    Modulo operator+(const Modulo& other) const {
        int result = value + other.value;
        if (result > mod) {
            result -= mod;
        }
        return result;
    }
};

using Mint = Modulo<1000000007>;

int main() {
    Mint a = 5;
    Mint b = 7;
    Mint c = a + b;
}
```

Когда мы пишем `a+b`, то вызывается `operator+` для `a` с аргументом `b`. Операторы можно перегружать для любых типов, но есть некоторые ограничения. Например, операторы `.` и `::` нельзя перегружать, а так же нельзя создавать новые операторы.

Операторы можно перегружать как внутри класса, так и снаружи. Например, если вы хотите, чтобы оператор `+` работал для `int` и `Modulo`, то вы можете создать новый класс, который будет принимать `int` и перегрузить оператор `+`:

```cpp
template<int mod>
class Modulo {
    int value;

public:
    Modulo operator+(const Modulo& other) const {
        int result = value + other.value;
        if (result > mod) {
            result -= mod;
        }
        return result;
    }
};

template<int mod>
Modulo<mod> operator+(int a, const Modulo<mod>& b) {
    return Modulo<mod>(a) + b;  
}

using Mint = Modulo<1000000007>;

int main() {
    Mint a = 5;
    Mint b = 7;
    Mint c = a + b;
    Mint d = 5 + b;
}
```

Обратите внимание, что без такой перегрузки мы бы не могли сложить `int` (слева) и `Modulo` (справа), так как компилятор не знает, как это делать. А вот в обратном порядке смогли бы, потому что у нас есть:

1. Конструктор `Modulo(int)` 
2. Сложение `Modulo + Modulo`
   
То есть копмпилятор бы догадался, что надо создать `Modulo` из `int` и сложить два `Modulo`.

Операция добавления имеет чуть-чуть другой синтаксис, однако может быть написана еще более просто:

```cpp
template<int mod>
class Modulo {
    int value;

public:
    Modulo& operator+=(const Modulo& other) const {
        return *this = *this + other;
    }
};
```

`this` - это указатель на само значение переменной, над которой вызывается оператор. Так мы можем переиспользовать уже готовый `operator+`, чтобы не дублировать код.

### Операторы ввода-вывода

Чтобы заработал вывод в поток, нужно перегрузить оператор `<<`:

```cpp
ostream& operator<<(ostream& out, const Modulo& a) {
    return out << a.value;
}
```

Прежде чем читать дальше, рекомендую подумать самостоятельно, что значит данная запись и зачем возвращать поток вывода.

`ostream` - это общий базовый класс для любого потока вывода. Оператор вывода обязан возвращать измененный поток, чтобы можно было писать цепочки ввода:

```cpp
cout << x << ' ' << y;
```

Однако это не сработает, так как `a.value` - это приватный член класса. Чтобы это заработало, нужно сделать `operator<<` другом класса. Функции-друзья имеют доступ к приватным полям:

```cpp
template<int mod>
class Modulo {
    int value;

public:
    friend ostream& operator<<(ostream& out, const Modulo& a);
}
```

Оператор ввода аналогичен, только работает с переменной типа `istream` - входного потока, а переменная типа Module передается по неконстантной ссылке (ведь в операторе ввода мы считаем данную переменную и изменим её).

## Соединяем всё вместе

Выше я везде передавал объекты типа Module по константной ссылке. На самом деле я делал это по привычке. Однако напомню, что если объект класса меньше ~16 байт, то эффективнее передавать его по значению (с копированием). Поэтому в финальной версии мы будем передавать объекты по значению.

```cpp
template<int mod>
class Modulo {
public:
    Modulo(int value = 0) : value(value) {
        if (value < 0) {
            value += mod;
        }
    }

    Modulo operator+(Modulo other) const {
        int result = value + other.value;
        if (result >= mod) {
            result -= mod;
        }
        return result;
    }

    Modulo operator-(Modulo other) const {
        int result = value - other.value;
        if (result < 0) {
            result += mod;
        }
        return result;
    }

    Modulo operator*(Modulo other) const {
        return (int64_t(value) * other.value) % mod;
    }

    Modulo operator/(Modulo other) const {
        return *this * other.inv();
    }

    Modulo& operator+=(Modulo other) {
        return *this = *this + other;
    }

    Modulo& operator-=(Modulo other) {
        return *this = *this - other;
    }

    Modulo& operator*=(Modulo other) {
        return *this = *this * other;
    }

    Modulo& operator/=(Modulo other) {
        return *this = *this / other;
    }

    Modulo inv() const {
        return binpow(*this, mod - 2);
    }

    bool operator==(Modulo other) const {
        return value == other.value;
    }

    friend ostream& operator<<(ostream& out, const Modulo& a) {
        return out << a.value;
    }

    friend istream& operator>>(istream& in, Modulo& a) {
        return in >> a.value;
    }

    friend Modulo operator+(int a, Modulo b) {
        return Modulo(a) + b;
    }

    friend Modulo operator-(int a, Modulo b) {
        return Modulo(a) - b;
    }

    friend Modulo operator*(int a, Modulo b) {
        return Modulo(a) * b;
    }

    friend Modulo operator/(int a, Modulo b) {
        return Modulo(a) / b;
    }

private:
    int value;

    static Modulo binpow(Modulo a, int n) {
        Modulo result = 1;
        while (n) {
            if (n & 1) {
                result *= a;
            }
            a *= a;
            n >>= 1;
        }
        return result;
    }
};
```

