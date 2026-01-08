---
type: Skill
name: Telegram Mini App Frontend
source: "@fitnessapp/SCROLL_RELIABILITY_GUIDE.md"
description: Critical rules for scrolling and layout in Telegram WebViews.
---

# SKILL: TELEGRAM MINI APP FRONTEND

You are an expert in building React Native Web apps specifically for Telegram Mini Apps (TMA).
You know that TMAs run in a unique WebView environment where standard web scrolling often breaks.

## 🚨 THE SCROLL RELIABILITY PROTOCOL (V3.0)

**1. The "Holy Grail" Layout (Absolute Positioning)**
NEVER rely on `flex: 1` + `height: 100%` for the main scroll container on Web. It often causes the container to grow infinitely, breaking `overflow: scroll`.

**Correct Pattern:**
Use absolute positioning to force the scrollview to stick to the viewport.

```tsx
// Inside your screen component
{Platform.OS === 'web' ? (
  <div style={{
    position: 'absolute',  // CRITICAL
    top: 50,               // Header Height
    bottom: 0,             // Anchor to bottom
    left: 0,
    right: 0,
    overflowY: 'scroll',   // Enable scroll
    WebkitOverflowScrolling: 'touch',
    display: 'flex',
    flexDirection: 'column'
  }}>
    <div style={{ flexGrow: 1, paddingBottom: 150 }}>
       {/* YOUR CONTENT HERE */}
    </div>
  </div>
) : (
  <ScrollView style={{ flex: 1 }}>...</ScrollView>
)}
```

**2. Safe Offsets**
*   ALWAYS add `paddingBottom: 150` to the last scrollable container.
*   This ensures content isn't covered by the Telegram Main Button or floaters.

**3. Root Constraints**
*   Assume `body` and `#root` have `overflow: hidden` and `height: 100%`.
*   Never try to scroll the `<body>`. Always scroll an inner container.
