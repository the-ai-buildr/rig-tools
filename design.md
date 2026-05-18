## **Rig-Apps Design Document**
This document outlines the foundational design principles, visual and UI guidelines, and tool specifications for developing the Rig-Apps platform.

---

### **1. Design Principles**

1. **Clarity and Simplicity**
   - Interfaces must be clean and intuitive for users who may not be highly technical.
   - Prioritize functionality and remove unnecessary visual clutter.

2. **Mobile-First Responsive Design**
   - Design the layout with mobile-first principles, ensuring seamless functionality on phones and tablets.
   - Use flexible grid layouts and components to scale gracefully across device sizes.

3. **Consistency**
   - Utilize a component-based design to maintain theme and style consistency across all pages and views (e.g., shadcn for design system).

4. **Dark/Light Mode Support**
   - Implement shadcn's built-in light/dark mode toggle for user preferences.
   - Ensure that key visuals, such as schematics and dashboard elements, are colorblind-friendly.

5. **Accessibility**
   - Adhere to WCAG 2.1 accessibility guidelines.
   - Support keyboard navigation and readable color contrasts.

---

### **2. Visual and UI Guidelines**

1. **Color Palette**
   - **Light Theme:**
     - Primary: `#004aad` (blue)
     - Accent: `#00aaff` (light blue)
     - Background: `#f9f9f9` (white-gray)
     - Text: `#000000` (black)
   - **Dark Theme:**
     - Primary: `#00aaff` (light blue)
     - Accent: `#66d9ea` (aqua)
     - Background: `#1e1e2e` (dark gray)
     - Text: `#ffffff` (white)

2. **Typography**
   - Font: `Inter` (modern and readable sans-serif font).
   - Sizes:
     - Heading 1 (H1): 32px bold.
     - Heading 2 (H2): 24px bold.
     - Body Text: 16px regular.
     - UI Labels: 14px regular.

3. **Layout Principles**
   - **Header:** Full-width header for branding and tools navigation.
   - **Sidebar7 Dashboard:**
     - Sidebar should include menu links for quick access to:
       - Projects (Wells)
       - Tasks
       - Messages (Chat)
       - Settings
     - Collapsible for mobile screens.
   - **Landing Page:**
     - Large full-height hero section with app overview text.
     - Call-to-action (e.g., “Create Your First Rig Project” button).
   - **Dashboard Pages:**
     - Split layout with:
       - **Main Content Area:** Well plans, schematics, or tasks.
       - **Right Sidebar:** Chat messages and notifications.

4. **Animations**
   - Subtle animations for transitions (e.g., toggling light/dark mode or collapsing menus).
   - Use CSS transitions to minimize performance impact.

5. **File Management Access**
   - Provide quick access to relevant files with a standardized UI element (e.g., a **Documents** or **Files** tab in the dashboard).

---

### **3. UI Wireframes**

#### **Landing Page**
- **Hero Section:**
  - Full-height welcome message with branding, app logo, and a call-to-action button.
  - "How It Works" text section beneath the hero.

#### **Dashboard**
- **Header:** Branding + light/dark theme toggle + user profile/dropdown.
- **Left Sidebar (Sidebar7):**
  - Links to:
    - Projects (with project list dropdown/collapsible).
    - Task Management.
    - Notifications.
    - Settings.
- **Main View:** Well plan schematic visualizer or task management UI.
- **Right Sidebar:**
  - Team chat with real-time updates.
  - Notifications (alerts for plan and task updates).

---

### **4. Technical Stack**

#### **Frontend**
- **Framework:** React.js (with TypeScript).
- **UI Library:** shadcn (TailwindCSS-based design system).
- **Styling:** TailwindCSS with a mobile-first design approach.
- **State Management:** Zustand or Redux for real-time and global state sync.
- **Routing:** React Router or Next.js (depending on navigation complexity).
- **Accessibility:** Utilize shadcn's accessibility-supported components.

#### **Backend**
- **Backend Framework:** Appwrite
  - **Database Service:** Define Appwrite collections for users, projects, tasks, etc.
  - **Authentication:** Use Appwrite for user roles and identity management.
  - **Functions:** Use serverless functions for task status updates and notifications.
  - **File Storage:** Store relevant documents linked to projects.

#### **Dev Tools**
- **Version Control:** Git (hosted with GitHub).
- **Containerization:** Docker (for backend setup with Appwrite).
- **Testing Frameworks:**
  - Unit Tests: Jest and React Testing Library.
  - Integration Tests: Mock Appwrite services with msw.js for end-to-end testing.
- **CI/CD Pipeline:** GitHub Actions for builds and tests.

---

### **5. Light/Dark Theme Implementation Plan**

1. **shadcn Theme Setup**
   - Use shadcn’s theme builder to set up a toggler between light and dark modes.
   - Test state persistence with browser localStorage or context API for theme synchronization.

2. **Dynamic Theme Transition**
   - Ensure smooth color transitions for the app (e.g., `transition-colors` with Tailwind).
   - Test components for proper contrast across themes.

3. **Theme-Specific Assets**
   - Customize images or visuals (if any) to suit light and dark modes.

---

### **6. Mobile Responsiveness Plan**

1. **Breakpoints**
   - Define responsive breakpoints: 
     - Small: `<640px` (mobile).
     - Medium: `641-1024px` (tablets).
     - Large: `>1024px` (desktop).
   - Layouts adjust at each point, utilizing TailwindCSS utilities (e.g., `md:grid`).

2. **Priority Adjustments for Mobile Use**
   - Collapse Sidebar7 navigation into a menu icon.
   - Simplify landing page content (e.g., hide non-essential text).
   - Optimize touch targets (e.g., larger buttons on mobile).

3. **Testing**
   - Test across devices:
     - iPhone/Android for mobile responsiveness.
     - Tablets for medium layouts.

---

### **7. File Management and Documentation**

1. **File Uploads**
   - Implement file upload and management via Appwrite's File Storage service.
   - Use input fields for tagging files (e.g., "reports," "standards").

2. **Processes and Standards Docs**
   - Include quick access or search for company standards and procedures within the Dashboard Sidebar.

---

### **Next Steps**
- Implement and test wireframes with Figma (or your preferred tool).
- Procure feedback from drilling engineers and advisors for the overall design.
- Iterate on this document as needed while finalizing UAT scenarios.

---

### **END OF DESIGN DOCUMENT**
