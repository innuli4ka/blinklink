// Wait for the page (HTML) to fully load before running anything
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("shortenForm");
  const input = document.getElementById("longUrl");
  const result = document.getElementById("result");
  const themeToggle = document.getElementById("themeToggle");

  const lambdaBaseUrl = "%%LAMBDA_URL%%";

  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    themeToggle.textContent = isDark ? "🌞" : "🌙";
  });

  async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      return true;
    }
  }

  function isValidUrl(url) {
    try {
      const urlObj = new URL(url);
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
      return false;
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const longUrl = input.value.trim();

    if (!longUrl) {
      result.innerHTML = '<span style="color: #ff5e78;">Please enter a URL.</span>';
      result.classList.remove('has-content');
      return;
    }

    if (!isValidUrl(longUrl)) {
      result.innerHTML = '<span style="color: #ff5e78;">Please enter a valid URL starting with http:// or https://</span>';
      result.classList.remove('has-content');
      return;
    }

    result.innerHTML = '<span style="color: #007bff;">Shortening your URL...</span>';
    result.classList.remove('has-content');

    try {
      const response = await fetch(lambdaBaseUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: longUrl }),
      });

      const data = await response.json();

      if (response.ok) {
        const shortUrl = `${lambdaBaseUrl}${data.short_id}`;

        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '📋 Copy';
        copyButton.onclick = async () => {
          const success = await copyToClipboard(shortUrl);
          if (success) {
            copyButton.innerHTML = '✅ Copied!';
            copyButton.style.background = '#90ee90';
            setTimeout(() => {
              copyButton.innerHTML = '📋 Copy';
              copyButton.style.background = '#007bff';
            }, 2000);
          }
        };

        const urlContainer = document.createElement('div');
        urlContainer.className = 'url-container';

        const urlLink = document.createElement('a');
        urlLink.href = shortUrl;
        urlLink.target = '_blank';
        urlLink.style.color = '#007bff';
        urlLink.style.textDecoration = 'underline';
        urlLink.textContent = shortUrl;

        urlContainer.appendChild(urlLink);
        urlContainer.appendChild(copyButton);

        result.innerHTML = '<span style="color: #007bff;">Shortened URL:</span>';
        result.appendChild(urlContainer);
        result.classList.add('has-content');
      } else {
        result.innerHTML = `<span style="color: #ff5e78;">Error: ${data.error || "Unexpected error"}</span>`;
        result.classList.remove('has-content');
      }
    } catch (err) {
      result.innerHTML = `<span style="color: #ff5e78;">Error: ${err.message}</span>`;
    }
  });
});
