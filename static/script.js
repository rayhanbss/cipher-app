// Real-time conversion between plaintext and binary in the input textarea

document.addEventListener('DOMContentLoaded', function() {
    // Helper to swap input and output text
    function swapInputOutputText() {
        const temp = inputElements.textarea.value;
        inputElements.textarea.value = outputElements.textarea.value;
        outputElements.textarea.value = temp;
    }
   
    // Download button for text input
    const downloadBtn = document.querySelector('.output-container .file-output button, .output-container button.execute, .output-container .execute');
    const mainDownloadBtn = document.querySelector('.chiper-container .execute');
    // Encrypt/Decrypt swapper
    const encryptRadio = document.getElementById('encrypt-selector');
    const decryptRadio = document.getElementById('decrypt-input');

    // Helper to get encrypt/decrypt mode
    function getEncryptMode() {
        return encryptRadio && encryptRadio.checked ? 'encrypt' : 'decrypt';
    }

    // File input Browse button triggers file input (fix double popup)
    const fileInput = document.getElementById('file-input');
    const loadFileBtn = document.getElementById('load-file');
    if (fileInput && loadFileBtn) {
        // Remove any previous event listeners before adding a new one
        loadFileBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default button behavior
            fileInput.click();
        },); // Only allow the event to be attached once
    }
    // Input type toggle (text/file)
    const inputTypeSelect = document.getElementById('inputType');
    const fileInputDiv = document.querySelector('.file-input');
    const fileOutputDiv = document.querySelector('.file-output');
    const textTypeDivs = document.querySelectorAll('.text-type'); // Select all text-type divs
    const inputTextDiv = document.querySelector('.input-container textarea');
    const outputTextDiv = document.querySelector('.output-container textarea');

    // Helper to get textarea and radio elements for a given container (input or output)
    function getTextAreaElements(containerClass) {
        const container = document.querySelector(containerClass);
        return {
            textarea: container.querySelector('textarea'),
            plaintextRadio: container.querySelector('input[type="radio"][id$="plaintext-selector"]'),
            binaryRadio: container.querySelector('input[type="radio"][id$="binary-input"]')
        };
    }

    const inputElements = getTextAreaElements('.input-container');
    const outputElements = getTextAreaElements('.output-container');

    function updateInputTypeVisibility() {
        if (inputTypeSelect.value === 'file') {
            inputTextDiv.classList.add('hidden');
            outputTextDiv.classList.add('hidden');
            textTypeDivs.forEach(div => div.classList.add('hidden'));
            fileInputDiv.classList.remove('hidden');
            fileOutputDiv.classList.remove('hidden');
            // Change Download Result to Execute
            if (mainDownloadBtn) {
                mainDownloadBtn.textContent = 'Execute';
            }
        } else {
            inputTextDiv.classList.remove('hidden');
            outputTextDiv.classList.remove('hidden');
            textTypeDivs.forEach(div => div.classList.remove('hidden'));
            fileInputDiv.classList.add('hidden');
            fileOutputDiv.classList.add('hidden');
            // Change Execute to Download Result
            if (mainDownloadBtn) {
                mainDownloadBtn.textContent = 'Download Result';
            }
        }
    }
    inputTypeSelect.addEventListener('change', updateInputTypeVisibility);
    // Initialize on load
    updateInputTypeVisibility();
    // Remove duplicate code for input/output textareas and radios

    function plaintextToBinary(text) {
        return text.split('').map(char => {
            return char.charCodeAt(0).toString(2).padStart(8, '0');
        }).join(' ');
    }

    function binaryToPlaintext(binary) {
        return binary.split(' ').map(bin => {
            if (/^[01]{8}$/.test(bin)) {
                return String.fromCharCode(parseInt(bin, 2));
            } else {
                return '';
            }
        }).join('');
    }

    // Generic function to update text type for input/output
    function updateTextType(elements) {
        let value = elements.textarea.value;
        if (elements.plaintextRadio.checked) {
            elements.textarea.value = binaryToPlaintext(value);
        } else if (elements.binaryRadio.checked) {
            elements.textarea.value = plaintextToBinary(value);
        }
    }
    
    
    // Cipher execution section
    const keyInput = document.querySelector('.chiper-container input[type="text"]');
    const cipherSelect = document.querySelector('.chiper-container select');
    
    function defaultKey(){
        const cipher = cipherSelect.value;
        if (cipher === 'shift-cipher') {
            keyInput.value = '3';
        } else if (cipher === 'substitution-cipher') {
            if (inputTypeSelect.value === 'text') {
            keyInput.value = 'qwertyuiopasdfghjklzxcvbnm';
            } else {
            keyInput.value = '1';
            }
        } else if (cipher === 'affine-cipher') {
            keyInput.value = '5,8';
        } else if (cipher === 'vigenere-cipher') {
            keyInput.value = 'KUNCI';
        } else if (cipher == 'hill-cipher') {
            keyInput.value = "GYBNQKURP";
        } else if (cipher === 'permutation-cipher') {
            keyInput.value = '3,1,4,2';
        } else {
            keyInput.value = ''; 
        }
    }

    // Update key hint based on cipher
    function updateKeyHint() {
        const cipher = cipherSelect.value;
        const keyHint = document.querySelector('.key-hint');
        let hint = '';
        switch (cipher) {
            case 'shift-cipher':
                hint = 'For Shift Cipher, key must be an integer. (e.g. 3)';
                break;
            case 'substitution-cipher':
                if (inputTypeSelect.value === 'file') {
                    hint = 'For Substitution Cipher with file input, key must be an integer (e.g. 1).';
                    break;
                } else {
                    hint = 'For Substitution Cipher, key must be a 26-letter permutation of the alphabet. (e.g. qwertyuiopasdfghjklzxcvbnm)';
                }
                break;
            case 'affine-cipher':
                hint = 'For Affine Cipher, key must be two integers a,b (e.g. 5,8).';
                break;
            case 'vigenere-cipher':
                hint = 'For Vigenère Cipher, key must be a word (e.g. KEY).';
                break;
            case 'hill-cipher':
                hint = 'For Hill Cipher, key must be a string representing a square matrix (e.g. GYBNQKURP for 3x3).';
                break;
            case 'permutation-cipher':
                hint = 'For Permutation Cipher, key must be a permutation of numbers, separated by commas (e.g. 3,1,4,2).';
                break;
            default:
                hint = '';
        }
        if (keyHint) keyHint.textContent = hint;
    }
    
    // Auto-execute cipher with debounce
    let debounceTimeout;
    const DEBOUNCE_DELAY = 500; // ms
    
    async function autoExecuteCipher() {
        let input_text = inputElements.textarea.value;
        const key = keyInput.value;
        const cipher_function = cipherSelect.value;
        const mode = getEncryptMode();

        // Only auto-execute for text input mode
        if (inputTypeSelect.value !== 'text') return;

        // Always send plaintext to backend, regardless of input view
        if (inputElements.binaryRadio.checked) {
            input_text = binaryToPlaintext(input_text);
        }

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    input_text,
                    key,
                    cipher_function,
                    mode,
                    is_bytes: false
                })
            });
            const data = await response.json();
            let output = data.output_text;
            // If output is in binary mode, convert output to binary
            if (outputElements.binaryRadio.checked) {
                output = plaintextToBinary(output);
            }
            outputElements.textarea.value = output;
        } catch (err) {
            outputElements.textarea.value = 'Error executing cipher.';
        }
    }
        
    function debounceAutoExecute() {
    // Download output as file for text input mode
    function downloadOutputText() {
        if (inputTypeSelect.value !== 'text') return;
        const text = outputElements.textarea.value;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'cipher_output.txt';
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 0);
    }

    // Execute cipher for file input mode
    async function executeFileCipher() {
        // Get file from file input
        const fileInput = document.getElementById('file-input');
        const file = fileInput && fileInput.files && fileInput.files[0];
        if (!file) return;
        const key = keyInput.value;
        const cipher_function = cipherSelect.value;
        const mode = getEncryptMode();
        // Read file as ArrayBuffer for binary support
        const reader = new FileReader();
        reader.onload = async function(e) {
            const arrayBuffer = e.target.result;
            // Convert ArrayBuffer to base64
            function arrayBufferToBase64(buffer) {
                let binary = '';
                const bytes = new Uint8Array(buffer);
                const len = bytes.byteLength;
                for (let i = 0; i < len; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                return btoa(binary);
            }
            const input_bytes_b64 = arrayBufferToBase64(arrayBuffer);
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        input_bytes_b64,
                        key,
                        cipher_function,
                        mode,
                        is_bytes: true
                    })
                });
                const data = await response.json();
                // Show output file name and enable download
                const fileOutputInput = document.getElementById('file-output');
                let baseName = file.name.replace(/(\.[^.]*)?$/, '');
                let ext = file.name.match(/\.[^\.]+$/);
                ext = ext ? ext[0] : '.bin';
                let suffix = mode === 'decrypt' ? '_decrypt' : '_encrypt';
                let outputFileName = baseName + suffix + ext;
                if (fileOutputInput) fileOutputInput.value = outputFileName;
                // Decode base64 output to ArrayBuffer
                function base64ToArrayBuffer(base64) {
                    const binary_string = atob(base64);
                    const len = binary_string.length;
                    const bytes = new Uint8Array(len);
                    for (let i = 0; i < len; i++) {
                        bytes[i] = binary_string.charCodeAt(i);
                    }
                    return bytes.buffer;
                }
                let blob;
                if (data.output_bytes_b64) {
                    blob = new Blob([base64ToArrayBuffer(data.output_bytes_b64)]);
                } else {
                    // fallback for text output
                    blob = new Blob([data.output_text], { type: 'text/plain' });
                }
                fileOutputInput._blob = blob;
                fileOutputInput._filename = outputFileName;
                // Enable download button
                const saveFileBtn = document.getElementById('save-file');
                if (saveFileBtn) saveFileBtn.disabled = false;
            } catch (err) {
                alert('Error executing cipher on file.');
            }
        };
        reader.readAsArrayBuffer(file);
    }

    // Attach download/execute event for main button
    if (mainDownloadBtn) {
        mainDownloadBtn.addEventListener('click', function(e) {
            if (inputTypeSelect.value === 'file') {
                e.preventDefault();
                executeFileCipher();
            }
        });
    }

    // Download button for file output
    const saveFileBtn = document.getElementById('save-file');
    const fileOutputInput = document.getElementById('file-output');
    if (saveFileBtn && fileOutputInput) {
        saveFileBtn.disabled = true;
        saveFileBtn.addEventListener('click', function() {
            if (fileOutputInput._blob && fileOutputInput._filename) {
                const url = URL.createObjectURL(fileOutputInput._blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = fileOutputInput._filename;
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                }, 0);
            }
        });
    }
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(autoExecuteCipher, DEBOUNCE_DELAY);
    }
        
    
    // Add event listeners for input/output text type radios
    inputElements.plaintextRadio.addEventListener('change', () => {
        if (inputTypeSelect.value === 'text') updateTextType(inputElements);
    });
    inputElements.binaryRadio.addEventListener('change', () => {
        if (inputTypeSelect.value === 'text') updateTextType(inputElements);
    });
    outputElements.plaintextRadio.addEventListener('change', () => {
        if (inputTypeSelect.value === 'text') updateTextType(outputElements);
    });
    outputElements.binaryRadio.addEventListener('change', () => {
        if (inputTypeSelect.value === 'text') updateTextType(outputElements);
    });
    cipherSelect.addEventListener('change', () => {
        if (inputTypeSelect.value === 'text') debounceAutoExecute();
        defaultKey();
        updateKeyHint();
    });
    inputElements.textarea.addEventListener('input', () => {
        if (inputTypeSelect.value === 'text') debounceAutoExecute();
    });
    keyInput.addEventListener('input', () => {
        if (inputTypeSelect.value === 'text') debounceAutoExecute();
    });
    // Encrypt/Decrypt swapper listeners (only for text input)
    if (encryptRadio && decryptRadio) {
        encryptRadio.addEventListener('change', () => {
            if (inputTypeSelect.value === 'text') {
                swapInputOutputText();
                debounceAutoExecute();
            }
        });
        decryptRadio.addEventListener('change', () => {
            if (inputTypeSelect.value === 'text') {
                swapInputOutputText();
                debounceAutoExecute();
            }
        });
    }
        
    // Initialize default key on page load
    defaultKey();
    updateKeyHint();
    debounceAutoExecute();
});
