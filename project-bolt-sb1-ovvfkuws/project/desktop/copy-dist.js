import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync, mkdirSync, cpSync, rmSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const frontendDistPath = join(__dirname, '../frontend/dist');
const desktopDistPath = join(__dirname, 'dist');

try {
  // Remove existing dist folder if it exists
  if (existsSync(desktopDistPath)) {
    rmSync(desktopDistPath, { recursive: true, force: true });
    console.log('✓ Removed existing dist folder');
  }

  // Check if frontend dist exists
  if (!existsSync(frontendDistPath)) {
    console.error('❌ Frontend dist folder not found. Please run "npm run build" in the frontend directory first.');
    process.exit(1);
  }

  // Copy frontend dist to desktop dist
  cpSync(frontendDistPath, desktopDistPath, { recursive: true });
  console.log('✓ Successfully copied frontend dist to desktop dist');
  
  // Verify the copy worked
  const indexPath = join(desktopDistPath, 'index.html');
  if (existsSync(indexPath)) {
    console.log('✓ index.html found in desktop dist');
  } else {
    console.error('❌ index.html not found after copy');
    process.exit(1);
  }

} catch (error) {
  console.error('❌ Error copying dist folder:', error.message);
  process.exit(1);
}