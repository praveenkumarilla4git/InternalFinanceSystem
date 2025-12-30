import subprocess
import re
import os

def update_readme():
    print("🔄 Fetching Load Balancer URL from Terraform...")

    # 1. Get the URL
    try:
        os.chdir("Ops-Infra")
        result = subprocess.run(["terraform", "output", "-raw", "alb_dns_name"], 
                                capture_output=True, text=True, shell=True)
        alb_url = result.stdout.strip()
        os.chdir("..")
    except Exception as e:
        print(f"❌ Error running Terraform: {e}")
        return

    # 2. Validation
    if not alb_url or "http" not in alb_url:
        print(f"❌ Error: Invalid URL found: '{alb_url}'")
        return

    print(f"✅ Found New URL: {alb_url}")

    # 3. Update README.md (Now handling the **stars**)
    readme_path = "README.md"
    try:
        with open(readme_path, "r") as f:
            content = f.read()
        
        # FIX: We now look for the stars "**" in the pattern
        # This matches "**Current Live URL:** [Waiting...]"
        pattern = r"\*\*Current Live URL:\*\* .*"
        replacement = f"**Current Live URL:** {alb_url}"
        
        # Check if we actually find it before replacing
        if not re.search(pattern, content):
            print("❌ Error: Could not find the 'Current Live URL' line in README.md.")
            print("   -> Make sure your README has a line starting with: **Current Live URL:**")
            return

        new_content = re.sub(pattern, replacement, content)

        with open(readme_path, "w") as f:
            f.write(new_content)
            
        print("✅ Success! README.md updated locally.")
        print("   -> Now check the file in VS Code!")

    except FileNotFoundError:
        print("❌ Error: Could not find README.md file.")

if __name__ == "__main__":
    update_readme()