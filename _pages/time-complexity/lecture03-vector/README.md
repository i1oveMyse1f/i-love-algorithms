---
layout: lecture
title:  "Метод потенциалов: динамический массив"
author: i_love_myself
categories: [ cpp ]
toc: true
---

Мы с вами уже много раз говорили о С-массивах и о динамических массивах в С++, которые эффективно поддерживают операции добавления и удаления элементов из конца (то есть работают за константу). В этом разделе мы рассмотрим алгоритм работы динамического массива и проанализируем время его работы с помощью метода потенциалов.

Поскольку мы будем самостоятельно реализовывать динамический массив, мы будем работать с сырой памятью, используя методы `new[n]` и `delete[]`. Напомню, что выделение памяти прозвольного размера в RAM-модели занимает $O(1)$ времени.

## Метод в лоб

Итак, предположим что у нас есть массив, которых хранит в себе $n$ элементов и приходит запрос на добавление элемента. Тогда:

1. Выделяем новый массив размера $n + 1$ - $O(1)$
2. Копируем все элементы из старого массива в новый - $O(n)$
3. Добавляем новый элемент в конец нового массива - $O(1)$
4. Удаляем старый массив - $O(1)$

Таким образом, время добавления нового элемента в массив равно $O(n)$. Безусловно это неудовлетворительно, поскольку мы хотим, чтобы операция добавления элемента в массив работала за константу.

Прежде чем перейти к улучшению алгоритма я рекомендую вам подумать самостоятельно о том, как можно улучшить алгоритм так, чтобы добавление элемента в массив работало за константу.

<details>
<summary>Подсказка</summary>
Время работы добавления элемента будет не константа, а константа в среднем.
</details>

## Одно простое улучшение

Вместо того, чтобы выделять новый массив размера $n + 1$ и копировать в него все элементы, мы можем выделить массив размера $2n$ и добавлять элементы в него. Интуитивно, после этого нам не придется делать копирования следующие $n$ увеличений массива. Однако давайте подробно проанализируем время работы алгоритма с помощью метода "монеток" и докажем формально время $O(1)$ на добавление в среднем.

## Метод монеток (потенциалов)

Этот метод крайне прост и нагляден, и в общем случае заключается в следующем:

1. На каждой "легкой" операции мы будем класть $C$ монеток в банк (где $C$ - некоторая заранее выбранная константа)
2. На каждой "тяжелой" операции мы будем тратить соответствующее количество монеток из банка (сколько операций нужно, столько мы и возьмем из банка)
3. Если баланс банка всегда неотрицателен, то среднее время работы на каждой опрации равно $O(1)$.

<details markdown="1">
<summary>Доказательство</summary>

Поскольку баланс банка всегда неотрицателен, то сумма всех "падений" баланса банка не превышает сумму всех "подъемов" баланса банка. Поскольку сумма всех "подъемов" баланса банка равна $Cn$, то сумма всех "падений" баланса банка не превышает $Cn$, то есть суммарное время работы алгоритма равно $O(n)$, а значит в среднем на одну операцию $O(1)$.

</details>

Итак, давайте применим метод монеток к нашему алгоритму добавления элемента в массив.

1. За каждую операцию добавления элемента в конец массива мы будем класть в банк 2 монетки
2. За каждую операцию копирования элементов из старого массива в новый мы будем тратить 1 монетку на каждый элемент, то есть всего $n$ монеток

Докажем, что при таком определении банка баланс банка всегда неотрицателен.

<details markdown="1">
<summary>Доказательство</summary>

1. Начнем с ситуации, в которой у нас есть массив размера $n$, но в неём зарезервировано $2n$ памяти, а баланс нулевой.
2. Следующие $n$ операций добавления в массив сделают наш банк размером $2n$ монеток
3. Затем мы будем вынуждены скопировать все элементы из старого массива (размера $2n$) в новый (размера $4n$) - то есть нам нужно $2n$ операций, но у нас есть $2n$ монеток в банке (за $n$ операций вставки), а значит мы можем себе это позволить
4. Таким образом, баланс в банке всегда неотрицательный, и, следовательно, время работы алгоритма на добавление элемента в массив равно $O(1)$ в среднем.

