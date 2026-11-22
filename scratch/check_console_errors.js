const { spawn } = require('child_process');
const http = require('http');

async function testPage(url, pageName) {
  return new Promise((resolve, reject) => {
    const port = 9333;
    const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
      '--headless=new',
      `--remote-debugging-port=${port}`,
      '--no-first-run',
      '--no-default-browser-check',
      url
    ]);

    let errors = [];
    let stdout = '';
    let stderr = '';

    chrome.stdout.on('data', d => { stdout += d; });
    chrome.stderr.on('data', d => {
      const text = d.toString();
      stderr += text;
      // Look for JS console errors or unhandled exceptions
      if (text.includes('Uncaught') || text.includes('SyntaxError') || text.includes('TypeError') || text.includes('ReferenceError')) {
        errors.push(text.trim());
      }
    });

    setTimeout(() => {
      chrome.kill('SIGKILL');
      resolve({ pageName, url, errors, stderrSnippet: stderr.slice(-300) });
    }, 4000);
  });
}

async function run() {
  console.log("Checking browser console logs for skill-gap and ats-checker...");
  const sg = await testPage('http://localhost:3002/skill-gap', 'Skill Gap');
  console.log(`[${sg.pageName}] JS Fatal Errors: ${sg.errors.length}`);
  if (sg.errors.length > 0) console.log(sg.errors);

  const ats = await testPage('http://localhost:3002/resume/ats-checker', 'ATS Checker');
  console.log(`[${ats.pageName}] JS Fatal Errors: ${ats.errors.length}`);
  if (ats.errors.length > 0) console.log(ats.errors);

  console.log("Browser console inspection complete.");
}

run();
