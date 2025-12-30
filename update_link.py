import subprocess
import re
import os

def update_readme():
    print("🔄 Fetching Load Balancer URL from Terraform...")

    # 1. Enter Ops-Infra, get the URL, and come back
    try:
        os.chdir("Ops-Infra")
        # Run terraform output command to get the raw URL
        result = subprocess.run(["terraform", "output", "-raw", "alb_dns_name"], 
                                capture_output=True, text=True, shell=True)
        alb_url = result.stdout.strip()
        os.chdir("..") # Go back to main folder
    except Exception as e:
        print(f"❌ Error running Terraform: {e}")
        return

    # 2. Validation
    if not alb_url or "http" not in alb_url:
        print("❌ Error: No valid URL found. Did 'terraform apply' finish successfully?")
        print(f"Debug Output: {alb_url}")
        return

    print(f"✅ Found New URL: {alb_url}")

    # 3. Read and Update README.md
    readme_path = "README.md"
    try:
        with open(readme_path, "r") as f:
            content = f.read()
        
        # Regex magic: Finds "Current Live URL:" and replaces the rest of the line
        new_content = re.sub(r"Current Live URL: .*", f"Current Live URL: {alb_url}", content)

        with open(readme_path, "w") as f:
            f.write(new_content)
            
        print("✅ Success! README.md updated.")
    except FileNotFoundError:
        print("❌ Error: Could not find README.md file.")

if __name__ == "__main__":
    update_readme()