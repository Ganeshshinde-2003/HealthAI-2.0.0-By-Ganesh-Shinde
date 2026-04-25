/**
 * Color Palette Configuration
 * Store and switch between different color schemes for Nova Health
 */

export const colorPalettes = {
  // Current: Purple Gradient (Original Nova Health)
  purpleGradient: {
    name: 'Purple Gradient',
    primary: {
      DEFAULT: '#667eea',
      dark: '#764ba2',
      50: '#f5f7ff',
      100: '#ebefff',
      200: '#d6dfff',
      300: '#b3c1ff',
      400: '#8a9eff',
      500: '#667eea',
      600: '#5568d3',
      700: '#4553b8',
      800: '#3a4694',
      900: '#323d7a',
    },
    accent: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    success: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    warning: {
      DEFAULT: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    danger: {
      DEFAULT: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    info: {
      DEFAULT: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },

  // Ocean Blue (Calm & Trustworthy)
  oceanBlue: {
    name: 'Ocean Blue',
    primary: {
      DEFAULT: '#0ea5e9',
      dark: '#0284c7',
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c4a6e',
    },
    accent: {
      DEFAULT: '#06b6d4',
      light: '#22d3ee',
      dark: '#0891b2',
    },
    success: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    warning: {
      DEFAULT: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    danger: {
      DEFAULT: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    info: {
      DEFAULT: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
    gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
  },

  // Sunset Orange (Warm & Energetic)
  sunsetOrange: {
    name: 'Sunset Orange',
    primary: {
      DEFAULT: '#f97316',
      dark: '#ea580c',
      50: '#fff7ed',
      100: '#ffedd5',
      200: '#fed7aa',
      300: '#fdba74',
      400: '#fb923c',
      500: '#f97316',
      600: '#ea580c',
      700: '#c2410c',
      800: '#9a3412',
      900: '#7c2d12',
    },
    accent: {
      DEFAULT: '#ec4899',
      light: '#f472b6',
      dark: '#db2777',
    },
    success: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    warning: {
      DEFAULT: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    danger: {
      DEFAULT: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    info: {
      DEFAULT: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
    gradient: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
  },

  // Forest Green (Natural & Healthy)
  forestGreen: {
    name: 'Forest Green',
    primary: {
      DEFAULT: '#059669',
      dark: '#047857',
      50: '#ecfdf5',
      100: '#d1fae5',
      200: '#a7f3d0',
      300: '#6ee7b7',
      400: '#34d399',
      500: '#10b981',
      600: '#059669',
      700: '#047857',
      800: '#065f46',
      900: '#064e3b',
    },
    accent: {
      DEFAULT: '#84cc16',
      light: '#a3e635',
      dark: '#65a30d',
    },
    success: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    warning: {
      DEFAULT: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    danger: {
      DEFAULT: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    info: {
      DEFAULT: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
    gradient: 'linear-gradient(135deg, #059669 0%, #84cc16 100%)',
  },

  // Royal Purple (Premium & Sophisticated)
  royalPurple: {
    name: 'Royal Purple',
    primary: {
      DEFAULT: '#9333ea',
      dark: '#7e22ce',
      50: '#faf5ff',
      100: '#f3e8ff',
      200: '#e9d5ff',
      300: '#d8b4fe',
      400: '#c084fc',
      500: '#a855f7',
      600: '#9333ea',
      700: '#7e22ce',
      800: '#6b21a8',
      900: '#581c87',
    },
    accent: {
      DEFAULT: '#ec4899',
      light: '#f472b6',
      dark: '#db2777',
    },
    success: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    warning: {
      DEFAULT: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    danger: {
      DEFAULT: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    info: {
      DEFAULT: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
    gradient: 'linear-gradient(135deg, #9333ea 0%, #ec4899 100%)',
  },

  // Teal Mint (Fresh & Modern)
  tealMint: {
    name: 'Teal Mint',
    primary: {
      DEFAULT: '#14b8a6',
      dark: '#0d9488',
      50: '#f0fdfa',
      100: '#ccfbf1',
      200: '#99f6e4',
      300: '#5eead4',
      400: '#2dd4bf',
      500: '#14b8a6',
      600: '#0d9488',
      700: '#0f766e',
      800: '#115e59',
      900: '#134e4a',
    },
    accent: {
      DEFAULT: '#06b6d4',
      light: '#22d3ee',
      dark: '#0891b2',
    },
    success: {
      DEFAULT: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    warning: {
      DEFAULT: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    danger: {
      DEFAULT: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    info: {
      DEFAULT: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
    gradient: 'linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%)',
  },
};

// Active color palette - CHANGE THIS TO SWITCH THEMES
export const activeColorPalette: keyof typeof colorPalettes = 'tealMint';

// Export the active palette
export const colors = colorPalettes[activeColorPalette];

// Helper to get all available palette names
export const availablePalettes = Object.keys(colorPalettes) as Array<keyof typeof colorPalettes>;

// Helper to preview all palettes
export function getAllPalettes() {
  return colorPalettes;
}
