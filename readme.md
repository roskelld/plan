# .plan Log Automation

A lightweight system to maintain a `.plan`-style log of daily thoughts in a single `plan.txt` file, automatically versioned via Git, transformed into a static HTML archive, and published with an RSS feed on GitHub Pages.

## Features

* **Single Text Source**: Write entries in `plan.txt` using `+` markers.
* **Git Auto-Commit**: Watchman + PowerShell auto-commits changes to `plan.txt`.
* **JSON Data**: `generate_plan_json.py` extracts commits into `plan_log.json`.
* **Static HTML**: `generate_plan_html.py` builds a styled `index.html` with:

  * Table of Contents by year/month/day
  * Anchored sections and individual entry links
  * Tag (`#tag`) and inline code (`` `code` ``) styling
  * Newest-first ordering per day
* **RSS Feed**: `generate_plan_rss.py` produces `feed.xml` for subscribers.
* **GitHub Pages Ready**: Pushes all outputs to `main` for instant publishing.

## Prerequisites

* Windows (PowerShell)
* [Watchman](https://facebook.github.io/watchman/) installed and in PATH
* Python 3.x
* Git

## Repository Layout

```
plan/
├── plan.txt                # Your live .plan file
├── generate_plan_json.py   # Extracts entries to JSON
├── generate_plan_html.py   # Builds index.html from JSON
├── generate_plan_rss.py    # Builds feed.xml for RSS
├── git_push_plan.ps1       # PowerShell push script
├── styles.css              # CSS for index.html
├── color_expanded.css      # Optional extra styles
├── .nojekyll               # Disable Jekyll on GitHub Pages
└── index.html, plan_log.json, feed.xml   # Generated outputs
```

## Installation & Setup

1. **Clone the repository**:

   ```powershell
   git clone https://github.com/roskelld/plan.git
   cd plan
   ```

2. **Install Watchman** and ensure `watchman.exe` is in your PATH.

3. **Place `plan.txt`** in the repo root. Start each entry with `+`:

   ```text
   + A new thought without timestamp
   More lines...
   #tag1 #tag2
   ```
3. **Customize script**:

   Edit `git_push_plan.ps1` and replace the working directory with your install location on line 8.
   
4. **Configure Watchman trigger**:

   ```powershell
   watchman watch C:/path/to/plan
   watchman -- trigger C:/path/to/plan plan-trigger plan.txt -- powershell.exe -ExecutionPolicy Bypass -File "$(pwd)\git_push_plan.ps1"
   ```

5. **Ensure PowerShell script is executable**. You may need to set ExecutionPolicy:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope CurrentUser
   ```
6. **[OPTIONAL] Add BurntToast notification module**
   Follow instructions in their github repro: [BuntToast Github](https://github.com/Windos/BurntToast)

## Usage

* **Write**: Open `plan.txt` in your editor, add `+` entries, then save.
* **Auto-commit & Build**: Watchman detects the save and runs `git_push_plan.ps1`:

  1. Commits `plan.txt` changes.
  2. Runs JSON, HTML, and RSS generators.
  3. Commits and pushes `plan_log.json`, `index.html`, and `feed.xml`.
* **View**:

  * Browse your archive at `https://yourname.github.io/plan/`.
  * Subscribe via RSS at `https://yourname.github.io/plan/feed.xml`.

## Customization

* **CSS**: Edit `styles.css` (and `color_expanded.css`) to tweak appearance.
* **Templates**: Modify HTML structure in `generate_plan_html.py` if needed.
* **Trigger**: Adjust the Watchman or Task Scheduler as per your environment.

## Contributing

Feel free to file issues or submit PRs for enhancements, such as:

* Theme support
* Markdown entry parsing
* Alternative date groupings

## Thanks

* NeverCease for [uchu](https://github.com/NeverCease/uchu) color palette css 
* [DEJAVU SANS MONO FONT](https://www.fontsquirrel.com/license/dejavu-sans-mono)
* [BurntToast](https://github.com/Windos/BurntToast) for the notification module.

## License

This project is released under the [GPL-3.0 license](LICENSE).
