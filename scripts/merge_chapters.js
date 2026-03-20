const fs = require('fs');
const path = require('path');

const baseDir = 'c:/Users/Xin58696e/Desktop/NarutoHououden';
const sourceDir = path.join(baseDir, 'rewritten_chapters');
const outputDir = path.join(sourceDir, 'merged');
const stateFile = path.join(baseDir, 'scripts', 'merge_progress.json');

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

function getChapterNumber(filename) {
    const match = filename.match(/^(\d+)_/);
    return match ? parseInt(match[1], 10) : null;
}

function main() {
    let state = { merged_chunks: [] };
    if (fs.existsSync(stateFile)) {
        state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
    }

    const files = fs.readdirSync(sourceDir)
        .filter(f => f.endsWith('.md') && getChapterNumber(f) !== null)
        .sort((a, b) => getChapterNumber(a) - getChapterNumber(b));

    const chapterMap = {};
    files.forEach(f => {
        chapterMap[getChapterNumber(f)] = f;
    });

    if (files.length === 0) {
        console.log("No chapters found.");
        return;
    }

    const maxChapter = getChapterNumber(files[files.length - 1]);
    const totalChunks = Math.floor(maxChapter / 10);

    let processedAny = false;

    for (let i = 0; i < totalChunks; i++) {
        const start = i * 10 + 1;
        const end = (i + 1) * 10;
        const chunkKey = `${start}-${end}`;

        if (state.merged_chunks.includes(chunkKey)) {
            continue;
        }

        // Check completeness
        let blockFiles = [];
        let isComplete = true;
        for (let j = start; j <= end; j++) {
            if (!chapterMap[j]) {
                isComplete = false;
                break;
            }
            blockFiles.push(chapterMap[j]);
        }

        if (isComplete) {
            console.log(`Merging chunk ${chunkKey}...`);
            let combinedContent = '';
            blockFiles.forEach(f => {
                const content = fs.readFileSync(path.join(sourceDir, f), 'utf8');
                combinedContent += `## ${f}\n\n${content}\n\n---\n\n`;
            });

            const outputName = `Vol_${String(i + 1).padStart(2, '0')}_${chunkKey}.md`;
            fs.writeFileSync(path.join(outputDir, outputName), combinedContent);
            
            state.merged_chunks.push(chunkKey);
            processedAny = true;
        } else {
            console.log(`Chunk ${chunkKey} is not yet complete.`);
        }
    }

    if (processedAny) {
        fs.writeFileSync(stateFile, JSON.stringify(state, null, 4));
        console.log("Merging complete. Progress saved.");
    } else {
        console.log("No new chunks to merge.");
    }
}

main();
