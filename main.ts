import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const botDirectory = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

try {
  mkdirSync(outputDirectory, { recursive: true });
  copyFileSync(join(botDirectory, 'POST.json'), join(outputDirectory, 'POST.json'));
} catch (error) {
  const reason = error instanceof Error ? error.message : String(error);
  console.error(`Cannot copy POST.json from ${botDirectory} to ${outputDirectory}: ${reason}`);
  process.exit(1);
}
