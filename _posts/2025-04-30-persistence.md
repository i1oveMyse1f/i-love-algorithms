---
layout: post
year: 25
title:  "Персистентные структуры данных"
author: i_love_myself
categories: [ info ]
comments: false
toc: false
---

Техника, позволяющая эффективно хранить все предыдущие версии структуры данных и продолжать с ней работать.

## Список разделов

<div>
<p>
{% assign theme_name = "/persistence/" %}

{% for lecture in site.pages %}
    {% if lecture.path contains 'README.md' and lecture.path contains theme_name %}
        {% assign lecture_path = lecture.path | remove: "_posts/" | remove: ".md" %}
        {% assign lecture_parted = lecture_path | split: "lecture" %}
        {% assign lecture_id = lecture_parted[1] | split: "/" | first | split: "-" | first %}
        {% assign lecture_dir = lecture_path | remove: "/README" %}
        <a href="{{ site.baseurl }}/{{ lecture_path }}">Раздел {{ lecture_id }}</a>: {{ lecture.title }}.
        {% if lecture.youtube or lecture.pdf %}
            [
            {% if lecture.youtube %}
                <a href="https://youtu.be/{{ lecture.youtube }}">Запись</a>
            {% endif %}
            {% if lecture.pdf %}
                <a href="{{ site.baseurl }}/{{ lecture_dir }}/{{ lecture.pdf }}">pdf</a>
            {% endif %}
            ]
        {% endif %}
        <br>
    {% endif %}
{% endfor %}
</p>
</div>
