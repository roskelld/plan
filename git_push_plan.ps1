# ───────────────────────────────────────────────────────────────────
#  Script: update‐and‐push.ps1
#  Purpose: commit & push plan files, rebuild site, then notify.
#  Note: Requires BurntToast module if you want to do toast notifications.
# ───────────────────────────────────────────────────────────────────

# Navigate to repo
cd "D:\_Dev\git\plan"

# Only commit if plan.txt changed
git diff --quiet plan.txt
if ($LASTEXITCODE -ne 0) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git add plan.txt
    git commit -m "Update plan $timestamp"
}

# Generate JSON and HTML
python generate_plan_json.py
python generate_plan_html.py
python generate_plan_rss.py

# Stage and commit generated files
git add plan_log.json index.html feed.xml
$timestamp2 = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "Rebuild site $timestamp2"

# Push to remote
git push origin main
$pushExit = $LASTEXITCODE

# Try to import BurntToast (if installed)
Import-Module BurntToast -ErrorAction SilentlyContinue

# On success/failure, fire a toast (if possible) AND play a sound
if ($pushExit -eq 0) {
    # → SUCCESS
    if (Get-Module -ListAvailable -Name BurntToast) {
        New-BurntToastNotification `
            -Text ".Plan → Git push succeeded", "Update now live!" `
            -Sound Default
    }
	else
	{
		# Play windows “success” ding
		[System.Media.SystemSounds]::Asterisk.Play()		
	}

} else {
    # → FAILURE
    if (Get-Module -ListAvailable -Name BurntToast) {
        New-BurntToastNotification `
            -Text ".Plan → Git push failed", "Check git output for errors." `
            -Sound Alarm
    }
	else 
	{
		# Play windows “failure” ding
		[System.Media.SystemSounds]::Hand.Play()
	}

}
