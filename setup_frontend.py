import os

BASE = "ai_finance_simulator/frontend"

FOLDERS = [
    "public",
    "src",
    "src/api",
    "src/components",
]

FILES = [
    "public/index.html",
    "src/App.jsx",
    "src/index.js",
    "src/index.css",
    "src/api/apiClient.js",
    "src/components/ProfileSetup.jsx",
    "src/components/ModeToggle.jsx",
    "src/components/DecisionTree.jsx",
    "src/components/ChartContainer.jsx",
    "src/components/ScenarioCards.jsx",
    "src/components/ReverseCards.jsx",
    "src/components/StoryDisplay.jsx",
    ".env",
    "tailwind.config.js",
    "package.json",
]


def create_frontend():
    print("\n📁 Creating frontend structure...\n")

    for folder in FOLDERS:
        full_path = os.path.join(BASE, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"  📂 {full_path}/")

    print()

    for file in FILES:
        full_path = os.path.join(BASE, file)
        with open(full_path, "w") as f:
            pass
        print(f"  📄 {full_path}")

    print(f"\n✅ Done! Created {len(FILES)} files across {len(FOLDERS)} folders.")
    print("\n📂 Final structure:")
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d != "node_modules" and not d.startswith(".")]
        depth = root.replace(BASE, "").count(os.sep)
        indent = "    " * depth
        print(f"{indent}📂 {os.path.basename(root)}/")
        for file in files:
            print(f"{indent}    📄 {file}")


if __name__ == "__main__":
    create_frontend()