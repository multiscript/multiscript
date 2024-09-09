
on get_text_via_api(module_id, bible_ref, use_citation_format)
	tell application "Accordance"
		return «event AccdTxRf» {module_id, bible_ref, use_citation_format}
	end tell
end get_text_via_api

on get_text_via_accessibility(module_name, bible_ref)
	tell application "Accordance"
		activate
	end tell
	tell application "System Events" to tell process "Accordance"
		key code 0 using {option down, command down} -- letter A key + option + command
		delay 0.25
		tell window "Get Verses"
			tell pop up button 1
				click
				tell menu 1
					pick menu item module_name
				end tell
			end tell
			tell text field 1
				keystroke bible_ref
			end tell
			click button "Copy to Clipboard"
		end tell
		set visible of it to false
	end tell
	return the clipboard as Unicode text
end get_text_via_accessibility

on get_module_ui_names()
	tell application "Accordance"
		activate
	end tell
	tell application "System Events" to tell process "Accordance"
		key code 0 using {option down, command down} -- letter A key
		delay 0.25
		tell window "Get Verses"
			tell pop up button 1
				click
				tell menu 1
					set menu_titles to title of every menu item
				end tell
				key code 53
			end tell
			tell (first button whose subrole is "AXCloseButton") to click
		end tell
		set visible of it to false
	end tell
	set module_ui_names to {}
	repeat with menu_title in menu_titles
		if length of menu_title is greater than 0 then
			set end of module_ui_names to menu_title as Unicode text
		end if
	end repeat
	return module_ui_names
end get_module_ui_names
