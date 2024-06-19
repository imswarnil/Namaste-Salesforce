---
layout: default
title: Courses
---

<section class="section">
  <div class="container">
    <h1 class="title">Courses</h1>
    <div class="columns is-multiline">
      {% for course in site.courses %}
        <div class="column is-one-third">
          <div class="box">
            <h2 class="subtitle">{{ course.title }}</h2>
            <p>{{ course.description }}</p>
            <a href="{{ course.url }}" class="button is-primary">View Course</a>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
</section>
