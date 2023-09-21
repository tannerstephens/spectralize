window.addEventListener('load', () => {
    const seedField = document.getElementById('seed');
    const generateButton = document.getElementById('generate');
    const downloadButton = document.getElementById('download');
    const ghostImage = document.getElementById('ghost');

    ghostImage.src = `/gen?seed=${seedField.value}`;

    generateButton.onclick = () => {
        ghostImage.src = `/gen?seed=${seedField.value}`;
    }

    downloadButton.onclick = () => {
        const a = document.createElement('a');
        a.href = ghostImage.src;
        a.download = 'ghost.png';

        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
});
