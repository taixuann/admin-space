#!/bin/bash
set -euo pipefail
# 2. Check if there are newly added PDFs in ~/knowledge-base since last index
LAST_INDEX_FILE="/Users/tai/.pqa/indexes/pqa_index_6b48380262929bb17cfa7a938ed5d6ed/files.zip"
if [ -f "$LAST_INDEX_FILE" ]; then
    NEW_PDFS=$(find "/Users/tai/knowledge-base" -type f -name "*.pdf" -newer "$LAST_INDEX_FILE" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$NEW_PDFS" -gt 0 ]; then
        echo "📚 Found $NEW_PDFS new PDF(s) in ~/knowledge-base. Triggering pqa-kb index sync..."
        /Users/tai/.local/bin/pqa-kb index || echo "⚠️ pqa-kb index warning, will retry on next run."
    else
        echo "📚 All PDFs in knowledge-base are up to date with index."
    fi
fi

