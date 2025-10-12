class FileUpload {
    constructor() {
        this.dropAreas = new Set();
    }

    init() {
        console.log('📁 File upload module initialized');
    }

    createDropZone(container, options = {}) {
        const dropZone = document.createElement('div');
        dropZone.className = 'file-drop-zone';
        dropZone.innerHTML = `
            <div class="drop-zone-content">
                <div class="drop-zone-icon">📁</div>
                <h4>${options.title || 'Upload Resume'}</h4>
                <p>${options.subtitle || 'Drag & drop files or click to browse'}</p>
                <input type="file" class="file-input" accept=".pdf,.doc,.docx,.txt" ${options.multiple ? 'multiple' : ''}>
                <div class="supported-formats">Supported: PDF, DOC, DOCX, TXT</div>
            </div>
            <div class="upload-progress" style="display: none;">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-text">Processing...</div>
            </div>
        `;

        const fileInput = dropZone.querySelector('.file-input');
        this.setupDropZone(dropZone, fileInput, options);

        if (container) {
            container.appendChild(dropZone);
        }

        return dropZone;
    }

    setupDropZone(dropZone, fileInput, options) {
        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drop-zone--active');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drop-zone--active');
            }, false);
        });

        // File drop handling
        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFiles(files, options);
        }, false);

        // File input change handling
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files, options);
        });

        // Click to open file dialog
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });
    }

    async handleFiles(files, options) {
        const validFiles = Array.from(files).filter(file => 
            this.isValidFileType(file) && this.isValidFileSize(file)
        );

        if (validFiles.length === 0) {
            this.showError('Please select valid PDF, DOC, DOCX, or TXT files (max 10MB)');
            return;
        }

        if (options.onFilesSelected) {
            options.onFilesSelected(validFiles);
        }

        // If single file and auto-upload enabled
        if (options.autoUpload && validFiles.length === 1) {
            await this.uploadFile(validFiles[0], options);
        }
    }

    isValidFileType(file) {
        const validTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];
        return validTypes.includes(file.type) || file.name.match(/\.(pdf|doc|docx|txt)$/i);
    }

    isValidFileSize(file) {
        return file.size <= 10 * 1024 * 1024; // 10MB
    }

    async uploadFile(file, options) {
        const formData = new FormData();
        formData.append('resume', file);

        try {
            if (options.onUploadStart) {
                options.onUploadStart(file);
            }

            const response = await fetch('/api/parse-resume-file', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }

            const result = await response.json();

            if (options.onUploadComplete) {
                options.onUploadComplete(result, file);
            }

            return result;

        } catch (error) {
            console.error('Upload error:', error);
            if (options.onUploadError) {
                options.onUploadError(error, file);
            }
            this.showError(`Failed to upload ${file.name}: ${error.message}`);
        }
    }

    showError(message) {
        // Use existing notification system or create simple alert
        if (window.UIUtils) {
            UIUtils.showNotification(message, 'error');
        } else {
            alert(message);
        }
    }

    showProgress(container, progress) {
        const progressBar = container.querySelector('.progress-fill');
        const progressText = container.querySelector('.progress-text');
        
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        if (progressText) {
            progressText.textContent = `Processing... ${progress}%`;
        }
    }
}

// Global instance
window.fileUpload = new FileUpload();