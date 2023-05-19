#!/bin/sh

PATH="$HOME/.npm-packages/bin:$PATH"

npx tsc --init
npx tsc basics.ts