</details>

<div id="dynamic-array-container">
    <div class="info">Size: <span id="n">1</span>, Capacity: <span id="capacity">2</span></div>
    <div class="info">Bank: <span id="potential" class="potential">0</span></div>

    <div class="array-container">
        <div class="array" id="current-array"></div>
        <div class="array" id="temp-array" style="display: none;"></div>
    </div>

    <button id="add-element">Add Element</button>
    <button id="clear-array">Clear</button>
</div>

<style>
    #dynamic-array-container {
        font-family: Arial, sans-serif;
        text-align: center;
        padding: 20px;
    }

    #dynamic-array-container .array-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }

    #dynamic-array-container .array {
        display: flex;
        border: 2px solid black;
        padding: 5px;
        margin: 0 10px;
        position: relative;
    }

    #dynamic-array-container .array .element {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid black;
        margin: 2px;
        background-color: #f0f0f0;
    }

    #dynamic-array-container .info {
        margin: 10px 0;
    }

    #dynamic-array-container .potential {
        font-weight: bold;
    }

    #dynamic-array-container .potential.positive {
        color: green;
    }

    #dynamic-array-container .potential.negative {
        color: red;
    }
</style>
<script>
    class DynamicArray {
        constructor() {
            this.reset();
        }

        reset() {
            this.array = [1];
            this.n = 1;
            this.capacity = 2;
            this.potential = 0;
            this.tempArray = null;
            this.enableButtons();
            this.render();
        }

        addElement() {
            const prevPotential = this.potential;
            if (this.n === this.capacity) {
                this.reallocate();
            } else {
                this.potential += 2;
                this.updatePotentialClass(prevPotential);
                this.array[this.n] = this.n + 1;
                this.n++;
                this.render();
            }
        }

        reallocate() {
            this.disableButtons();
            const prevPotential = this.potential;
            this.tempArray = Array(this.capacity * 2).fill(null);
            const tempArrayDiv = document.getElementById('temp-array');
            tempArrayDiv.style.display = 'flex';
            this.renderTempArray();

            let index = 0;
            const copyInterval = setInterval(() => {
                this.tempArray[index] = this.array[index];
                this.potential--;
                this.updatePotentialClass(prevPotential);
                this.renderTempArray();
                this.renderBank();
                index++;

                if (index === this.n) {
                    clearInterval(copyInterval);
                    this.finalizeReallocation();
                }
            }, 500);
        }

        finalizeReallocation() {
            this.array = this.tempArray;
            this.capacity *= 2;
            this.tempArray = null;
            const prevPotential = this.potential;
            this.updatePotentialClass(prevPotential);
            document.getElementById('temp-array').style.display = 'none';
            this.enableButtons();
            this.render();
        }

        render() {
            const currentArrayDiv = document.getElementById('current-array');
            currentArrayDiv.innerHTML = '';
            const filledArray = this.array.slice(0, this.n).concat(Array(this.capacity - this.n).fill(null));
            filledArray.forEach(value => {
                const elementDiv = document.createElement('div');
                elementDiv.className = 'element';
                elementDiv.textContent = value !== null ? value : '';
                currentArrayDiv.appendChild(elementDiv);
            });
            document.getElementById('n').textContent = this.n;
            document.getElementById('capacity').textContent = this.capacity;
            this.renderBank();
        }

        renderTempArray() {
            const tempArrayDiv = document.getElementById('temp-array');
            tempArrayDiv.innerHTML = '';
            this.tempArray.forEach(value => {
                const elementDiv = document.createElement('div');
                elementDiv.className = 'element';
                elementDiv.textContent = value !== null ? value : '';
                tempArrayDiv.appendChild(elementDiv);
            });
        }

        renderBank() {
            const potentialSpan = document.getElementById('potential');
            potentialSpan.textContent = this.potential;
        }

        updatePotentialClass(prevPotential) {
            const potentialSpan = document.getElementById('potential');
            if (this.potential > prevPotential) {
                potentialSpan.className = 'potential positive';
            } else if (this.potential < prevPotential) {
                potentialSpan.className = 'potential negative';
            } else {
                potentialSpan.className = 'potential';
            }
        }

        disableButtons() {
            document.getElementById('add-element').disabled = true;
            document.getElementById('clear-array').disabled = true;
        }

        enableButtons() {
            document.getElementById('add-element').disabled = false;
            document.getElementById('clear-array').disabled = false;
        }
    }

    const dynamicArray = new DynamicArray();
    document.getElementById('add-element').addEventListener('click', () => {
        dynamicArray.addElement();
    });
    document.getElementById('clear-array').addEventListener('click', () => {
        dynamicArray.reset();
    });
