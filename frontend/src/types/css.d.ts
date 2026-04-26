/**
 * Type declarations for CSS imports
 * This allows TypeScript to recognize CSS file imports
 */

// For CSS modules (*.module.css)
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

// For global CSS files (side-effect imports)
declare module '*.css';

// For SCSS modules
declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}

// For global SCSS files
declare module '*.scss';

// For SASS modules
declare module '*.module.sass' {
  const classes: { [key: string]: string };
  export default classes;
}

// For global SASS files
declare module '*.sass';
