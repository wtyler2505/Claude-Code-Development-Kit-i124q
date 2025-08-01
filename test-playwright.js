const { chromium, firefox, webkit } = require('@playwright/test');

async function testBrowsers() {
  console.log('Testing Playwright browser availability...\n');
  
  const browsers = [
    { name: 'Chromium', launcher: chromium },
    { name: 'Firefox', launcher: firefox },
    { name: 'WebKit', launcher: webkit }
  ];
  
  for (const { name, launcher } of browsers) {
    try {
      console.log(`Testing ${name}...`);
      const executablePath = launcher.executablePath();
      console.log(`✓ ${name} executable path: ${executablePath}`);
      
      // Try to launch
      const browser = await launcher.launch({ headless: true });
      console.log(`✓ ${name} launched successfully`);
      await browser.close();
    } catch (error) {
      console.log(`✗ ${name} failed: ${error.message}`);
    }
    console.log('');
  }
}

testBrowsers().catch(console.error);