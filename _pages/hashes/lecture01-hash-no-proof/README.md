---
layout: lecture
title:  "Хеши"
author: i_love_myself
categories: [ hashes ]
toc: true
---

В этом разделе мы придумаем некоторую универсальную интуитивную технику, которая позволит сравнивать элементы почти произвольных типов на равенство за $O(1)$. Почему это фундаментально важно? Приведу лишь часть примеров, в которых данная техника будет давать ускорение:

| Задача | Сложность без хешей | Сложность с хешами |
|--------|--------------------|--------------------|
| Сравнение двух строк на равенство | $O(n)$ | $O(1)$ |
| Сравнение двух строк лексикографически | $O(n)$ | $O(\log n)$ |
| Проверка строки на палиндром | $O(n)$ | $O(1)$ |
| Сравнение двух множеств на равенство | $O(n \log n)$ | $O(1)$ |
| [Изоморфизм](https://ru.wikipedia.org/wiki/%D0%98%D0%B7%D0%BE%D0%BC%D0%BE%D1%80%D1%84%D0%B8%D0%B7%D0%BC_%D0%B3%D1%80%D0%B0%D1%84%D0%BE%D0%B2) деревьев | $O(n!)$ | $O(n)$ |

Равенство в нашем контексте - это не только равенство по значению, но и равенство по другому признаку, как в примере с изоморфизмом деревьев (=равенству деревеьев с точностью до перенумерации вершин).

Пока звучит как магия. Математика, стоящая за этой магией будет разобрана в одном из следующих разделов, а пока мы будем довольствоваться интуицией, которую я постараюсь донести.

## Хеш-функция

Хеш-функция $h(x)$ - это функция, которая принимает на вход некоторый объект $x \in \mathcal X$ - какое-то абстрактное множество определения и возвращает его хеш - некоторое целое число (от $0$ до $P - 1$; типичное значение будет порядка $P \approx 10^9$, то есть `int`):

$$
h(x): \mathcal X \to [0, 1, \ldots P - 1]
$$

После такого преобразования вместо сравнения двух объектов $x$ и $y$ на равенство, мы можем сравнить их хеши $h(x)$ и $h(y)$ на равенство.

Но вот беда, если $\\| \mathcal X \\| > P$, то по принципу Дирихле найдется хотя бы два разных объекта, которые имеют одинаковый хеш - такая ситуация называется **коллизией**.

Коллизии будут неизбежны, поскольку это и есть сама цель хеш-функции - компактно представлять объекты из очень большого множества для быстрой операции равенства. Чтобы оценить масштаб коллизий, представьте, что вы хотите построить хеш-функцию для строк длины $n=10^5$ с алфавитом из $k=26$ латинских строчных букв. Тогда количество различных строк будет равно $k^n$. Подставляя мы с ужасом получим, что найдется хотя бы одно значние хеша, в которую отобразится $10^{120}$ различных строк!

Плохо ли наличие стольких коллизий? Оказывается, что нет! Хотя под определение хеш-функции подходит куча "глупых" отображений, среди них мы выделим некоторый класс **хороших** хеш-функций. Мы будем постепенно уточнять, что же это значит, а пока для первого приближения мы будем называть функцию хорошей, если вероятность коллизии в программе будет крайне мала (подуйте, в чем разница с тем, что всего коллизий в отображении много!).

## Хеш пары

Начнем придумывать хеш-функции с хеша пары целых чисел. Итак, мы хотим построить хеш-функцию для пары целых чисел $x$ и $y$ из $[0, 1, \ldots, P-1] \times [0, 1, \ldots, P-1]$ в $[0, 1, \ldots, P-1]$. Рекомендую самостоятельно придумать хоть какое-нибудь отображение!

### "Плохая" хеш-функция

Предположим, что мы придумали следующую функцию:

$$
h(x, y) = (x + y) \bmod P
$$

К сожалению, это отображение нам не подойдет, потому что мы можем легко придумать пример, когда две разные пары будут иметь одинаковый хеш $\forall x, y$:

$$
h(x, y) = h(y, x)
$$

### "Хорошая" хеш-функция

Проблема прошлой функции заключалась в том, что она была симметрична. Давайте уберем симметрию, домножив $y$ на какое-нибудь случайное число:

$$
h(x, y) = (x + 100500 \cdot y) \bmod P
$$

Хорошая ли это хеш-функция? Да! Подобрать разные пары $(x, y)$ и $(x', y')$ с одинаковым хешем будет крайне сложно, поскольку для этого нужно решить уравнение:

$$
(x + 100500 \cdot y) \bmod P = (x' + 100500 \cdot y') \bmod P
$$

Чтобы придумать "хорошую" хеш-функцию, её надо зачеленджить и попытаться придумать пример, когда она будет давать одинаковый хеш для разных пар. Если не получается, то это будет одним из признаков того, что хеш-функция хорошая.

## Хеш строки

### Расширяем идею хеша пары

Теперь мы хотим построить хорошую хеш-функцию для строки $s$. Никто не мешает нам применить идею с парой к строке, зафиксировав некоторый набор чисел $a_0, a_1, \ldots, a_{n-1}$:

$$
h(s) = (s_0 a_0 + s_1 a_1 + \ldots + s_{n-1}a_{n-1}) \bmod P
$$

Но мы можем немного упростить себе задачу и вместо того, чтобы заранее фиксировать целый набор чисел, использовать некоторую функцию $f(i)$, которая будет генерировать числа $a_i$. Например, можно использовать $a_i = 100500^i$ (далее $Q = 100500$).

$$
h(s) = (s_0 + s_1 Q^1 + \ldots + s_{n-1}Q^{n-1}) \bmod P
$$

Такую хеш-функцию называют **полиномиальной**, поскольку она является полиномом от $Q$.

### Задачи

За счёт внутренней структуры полиномиального хеша мы можем научиться решать более интересную задачу, чем сравнивать две произвольные строки на равенство - мы научимся **сравнивать две подстроки** на равенство за $O(1)$ и $O(L)$ предпросчета. Подумайте самостоятельно, как это сделать, прежде чем читать решение!

<details>
<summary>Сравнение двух подстрок за $O(1)$</summary>
Для того, чтобы сравнить две подстроки $s[l_1 \ldots r_1]$ и $s[l_2 \ldots r_2]$ нам нужно сравнить их хеши:

$$
h(s[l_1 \ldots r_1]) = (s[l_1] + s[l_1 + 1] Q^1 + \ldots + s[r_1]Q^{r_1 - l_1}) \bmod P
$$

и

$$
h(s[l_2 \ldots r_2]) = (s[l_2] + s[l_2 + 1] Q^1 + \ldots + s[r_2]Q^{r_2 - l_2}) \bmod P
$$

К сожалению, в лоб это выражение посчитать за $O(1)$ не получится, но это очень похоже на задачу поиска суммы на отрезке, которую мы умеем решать за $O(1)$ с помощью префиксных сумм. Давайте попробуем сделать что-то похожее.

Для этого насчитаем префиксные суммы:

$$
p_i = (s[0] + s[1] Q^1 + \ldots + s[i]Q^{i}) \bmod P
$$

Тогда посмотрим на то, что значит $pref_r - pref_{l-1}$ по аналогии с префиксными суммами:

$$
p_{r} - p_{l - 1} = (Q^{l} s[l] + s[l + 1] Q^{l + 1} + \ldots + s[r]Q^{r}) \bmod P
$$

Вынесем $Q^{l}$ за скобки:

$$p_{r} - p_{l - 1} = Q^{l} (s[l] + s[l + 1] Q^1 + \ldots + s[r]Q^{r - l}) \bmod P$$

А внутри осталась хеш-функция от подстроки $s[l \ldots r]$:

$$p_{r} - p_{l - 1} = Q^{l} h(s[l \ldots r]) \bmod P$$

То есть хеш подстроки, домноженный на $Q^{l}$ мы можем вычислить за $O(1)$! Но нам то надо проверить на равенство сами хеши: $h(s[l_1 \ldots r_1])$ и $h(s[l_2 \ldots r_2])$, поэтому дальше есть два пути:

1. Если $P$ - простое число, то мы можем домножить обе части на $Q^{-l} \bmod P$ (заранее предпросчитать обратные числа по Малой Теореме Ферма), так мы найдем честный хеш любой подстроки за $O(1)$ (но предпросчет будет тяжелый).
2. Есть способ и проще - вместо того чтобы сравнивать хеши подстрок, мы можем домножить оба хеша на одно и то же число $Q^{l_1 + l_2}$, тогда мы получим:

$$
Q^{l_1 + l_2} h(s[l_1 \cdots r_1]) \overset{?}{=} Q^{l_1 + l_2} h(s[l_2 \cdots r_2])
$$

Или применяя выражение с префиксными суммами:

$$
Q^{l_2} (p_{r_1} - p_{l_1 - 1}) \overset{?}{=} Q^{l_1} (p_{r_2} - p_{l_2 - 1})
$$

А такую проверку мы уже можем сделать за $O(1)$, поскольку у нас есть префиксные суммы (и предпросчитанные степени $Q$).

</details>

<details markdown="1">
<summary>Реализация</summary>

```cpp
const int P = 1e9 + 7;
const int Q = 543;

const int N = 1e5 + 1;

int degq[N], h[N];

bool is_equal(int l1, int r1, int l2, int r2) {
    int h1 = h[r1] - (l1 == 0 ? 0 : h[l1 - 1]);
    if (h1 < 0) h1 += P;
    int h2 = h[r2] - (l2 == 0 ? 0 : h[l2 - 1]);
    if (h2 < 0) h2 += P;
    return h1 * 1LL * degq[l2] % P == h2 * 1LL * degq[l1] % P;
}

int main() {
    // h(s1s2s3...) = s1 + s2*Q + s3*Q^2 + ...
    degq[0] = 1;
    for (int i = 1; i < N; ++i) {
        degq[i] = degq[i - 1] * 1LL * Q % P;
    }
 
    string s;
    cin >> s;
 
    int n = s.size();
 
    for (int i = 0; i < n; ++i) {
        h[i] = ((i == 0 ? 0 : h[i - 1]) + s[i] * 1LL * degq[i]) % P;
    }
 
    int q;
    cin >> q;
    for (int i = 0; i < q; ++i) {
        int l1, r1, l2, r2;
        cin >> l1 >> r1 >> l2 >> r2;
        --l1; --l2; --r1; --r2;
        cout << (is_equal(l1, r1, l2, r2) ? "YES" : "NO") << "\n";
    }
}
```

</details>

Теперь рекомендую придумать как с помощью полиномиальных хешей решить следующие задачи:

* Проверить подстроку на палиндром за $O(1)$
* Понять, какая из двух строк лексикографически меньше за $O(\log L)$
* На двумерной таблице символов проверять подматрицы на равенство за $O(1)$

## Хеш множества

Представьте, что теперь мы хотим научиться сравнивать два множества на равенство за $O(1)$, а так же уметь добавлять и удалять элементы из множества. Под множеством я имею ввиду неупорядоченный набор элементов, в котором каждый элемент встречается не больше одного раза.

Можем ли мы здесь использовать идею полиномиального хеша? Нет, поскольку если раньше нам важен был порядок элементов во множестве, то теперь - нет. Предлагаю вам самостоятельно разрешить этот консенсус, прежде чем читать решение!

<details>
<summary>Подсказка</summary>
Кажется, у нас уже была хеш-функция, которая не учитывала порядок элементов - это "плохая" хеш-функция для пары.
</details>

<details>
<summary>Решение</summary>
Мы можем взять идею "плохого" хеша пары и применить ее к множеству $A$:

$$h(A) = (a_0 + a_1 + \ldots + a_{n-1}) \bmod P$$

Однако мы опять легко можем придумать пример, когда два разных множества будут иметь одинаковый хеш, например если $P$ достаточно большое то $h([2, 3]) = h(1, 4)$.

Поэтому мы предварительно преобразуем все элементы в некоторый другой набор случайных чисел $a_i \to f(a_i)$ с помощью некоторой функции $f(x)$, например:

$$
f(x) = (100500 \cdot x) \bmod P
$$

Мы также можем расширить эту идею на мультимножетсва или оставить множества, но повысить скорость за счет перехода от суммы к битовому ксору.

</details>

## Парадокс дней рождений и вероятность коллизий

Парадокс дней рождений формулируется следующим образом: с вероятностью больше 50% в группе из 23 человек найдется хотя бы одна пара людей, у которых совпадают дни рождения (замечали ли вы раньше, что у вас в классе/группе есть два человека с одинаковым днем рождения?).

Это утверждение очень похоже на то, что происходит с коллизиями в хеш-функциях, только в них количество дней в году мы обозначали как $P=365$, а количество людей в классе - это количество элементов, которые мы хешируем (проверяем на равенство).

Комбинаторика стоящая за парадоксом дней рождений не сложная. Будем считать вероятность того что в классе из $n$ человек не будет совпадений ДР:

* $n = 1: P_1 = 1$
* $n = 2: P_2 = 1 - \frac{1}{365}$ - с вероятностью $\frac{1}{365}$ у нас совпадут дни рождения
* $n = 3:$ С вероятностью $P_2$ у двух людей ДР в разные дни и с вероятностью $\frac{2}{365}$ ДР третьего человека совпадет с одним из двух первых. То есть $P_3 = P_2 \cdot (1 - \frac{2}{365}) = (1 - \frac{1}{365})(1 - \frac{2}{365})$
* $n = 4:$ По аналогии $P_4 = P_3 \cdot (1 - \frac{3}{365}) = (1 - \frac{1}{365})(1 - \frac{2}{365})(1 - \frac{3}{365})$
* $\ldots$

Чтобы понять, как быстро падает вероятность того, что в классе нет людей с одинаковым днем рождения, воспользуемся оценкой (можно взять из формулы Стирлинга или доказать более простыми способами):

$$ e^x > 1 + x $$

Тогда мы можем оценить:

$$
P_n = \prod_{i=1}^{n-1} \left(1 - \frac{i}{365}\right) > \prod_{i=1}^{n-1} e^{-\frac{i}{365}} = e^{-\frac{n(n-1)}{2 \cdot 365}} > e^{-\frac{n^2}{2 \cdot 365}}
$$

Что это значит, обобщая на хеш-функции?

<div class="alert alert-info" markdown="1">
**Вероятность коллизии** становится больше $50\%$ при $P \approx C < N^2$, где $P$ - это количество возможных значений функции, а $C$ - количество потенциальных мест коллизии, которое не превосходит $N^2$, где $N$ - количество элементов.
</div>

Подробно объясню, как посчитать $C$:

* Если в задаче требуется проверить, есть ли в массиве хотя бы $2$ одинаковых элемента, то $C = N^2$, поскольку любая пара элементов может поздать коллизию (хотя в реальности мы наверняка не будем за квадрат проверять все пары, а запустим сортировку).
* Если в массиве нужно сравнить $N$ попарно соседних элементов, то $C = N$, поскольку только соседние элементы могут вызвать коллизию.

## Так что же такое хорошая хеш-функция?

Если помедитировать над парадоксом дней рождений, то мы требовали того, чтобы вероятность каждого элемента была независима равна $1/P$. То есть мы можем сказать, что хорошая хеш-функция - это такая, которая генерирует случайные числа от $0$ до $P-1$ с равной вероятностью.

Но на самом деле это требование слишком сильное, хотя и очень интуитивное. Оказывается, мы можем сохранить доказательство парадокса дней рождений, но ослабить требование до вероятности того, что у двух элементов будет одинаковый хеш, будет не больше $1/P$ - именно это и будет хорошей хеш-функцией. В одном из следующих разделов мы подробно разберем математику, стоящую за этим интуитивным утверждением.

Еще одно неявное требование - мы хотим, чтобы хорошая хеш-функция была быстро вычислимой.

## Про выбор $P$ и $Q$

Общие рекомендации по хешированию:

* $P$ - большое простое число, позволяющее делать все операции по модулю $P$ (сложение, умножение, разность) (например, $10^9 + 7$ или $10^9 + 9$).
* $Q$ - случайное число, желательно большее чем любой элемент, который мы хешируем (например, для строк - что угодно больше $256$).
* Хешируемые элементы - крайне рекомендую делать так, чтобы элементы были $>0$, в противном случае есть риск простейшей коллизии: $h(\text{"000"}) = h(\text{"0000"}) = 0$
* $P > С$, где $С$ - количество потенциальных коллизий, в худшем случае: $P > N^2$. Но как быть в худшем случае: если $N>10^5$, то $P>10^{10}$, а это уже не влезает в `int` (а `long long` брать нельзя, поскольку у нас есть умножения)?

<details>
<summary>Как быть, если не можем делать арифметику с таким большим $P$?</summary>
Если нам нужно достаточно большое $P$, то мы можем использовать одновременно несколько хеш-функций с разными $Q$. То есть хеш функция будет представлять собой вектор из нескольких хешей, это называется двойное/тройное хеширование:

$$
h(x) = (h_1(x), h_2(x), \ldots)
$$

</details>
