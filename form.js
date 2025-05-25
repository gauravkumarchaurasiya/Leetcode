document.getElementById('leetcodeForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const title = document.getElementById('title').value.trim();
  const tags = document.getElementById('tags').value.trim();
  const code = document.getElementById('code').value.trim();
  const explanation = document.getElementById('explanation').value.trim();
  const screenshotInput = document.getElementById('screenshot');
  const date = new Date();
  
  if (!title || !code || !explanation) {
    alert('Please fill required fields: Title, Code, Explanation');
    return;
  }

  // Generate a slug for the filename (e.g. two-sum)
  const slug = title.toLowerCase().replace(/[^\w]+/g, '-').replace(/(^-|-$)/g, '');
  const dateString = date.toISOString().split('T')[0]; // YYYY-MM-DD

  // Prepare front matter YAML
  const frontMatter = `---
title: "${title}"
date: ${dateString}
tags: [${tags.split(',').map(t => `"${t.trim()}"`).join(', ')}]
screenshot: /assets/screenshots/${slug}.png
---\n\n`;

  // Prepare markdown body with explanation and code block
  const body = `${explanation}\n\n\`\`\`python\n${code}\n\`\`\`\n`;

  // Full markdown content
  const markdown = frontMatter + body;

  // Download markdown file
  const markdownBlob = new Blob([markdown], { type: 'text/markdown' });
  const markdownUrl = URL.createObjectURL(markdownBlob);
  const mdLink = document.createElement('a');
  mdLink.href = markdownUrl;
  mdLink.download = `${dateString}-${slug}.md`;
  mdLink.click();
  URL.revokeObjectURL(markdownUrl);

  // Handle screenshot download if any
  if (screenshotInput.files.length > 0) {
    const file = screenshotInput.files[0];
    const reader = new FileReader();
    reader.onload = function (event) {
      const imageBlob = new Blob([event.target.result], { type: file.type });
      const imgUrl = URL.createObjectURL(imageBlob);
      const imgLink = document.createElement('a');
      imgLink.href = imgUrl;
      imgLink.download = `${slug}.png`;
      imgLink.click();
      URL.revokeObjectURL(imgUrl);
    };
    reader.readAsArrayBuffer(file);
  }

  document.getElementById('status').textContent = 'Markdown and screenshot files downloaded! Please add them to your repo and push.';
  this.reset();
});
