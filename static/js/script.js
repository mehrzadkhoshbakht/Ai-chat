document.addEventListener("DOMContentLoaded", () => {
    const generateButton = document.getElementById("generate-button");
    const uploadButton = document.getElementById("upload-button");
    const statusMessages = document.getElementById("status-messages");

    const showMessage = (message, isError = false) => {
        const messageElement = document.createElement("div");
        messageElement.textContent = message;
        messageElement.className = `p-4 rounded-md ${isError ? "bg-red-500" : "bg-green-500"}`;
        statusMessages.innerHTML = "";
        statusMessages.appendChild(messageElement);
    };

    generateButton.addEventListener("click", async () => {
        const keywords = document.getElementById("keywords").value;
        const platform = document.getElementById("platform").value;

        showMessage("Generating script...", false);

        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ keywords, platform }),
        });

        const result = await response.json();

        if (result.message) {
            showMessage(result.message);
        } else {
            showMessage("Error generating script.", true);
        }
    });

    uploadButton.addEventListener("click", async () => {
        // For now, we'll just use a dummy video path
        const video_path = "data/videos/placeholder.mp4";
        const platform = document.getElementById("platform").value;
        const title = "My Awesome Video";
        const description = "This is a great video about MikroTik.";
        const caption = "Check out my new video!";


        showMessage("Uploading video...", false);

        const response = await fetch("/upload", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ video_path, platform, title, description, caption }),
        });

        const result = await response.json();

        if (result.url) {
            showMessage(`Video uploaded successfully: ${result.url}`);
        } else {
            showMessage("Error uploading video.", true);
        }
    });
});
