---
layout: lecture
title:  "Квадратичные сортировки"
author: i_love_myself
categories: [ sorting ]
toc: true
---

Сортировки в этом раздле нужны исключительно для ознакомления и понимания того, как работают сортировки. На практике их использовать не стоит, так как они работают за квадратичное время.

## Сортировка вставкой

Сортировка вставкой (англ. _insertion sort_) - это одна из самых простых сортировок, которые можно придумать. Разберём сортировку на примере: пусть дан массив [2, 1, 10, 5]. Отсортируем его за 4 шага, для этого на каждом шаге $k$ будем поддерживать инвариант, что массив из $k$ элементов является отсортированным.

* [2] - отсортированный массив
* к массиву [2] добавляется 1, после сортировки становится [1, 2]
* к массиву [1, 2] добавляется 10, после сортировки становится [1, 2, 10]
* к массиву [1, 2, 10] добавляется 5. После сортировки становится [1, 2, 5, 10]

Теперь должно стать понятно, почему сортировка называется "сортировка вставкой". На каждой итерации, чтобы отсортировать массив, нам необходимо лишь вставить его в нужное место. Например, на последней итерации мы вставили 5 между 2 и 10, чтобы массив вновь стал отсортированным.

![Insertion sort](./img/insertion_sort.gif)

Реализуем эту сортировку на C++. Мы не будем явно вставлять элемент, а будем просто сдвигать его влево, пока не найдём нужное место:

```cpp
void sort(vector<int>& a) {
    for (int i = 1; i < a.size(); ++i) { // цикл по всем префиксам массива
        for (int j = i; j > 0 && a[j] < a[j - 1]; --j) { // двигаем элемент влево, пока не найдем нужное место
            swap(a[j], a[j - 1]);
        }
    }
    return a;
}
```

## Пузырьковая сортировка

В пузырьковой сортировке (англ. _Bubble sort_) мы опять будем сортировать массив "потихоньку". На каждой итерации мы вновь будем требовать, чтобы была отсортирована некоторая часть нашего массива, а именно - суффикс. Алгоритм будет состоять из $n - 1$ итераций, на каждой из которых мы будем проталкивать максимум из неотсортированного префикса в конец. Однако мы заранее не знаем, где находится максимум, поэтому если будем видеть два соседних элемента, где $a_{i} > a_{i+1}$, то будем их менять местами.

![Bubble sort](./img/bubble_sort.gif)

Таким образом мы, во-первых, рано или поздно мы доведем максимум на префиксе до конца неотсортированной части, а во-вторых, частично уменьшим "неотсортированность" на префиксе, поскольку двигали не только максимум, обратите на это внимание еще раз на визуализации.

```cpp
void sort(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n - 1; ++i) { // n - 1 итерация
        for (int j = 0; j < n - 1 - i; ++j) { // суффикс [n-1-i; i) уже отсортирован
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
            }
        }
    }
}
```

Конечно, данный код можно оптимизировать - если на какой-то итерации не было ни одной перестановки, то массив уже отсортирован и можно выйти из цикла. Таким образом мы можем улучшить время работы алгоритма в лучшем случае до $O(n)$. Однако в худшем (и среднем) случае алгоритм всё ещё будет работать за $O(n^2)$.

Крайне рекомендую посмотреть как работает пузырьковая сортировка на примере танца: [Bubble-sort with Hungarian](https://youtu.be/lyZQPjUT5B48).
