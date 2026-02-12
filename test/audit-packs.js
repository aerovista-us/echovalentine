// Playwright script to audit all card packs for overlay positioning and placeholder issues
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = process.env.BASE_URL || 'http://localhost:8765';
const RESULTS_DIR = path.join(__dirname, 'audit-results');

// Ensure results directory exists
if (!fs.existsSync(RESULTS_DIR)) {
  fs.mkdirSync(RESULTS_DIR, { recursive: true });
}

async function loadManifest() {
  const manifestPath = path.join(__dirname, '..', 'packs', 'manifest.json');
  return JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
}

async function loadPack(packId) {
  const packPath = path.join(__dirname, '..', 'packs', packId, 'pack.json');
  if (!fs.existsSync(packPath)) {
    throw new Error(`Pack file not found: ${packPath}`);
  }
  return JSON.parse(fs.readFileSync(packPath, 'utf8'));
}

async function loadPackData(packId) {
  const pack = await loadPack(packId);
  const basePath = path.join(__dirname, '..', 'packs', packId);
  
  const cardsPath = path.join(basePath, pack.data.cards);
  const cardsRaw = JSON.parse(fs.readFileSync(cardsPath, 'utf8'));
  const cards = Array.isArray(cardsRaw) ? { cards: cardsRaw } : cardsRaw;
  
  // Get first non-sticker card
  const launchCards = (cards.cards || []).filter(c => {
    const id = String(c?.id || "").toLowerCase();
    const src = String(c?.front_svg || c?.src || "").toLowerCase();
    return !id.includes("-st-") && !id.includes("_st_") && !id.includes("sticker") &&
           !src.includes("-st-") && !src.includes("_st_") && !src.includes("sticker");
  });
  
  return {
    pack,
    firstCard: launchCards[0] || cards.cards?.[0],
    sampleCards: launchCards.slice(0, 3) // Test up to 3 cards per pack
  };
}

async function checkPlaceholderInSvg(page, cardSrc) {
  try {
    // Fetch SVG content
    const response = await page.goto(`${BASE_URL}/${cardSrc}`, { waitUntil: 'networkidle' });
    const svgContent = await response.text();
    
    // Check for placeholder patterns
    const placeholderPatterns = [
      /To:\s*_{3,}/i,
      /From:\s*_{3,}/i,
      /To:\s*_{2,}\s*From:/i,
      /To:\s*________/i,
      /From:\s*________/i
    ];
    
    const found = placeholderPatterns.some(pattern => pattern.test(svgContent));
    return {
      hasPlaceholder: found,
      svgContent: found ? svgContent.substring(0, 500) : null // Sample for debugging
    };
  } catch (err) {
    return {
      hasPlaceholder: false,
      error: err.message
    };
  }
}

