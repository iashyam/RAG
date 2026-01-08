#!/usr/bin/env python3
import os
import curses
import sys
from pathlib import Path

def get_files(root_dir="."):
    """Recursively list all files, ignoring hidden ones and common build dirs."""
    file_list = []
    skip_dirs = {'.git', '.venv', '__pycache__', 'node_modules', '.DS_Store', 'cache'}
    
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file in skip_dirs or file.endswith('.pyc'):
                continue
            # Store relative path
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            file_list.append(rel_path)
    return file_list

def fuzzy_score(query, text):
    """
    Simple fuzzy score: 
    - Case insensitive
    - Characters must appear in order
    - Higher score for better match
    Returns score (higher is better), or -1 if no match.
    """
    if not query:
        return 1
    
    query = query.lower()
    text = text.lower()
    
    if query not in text and not all(c in text for c in query):
         # If strict substring fails, try subsequence
         pass

    # Simple subsequence check
    t_idx = 0
    q_idx = 0
    score = 0
    consecutive = 0
    first_match_idx = -1
    
    while t_idx < len(text) and q_idx < len(query):
        if text[t_idx] == query[q_idx]:
            if first_match_idx == -1:
                first_match_idx = t_idx
            
            score += 10
            score += consecutive * 5 # Bonus for consecutive
            consecutive += 1
            q_idx += 1
        else:
            consecutive = 0
        t_idx += 1
        
    if q_idx == len(query):
        # Match found
        # Penalize for length of text to prefer shorter matches
        score -= len(text) * 0.1
        # Bonus for match at start
        if first_match_idx == 0:
            score += 20
        return score
    
    return -1

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # Highlight
    
    files = get_files()
    if not files:
        return None
        
    current_selection = 0
    query = ""
    filtered_files = files
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw search box
        stdscr.addstr(0, 0, f"Search: {query}", curses.color_pair(1))
        
        # Draw files
        max_display = height - 2
        
        # Ensure selection is within bounds
        if not filtered_files:
            current_selection = 0
        elif current_selection >= len(filtered_files):
            current_selection = len(filtered_files) - 1
        elif current_selection < 0:
            current_selection = 0

        # Scroll window
        start_idx = 0
        if current_selection >= max_display:
            start_idx = current_selection - max_display + 1

        for i in range(min(len(filtered_files), max_display)):
            file_idx = start_idx + i
            if file_idx >= len(filtered_files):
                break
                
            file_name = filtered_files[file_idx]
            
            # Truncate if too long
            if len(file_name) > width - 2:
                file_name = file_name[:width-5] + "..."
                
            if file_idx == current_selection:
                stdscr.addstr(i + 1, 0, f"> {file_name}", curses.color_pair(2))
            else:
                stdscr.addstr(i + 1, 0, f"  {file_name}", curses.color_pair(1))
        
        stdscr.refresh()
        
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            return None

        if key == curses.KEY_UP:
            if current_selection > 0:
                current_selection -= 1
        elif key == curses.KEY_DOWN:
            if current_selection < len(filtered_files) - 1:
                current_selection += 1
        elif key == curses.KEY_DC or key == 127 or key == curses.KEY_BACKSPACE: # DEL/Backspace
            if len(query) > 0:
                query = query[:-1]
                # Re-filter
                if not query:
                    filtered_files = files
                else:
                    scored = [(f, fuzzy_score(query, f)) for f in files]
                    scored = [x for x in scored if x[1] > -1]
                    scored.sort(key=lambda x: x[1], reverse=True)
                    filtered_files = [x[0] for x in scored]
                current_selection = 0
        elif key == 10 or key == 13: # Enter
            if filtered_files:
                return filtered_files[current_selection]
            return None
        elif key == 27: # ESC
             return None
        elif 32 <= key <= 126: # Printable char
            query += chr(key)
            # Re-filter
            scored = [(f, fuzzy_score(query, f)) for f in files]
            scored = [x for x in scored if x[1] > -1]
            scored.sort(key=lambda x: x[1], reverse=True)
            filtered_files = [x[0] for x in scored]
            current_selection = 0

if __name__ == "__main__":
    try:
        selected_file = curses.wrapper(main)
        if selected_file:
            # Try to open with EDITOR, fallback to open command (mac) or print
            editor = os.environ.get("EDITOR", "vi") # Default to vi as code is missing
            # If on mac, 'open' works for default app
            # But user wants to open in project editor.
            # We'll print instructions or try 'code' if path fixed?
            # Since 'code' failed, we stick to editor env var or vi.
            
            # Assuming mac
            # Check if we should try to use 'open' (default macOS opener)
            # but that might open Xcode or TextEdit.
            # Best is to let the shell open it or use python to spawn.
            
            os.system(f"{editor} {selected_file}")
    except KeyboardInterrupt:
        pass
