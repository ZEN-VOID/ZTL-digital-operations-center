# Artifacts Builder - Technical Reference

## Architecture Overview

The artifacts-builder skill follows the **three-layer architecture** defined in global CLAUDE.md:

### Layer 1: Knowledge Layer (SKILL.md)
- Development guidelines
- Design principles (avoid "AI slop")
- Tech stack documentation

### Layer 2: Plan/Configuration Layer (JSON specs)
```json
{
  "project_name": "餐饮网站原型",
  "agent_name": "X4-平面设计师",
  "artifact_name": "hotpot-menu-app",
  "description": "交互式火锅菜单应用",
  "components": ["button", "card", "dialog", "tabs"],
  "routing": false,
  "state_management": "useState",
  "timestamp": "20251029_103000"
}
```

### Layer 3: Execution Layer
- **Shell scripts**: `init-artifact.sh`, `bundle-artifact.sh`
- **Python orchestration**: `artifact_builder.py`
- **Build tools**: Vite, Parcel, npm

---

## Output Path Convention

Following the global standard defined in `~/.claude/CLAUDE.md`:

```
output/[项目名]/X4-平面设计师/artifacts-builder/[artifact-name]/
├── plans/       # JSON execution specifications
├── results/     # Final bundle.html files
├── logs/        # Build logs (init, bundle)
├── metadata/    # Traceability metadata
└── workspace/   # React development files
    └── [artifact-name]/
        ├── src/
        │   ├── App.tsx
        │   ├── main.tsx
        │   └── components/ui/  # 40+ shadcn/ui components
        ├── public/
        ├── index.html
        ├── package.json
        ├── tsconfig.json
        ├── tailwind.config.js
        └── vite.config.ts
```

---

## API Reference

### ArtifactBuilder Class

```python
from scripts.artifact_builder import ArtifactBuilder

builder = ArtifactBuilder(
    project_name="餐饮网站原型",
    agent_name="X4-平面设计师",
    workspace_dir=None  # Optional custom workspace
)
```

#### Methods

##### `create_artifact()`

Initialize a new React artifact project.

```python
result = builder.create_artifact(
    artifact_name="hotpot-menu-app",  # kebab-case
    description="交互式火锅菜单应用",
    components=["button", "card", "tabs"],  # shadcn/ui components
    routing=False,  # Enable React Router
    state_management="useState"  # useState | zustand | redux
)
```

**Returns**:
```python
{
    "status": "initialized",
    "message": "...",
    "workspace": Path("output/.../workspace/hotpot-menu-app"),
    "spec_file": Path("output/.../...json"),
    "metadata_file": Path("output/.../...json"),
    "phase": "development_ready"
}
```

##### `bundle_artifact()`

Bundle the developed artifact into a single HTML file.

```python
bundle_result = builder.bundle_artifact(
    artifact_name="hotpot-menu-app",
    workspace=None  # Auto-detect if None
)
```

**Returns**:
```python
{
    "status": "success",
    "message": "✅ Artifact bundled: ...",
    "bundle_file": Path("output/.../hotpot-menu-app_20251029_103000.html"),
    "workspace": Path("output/.../workspace/hotpot-menu-app"),
    "phase": "completed"
}
```

---

## Shell Scripts Reference

### init-artifact.sh

**Purpose**: Initialize a React + TypeScript + Vite project with shadcn/ui.

**Usage**:
```bash
bash scripts/init-artifact.sh <project-name>
```

**What it does**:
1. Creates Vite React TypeScript project
2. Installs Tailwind CSS 3.4.1
3. Configures path aliases (`@/`)
4. Extracts 40+ shadcn/ui components from `shadcn-components.tar.gz`
5. Installs all dependencies (including Radix UI primitives)
6. Auto-detects Node version and pins Vite if needed

**Output**: Fully configured React project in `<project-name>/`

### bundle-artifact.sh

**Purpose**: Bundle React app into a single HTML file.

**Usage**:
```bash
cd <project-name>
bash scripts/bundle-artifact.sh
```

**What it does**:
1. Installs bundling dependencies (parcel, html-inline)
2. Creates `.parcelrc` config
3. Builds with Parcel (no source maps)
4. Inlines all assets into `bundle.html`

**Requirements**:
- Project must have `index.html` in root
- All imports must be valid

**Output**: `bundle.html` (single-file artifact)

---

## shadcn/ui Components

### Pre-installed Components (40+)

**Form Controls** (11):
- button, checkbox, radio-group, select, switch
- slider, input, textarea, label, form, input-otp

**Data Display** (10):
- card, table, badge, avatar, separator
- progress, skeleton, data-table, chart, calendar

**Feedback** (7):
- alert, alert-dialog, dialog, toast
- tooltip, popover, hover-card

**Navigation** (8):
- tabs, dropdown-menu, menubar, navigation-menu
- breadcrumb, pagination, context-menu, command

**Layout** (8):
- accordion, collapsible, resizable, scroll-area
- sheet, sidebar, carousel, drawer

**Advanced** (4):
- date-picker, sonner (toast system), command palette

### Component Usage

All components are TypeScript-ready and located in `src/components/ui/`:

```tsx
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Dialog, DialogTrigger, DialogContent } from '@/components/ui/dialog'

function App() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>火锅菜单</CardTitle>
      </CardHeader>
      <CardContent>
        <Dialog>
          <DialogTrigger asChild>
            <Button>查看详情</Button>
          </DialogTrigger>
          <DialogContent>
            {/* Dialog content */}
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  )
}
```

---

## State Management

### useState (Default)

Built-in React hook, suitable for most artifacts:

