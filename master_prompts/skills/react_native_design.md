---
type: Skill
name: React Native Design System
source: "@fitnessapp/DESIGN_SYSTEM.md"
description: Enforcement of Theme Tokens and Core Components.
---

# SKILL: REACT NATIVE DESIGN SYSTEM

You strictly adhere to the project's Design System.
**⛔ PROHIBITED:** Hardcoding colors (`#F3F4F6`), font sizes (`fontSize: 24`), or spacings (`padding: 16`).
**✅ REQUIRED:** Importing tokens from `@src/theme`.

## 🎨 Theme Tokens

**Imports:**
```typescript
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '@src/theme';
```

**Mappings:**
*   **Colors:** `Colors.background.primary`, `Colors.text.primary`, `Colors.primary.main` (#3B82F6).
*   **Typography:** `Typography.heading1` (26px), `Typography.body` (20px - KEY for readability).
*   **Spacing:** `Spacing.lg` (18px), `Spacing.md` (12px).
*   **Borders:** `BorderRadius.lg` (14px).

## 🧱 Core Components

Don't build primitives from scratch. Use these:

1.  **Button:** `<Button title="Save" variant="primary" onPress={...} />`
    *   Variants: `primary`, `success`, `danger`, `outline`, `secondary`.
2.  **Card:** `<Card variant="elevated">...</Card>`
3.  **Input:** `<Input label="Weight" error={...} />`
4.  **Badge:** `<Badge label="Pending" variant="warning" />`
