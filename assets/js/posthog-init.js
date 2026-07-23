/* ============================================================================
   posthog-init.js — PostHog analytics initialisation
   ----------------------------------------------------------------------------
   Token and host are injected at build time from .env by the gulp pipeline
   (POSTHOG_PROJECT_TOKEN / POSTHOG_API_HOST). If the token is absent the
   snippet is skipped; in development a console warning is emitted.
   ========================================================================== */
(function () {
  'use strict';

  var token = '__POSTHOG_TOKEN__';
  var host  = '__POSTHOG_HOST__';

  if (!token) {
    if (typeof console !== 'undefined' &&
        (window.location.hostname === 'localhost' ||
         window.location.hostname === '127.0.0.1')) {
      console.warn(
        'POSTHOG_PROJECT_TOKEN variable required by PostHog is missing or ' +
        'un-configured, this causes events to be silently missed. ' +
        'This error stops appearing once POSTHOG_PROJECT_TOKEN is configured'
      );
    }
    return;
  }

  /* posthog-js array.js snippet (v1) */
  /* eslint-disable */
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+" (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  /* eslint-enable */

  window.posthog.init(token, {
    api_host:                 host,
    person_profiles:          'identified_only',
    autocapture:              true,
    capture_pageview:         true,
    capture_pageleave:        true,
    enable_recording_console_log: false,
    loaded: function (ph) {
      /* Identify Ghost members on page load.
         window.__phMember is injected by default.hbs when a member is logged in.
         Using member UUID as distinct_id keeps PII out of event properties. */
      var m = window.__phMember;
      if (m && m.id) {
        ph.identify(m.id, { email: m.email, name: m.name, subscription_status: m.subscribed ? 'active' : 'free' });
      }
    }
  });

  /* Capture unhandled JS errors and promise rejections so they appear in
     PostHog Error Tracking alongside the session recording. */
  window.addEventListener('error', function (e) {
    if (window.posthog && e.error) {
      window.posthog.captureException(e.error);
    }
  });

  window.addEventListener('unhandledrejection', function (e) {
    if (window.posthog && e.reason) {
      var err = e.reason instanceof Error ? e.reason : new Error(String(e.reason));
      window.posthog.captureException(err);
    }
  });
})();
