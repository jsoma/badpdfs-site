// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // For GitHub Pages deployment
  // If your repo is <username>/<repo-name>, set base to '/<repo-name>/'
  // If it's a user/org site (<username>.github.io), remove this line
  base: '/',
  site: 'https://badpads.com', // Replace with your GitHub username
  
  vite: {
    plugins: [tailwindcss()]
  },
  // Serve artifacts directory in dev mode
  devToolbar: {
    enabled: false
  }
});