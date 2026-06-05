// Copy the rendered digital-stamp SVG to the clipboard as a PNG image.
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.digital_stamp = {
    copy: function (n_clicks, svg, size) {
        if (!n_clicks || !svg) {
            return window.dash_clientside.no_update;
        }

        const heights = { lg: 400, md: 300, sm: 200 };
        const targetH = heights[size] || 400;
        const baseW = 720;
        const baseH = 272;
        const scale = 2; // render at 2x for a crisp paste
        const svgBlob = new Blob([svg], { type: "image/svg+xml;charset=utf-8" });
        const url = URL.createObjectURL(svgBlob);
        const img = new Image();

        const showStatus = function (msg) {
            const el = document.getElementById("stamp-copy-status");
            if (!el) return;
            el.textContent = msg;
            if (window._stampStatusTimer) {
                clearTimeout(window._stampStatusTimer);
            }
            window._stampStatusTimer = setTimeout(function () {
                const e = document.getElementById("stamp-copy-status");
                if (e) e.textContent = "";
            }, 3000);
        };

        img.onload = function () {
            const canvas = document.createElement("canvas");
            canvas.height = targetH * scale;
            canvas.width = targetH * (baseW / baseH) * scale;
            const ctx = canvas.getContext("2d");
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            URL.revokeObjectURL(url);

            canvas.toBlob(function (blob) {
                if (navigator.clipboard && window.ClipboardItem) {
                    navigator.clipboard
                        .write([new ClipboardItem({ "image/png": blob })])
                        .then(function () {
                            showStatus("Copied to clipboard!");
                        })
                        .catch(function () {
                            showStatus("Copy failed");
                        });
                } else {
                    showStatus("Clipboard not supported");
                }
            }, "image/png");
        };

        img.src = url;

        // Status is managed directly in the DOM (above) so it re-triggers on
        // every click; leave Dash's own state untouched.
        return window.dash_clientside.no_update;
    },
};
