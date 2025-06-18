poetry run pyright $(git ls-files '*.py' | grep -v '^tests/') || {
  echo "Pyright failed"
  exit 1
}