</script>

## *Реализация на C++

Я напишу шаблонный код - сильно упрощенный аналог `std::vector`, который будет поддерживать только операцию добавления элемента в конец массива. И взятия элемента по индексу.

```cpp
#include <iostream>

using namespace std;

template <typename T>
class DynamicArray {
private:
    T* array; // указатель на массив элементов типа T
    int n; // количество элементов в массиве
    int capacity; // количество элементов, которые могут быть добавлены в массив
public:
    DynamicArray() {
        n = 0; // изначально массив пуст
        capacity = 1; // изначально зарезервировано место для 1 элемента
        array = new T[capacity]; // выделяем память под 1 элемент
    }

    ~DynamicArray() {
        delete[] array; // освобождаем память при удалении объекта
    }

    void push_back(T value) {
        if (n == capacity) { // если массив заполнен
            reallocate(); // перевыделяем память
        }
        array[n] = value; // добавляем элемент в конец массива
        n++; // увеличиваем количество элементов в массиве
    }

    T& operator[](int index) {
        return array[index];
    }

private:
    void reallocate() {
        T* tempArray = new T[capacity * 2]; // создаем новый массив размера 2 * capacity
        for (int i = 0; i < n; i++) {
            tempArray[i] = array[i]; // копируем все элементы из старого массива в новый
        }
        delete[] array; // удаляем старый массив
        array = tempArray; // переопределяем указатель на новый массив
        capacity *= 2; // увеличиваем capacity вдвое
    }
};

int main() {
    DynamicArray<int> dynamicArray;
    for (int i = 1; i <= 10; i++) {
        dynamicArray.push_back(i);
    }

    for (int i = 0; i < 10; i++) {
        cout << dynamicArray[i] << ' ';
    }
    cout << endl;

    return 0;
}
```

## *Деамортизация

В некоторых жизненно важных случаях нужно гарантировать время работы программы не в среднем, а в худшем случае. Действительно, представте, что в среднем ваш запрос в гугл занимает 0.01 секунды, но в один прекрасный день он занимает 100 секунд. Ситуация неприятная, поэтому в некоторых областях нужно гарантировать время работы в худшем случае.

Оказывается, динамический массив можно деамортизировать, то есть гарантировать время работы в худшем случае. Прежде чем перейти к решению я рекомендую подумать над этой задачей как минимум день.

<details>
<summary>Подсказка</summary>
Вам понадобится больше памяти
</details>

<details markdown="1">
<summary>Решение</summary>

Давайте опять начнем со случая, когда у вас есть массив размера $2n$ и $n$ элементов в нем заняты.

Ключевой трюк - добавим еще один массив размера $4n$. Теперь на каждое добавление в конец первого массива мы будем совершать еще 2 операции копирования очередных элементов из первого массива во второй. Таким образом к моменту полного заполнения первого массива ($n$ операций) у нас будет второй массив, в котором все элементы из первого массива будут скопированы ($2n$ копирований). После этого мы можем забыть о первом заполненном массиве и создать новый массив размера $8n$ и так продолжать.

</details>
