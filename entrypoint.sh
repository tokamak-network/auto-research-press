#!/bin/sh
# Railway persistent volume setup
# Mount a single volume at /app/persistent, then symlink data directories into it.
# This ensures SQLite DB, results, and published articles survive redeployments.

if [ -d "/app/persistent" ]; then
  mkdir -p /app/persistent/data
  mkdir -p /app/persistent/results
  mkdir -p /app/persistent/results/submissions
  mkdir -p /app/persistent/web-data
  mkdir -p /app/persistent/web-articles

  # Remove empty dirs created during build, replace with symlinks
  rm -rf /app/data /app/results /app/web/data /app/web/articles
  ln -sf /app/persistent/data /app/data
  ln -sf /app/persistent/results /app/results
  ln -sf /app/persistent/web-data /app/web/data
  ln -sf /app/persistent/web-articles /app/web/articles
fi

exec "$@"
