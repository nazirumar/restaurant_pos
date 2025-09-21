document.addEventListener('DOMContentLoaded', function() {
  // fetch chart data from api endpoint or use inline data present in the page
  const salesCtx = document.getElementById('salesLine')?.getContext('2d');
  if (salesCtx) {
    // Try to find a global data object if Django rendered it (fallback sample data)
    const fallback = {
      labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
      data: [120,140,150,170,160,190,220]
    };

    // If you want dynamic data, fetch /dashboard/stats/ JSON
    fetch('/dashboard/stats/')
      .then(r => r.json())
      .then(json => {
        const cfg = {
          type: 'line',
          data: {
            labels: json.sales.labels || fallback.labels,
            datasets: [{
              label: 'Sales',
              data: json.sales.data || fallback.data,
              fill: true,
              tension: 0.3,
              pointRadius: 2
            }]
          },
          options: {
            plugins: { legend: { display: false } },
            scales: {
              x: { display: false },
              y: { display: false }
            },
            elements: {
              line: { borderWidth: 2, borderColor: '#f59e0b' },
              point: { radius: 0 }
            },
            maintainAspectRatio: false
          }
        };
        new Chart(salesCtx, cfg);
      })
      .catch(err => {
        // fallback chart
        new Chart(salesCtx, {
          type: 'line',
          data: { labels: fallback.labels, datasets: [{ data: fallback.data, fill:true, tension:0.3 }]},
          options: { plugins:{legend:{display:false}}, scales:{x:{display:false},y:{display:false}}}
        });
      });
  }
});
