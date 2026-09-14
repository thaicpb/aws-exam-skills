/* End-to-end tests use synthetic fixtures, never a production question bank. */
const {test, before, after} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const python = process.env.PYTHON || 'python3';
let directory, browser;
before(async () => {
  directory = fs.mkdtempSync(path.join(os.tmpdir(), 'aws-exam-browser-'));
  execFileSync(python, [path.join(__dirname, 'fixtures.py'), directory]);
  for (const mode of ['practice','exam']) for (const count of [15,65]) {
    execFileSync(python, [path.join(root, 'scripts/build_exam.py'), path.join(directory, `${mode}-${count}.json`), '--output', path.join(directory, `${mode}-${count}.html`)]);
  }
  browser = await chromium.launch({headless: true});
});
after(async () => { if (browser) await browser.close(); if (directory) fs.rmSync(directory, {recursive:true,force:true}); });
async function run(mode, count, fn, options = {}) {
  const context = await browser.newContext({offline:true, ...options});
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  try {
    await page.clock.install();
    await page.goto(pathToFileURL(path.join(directory, `${mode}-${count}.html`)).href);
    await fn(page);
    assert.deepEqual(errors, []);
  } finally { await context.close(); }
}
for (const mode of ['practice','exam']) for (const count of [15,65]) {
  test(`${mode} ${count}: full navigation, offline UI, submit and review`, async () => run(mode,count,async page => {
    assert.equal(await page.locator('#workspace').isVisible(),false);
    await page.locator('#start').click();
    assert.equal(await page.locator('#question-nav button').count(),count);
    assert.equal(await page.locator('#feedback').isVisible(),false);
    await page.locator('input[value=B]').check();
    if (mode === 'practice') {
      await page.locator('#confirm').click();
      assert.match(await page.locator('#feedback').innerText(),/Đáp án đúng: B/);
      assert.equal(await page.locator('#feedback ul li').count(),1);
      assert.equal(await page.locator('input[value=B]').isDisabled(),true);
    } else {
      assert.equal(await page.locator('#running-score').innerText(),'');
      assert.equal(await page.locator('#feedback').innerText(),'');
    }
    await page.locator('#flag').click();
    await page.locator('#next').click();
    await page.locator('input[value=C]').check();
    await page.locator('input[value=A]').check();
    if (mode === 'practice') await page.locator('#confirm').click();
    await page.locator('#previous').click();
    assert.equal(await page.locator('input[value=B]').isChecked(),true);
    assert.equal(await page.locator('#flag').getAttribute('aria-pressed'),'true');
    await page.locator('#submit').click();
    assert.match(await page.locator('#submit-description').innerText(),new RegExp(`Còn ${count - 2} câu`));
    await page.locator('#cancel-submit').click();
    assert.equal(await page.locator('#summary').isVisible(),false);
    await page.locator('#submit').click(); await page.locator('#finish-submit').click();
    assert.match(await page.locator('#summary .score').innerText(),new RegExp(`2/${count} câu đúng`));
    assert.equal(await page.locator('#summary tbody tr').count(),4);
    await page.locator('#question-nav button').last().click();
    assert.match(await page.locator('#feedback').innerText(),/Bỏ trống/);
    assert.equal(await page.locator('#submit').isVisible(),false);
  }));
}
test('practice: incomplete validation, selection limit and no duplicate scoring', async () => run('practice',15,async page => {
  await page.locator('#start').click(); await page.locator('#confirm').click();
  assert.match(await page.locator('#message').innerText(),/Cần chọn đủ/);
  await page.locator('#next').click(); await page.locator('input[value=A]').check();
  await page.locator('#confirm').click(); assert.match(await page.locator('#message').innerText(),/Cần chọn đủ 2/);
  await page.locator('input[value=C]').check(); await page.locator('input[value=B]').click();
  assert.equal(await page.locator('input[value=B]').isChecked(),false);
  await page.locator('#confirm').click(); await page.locator('#next').click(); await page.locator('#previous').click();
  assert.equal(await page.locator('#confirm').isVisible(),false);
  assert.match(await page.locator('#running-score').innerText(),/Đúng 1\/15/);
}));
test('exam: timer begins on start, auto-submit closes confirmation and freezes answers', async () => run('exam',65,async page => {
  await page.clock.fastForward(600000);
  assert.equal(await page.locator('#summary').isVisible(),false);
  await page.locator('#start').click(); assert.match(await page.locator('#timer').innerText(),/130:00/);
  await page.locator('input[value=B]').check(); await page.locator('#submit').click();
  await page.clock.fastForward(130 * 60000);
  assert.equal(await page.locator('#submit-dialog').isVisible(),false);
  assert.match(await page.locator('#summary').innerText(),/Hết giờ — đã nộp bài/);
  assert.match(await page.locator('#summary .score').innerText(),/1\/65/);
  assert.equal(await page.locator('input[value=B]').isDisabled(),true);
}));
test('mobile layout and keyboard selection', async () => run('practice',15,async page => {
  await page.locator('#start').click();
  await page.locator('input[value=B]').focus(); await page.keyboard.press('Space');
  assert.equal(await page.locator('input[value=B]').isChecked(),true);
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),true);
  if (process.env.QA_OUTPUT) {
    fs.mkdirSync(process.env.QA_OUTPUT,{recursive:true});
    await page.screenshot({path:path.join(process.env.QA_OUTPUT,'mobile.png'),fullPage:true});
  }
}, {viewport:{width:390,height:844}}));
test('desktop screenshot and no horizontal overflow', async () => run('exam',65,async page => {
  await page.locator('#start').click();
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),true);
  if (process.env.QA_OUTPUT) {
    fs.mkdirSync(process.env.QA_OUTPUT,{recursive:true});
    await page.screenshot({path:path.join(process.env.QA_OUTPUT,'desktop.png'),fullPage:true});
  }
}, {viewport:{width:1280,height:900}}));
