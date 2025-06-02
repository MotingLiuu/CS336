SCRIPT_PATH="scripts/scalene1.py"
REPORT_PATH="profile.html"

if [ "$1" ]; then
    SCRIPT_PATH="$1"
fi
if [ "$2" ]; then
    REPORT_PATH="$2"s
fi

echo "📊 Profiling $SCRIPT_PATH..."
PYTHONPATH=. scalene --html --profile-all --reduced-profile --outfile "$REPORT_PATH" "$SCRIPT_PATH"
echo "✅ Done. Report saved to $REPORT_PATH"
