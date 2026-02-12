// Simple pack audit script that analyzes SVGs and pack configs without requiring a server
const fs = require('fs');
const path = require('path');

const RESULTS_DIR = path.join(__dirname, 'audit-results');

if (!fs.existsSync(RESULTS_DIR)) {
  fs.mkdirSync(RESULTS_DIR, { recursive: true });
}

function loadManifest() {
  const manifestPath = path.join(__dirname, '..', 'packs', 'manifest.json');
  return JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
}

function loadPack(packId) {
  const packPath = path.join(__dirname, '..', 'packs', packId, 'pack.json');
  if (!fs.existsSync(packPath)) {
    throw new Error(`Pack file not found: ${packPath}`);
  }
  return JSON.parse(fs.readFileSync(packPath, 'utf8'));
}

function loadPackData(packId) {
  const pack = loadPack(packId);
  const basePath = path.join(__dirname, '..', 'packs', packId);
  
  // Try different possible paths for cards.json
  const possiblePaths = [
    path.join(basePath, pack.data?.cards || 'cards.json'),
    path.join(basePath, 'cards.json'),
    path.join(basePath, 'assets', 'cards', 'cards.json'),
    path.join(basePath, 'cards', 'cards.json')
  ];
  
  let cardsPath = null;
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      cardsPath = p;
      break;
    }
  }
  
  if (!cardsPath) {
    return { pack, cards: [], error: 'cards.json not found' };
  }
  
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
    sampleCards: launchCards.slice(0, 3)
  };
}

function checkPlaceholderInSvg(svgPath) {
  if (!fs.existsSync(svgPath)) {
    return { hasPlaceholder: false, error: 'SVG file not found' };
  }
  
  try {
    const svgContent = fs.readFileSync(svgPath, 'utf8');
    
    const placeholderPatterns = [
      /To:\s*_{3,}/i,
      /From:\s*_{3,}/i,
      /To:\s*_{2,}\s*From:/i,
      /To:\s*________/i,
      /From:\s*________/i,
      /To:\s*_{4,}\s*From:\s*_{4,}/i
    ];
    
    const found = placeholderPatterns.some(pattern => pattern.test(svgContent));
    return {
      hasPlaceholder: found,
      svgPath: svgPath,
      sample: found ? svgContent.match(/To:.*From:/i)?.[0]?.substring(0, 100) : null
    };
  } catch (err) {
    return { hasPlaceholder: false, error: err.message };
  }
}

function analyzeSvgLayout(svgPath) {
  if (!fs.existsSync(svgPath)) {
    return null;
  }
  
  try {
    const svgContent = fs.readFileSync(svgPath, 'utf8');
    
    // Extract text elements and their y positions
    const textMatches = svgContent.matchAll(/<text[^>]*y="(\d+)"[^>]*>/g);
    const textPositions = [];
    for (const match of textMatches) {
      textPositions.push(parseInt(match[1]));
    }
    
    // Find main content areas
    const hasTopText = textPositions.some(y => y < 200);
    const hasMiddleText = textPositions.some(y => y >= 200 && y < 400);
    const hasBottomText = textPositions.some(y => y >= 500);
    
    return {
      hasTopText,
      hasMiddleText,
      hasBottomText,
      textPositions: textPositions.sort((a, b) => a - b)
    };
  } catch (err) {
    return null;
  }
}

