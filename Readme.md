# How to build
Requirements:
- uv - this now uses uv as the python package manager.
- npm - to get the package
- git - to clone this

first clone this repo.

to update pintora get the latest source from:
- https://www.npmjs.com/package/@pintora/target-wintercg

I use the command like the following to download the package
```
npm pack @pintora/target-wintercg@0.1.4
```

get the "runtime.esm.js"
and replace it with the copy in the git repo.

then run
```
uv run build.py
```

This will place an updated copy of pintora.js in the package.