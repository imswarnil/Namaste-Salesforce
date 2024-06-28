---
layout: default
title: "Training Home"
description: "Welcome to the CRM Analytics Academy Training"
permalink: /training
aside : false
---

<div class="hero is-lights">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
           {{ page.description }}
      </h1>
      <h2 class="subtitle">
        {{ page.description }}
      </h2>
    </div>
  </div>
</div>

<div class="container">
  <section class="section">
    <div class="columns">
      <div class="column is-three-quarters">
        <div class="box">
          <h2 class="title is-4">{{ site.data.course_navigation.course_name }}</h2>
          <p>{{ site.data.course_navigation.course_description }}</p>
          <figure class="image is-16by9">
            <img src="{{ site.data.course_navigation.course_image }}" alt="Course Image">
          </figure>
          <!-- Tabs -->
          <div class="tabs is-centered mt-5">
            <ul>
              <li class="is-active"><a href="#course-info">Course Info</a></li>
              <li><a href="#course-reviews">Reviews</a></li>
              <li><a href="#course-qa">Q&A</a></li>
              <li><a href="#course-announcements">Announcements</a></li>
            </ul>
          </div>
          <!-- Course Info -->
          <div id="course-info" class="content">
            <h3 class="title is-5">About Course</h3>
            <p>{{ site.data.course_navigation.course_description }}</p>
            <h4 class="title is-6">Course Content</h4>
            <div class="content">
              <ul>
                {% for section in site.data.course_navigation.sections %}
                  <li>
                    <strong>{{ section.section }}</strong>
                    <ul>
                      {% for lesson in section.lessons %}
                        <li>
                          <a href="{{ lesson.link }}">
                            <i class="{{ lesson.icon }}"></i> {{ lesson.title }}
                          </a>
                        </li>
                      {% endfor %}
                    </ul>
                  </li>
                {% endfor %}
              </ul>
            </div>
          </div>
          <!-- Reviews -->
          <div id="course-reviews" class="content is-hidden">
            <h3 class="title is-5">Reviews</h3>
            <!-- Add your reviews content here -->
          </div>
          <!-- Q&A -->
          <div id="course-qa" class="content is-hidden">
            <h3 class="title is-5">Q&A</h3>
            <!-- Add your Q&A content here -->
          </div>
          <!-- Announcements -->
          <div id="course-announcements" class="content is-hidden">
            <h3 class="title is-5">Announcements</h3>
            <!-- Add your announcements content here -->
          </div>
        </div>
      </div>
      <div class="column">
        <div class="box">
          <h3 class="title is-5">Course Progress</h3>
          <progress class="progress is-primary" value="0" max="100">0%</progress>
          <p class="mt-2">Complete all lessons to mark this course as complete.</p>
          <button class="button is-primary is-fullwidth">Start Learning</button>
        </div>
        <div class="box">
          <h3 class="title is-5">Course Details</h3>
          <ul>
            <li><strong>Level:</strong> Beginner</li>
            <li><strong>Enrolled:</strong> 7 Total Enrolled</li>
            <li><strong>Duration:</strong> 1 Hour</li>
            <li><strong>Last Updated:</strong> May 15, 2024</li>
          </ul>
        </div>
        <div class="box">
          <h3 class="title is-5">Author</h3>
          <div class="media">
            <div class="media-left">
              <figure class="image is-48x48">
                <img src="https://namastesalesforce.com/wp-content/litespeed/avatar/25fe46c993efce870036b2cb94df4064.jpg?ver=1718713637" alt="Author Image">
              </figure>
            </div>
            <div class="media-content">
              <p class="title is-6">Admin</p>
              <p class="subtitle is-7">Development</p>
            </div>
          </div>
        </div>
        <div class="box">
          <h3 class="title is-5">Material Includes</h3>
          <ul>
            <li>Video Lectures</li>
            <li>Hands-on Exercises</li>
            <li>Course Notes</li>
            <li>Community Access</li>
            <li>Certificate of Completion</li>
          </ul>
        </div>
        <div class="box">
          <h3 class="title is-5">Requirements</h3>
          <ul>
            <li>Basic Understanding of Salesforce</li>
            <li>Access to Salesforce Org</li>
            <li>Desire to Learn</li>
          </ul>
        </div>
        <div class="box">
          <h3 class="title is-5">Tags</h3>
          <span class="tag is-primary">apex</span>
          <span class="tag is-primary">basics</span>
          <span class="tag is-primary">developer</span>
        </div>
        <div class="box">
          <h3 class="title is-5">Audience</h3>
          <ul>
            <li>Aspiring Salesforce Developers</li>
            <li>New Programmers</li>
            <li>Salesforce Admins</li>
            <li>IT Professionals</li>
            <li>Tech Enthusiasts</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</div>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tabs ul li a');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
      tab.addEventListener('click', event => {
        event.preventDefault();
        const target = tab.getAttribute('href').substring(1);

        tabs.forEach(t => t.parentElement.classList.remove('is-active'));
        contents.forEach(content => content.classList.add('is-hidden'));

        tab.parentElement.classList.add('is-active');
        document.getElementById(target).classList.remove('is-hidden');
      });
    });
  });
</script>

