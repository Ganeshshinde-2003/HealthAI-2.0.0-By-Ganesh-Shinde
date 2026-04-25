# 🎨 Nova Health Color Palettes

This file documents all available color palettes and how to switch between them.

## Available Palettes

### 1. Purple Gradient (Current) ✨
**Best for:** Premium, sophisticated, health-tech feel
- Primary: Purple gradient (#667eea → #764ba2)
- Accent: Green (#10b981)
- Vibe: Modern, trustworthy, professional

### 2. Ocean Blue 🌊
**Best for:** Calm, medical, trustworthy feel
- Primary: Sky blue → Cyan (#0ea5e9 → #06b6d4)
- Accent: Cyan (#06b6d4)
- Vibe: Clinical, calm, reliable

### 3. Sunset Orange 🌅
**Best for:** Warm, energetic, wellness feel
- Primary: Orange → Pink (#f97316 → #ec4899)
- Accent: Pink (#ec4899)
- Vibe: Energetic, friendly, approachable

### 4. Forest Green 🌲
**Best for:** Natural, healthy, organic feel
- Primary: Emerald → Lime (#059669 → #84cc16)
- Accent: Lime green (#84cc16)
- Vibe: Natural, wellness-focused, earthy

### 5. Royal Purple 👑
**Best for:** Premium, luxury, high-end feel
- Primary: Purple → Pink (#9333ea → #ec4899)
- Accent: Pink (#ec4899)
- Vibe: Luxury, premium, sophisticated

### 6. Teal Mint 💚
**Best for:** Fresh, modern, clean feel
- Primary: Teal → Cyan (#14b8a6 → #06b6d4)
- Accent: Cyan (#06b6d4)
- Vibe: Fresh, clean, modern

---

## How to Switch Palettes

### Method 1: Change Active Palette (Easy)

1. Open `src/styles/colors.ts`
2. Find this line:
   ```typescript
   export const activeColorPalette: keyof typeof colorPalettes = 'purpleGradient';
   ```
3. Change `'purpleGradient'` to one of:
   - `'purpleGradient'` (current)
   - `'oceanBlue'`
   - `'sunsetOrange'`
   - `'forestGreen'`
   - `'royalPurple'`
   - `'tealMint'`

4. Restart the dev server:
   ```bash
   npm run dev
   ```

### Method 2: Add Your Own Palette

1. Open `src/styles/colors.ts`
2. Add a new palette to the `colorPalettes` object:
   ```typescript
   myCustomPalette: {
     name: 'My Custom Palette',
     primary: {
       DEFAULT: '#your-color',
       dark: '#your-dark-color',
       // ... add 50-900 shades
     },
     accent: { ... },
     success: { ... },
     warning: { ... },
     danger: { ... },
     info: { ... },
     gradient: 'linear-gradient(135deg, #color1 0%, #color2 100%)',
   }
   ```
3. Update the active palette to use your new one

---

## Color Usage in Components

All components automatically use the active palette via Tailwind classes:

```tsx
// Primary colors
<div className="bg-primary text-white">
<div className="bg-primary-50"> // Light background
<div className="bg-primary-600"> // Specific shade

// Accent colors
<div className="text-accent">
<div className="bg-accent-light">

// Status colors
<div className="text-success"> // Green
<div className="text-warning"> // Yellow/Amber
<div className="text-danger">  // Red
<div className="text-info">    // Blue

// Gradients
<div className="bg-gradient-primary"> // Uses active palette gradient
```

---

## Tips for Choosing a Palette

1. **Purple Gradient** - Best all-rounder, modern and professional
2. **Ocean Blue** - If you want medical/clinical trust
3. **Forest Green** - If emphasizing natural health and wellness
4. **Sunset Orange** - If targeting energy and vitality
5. **Royal Purple** - If positioning as premium/luxury service
6. **Teal Mint** - If going for fresh, modern, clean aesthetic

---

## Preview Palettes Before Switching

You can see all palettes at once by creating a preview page or temporarily logging them:

```typescript
import { getAllPalettes } from '@/styles/colors';

console.log(getAllPalettes());
```

---

**Need a custom color?** Just tell me the hex codes or the vibe you're going for!
