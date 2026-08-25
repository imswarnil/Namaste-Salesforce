# Fonts — vendored from NS-Design-System

Two self-hosted variable woff2 faces, copied verbatim from
`NS-Design-System/fonts/`. A Ghost theme ships as a self-contained zip, so
anything reaching outside the theme root resolves on your machine and 404s on
the server — these files have to live here, not be referenced across.

| role | face | file | axis | size |
|---|---|---|---|---|
| sans — interface and reading | **Switzer** | `switzer-var-latin.woff2` | `wght 100–900` | 29 KB |
| mono — data, labels, code | **Roboto Mono** | `roboto-mono-var-latin.woff2` | `wght 100–700` | 37 KB |

`@font-face` declarations live in `../css/screen.css`.

## Licences — both must stay in this directory

**Switzer** — Indian Type Foundry, via Fontshare, under the **Fontshare Free
Font EULA** (`FONTSHARE-EULA.txt`). Free for personal *and* commercial use, any
medium, unlimited time, self-hosting explicitly permitted. The EULA must travel
with the file.

> **This licence permits self-hosting on your own site. It does NOT permit
> redistributing the font software to anyone else.** §02 forbids the fonts
> being "distributed, duplicated, loaned, resold or licensed in any way". That
> is fine here — this theme runs *your* site. It is why a theme sold to other
> people cannot bundle Switzer, and why `Scratchpad-Ghost-Theme` ships Figtree
> (SIL OFL) instead.

**Roboto Mono** — SIL Open Font Licence 1.1, `licences/roboto-mono-OFL.txt`.
Use, self-host and redistribute freely including commercially, provided the
licence ships with the file.

To re-cut either face with wider Unicode coverage, see
`NS-Design-System/fonts/README.md` § Subsetting.
