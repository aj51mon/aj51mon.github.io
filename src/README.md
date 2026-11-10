# Gym Library source

The two apps are generated from these files. **Edit here, not the built HTML.**

- `app_template.html`: the app (markup, styles, script). `__DATA__` and `__FRIENDS__` are filled in at build time.
- `build.py`: the exercise library, workouts (W001–W008), coaching cues; writes `gym-library.html`, `data.json` and the Excel workbook.
- `make_pwa.py`: wraps the page as the main home-screen app → `index.html` at the site root.
- `make_friends.py`: builds the empty-library friends version → `lifts/index.html`.
- `exdb.txt`: built-in exercise database (name|body|helpers|flags|aliases; flags p=per hand, b=bodyweight, i=isolation, y=power, c=carry).

Build: `python build.py && python make_pwa.py && python make_friends.py`, then copy `pwa/*` to the root and `pwa_friends/*` to `lifts/`.

Before changing anything, pull the latest commit: other chats may have edited the app since. The built `index.html` must stay byte-identical to a fresh build of this folder.
