// ═══════════════════════════════════════════════════════════════════════════
// gulpfile.js — Build pipeline for the Namaste Salesforce Ghost theme
// ---------------------------------------------------------------------------
// Tasks (run via `yarn <name>`):
//   dev    → build once, then watch assets + livereload (default export)
//   build  → compile css + js + locales into assets/built/
//   zip    → build, then package the theme into dist/ for upload to Ghost
//
// Output in assets/built/ is committed to git because Ghost serves it directly,
// so remember to rebuild after editing SCSS or JS.
// ═══════════════════════════════════════════════════════════════════════════
const {series, watch, src, dest, parallel} = require('gulp');
const pump = require('pump');

// gulp plugins & utils
const livereload = require('gulp-livereload');
const postcss = require('gulp-postcss');
const zip = require('gulp-zip');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const beeper = require('beeper');

// postcss plugins
const tailwindcss = require('@tailwindcss/postcss'); // Tailwind v4 (CSS-first)
const cssnano = require('cssnano');

// translations support
const {mergeLocales} = require('@tryghost/theme-translations/build');

// Beep on error so failures are noticed during `yarn dev` watch sessions.
const handleError = (done) => {
    return function (err) {
        if (err) {
            beeper();
        }
        return done(err);
    };
};

function serve(done) {
    livereload.listen();
    done();
}

// Reload the browser when a template changes.
function hbs(done) {
    pump([
        src(['*.hbs', 'partials/**/*.hbs']),
        livereload()
    ], handleError(done));
}

// Tailwind entry → generated, minified CSS. Tailwind v4 emits its own vendor
// prefixes via Lightning CSS, so autoprefixer is no longer needed.
function css(done) {
    pump([
        src('assets/css/screen.css', {sourcemaps: true}),
        postcss([
            tailwindcss(),
            cssnano()
        ]),
        dest('assets/built/', {sourcemaps: '.'}),
        livereload()
    ], handleError(done));
}

// Concatenate our small scripts (theme toggle, TOC, effects) and minify.
// Note: assets/js/vendor/* (e.g. Alpine) is loaded separately in default.hbs,
// so it is intentionally NOT part of this bundle.
function js(done) {
    pump([
        src('assets/js/*.js', {sourcemaps: true}),
        concat('casper.js'),
        uglify(),
        dest('assets/built/', {sourcemaps: '.'}),
        livereload()
    ], handleError(done));
}

// Package the theme for upload to Ghost admin.
function zipper(done) {
    const filename = require('./package.json').name + '.zip';

    pump([
        src([
            '**',
            '!node_modules', '!node_modules/**',
            '!dist', '!dist/**',
            '!yarn-error.log',
            '!yarn.lock',
            '!gulpfile.js'
        ]),
        zip(filename),
        dest('dist/')
    ], handleError(done));
}

// Merge author overrides in locales-local/ into the shipped locales/.
function locales(done) {
    mergeLocales({
        local: './locales-local',
        output: './locales'
    })(done);
}

// Recompile CSS when the entry changes OR when templates change (new class
// names in .hbs need Tailwind to regenerate utilities).
const cssWatcher = () => watch(['assets/css/**/*.css', '*.hbs', 'partials/**/*.hbs'], css);
const jsWatcher = () => watch('assets/js/**', js);
const hbsWatcher = () => watch(['*.hbs', 'partials/**/*.hbs'], hbs);
const localesWatcher = () => watch('./locales-local/**/*.json', locales);
const watcher = parallel(cssWatcher, jsWatcher, hbsWatcher, localesWatcher);
const build = series(css, js, locales);

exports.build = build;
exports.zip = series(build, zipper);
exports.default = series(build, serve, watcher);
