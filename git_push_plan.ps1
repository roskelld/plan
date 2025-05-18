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

git push origin main