async function auditPack(packId, packData) {
  const results = {
    packId,
    packName: packData.pack.name || packId,
    timestamp: new Date().toISOString(),
    cards: [],
    issues: [],
    overlayConfig: packData.pack.overlay || null,
    recommendations: []
  };

  if (!packData.firstCard) {
    results.issues.push('No launch cards found');
    return results;
  }

  const basePath = path.join(__dirname, '..', 'packs', packId);
  
  // Test each sample card
  for (const card of packData.sampleCards || [packData.firstCard]) {
    const cardId = card.id;
    const cardSrc = card.front_svg || card.src || '';
    const svgPath = path.join(basePath, cardSrc);
    
    // Check for placeholder
    const placeholderCheck = checkPlaceholderInSvg(svgPath);
    
    // Analyze layout
    const layout = analyzeSvgLayout(svgPath);
    
    const cardInfo = {
      cardId,
      cardTitle: card.title || cardId,
      svgPath: cardSrc,
      placeholder: placeholderCheck,
      layout: layout
    };
    
    results.cards.push(cardInfo);
    
    // Collect issues
    if (placeholderCheck.hasPlaceholder) {
      results.issues.push(`Card ${cardId} has placeholder text in SVG`);
    }
    
    // Generate recommendations based on layout
    if (layout) {
      if (layout.hasBottomText && !results.recommendations.includes('bottom-content')) {
        results.recommendations.push('Has bottom text - may need To/From positioned higher');
      }
      if (layout.hasMiddleText && !results.recommendations.includes('middle-content')) {
        results.recommendations.push('Has middle text - message box may need adjustment');
      }
    }
  }
  
  return results;
}

async function main() {
  console.log('Starting pack audit (SVG analysis)...\n');
  
  const manifest = loadManifest();
  const packs = manifest.packs || [];
  
  console.log(`Found ${packs.length} packs to audit\n`);
  
  const allResults = [];
  
  for (const packEntry of packs) {
    const packId = packEntry.id;
    console.log(`Auditing pack: ${packId}`);
    
    try {
      const packData = loadPackData(packId);
      const result = await auditPack(packId, packData);
      allResults.push(result);
      
      if (result.issues.length > 0) {
        console.log(`  ⚠️  Issues found: ${result.issues.length}`);
        result.issues.forEach(issue => console.log(`    - ${issue}`));
      }
      if (result.recommendations.length > 0) {
        console.log(`  💡 Recommendations: ${result.recommendations.length}`);
        result.recommendations.forEach(rec => console.log(`    - ${rec}`));
      }
      if (result.issues.length === 0 && result.recommendations.length === 0) {
        console.log(`  ✓ No issues found`);
      }
      console.log('');
    } catch (err) {
      console.error(`  ❌ Failed to audit ${packId}:`, err.message);
      allResults.push({
        packId,
        error: err.message,
        timestamp: new Date().toISOString()
      });
    }
  }
  
  // Write summary report
  const reportPath = path.join(RESULTS_DIR, 'audit-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(allResults, null, 2));
  console.log(`\nAudit complete! Report saved to: ${reportPath}`);
  
  // Generate markdown summary
  const markdownPath = path.join(RESULTS_DIR, 'audit-report.md');
  let markdown = '# Pack Overlay Audit Report (SVG Analysis)\n\n';
  markdown += `Generated: ${new Date().toISOString()}\n\n`;
  markdown += `Total packs audited: ${allResults.length}\n\n`;
  
  const packsWithIssues = allResults.filter(r => r.issues && r.issues.length > 0);
  markdown += `## Summary\n\n`;
  markdown += `- Packs with issues: ${packsWithIssues.length}\n`;
  markdown += `- Total issues found: ${packsWithIssues.reduce((sum, r) => sum + (r.issues?.length || 0), 0)}\n\n`;
  
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
        markdown += `- ⚠️ ${issue}\n`;
      });
    }
    
    if (result.recommendations && result.recommendations.length > 0) {
      markdown += '\n### Recommendations:\n';
      result.recommendations.forEach(rec => {
        markdown += `- 💡 ${rec}\n`;
      });
    }
    
    if (result.cards && result.cards.length > 0) {
      markdown += '\n### Card Details:\n';
      result.cards.forEach(card => {
        markdown += `- **${card.cardTitle}** (${card.cardId})\n`;
        if (card.placeholder?.hasPlaceholder) {
          markdown += `  - ⚠️ Placeholder text found in SVG\n`;
        }
        if (card.layout) {
          markdown += `  - Layout: `;
          const layoutParts = [];
          if (card.layout.hasTopText) layoutParts.push('top text');
          if (card.layout.hasMiddleText) layoutParts.push('middle text');
          if (card.layout.hasBottomText) layoutParts.push('bottom text');
          markdown += layoutParts.join(', ') || 'no text elements detected';
          markdown += `\n`;
        }
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