async function auditPack(browser, packId, packData) {
  const page = await browser.newPage();
  const results = {
    packId,
    packName: packData.pack.name || packId,
    timestamp: new Date().toISOString(),
    cards: [],
    issues: [],
    overlayConfig: packData.pack.overlay || null
  };

  try {
    if (!packData.firstCard) {
      results.issues.push('No launch cards found');
      return results;
    }

    // Test each sample card
    for (const card of packData.sampleCards || [packData.firstCard]) {
      const cardId = card.id;
      const cardSrc = `packs/${packId}/${card.front_svg || card.src || ''}`;
      
      console.log(`  Testing card: ${cardId}`);
      
      // Navigate to compose page
      const composeUrl = `${BASE_URL}/#/compose?pack=${encodeURIComponent(packId)}&card=${encodeURIComponent(cardId)}`;
      await page.goto(composeUrl, { waitUntil: 'networkidle' });
      
      // Wait for card to load
      await page.waitForSelector('.composeStage', { timeout: 10000 });
      await page.waitForTimeout(1000); // Allow overlays to render
      
      // Fill in test data
      const toInput = page.locator('#composeTo');
      const fromInput = page.locator('#composeFrom');
      const msgInput = page.locator('#composeMessage');
      
      if (await toInput.count() > 0) {
        await toInput.fill('Test Recipient');
      }
      if (await fromInput.count() > 0) {
        await fromInput.fill('Test Sender');
      }
      if (await msgInput.count() > 0) {
        await msgInput.fill('Testing overlay positioning and alignment');
      }
      
      // Wait for overlays to update
      await page.waitForTimeout(500);
      
      // Check for placeholder in SVG
      const placeholderCheck = await checkPlaceholderInSvg(page, cardSrc);
      
      // Take screenshots
      const safeCardId = cardId.replace(/[^a-zA-Z0-9]/g, '_');
      const screenshotPath = path.join(RESULTS_DIR, `${packId}_${safeCardId}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      
      // Get overlay element positions
      const toFromRow = page.locator('.cardToFromRow');
      const messageEl = page.locator('.cardMessage');
      
      const cardInfo = {
        cardId,
        cardTitle: card.title || cardId,
        screenshot: path.relative(__dirname, screenshotPath),
        placeholder: placeholderCheck,
        overlayVisible: {
          toFrom: await toFromRow.count() > 0 && await toFromRow.isVisible(),
          message: await messageEl.count() > 0 && await messageEl.isVisible()
        },
        overlayStyles: {}
      };
      
      // Get computed styles if elements exist
      if (await toFromRow.count() > 0) {
        cardInfo.overlayStyles.toFrom = await toFromRow.evaluate(el => ({
          top: window.getComputedStyle(el).top,
          gap: window.getComputedStyle(el).gap,
          display: window.getComputedStyle(el).display
        }));
      }
      
      if (await messageEl.count() > 0) {
        cardInfo.overlayStyles.message = await messageEl.evaluate(el => ({
          top: window.getComputedStyle(el).top,
          width: window.getComputedStyle(el).width,
          left: window.getComputedStyle(el).left,
          transform: window.getComputedStyle(el).transform,
          display: window.getComputedStyle(el).display
        }));
      }
      
      results.cards.push(cardInfo);
      
      // Collect issues
      if (placeholderCheck.hasPlaceholder) {
        results.issues.push(`Card ${cardId} has placeholder text in SVG`);
      }
      if (!cardInfo.overlayVisible.toFrom) {
        results.issues.push(`Card ${cardId}: To/From row not visible`);
      }
      if (!cardInfo.overlayVisible.message) {
        results.issues.push(`Card ${cardId}: Message box not visible`);
      }
    }
    
  } catch (err) {
    results.error = err.message;
    console.error(`  Error auditing ${packId}:`, err.message);
  } finally {
    await page.close();
  }
  
  return results;
}

async function main() {
  console.log('Starting pack audit...');
  console.log(`Base URL: ${BASE_URL}`);
  console.log(`Results directory: ${RESULTS_DIR}`);
  
  const manifest = await loadManifest();
  const packs = manifest.packs || [];
  
  console.log(`Found ${packs.length} packs to audit\n`);
  
  const browser = await chromium.launch({ headless: true });
  const allResults = [];
  
  try {
    for (const packEntry of packs) {
      const packId = packEntry.id;
      console.log(`Auditing pack: ${packId}`);
      
      try {
        const packData = await loadPackData(packId);
        const result = await auditPack(browser, packId, packData);
        allResults.push(result);
        
        if (result.issues.length > 0) {
          console.log(`  Issues found: ${result.issues.length}`);
          result.issues.forEach(issue => console.log(`    - ${issue}`));
        } else {
          console.log(`  ✓ No issues found`);
        }
        console.log('');
      } catch (err) {
        console.error(`  Failed to audit ${packId}:`, err.message);
        allResults.push({
          packId,
          error: err.message,
          timestamp: new Date().toISOString()
        });
      }
    }
  } finally {
    await browser.close();
  }
  
  // Write summary report
  const reportPath = path.join(RESULTS_DIR, 'audit-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(allResults, null, 2));
  console.log(`\nAudit complete! Report saved to: ${reportPath}`);
  
  // Generate markdown summary
  const markdownPath = path.join(RESULTS_DIR, 'audit-report.md');
  let markdown = '# Pack Overlay Audit Report\n\n';
  markdown += `Generated: ${new Date().toISOString()}\n\n`;
  markdown += `Total packs audited: ${allResults.length}\n\n`;
  
  for (const result of allResults) {
    markdown += `## ${result.packName || result.packId}\n\n`;
    markdown += `- **Pack ID**: ${result.packId}\n`;
    if (result.overlayConfig) {
      markdown += `- **Has overlay config**: Yes\n`;
    } else {
      markdown += `- **Has overlay config**: No (using defaults)\n`;
    }
    markdown += `- **Cards tested**: ${result.cards?.length || 0}\n`;
    markdown += `- **Issues**: ${result.issues?.length || 0}\n`;
    
    if (result.issues && result.issues.length > 0) {
      markdown += '\n### Issues:\n';
      result.issues.forEach(issue => {
        markdown += `- ${issue}\n`;
      });
    }
    
    if (result.cards && result.cards.length > 0) {
      markdown += '\n### Card Details:\n';
      result.cards.forEach(card => {
        markdown += `- **${card.cardTitle}** (${card.cardId})\n`;
        if (card.placeholder?.hasPlaceholder) {
          markdown += `  - ⚠️ Placeholder text found in SVG\n`;
        }
        markdown += `  - Screenshot: ${card.screenshot}\n`;
      });
    }
    
    markdown += '\n';
  }
  
  fs.writeFileSync(markdownPath, markdown);
  console.log(`Markdown report saved to: ${markdownPath}`);
}

if (require.main === module) {
  main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
  });
}

module.exports = { auditPack, loadPackData };
