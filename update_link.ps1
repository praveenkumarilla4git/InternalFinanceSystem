# 1. Get the URL from Terraform (Running inside the subfolder)
Write-Host "Fetching Load Balancer URL..."
cd Ops-Infra
$alb_url = terraform output -raw alb_dns_name
cd ..

# 2. Check if we got a URL
if ([string]::IsNullOrWhiteSpace($alb_url)) {
    Write-Host "Error: No URL found. Did you run 'terraform apply'?" -ForegroundColor Red
    exit
}

# 3. Read the Readme file
$readme_path = "README.md"
$content = Get-Content $readme_path -Raw

# 4. Replace the old link with the new one using Regex
# This looks for "Current Live URL:" and replaces everything after it
$new_content = $content -replace "Current Live URL: .*", "Current Live URL: $alb_url"

# 5. Save the file
Set-Content $readme_path $new_content
Write-Host "✅ Success! Updated README with: $alb_url" -ForegroundColor Green