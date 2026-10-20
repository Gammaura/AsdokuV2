let selectedFile = null;

        function handleFileSelect(e) {
            const files = e.target.files;
            if (files && files[0]) {
                selectedFile = files[0];
                const fileInfo = document.getElementById('file-info');
                fileInfo.style.display = 'inline-flex';
                fileInfo.className = 'file-pill';
                fileInfo.innerHTML = `${selectedFile.name} &nbsp;•&nbsp; ${(selectedFile.size/1024).toFixed(1)} KB`;
                document.getElementById('dz-title').innerText = selectedFile.name;
                document.getElementById('dz-subtitle').innerText = "Berkas terpilih. Klik tombol 'Mulai Rapikan Dokumen' di bawah untuk memproses.";
                document.getElementById('btn-process').disabled = false;
            }
        }

        // Drag & Drop Listeners
        const dz = document.getElementById('dropzone');
        if (dz) {
            ['dragenter', 'dragover'].forEach(eventName => {
                dz.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    dz.classList.add('dragover');
                }, false);
            });
            ['dragleave', 'drop'].forEach(eventName => {
                dz.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    dz.classList.remove('dragover');
                }, false);
            });
            dz.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                if (dt.files && dt.files[0]) {
                    document.getElementById('file-input').files = dt.files;
                    handleFileSelect({ target: { files: dt.files } });
                }
            }, false);
        }

        async function processDocument() {
            if (!selectedFile) return;

            const btn = document.getElementById('btn-process');
            const btnText = document.getElementById('btn-text');
            const btnSpinner = document.getElementById('btn-spinner');
            const resultsArea = document.getElementById('results-area');

            btn.disabled = true;
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline';

            // Reset Agents UI Status
            setAgentStatus(1, "running");
            setAgentStatus(2, "idle");
            setAgentStatus(3, "idle");

            const formData = new FormData();
            formData.append('file', selectedFile);

            try {
                // Step 1: Inspector UI simulation
                await new Promise(r => setTimeout(r, 400));
                setAgentStatus(1, "done");
                setAgentStatus(2, "running");

                // Step 2: Critic UI simulation
                await new Promise(r => setTimeout(r, 400));
                setAgentStatus(2, "done");
                setAgentStatus(3, "running");

                const response = await fetch('/api/format', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.detail || "Gagal memproses dokumen");
                }

                const data = await response.json();

                // All Agents Done
                setAgentStatus(1, "done");
                setAgentStatus(2, "done");
                setAgentStatus(3, "done");

                // Populate Stats Metrics
                document.getElementById('stat-time').innerText = `${data.elapsed_time || 0}s`;
                document.getElementById('stat-paras').innerText = data.total_paragraphs || 0;
                document.getElementById('stat-corrections').innerText = data.total_corrections || 0;
                document.getElementById('stat-chapters').innerText = `${(data.approved_chapters || []).length} Bab`;
                document.getElementById('stat-sqa').innerText = `${data.sqa_score || 100}%`;

                // Update SQA Badge
                const sqaBadge = document.getElementById('badge-sqa-status');
                const defectsCount = (data.sqa_defects || []).length;
                if (data.sqa_status === "PASS") {
                    sqaBadge.className = "pill-badge badge-emerald";
                    sqaBadge.innerText = `PASS 100% (Iterasi ${data.sqa_tier2_iterations || 1})`;
                } else {
                    sqaBadge.className = "pill-badge badge-pink";
                    sqaBadge.innerText = `SCORE ${data.sqa_score || 100}% (${defectsCount} Defect)`;
                }

                // Update Download Link
                const dlBtn = document.getElementById('btn-download');
                dlBtn.href = `/api/download/${encodeURIComponent(data.output_filename || '')}`;
                document.getElementById('out-filename-label').innerText = data.output_filename || 'hasil_skripsi.docx';

                // Populate Corrections Log Table
                const tbody = document.getElementById('corrections-tbody');
                tbody.innerHTML = '';
                if (data.corrections_log && data.corrections_log.length > 0) {
                    data.corrections_log.slice(0, 50).forEach(c => {
                        const tr = document.createElement('tr');
                        const pIdx = c.idx !== undefined ? c.idx : (c.para_id !== undefined ? c.para_id : '-');
                        const origPred = c.agent1_pred || c.original_pred || '-';
                        const corrTo = c.corrected_to || c.corrected_label || '-';
                        tr.innerHTML = `
                            <td style="font-family: 'JetBrains Mono'; font-weight: 600; color: var(--text-muted);">P[${pIdx}]</td>
                            <td style="color: var(--text-heading); font-weight: 500;">"${c.text || ''}"</td>
                            <td><span style="background: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">${origPred}</span></td>
                            <td><span style="background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">${corrTo}</span></td>
                            <td style="font-size: 0.75rem; color: var(--text-muted);">${c.reason || ''}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--emerald-text); font-weight: 600; padding: 1rem;">Sempurna! Agent 1 berhasil memprediksi seluruh struktur dengan 0 anomali.</td></tr>`;
                }

                resultsArea.style.display = 'block';
                resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

            } catch (err) {
                alert("Terjadi kesalahan: " + err.message);
                setAgentStatus(1, "idle");
                setAgentStatus(2, "idle");
                setAgentStatus(3, "idle");
            } finally {
                btn.disabled = false;
                btnText.style.display = 'inline';
                btnSpinner.style.display = 'none';
            }
        }

        function setAgentStatus(agentNum, status) {
            const card = document.getElementById(`card-agent-${agentNum}`);
            const badge = document.getElementById(`badge-agent-${agentNum}`);

            card.classList.remove("active", "done");
            badge.className = "agent-status-badge";

            if (status === "idle") {
                badge.classList.add("status-idle");
                badge.innerText = "Idle";
            } else if (status === "running") {
                card.classList.add("active");
                badge.classList.add("status-running");
                badge.innerText = "Running...";
            } else if (status === "done") {
                card.classList.add("done");
                badge.classList.add("status-done");
                badge.innerText = "Approved";
            }
        }