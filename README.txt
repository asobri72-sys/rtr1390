README - Ready-to-build package for DTF Print Manager (Creates .exe and installer via GitHub Actions)
==============================================================================================

Goal:
- Provide a one-click GitHub Actions pipeline that builds a single-file Windows executable (PyInstaller)
  and then creates an installer (Inno Setup). After the workflow runs, you can download the built .exe or installer
  from the Actions artifacts — no local build required beyond creating the GitHub repository and triggering the workflow.

What I packaged here:
- dtf_printer_manager.py        -> Application source
- requirements.txt              -> Python deps
- build_exe.bat                 -> Local build helper (optional)
- installer.iss                 -> Inno Setup script
- .github/workflows/windows-build.yml -> GitHub Actions workflow
- README.txt                    -> This file

How to get a ready-made .exe/installer (easy steps):
1) Create a new GitHub repository (public or private) under your GitHub account.
2) Upload all files from this package into the repository root (keep the .github/workflows folder).
3) Commit to branch `main`.
4) Go to the "Actions" tab in GitHub for your repository; you'll see the "Build DTF Print Manager (Windows)" workflow.
5) Click "Run workflow" (or push a commit to `main`) to start the build.
6) Wait a few minutes for the workflow to complete. When finished, open the workflow run and download artifacts:
   - `dtf-exe` (contains the .exe)
   - `dtf-installer` (contains the Inno Setup compiled installer)

Notes:
- GitHub Actions runs on Microsoft-hosted Windows runners and will compile the exe and build an installer for you.
- If the Inno Setup compilation step fails, you can still download the standalone .exe from the `dtf-exe` artifact.
- After downloading the exe/installer, transfer to your Windows machine and run the installer to install the app.

Security & permissions:
- The built installer may require admin privileges to add printer ports (install.ps1 approach). Run installer as Administrator if needed.

If you want, I can:
- Create the repository structure and zip it for you to upload directly to GitHub (I can produce the ZIP here).
- Or, if you prefer, I can provide exact copy-paste commands to run locally (PowerShell + Git commands).

I will now produce the ZIP of the repo-ready package for you to upload to GitHub.