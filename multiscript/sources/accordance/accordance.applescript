
on get_bible_text(module_id, bible_ref, use_citation_format)
	tell application "Accordance"
		return «event AccdTxRf» {module_id, bible_ref, use_citation_format}
	end tell
end get_bible_text
