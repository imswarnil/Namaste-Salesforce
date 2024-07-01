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



  <header class="header">
        <section class="hero is-primary is-bold">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <div class="column is-8 is-offset-2">
                        <h2 class="subtitle is-3 mb-3">Promote Your Online Course <br class="is-hidden-desktop">Like A Pro</h2>
                        <h1 class="title is-1 mb-5">
                            <span class="brand mb-4">
                                <span class="has-text-warning">{</span>
                                <span class="name">DevCourse</span>
                                <span class="has-text-warning">}</span>
                            </span>
                            <span class="subtitle">A Course Landing Page Template For Developers</span>
                        </h1>
                        <div class="mb-5">
                            <a href="#section-pricing" class="button is-primary is-large">Start Learning Now</a>
                        </div>
                        <div class="columns is-vcentered is-centered">
                            <div class="column is-4 has-text-centered">
                                <div class="mb-1">
                                    <i class="fas fa-video icon mr-2"></i>Content
                                </div>
                                <h4 class="title is-4">80+ <span class="subtitle is-6">Videos</span></h4>
                            </div>
                            <div class="column is-4 has-text-centered">
                                <div class="mb-1">
                                    <i class="fas fa-clock icon mr-2"></i>Duration
                                </div>
                                <h4 class="title is-4">72 <span class="subtitle is-6">Hours</span></h4>
                            </div>
                            <div class="column is-4 has-text-centered">
                                <div class="mb-1">
                                    <i class="fas fa-circle-user icon mr-2"></i>Access
                                </div>
                                <h4 class="title is-4">Lifetime</h4>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </header>
    <div class="sections-wrapper">
        <section id="section-overview" class="section">
            <div class="container">
                <div class="column is-8 is-offset-2 has-text-centered">
                    <h3 class="title is-3 mb-4">What Will You Learn</h3>
                    <p class="mb-4">Your course overview goes here. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae posuere nibh, at posuere enim. Sed vulputate ante congue, euismod odio a, gravida neque. Maecenas volutpat risus dolor.</p>
                    <div class="mb-3">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check has-text-success mr-2"></i>Course highlight lorem ipsum</li>
                            <li><i class="fas fa-check has-text-success mr-2"></i>Course highlight lorem ipsum</li>
                            <li><i class="fas fa-check has-text-success mr-2"></i>Course highlight lorem ipsum</li>
                            <li><i class="fas fa-check has-text-success mr-2"></i>Course highlight lorem ipsum</li>
                            <li><i class="fas fa-check has-text-success mr-2"></i>Course highlight lorem ipsum</li>
                            <li><i class="fas fa-check has-text-success mr-2"></i>Course highlight lorem ipsum</li>
                        </ul>
                    </div>
                    <div class="mb-5">
                        <a href="#section-pricing" class="button is-primary">Join Course Now</a>
                    </div>
                    <div class="video-container">
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe width="560" height="315" src="https://www.youtube.com/embed/qz0aGYrrlhU" frameborder="0" allowfullscreen></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section id="section-content" class="section">
            <div class="container">
                <div class="column is-8 is-offset-2">
                    <h3 class="title is-3 mb-5">What's Included</h3>
                    <div class="columns is-multiline has-text-centered">
                        <div class="column is-3">
                            <div class="box">
                                <div class="title is-4">10+</div>
                                <div class="subtitle">Modules</div>
                            </div>
                        </div>
                        <div class="column is-3">
                            <div class="box">
                                <div class="title is-4">80+</div>
                                <div class="subtitle">Videos</div>
                            </div>
                        </div>
                        <div class="column is-3">
                            <div class="box">
                                <div class="title is-4">40+</div>
                                <div class="subtitle">Resources</div>
                            </div>
                        </div>
                        <div class="column is-3">
                            <div class="box">
                                <div class="title is-4">72</div>
                                <div class="subtitle">Hours</div>
                            </div>
                        </div>
                    </div>
                    <h4 class="title is-4 has-text-centered mb-4">Course Modules</h4>
                    <div class="accordion">
                        <article class="message is-primary">
                            <div class="message-header">
                                <p>Module 1 - Lorem Ipsum Dolor Sit Amet</p>
                            </div>
                            <div class="message-body">
                                Module intro goes here. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            </div>
                        </article>
                        <article class="message">
                            <div class="message-header">
                                <p>Module 2 - Lorem Ipsum Dolor Sit Amet</p>
                            </div>
                            <div class="message-body">
                                Module intro goes here. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            </div>
                        </article>
                        <article class="message">
                            <div class="message-header">
                                <p>Module 3 - Lorem Ipsum Dolor Sit Amet</p>
                            </div>
                            <div class="message-body">
                                Module intro goes here. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            </div>
                        </article>
                    </div>
                    <div class="has-text-centered mt-5">
                        <a href="#section-pricing" class="button is-primary">Enroll Now</a>
                    </div>
                </div>
            </div>
        </section>
        <section id="section-requirements" class="section">
            <div class="container">
                <div class="column is-8 is-offset-2">
                    <h3 class="title is-3 mb-4">Who Is This Course For</h3>
                    <p class="mb-4">This course is designed for developers lorem ipsum consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>
                    <div class="box">
                        <h4 class="title is-4 has-text-centered">Get Free Course Previews</h4>
                        <div class="content has-text-centered mb-3">Sign up to get instant access to the course previews.</div>
                        <form>
                            <div class="field">
                                <label class="label">Email</label>
                                <div class="control">
                                    <input class="input" type="email" placeholder="Your Email">
                                </div>
                            </div>
                            <div class="control">
                                <button class="button is-primary is-fullwidth">Sign Up Now</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
        <section id="section-tutor" class="section has-background-primary has-text-white">
            <div class="container">
                <div class="columns">
                    <div class="column is-3 has-text-centered">
                        <figure class="image is-128x128 is-inline-block">
                            <img class="is-rounded" src="assets/images/tutor.jpg" alt="">
                        </figure>
                    </div>
                    <div class="column is-9">
                        <h3 class="title is-3 has-text-white">Meet The Tutor</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus at hendrerit augue, eu pellentesque dolor. Praesent vel congue velit. Fusce lorem nisl, condimentum in pulvinar et, laoreet vel felis. Duis tincidunt ex sed risus posuere, quis venenatis quam tincidunt. Quisque arcu lacus, mollis volutpat turpis sit amet, interdum eleifend sem.</p>
                        <p>Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Etiam auctor leo at mi dignissim, tempor porttitor leo vehicula.</p>
                        <div class="field is-grouped">
                            <p class="control">
                                <a class="button is-medium is-link" href="#">
                                    <span class="icon">
                                        <i class="fab fa-github"></i>
                                    </span>
                                </a>
                            </p>
                            <p class="control">
                                <a class="button is-medium is-link" href="#">
                                    <span class="icon">
                                        <i class="fab fa-twitter"></i>
                                    </span>
                                </a>
                            </p>
                            <p class="control">
                                <a class="button is-medium is-link" href="#">
                                    <span class="icon">
                                        <i class="fab fa-linkedin"></i>
                                    </span>
                                </a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section id="section-pricing" class="section">
            <div class="container">
                <div class="column is-8 is-offset-2 has-text-centered">
                    <h3 class="title is-3 mb-4">Choose Your Plan</h3>
                    <p class="mb-5">Simple pricing plans for developers of all levels.</p>
                    <div class="columns is-multiline is-centered">
                        <div class="column is-4">
                            <div class="box">
                                <h4 class="title is-4">Basic</h4>
                                <p class="subtitle is-6">$29</p>
                                <ul class="list-unstyled mb-3">
                                    <li><i class="fas fa-check mr-2"></i>Access to course content</li>
                                    <li><i class="fas fa-check mr-2"></i>10 modules</li>
                                    <li><i class="fas fa-check mr-2"></i>Lifetime access</li>
                                    <li><i class="fas fa-check mr-2"></i>Community support</li>
                                </ul>
                                <a href="#" class="button is-primary is-fullwidth">Enroll Now</a>
                            </div>
                        </div>
                        <div class="column is-4">
                            <div class="box">
                                <h4 class="title is-4">Pro</h4>
                                <p class="subtitle is-6">$49</p>
                                <ul class="list-unstyled mb-3">
                                    <li><i class="fas fa-check mr-2"></i>Access to course content</li>
                                    <li><i class="fas fa-check mr-2"></i>All modules</li>
                                    <li><i class="fas fa-check mr-2"></i>Lifetime access</li>
                                    <li><i class="fas fa-check mr-2"></i>Community support</li>
                                    <li><i class="fas fa-check mr-2"></i>Bonus content</li>
                                </ul>
                                <a href="#" class="button is-primary is-fullwidth">Enroll Now</a>
                            </div>
                        </div>
                        <div class="column is-4">
                            <div class="box">
                                <h4 class="title is-4">Ultimate</h4>
                                <p class="subtitle is-6">$99</p>
                                <ul class="list-unstyled mb-3">
                                    <li><i class="fas fa-check mr-2"></i>Access to course content</li>
                                    <li><i class="fas fa-check mr-2"></i>All modules</li>
                                    <li><i class="fas fa-check mr-2"></i>Lifetime access</li>
                                    <li><i class="fas fa-check mr-2"></i>Community support</li>
                                    <li><i class="fas fa-check mr-2"></i>Bonus content</li>
                                    <li><i class="fas fa-check mr-2"></i>1-on-1 mentorship</li>
                                </ul>
                                <a href="#" class="button is-primary is-fullwidth">Enroll Now</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section id="section-testimonials" class="section has-background-primary has-text-white">
            <div class="container">
                <div class="column is-8 is-offset-2 has-text-centered">
                    <h3 class="title is-3 mb-5">What Our Students Say</h3>
                    <div class="columns is-multiline is-centered">
                        <div class="column is-4">
                            <div class="card has-background-primary has-text-white">
                                <div class="card-content">
                                    <p class="subtitle">"This course is amazing! I learned so much and I'm now confident to build my own projects."</p>
                                    <p class="has-text-weight-bold">- Jane Doe</p>
                                </div>
                            </div>
                        </div>
                        <div class="column is-4">
                            <div class="card has-background-primary has-text-white">
                                <div class="card-content">
                                    <p class="subtitle">"The tutor is very knowledgeable and the content is well-structured. Highly recommend!"</p>
                                    <p class="has-text-weight-bold">- John Smith</p>
                                </div>
                            </div>
                        </div>
                        <div class="column is-4">
                            <div class="card has-background-primary has-text-white">
                                <div class="card-content">
                                    <p class="subtitle">"A great course for developers of all levels. The community support is also fantastic."</p>
                                    <p class="has-text-weight-bold">- Emily Johnson</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <footer class="footer has-background-dark has-text-white">
            <div class="container">
                <div class="columns">
                    <div class="column is-4 has-text-centered">
                        <p class="title is-4">DevCourse</p>
                        <p>&copy; 2024 DevCourse. All rights reserved.</p>
                    </div>
                    <div class="column is-4 has-text-centered">
                        <div class="field is-grouped is-grouped-centered">
                            <p class="control">
                                <a class="button is-medium is-link" href="#">
                                    <span class="icon">
                                        <i class="fab fa-facebook"></i>
                                    </span>
                                </a>
                            </p>
                            <p class="control">
                                <a class="button is-medium is-link" href="#">
                                    <span class="icon">
                                        <i class="fab fa-twitter"></i>
                                    </span>
                                </a>
                            </p>
                            <p class="control">
                                <a class="button is-medium is-link" href="#">
                                    <span class="icon">
                                        <i class="fab fa-instagram"></i>
                                    </span>
                                </a>
                            </p>
                        </div>
                    </div>
                    <div class="column is-4 has-text-centered">
                        <p class="title is-4">Contact Us</p>
                        <p>Email: info@devcourse.com</p>
                        <p>Phone: +1 234 567 890</p>
                    </div>
                </div>
            </div>
        </footer>
    </div>