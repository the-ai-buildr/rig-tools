# Repository Setup Notes (`rig-apps`)

These notes are kept here as reference for how the `rig-apps` repository was created and initialized.

#### **1. Create the Repository**
1. Go to [GitHub](https://github.com/) and log in to your account.
2. Click the **+ (plus)** icon at the top-right corner and select **“New repository”**.
3. Use the following details:
   - **Repository name:** `rig-apps`
   - **Description:** Dashboard-style Plotly Dash + FastAPI app for drilling engineers and advisors with collaboration, task tracking, and planning tools.
   - **Repository visibility:** Private (you can make it public later).
   - Check **“Add a README file”** (this creates the initial README which we will replace).
   - Add a `.gitignore` file with templates for **Python**.
   - Choose a license (e.g., MIT, or skip this for now).

4. Click **Create repository**.

---

#### **2. Clone the Repository to Your Local Machine**
1. Open your terminal and run:
   ```bash
   git clone https://github.com/<your-github-username>/rig-apps.git
   cd rig-apps
   ```

---

#### **3. Add `repo.md` to the Repository**
1. Create the `repo.md` file:
   ```bash
   touch repo.md
   ```
2. Open it in your code editor:
   ```bash
   code repo.md
   ```
3. Paste the provided `repo.md` content.

4. Save the file and commit the change:
   ```bash
   git add repo.md
   git commit -m "Add repo.md with repository organization and setup guide"
   git push origin main
   ```

---

#### **4. Verify the Repository**
1. Navigate to the GitHub repository in your browser.
2. Ensure that the `repo.md` file is visible in the root.
