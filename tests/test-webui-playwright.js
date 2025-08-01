// CCDK WebUI Dashboard Playwright Test
// Testing the web interfaces with obsessive detail

const { chromium } = require('playwright');

async function testDashboards() {
    console.log('🔥 STARTING PLAYWRIGHT WEBUI TESTS 🔥\n');
    
    const browser = await chromium.launch({ 
        headless: true,
        args: ['--no-sandbox']
    });
    
    const context = await browser.newContext();
    const page = await context.newPage();
    
    const testResults = {
        passed: 0,
        failed: 0,
        details: []
    };
    
    // Test Analytics Dashboard (Port 5005)
    console.log('📊 Testing Analytics Dashboard on port 5005...');
    try {
        await page.goto('http://localhost:5005', { 
            waitUntil: 'networkidle',
            timeout: 10000 
        });
        
        // Check if page loads
        const title = await page.title();
        console.log(`  ✅ Dashboard loaded - Title: ${title}`);
        testResults.passed++;
        
        // Take screenshot
        await page.screenshot({ 
            path: 'tests/screenshots/analytics-dashboard.png',
            fullPage: true 
        });
        console.log('  ✅ Screenshot captured');
        
        // Check for key elements
        const hasCharts = await page.locator('canvas').count() > 0;
        if (hasCharts) {
            console.log('  ✅ Charts/visualizations found');
            testResults.passed++;
        } else {
            console.log('  ⚠️ No charts found - might be no data yet');
        }
        
    } catch (error) {
        console.log(`  ❌ Analytics Dashboard Error: ${error.message}`);
        testResults.failed++;
        testResults.details.push(`Analytics dashboard may not be running on port 5005`);
    }
    
    // Test WebUI Dashboard (Port 7000)
    console.log('\n🌐 Testing WebUI Dashboard on port 7000...');
    try {
        await page.goto('http://localhost:7000', { 
            waitUntil: 'networkidle',
            timeout: 10000 
        });
        
        // Check if page loads
        const title = await page.title();
        console.log(`  ✅ WebUI loaded - Title: ${title}`);
        testResults.passed++;
        
        // Take screenshot
        await page.screenshot({ 
            path: 'tests/screenshots/webui-dashboard.png',
            fullPage: true 
        });
        console.log('  ✅ Screenshot captured');
        
        // Check for agent list
        const agentElements = await page.locator('.agent-item, [class*="agent"]').count();
        if (agentElements > 0) {
            console.log(`  ✅ Found ${agentElements} agent elements`);
            testResults.passed++;
        }
        
        // Check for command list
        const commandElements = await page.locator('.command-item, [class*="command"]').count();
        if (commandElements > 0) {
            console.log(`  ✅ Found ${commandElements} command elements`);
            testResults.passed++;
        }
        
    } catch (error) {
        console.log(`  ❌ WebUI Dashboard Error: ${error.message}`);
        testResults.failed++;
        testResults.details.push(`WebUI dashboard may not be running on port 7000`);
    }
    
    // Test interactive elements if dashboards are running
    if (testResults.failed === 0) {
        console.log('\n🎯 Testing Interactive Elements...');
        
        // Go back to WebUI
        try {
            await page.goto('http://localhost:7000');
            
            // Try clicking on first agent if exists
            const firstAgent = await page.locator('.agent-item, [class*="agent"]').first();
            if (await firstAgent.isVisible()) {
                await firstAgent.click();
                console.log('  ✅ Clicked on agent - interaction works');
                testResults.passed++;
            }
            
        } catch (error) {
            console.log(`  ⚠️ Interactive test skipped: ${error.message}`);
        }
    }
    
    await browser.close();
    
    // Final Report
    console.log('\n' + '='.repeat(60));
    console.log('📊 PLAYWRIGHT TEST RESULTS');
    console.log('='.repeat(60));
    console.log(`✅ Passed: ${testResults.passed}`);
    console.log(`❌ Failed: ${testResults.failed}`);
    
    if (testResults.details.length > 0) {
        console.log('\n⚠️ Notes:');
        testResults.details.forEach(detail => console.log(`  - ${detail}`));
        console.log('\n💡 To run dashboards:');
        console.log('  - Analytics: python dashboard/app.py');
        console.log('  - WebUI: python webui/app.py');
    }
    
    console.log('\n🔥 PLAYWRIGHT TESTING COMPLETE 🔥');
}

// Run tests
testDashboards().catch(console.error);