```tsx
const [count, setCount] = useState(0)
```

### Zustand (Optional)

For complex state:

```bash
npm install zustand
```

```tsx
import create from 'zustand'

const useStore = create((set) => ({
  cart: [],
  addItem: (item) => set((state) => ({ cart: [...state.cart, item] }))
}))
```

### Redux Toolkit (Optional)

For very complex state:

```bash
npm install @reduxjs/toolkit react-redux
```

---

## Design Anti-Patterns (Avoid "AI Slop")

### ❌ Don't Do

1. **Centered Everything**
   ```tsx
   // Bad
   <div className="flex items-center justify-center h-screen">
   ```

2. **Purple Gradients**
   ```tsx
   // Bad
   <div className="bg-gradient-to-r from-purple-500 to-pink-500">
   ```

3. **Uniform Rounded Corners**
   ```tsx
   // Bad
   <Card className="rounded-2xl">  // Everything rounded-2xl
   ```

4. **Inter Font Everywhere**
   ```css
   /* Bad */
   font-family: 'Inter', sans-serif;
   ```

### ✅ Do Instead

1. **Varied Layouts**
   ```tsx
   <div className="grid grid-cols-3 gap-4">
     <div className="col-span-2">Main content</div>
     <div>Sidebar</div>
   </div>
   ```

2. **Purposeful Colors**
   ```tsx
   // Restaurant context: warm earth tones
   <div className="bg-amber-50 border-amber-200">
   ```

3. **Mixed Geometry**
   ```tsx
   <Card className="rounded-lg">
     <Button className="rounded-full">  // Contrast
   ```

4. **Diverse Typography**
   ```css
   /* Better */
   font-family: 'Georgia', serif;  // Or custom fonts
   ```

---

## Performance Optimization

### Bundle Size

- Bundle.html typically 200-500 KB (gzipped)
- Parcel tree-shakes unused code
- Consider lazy loading for large apps

### React Performance

```tsx
// Memoize expensive computations
const expensiveValue = useMemo(() => computeExpensiveValue(data), [data])

// Memoize callbacks
const handleClick = useCallback(() => {
  // ...
}, [deps])

// Memoize components
const MemoizedComponent = React.memo(Component)
```

---

## Troubleshooting

### Node Version Issues

**Problem**: Vite fails to start

**Solution**: Script auto-detects Node version:
- Node 18+: Uses latest Vite
- Node 16: Pins to Vite 4.3.9

### Missing Components

**Problem**: `Cannot find module '@/components/ui/button'`

**Solution**: Check that `shadcn-components.tar.gz` was extracted:
```bash
ls src/components/ui/  # Should list 40+ components
```

### Bundle Script Fails

**Problem**: `bundle.html` not generated

**Solution**:
1. Ensure `index.html` exists in project root
2. Check build logs in `output/**/`
3. Verify all imports are valid:
   ```tsx
   // Good
   import { Button } from '@/components/ui/button'

   // Bad
   import { Button } from './components/ui/button'  // No path alias
   ```

### TypeScript Errors

**Problem**: Type errors during development

**Solution**:
```bash
npx tsc --noEmit  # Check types without building
```

---

## Best Practices

### 1. Component Selection

Start minimal, add as needed:

```python
# Good: Start with essentials
components=["button", "card", "input"]

# Avoid: Loading everything upfront
components=["button", "card", "input", "table", "dialog", "tabs", ...]
```

### 2. File Organization

```
src/
├── App.tsx              # Main app component
├── main.tsx             # Entry point
├── components/
│   ├── ui/              # shadcn/ui components (don't modify)
│   ├── MenuCard.tsx     # Custom components
│   └── CartDrawer.tsx
├── lib/
│   └── utils.ts         # Utility functions
└── styles/
    └── globals.css      # Global styles
```

### 3. Responsive Design

Always test mobile:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

### 4. Accessibility

Use semantic HTML and ARIA:

```tsx
<Button aria-label="添加到购物车">
  <Plus className="h-4 w-4" />
</Button>
```

---

## Advanced Usage

### Custom Themes

Modify `tailwind.config.js`:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Restaurant brand colors
        'hotpot-red': '#D32F2F',
        'hotpot-gold': '#FFC107',
      }
    }
  }
}
```

### React Router (Routing)

```python
result = builder.create_artifact(
    artifact_name="multi-page-app",
    routing=True  # Enables React Router
)
```

Then use in code:

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/menu" element={<MenuPage />} />
      </Routes>
    </BrowserRouter>
  )
}
```

### External APIs

```tsx
import { useEffect, useState } from 'react'

function MenuList() {
  const [items, setItems] = useState([])

  useEffect(() => {
    fetch('https://api.example.com/menu')
      .then(res => res.json())
      .then(setItems)
  }, [])

  return items.map(item => <MenuCard key={item.id} {...item} />)
}
```

---

## Version Control

Following global CLAUDE.md conventions:

**Track in Git**:
- ✅ `SKILL.md`, `README.md`, `reference.md`
- ✅ `scripts/*.sh`, `scripts/*.py`
- ✅ `output/**/*.json` (execution plans)

**Ignore in Git**:
- ❌ `output/**/*` (bundle.html files)
- ❌ `output/**/*` (build logs)
- ❌ `output/**/*` (runtime metadata)
- ❌ `output/**/workspace/*` (development files)

---

## Related Skills

- **canvas-design**: Static design artifacts (posters, logos)
- **algorithmic-art**: Generative art patterns
- **theme-factory-restaurant**: Restaurant theming system

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
**Maintainer**: X4-平面设计师 (via Claude Code)
