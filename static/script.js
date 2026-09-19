document.getElementById('analyze-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    loading.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    analyzeBtn.disabled = true;

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze resume');
        }
        
        // Populate results
        document.getElementById('score-text').textContent = data.score + '%';
        document.getElementById('status-text').textContent = 'Status: ' + data.status;
        
        // Matched Skills
        const matchedList = document.getElementById('matched-skills');
        matchedList.innerHTML = '';
        document.getElementById('matched-count').textContent = data.matched.length;
        data.matched.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            matchedList.appendChild(li);
        });

        // Missing Skills
        const missingList = document.getElementById('missing-skills');
        missingList.innerHTML = '';
        document.getElementById('missing-count').textContent = data.missing.length;
        data.missing.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            missingList.appendChild(li);
        });
        
        // Learning Roadmap
        const roadmapList = document.getElementById('learning-roadmap');
        roadmapList.innerHTML = '';
        data.learning_roadmap.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            roadmapList.appendChild(li);
        });

        // Job Recs
        const jobsList = document.getElementById('job-recs');
        jobsList.innerHTML = '';
        data.job_recommendations.forEach(job => {
            const li = document.createElement('li');
            li.textContent = job;
            jobsList.appendChild(li);
        });

        // Store data for download
        window.latestAnalysisData = data;
        
        resultsSection.classList.remove('hidden');
        
    } catch (error) {
        alert(error.message);
    } finally {
        loading.classList.add('hidden');
        analyzeBtn.disabled = false;
    }
});

document.getElementById('download-btn').addEventListener('click', async () => {
    if (!window.latestAnalysisData) {
        alert('Please analyze a resume first');
        return;
    }
    
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(window.latestAnalysisData)
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to download report');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'AI_Resume_Analysis_Report.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
        
    } catch (error) {
        alert(error.message);
    }
});
